from cal_model_t import COVID_model
import argparse
import os, sys
from datetime import date as datemethod
from datetime import datetime
from datetime import timedelta
import mesa_SIR.calculations_and_plots as c_p

from multiprocessing import  cpu_count
from pathos.multiprocessing import ProcessingPool as Pool
from functools import partial

import pickle

# For the graph
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import bipartite
#from graph_utils import node_metrics, network_metrics, projections

import pandas as pd

import time




import numpy as np

import itertools


from usr_collection import usr_collector




def experiment(cat, step_pol, p, I_asym, alpha, n, start_date, m):
    
    gate = True
    
    
    usr_collector('all', start_date, m)
      

        

    
    def simulations(start_date, step_pol, p, I_asym,  alpha, m, cat, n):

        output_list = []


        

        for j in n:
            print("Iter: " + str(j+1))
            campus_model  = COVID_model(start_date, step_pol, p , I_asym, alpha , m, cat)

            for i in range(m):
                print('Running step {}'.format(str(i)))

                campus_model.step()

            output = campus_model.datacollector.get_model_vars_dataframe()
            coins = campus_model.coin_flips
            print(len(coins))
            output['coins'] = coins
            output_list.append(output)
            
            
            
            

        return output_list



    def helper(start_date, n, m, cat):

        iters = range(n)

        folds = np.array_split(iters, cpu_count())

        with Pool(cpu_count()) as pool:
            
            func = partial(simulations, start_date, step_pol, p, I_asym, alpha, m, cat)
            output = pool.map(func, folds)


        return list(itertools.chain.from_iterable(output))

    if gate:
        
        saving_path = "/cv19wifi/tmp/network_modeling/simulation_output/calibration_output/" + cat+"_"+start_date+"_"+ "p:"+str(p)+"_" + 'I_asym:' +str(I_asym)+ '_' +"alpha:"+str(alpha)+ '_simu.pkl'
        #saving_path = "/cv19wifi/tmp/network_modeling/simulation_output/" + cat+"_"+start_date+"_"+ "p:"+str(p)+"_" + 'I_asym:' +str(I_asym)+ '_' +"alpha:"+str(alpha)+ '_simu.pkl'
        
        saving_path_list = "/cv19wifi/tmp/network_modeling/simulation_output/calibration_output/" + cat+"_"+start_date+"_"+ "p:"+str(p)+"_" + 'I_asym:' +str(I_asym)+ '_' +"alpha:"+str(alpha)+ '_simu_list.pkl'
        #saving_path_list = "/cv19wifi/tmp/network_modeling/simulation_output/" + cat+"_"+start_date+"_"+ "p:"+str(p)+"_" + 'I_asym:' +str(I_asym)+ '_' +"alpha:"+str(alpha)+ '_simu_list.pkl'
                
     
        if (os.path.isfile(saving_path)):
            
            print(saving_path +" already exists")
            
            output_data =  pickle.load(open(saving_path, 'rb'))
            R0= output_data['R0'].to_numpy()
            
            return (p, alpha , np.min(R0), np.max(R0), output_data)
        else:        
            start = time.time()

            output_list = helper(start_date, n, m, cat)


            end  = time.time()

            print(len(output_list))
            print("time elapsed: ",end - start)

            output_data = pd.concat(output_list, axis =0)
            output_data = output_data.groupby(output_data.index).mean()

            R0= output_data['R0'].to_numpy()



            pickle.dump( output_data,  open( saving_path, "wb" ) )
            print('Saving data into: '+saving_path)

            pickle.dump( output_list,  open( saving_path_list, "wb" ) )
            print('Saving data into: '+saving_path_list)
            #output_data.to_pickle("/cv19wifi/tmp/res_output_data_simu.pkl")
            #output_data.to_pickle("/cv19wifi/tmp/crs_output_data_simu.pkl")


            return (p, alpha , np.min(R0), np.max(R0), output_data, output_list)      


#experiment('all', p , alpha, 25, start_date, m)

