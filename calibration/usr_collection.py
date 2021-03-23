import pickle
from data_shaping import write_G
import datetime
import numpy as np
import os
from datetime import timedelta






def usr_collector(cat, starts, steps):

    current_step =0
    
    steps = 118
    
    abs_path = '/cv19wifi/tmp/network_modeling/simulation_output/usr_sets/'


    td =1





    start_date =  datetime.datetime.strptime(starts, '%Y-%m-%d')


    usr_set = []

    date_missing =[]

    week_usr_set = []




    current_step =0
    start_date =  datetime.datetime.strptime(starts, '%Y-%m-%d')

    week = 1

    days = 0

    
    set_path = abs_path + 'set'+'_'+ str(steps)+'_'+starts+ '_'+ cat +'.p'



    if os.path.isfile(set_path):
        print("File already exists")

    else:
        while current_step < steps:

            if days == 7:    
                days = 0
                print("week: "+ str(week))
                print(len(week_usr_set))
                
                week +=1

                week_usr_set = []

            G = None

            if start_date not in date_missing:
                G = write_G(cat, start_date)
                #print(len(G.nodes()))
                for node in list(G.nodes()):
                    if node not in usr_set:
                        usr_set.append(node)
                    if node not in week_usr_set:    
                        week_usr_set.append(node)


                print(start_date)



                current_step +=1

                days +=1
            else:
                print(start_date)
                print('----- Data is skipping')






            start_date += datetime.timedelta(days = td)





        print(len(week_usr_set))

        print(len(usr_set))



        #if cat =='all':
            #set_path = './set'+'_'+ str(steps)+'_'+starts+ '_'+ cat +'.p'



        print("saving into")
        print(set_path)
        pickle.dump( usr_set , open(  set_path, 'wb'))
        
        
if __name__ == "__main__":
    usr_collector('all', '2020-10-26', 35)
    