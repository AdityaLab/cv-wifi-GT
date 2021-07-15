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

uiuc_cats = ['uiuc_all','uiuc_crs_pol_30',  'uiuc_crs_pol_30_1','uiuc_crs_pol_30_2',  "uiuc_pr_pol", "uiuc_pr_pol_1", "uiuc_pr_pol_2", 'uiuc_pr_pol_exp', 'uiuc_pr_pol_exp_1', 'uiuc_pr_pol_exp_2']


berkeley_cats = ['berkeley_all','berkeley_crs_pol_30',  'berkeley_crs_pol_30_1','berkeley_crs_pol_30_2',  "berkeley_pr_pol", "berkeley_pr_pol_1", "berkeley_pr_pol_2", 'berkeley_pr_pol_exp', 'berkeley_pr_pol_exp_1', 'berkeley_pr_pol_exp_2']

second_cats = ['2nd_all','2nd_crs_pol_30',  '2nd_crs_pol_30_1','2nd_crs_pol_30_2',  "2nd_pr_pol", "2nd_pr_pol_1", "2nd_pr_pol_2", '2nd_pr_pol_exp', '2nd_pr_pol_exp_1', '2nd_pr_pol_exp_2']


third_cats = ['3rd_all','3rd_crs_pol_30',  '3rd_crs_pol_30_1','3rd_crs_pol_30_2',  "3rd_pr_pol", "3rd_pr_pol_1", "3rd_pr_pol_2", '3rd_pr_pol_exp', '3rd_pr_pol_exp_1', '3rd_pr_pol_exp_2']

base_cats = ['all','crs_pol_30',  'crs_pol_30_1','crs_pol_30_2',  "pr_pol", "pr_pol_1", "pr_pol_2", 'pr_pol_exp', 'pr_pol_exp_1', 'pr_pol_exp_2']


GT_0_4 = np.array([[0.02940123, 0.01138308, 0.02935103],
       [0.02958333, 0.01130556, 0.02947778],
       [0.03      , 0.011     , 0.0294    ],
        [0.02385223, 0.00952549, 0.02614507],
        [0.04478056, 0.01204282, 0.03185417],
       [0.04522626, 0.01195731, 0.03151456],
       [0.0455    , 0.01166667, 0.03135   ],
         [0.03    , 0.011957, 0.031515],
        [0.02357202, 0.01064115, 0.03483618],
       [0.02769547, 0.01023282, 0.03054143],
       [0.02833333, 0.01003704, 0.02856591],
        [0.02697687, 0.01303429, 0.0385675 ],
       [0.02802451, 0.01277361, 0.03221521],
       [0.02966873, 0.01164397, 0.03211438] ,
       [0.037398 ,  0.010652 , 0.036342],
[0.032604 ,  0.012396 , 0.030682],
[0.034905 ,  0.011540 , 0.034525],
[0.030611 ,  0.013039  , 0.031093],
[0.034905  , 0.011540 , 0.040000],
[0.033742  , 0.011732 , 0.036000],
[0.042000  , 0.012117 , 0.036000],
[0.041481  , 0.012651 , 0.032593],
[0.043920  , 0.012874 , 0.028176],
[0.044938  , 0.012300 , 0.032412],
[0.042518  , 0.012335 , 0.033408]     ])


GT_5_9 = np.array([
[0.071300  , 0.000620 , 0.003705],

[0.067083  , 0.000633 , 0.003770],

[0.074073 ,  0.000644 , 0.003540],

[0.078608 ,  0.000500 , 0.004500],

[0.076737 ,  0.000512 , 0.004500],

[0.076780 ,  0.000513 , 0.004528],

[0.079189  , 0.000470 , 0.005274],

[0.079301  , 0.000468 , 0.005272],

[0.067968 ,  0.000636 , 0.003778],

[0.068411  , 0.000638 , 0.003782],

[0.068853  , 0.000639 , 0.003786],

])

GT_10_14 = np.array([
[0.002157 , 0.002799 , 0.013248],

[0.001977 ,  0.002078 , 0.016362],

[0.002025 ,  0.002311 , 0.015877],

[0.002341 ,  0.003231 , 0.013171],

[0.002493 ,  0.002802 , 0.014905],

[0.002778  , 0.002205 , 0.016838],

[0.002473 ,  0.003654  ,0.019977],

[0.002713 ,  0.003811 , 0.015314],

[0.002626 ,  0.003839 , 0.016091],

[0.002611 ,  0.003880 , 0.016251],

[0.001989  , 0.002143 , 0.016464]])


UIUC = np.array([
[0.025276 ,  0.005815 , 0.004961],

[0.024390 ,  0.004653 , 0.006181],

[0.025209  , 0.003269 , 0.007596],

[0.024578  , 0.002721 , 0.008021],

[0.023331 ,  0.003118 , 0.007671],

[0.023279 ,  0.003087 , 0.007723],

[0.026042  , 0.005793 , 0.005016],

[0.025975 ,  0.005828 , 0.005009],

[0.024168 ,  0.002857 , 0.007754],

[0.024066  , 0.002823 , 0.007988],

[0.024578 ,  0.002721 , 0.008021],

])

UCB  = np.array([
[0.036000 ,  0.005250 , 0.045000],

[0.036409  , 0.005197 , 0.043429],

[0.040000  , 0.005000 , 0.046125],

[0.039944  , 0.005081 , 0.045729],

[0.042750 ,  0.004400 , 0.040500],

[0.045000  , 0.004533 , 0.033000],

[0.038695 ,  0.004803 , 0.030055],

[0.038779  , 0.004799 , 0.029957],

[.044175  , 0.004547 , 0.038475],

[0.043014 ,  0.004688 , 0.036750],

[0.044696  , 0.004749 , 0.034443]
])

def experiment(cat, step_pol, n, start_date, m):
    
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
        
        output_total = []
            
        if cat in uiuc_cats:
            
            A = UIUC

        elif cat in berkeley_cats:
            
            A = UCB

        elif cat in second_cats:
            A = GT_5_9
        
        elif cat in third_cats:
            
            A = GT_10_14
            
        else:
            
            A = GT_0_4
                
               
        
        for row in A:
            
            p = row[0]
            
            I_asym = row[1]
            
            alpha = row[2]
            
            print(row)

            iters = range(n)

            folds = np.array_split(iters, cpu_count())

            with Pool(cpu_count()) as pool:

                func = partial(simulations, start_date, step_pol, p, I_asym, alpha, m, cat)
                output = pool.map(func, folds)

            output_total.extend(list(itertools.chain.from_iterable(output)))

        return output_total

    if gate:
        
        saving_path = "path_to_simulation_output/" + cat+"_"+start_date+"_"+ 'pool_simu.pkl'
        
        saving_path_list = "path_to_simulation_output/" + cat+"_"+start_date+"_"+ 'pool_simu_list.pkl'
        
     
        if (os.path.isfile(saving_path)):
            
            print(saving_path +" already exists")
            
            output_data =  pickle.load(open(saving_path, 'rb'))
            output_list =  pickle.load(open(saving_path_list, 'rb'))
            #R0= output_data['R0'].to_numpy()
            
            return (output_data, output_list) 
        else:        
            start = time.time()

            output_list = helper(start_date, n, m, cat)


            end  = time.time()

            print(len(output_list))
            print("time elapsed: ",end - start)

            output_data = pd.concat(output_list, axis =0)
            output_data = output_data.groupby(output_data.index).mean()

            #R0= output_data['R0'].to_numpy()



            pickle.dump( output_data,  open( saving_path, "wb" ) )
            print('Saving data into: '+saving_path)

            pickle.dump( output_list,  open( saving_path_list, "wb" ) )
            print('Saving data into: '+saving_path_list)
            #output_data.to_pickle("/cv19wifi/tmp/res_output_data_simu.pkl")
            #output_data.to_pickle("/cv19wifi/tmp/crs_output_data_simu.pkl")


            return (output_data, output_list)      


#experiment('all', p , alpha, 25, start_date, m)

