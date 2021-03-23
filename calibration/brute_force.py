import pickle 
import numpy as np
import pandas as pd

from calibration_RMSE import experiment

population = [10205 , 13300, 13401, 13557, 13525, 14028]

obs_rates = [0.0016, 0.0210, 0.0201, 0.0092, 0.0038, 0.0031]

start_date = '2020-08-10'

p_space = np.linspace(0.1, 0.0008, num= 25)


I0_space = np.linspace(0.1, 0.005, num = 25)


history = []

combos = [(p, I0) for p in p_space for I0 in I0_space]


p_prev = 0
I0_prev = 0
RMSE_prev = 10000000000

for combo in combos:
    p, I0 = combo
    output = experiment('all',p, I0, 15, start_date, 42)
    df = output[4]
    N = 7
    df1 = df.groupby(df.index // N).sum()
    df1.drop(df1.tail(1).index,inplace=True)
    
    RMSE = 0
    
    
    
    counter = 0
    
    if output[3] > 0.79:

        for index, row in df1.iterrows():

            test_rate = row['new asym']/(population[index] - row['SIRD'])

            error = (test_rate - obs_rates[index])**2

            RMSE += error
            
            counter +=1


        RMSE = np.sqrt(RMSE/counter)

        if RMSE < RMSE_prev:

            RMSE_prev = RMSE

            p_prev = p

            I0_prev = I0
            
            history.append(RMSE)
                
        

        print("RMSE: "+ str(RMSE))
        
        
        print('------------------------')
        print('Current optimal Solution Found')
        print("Combo: ({},{})".format(p_prev, I0_prev))
        print('RMSE: {}'.format(RMSE_prev))

    else:
        
        print('Infeasible R0')
        pass
            
print('------------------------')
print('optimal Solution Found')
print("Combo: ({},{})".format(p_prev, I0_prev))
print('RMSE: {}'.format(RMSE_prev))


 pickle.dump( history,  open( './es_history.pkl', "wb" ) )
            
            
            
            
            
            
            
            
            
            
            
            
            
            