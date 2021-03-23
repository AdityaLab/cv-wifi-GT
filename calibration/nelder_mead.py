import pickle 
import numpy as np
import pandas as pd


from calibration_RMSE_t import experiment as experiment_t

from scipy.optimize import minimize


def objective(params):
    
    
    #I_asym, alpha =   0.011859  ,  0.030579
    p = params[0]
    I_asym = params[1]
    alpha = params[2]
    start_date = '2020-08-17'
    #start_date = '2020-09-21'
    #start_date = '2020-10-26'
    
    
    population = [ 13300, 13401, 13557, 13525, 14028]
    #population = [ 14241, 14369, 14471, 15025, 14568]
    #population = [ 14800, 14213, 14471, 14249, 10176]
    
    
    #obs_rates = [ 0.0210, 0.0201, 0.0092, 0.0038, 0.0031]
    #obs_rates = [ 0.0008, 0.0018, 0.0007, 0.0031, 0.0044]
    #obs_rates = [ 0.0035, 0.0078, 0.0078, 0.0040, 0.0023]
    
    
    ##uiuc
    #obs_rates = [ 0.0065, 0.0111, 0.0052, 0.0031, 0.0041]
    
    ##berkeley
    obs_rates = [0.012, 0.012, 0.004, 0.003, 0.001]
    
    ##TexasAM
    #obs_rates = [0.099, 0.102, 0.075, 0.101, 0.038]
    
    
    ##umich
    #obs_rates = [0.019, 0.028, 0.036, 0.076, 0.034]
    
    ##purdue
    #obs_rates = [0.0269, 0.0287, 0.0311, 0.0279, 0.0394]    

    #output = experiment_t('all', 7, p, I_asym ,alpha, 15, start_date, 35)
    #output = experiment_t('uiuc_all', 7, p, I_asym ,alpha, 15, start_date, 35)
    output = experiment_t('berkeley_all', 7, p, I_asym ,alpha, 15, start_date, 35)
    #output = experiment_t('texasAM_all', 7, p, I_asym ,alpha, 15, start_date, 35)
    #output = experiment_t('umich_all', 7, p, I_asym ,alpha, 15, start_date, 35)
    #output = experiment_t('purdue_all', 7, p, I_asym ,alpha, 15, start_date, 35)

        
    df = output[4]
    N = 7
    df1 = df.groupby(df.index // N).sum()
    df1.drop(df1.tail(1).index,inplace=True)
    
    RMSE = 0
    counter = 0
    for index, row in df1.iterrows():
        

        test_rate = row['new asym']/(population[index] - row['SIRD'])

        error = (test_rate - obs_rates[index])**2

        RMSE += error

        counter +=1


    RMSE = np.sqrt(RMSE/counter)    
    
    
    return RMSE



            
            
            
            
            
            
            
            
            
            
            
            
            
            