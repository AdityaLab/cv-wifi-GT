from datetime import date as datemethod
from datetime import datetime
from datetime import timedelta


import networkx as nx
from networkx.algorithms import bipartite

import pandas as pd

import time

import pickle


#date_time_str = '2019-11-18'
#end_time = datetime.strptime(date_time_str, '%Y-%m-%d')

td =1



path_crs_30  = '/cv19wifi/tmp/network_modeling/coloc_proj/crs_pol_30_locs/' 
path_pr = '/cv19wifi/tmp/network_modeling/coloc_proj/pr_pol_locs/' 
path_all  = '/cv19wifi/tmp/network_modeling/coloc_proj/all_locs/' 
path_res  = '/cv19wifi/tmp/network_modeling/coloc_proj/res_locs/' 
path_netc  = '/cv19wifi/tmp/network_modeling/coloc_proj/netc_pol_loc/'
path_mob = '/cv19wifi/tmp/network_modeling/mobil_proj/'


path_ec = '/cv19wifi/tmp/network_modeling/coloc_proj/ec_pol_locs/'

path_lc = '/cv19wifi/tmp/network_modeling/coloc_proj/lc_pol_locs/'

path_bc = '/cv19wifi/tmp/network_modeling/coloc_proj/bc_pol_locs/'


#OUT_DIR+'coloc_graph_'+POL+'_'+str(LEARNING_TIME)+'_'+str(CONSTRAINT)+'_'+date_str+'.p'

mapping = {num: str(num) for num in range(1000001, 2000001)}

gamma = 50

CONSTRAINT_exp = 18800  # Average weekly risk of exposure ~ testing burden
CONSTRAINT_exp_1 = 16900  # This excludes non-res students with completely ol schedules
CONSTRAINT_exp_2 = 12700  # This excludes non-res students with completely ol schedules

CONSTRAINT = 1 - 0.045  # Aggregate mobility over a week ~ number of edges
CONSTRAINT_1 = 1 - 0.077    # This excludes non-res students with completely ol schedules
CONSTRAINT_2 = 1 - 0.308    # This excludes all students with completely ol schedules

def write_G(cat, start_time):


    
    try:
        
        date = start_time.strftime('%Y-%m-%d')
        
        
        if cat =='crs_pol_30':
            GPATH = path_crs_30+'coloc_graph_'  + date+'.p'
        elif cat =='crs_pol_30_1':
            GPATH = path_crs_30+'coloc_graph_' + 'nonresol' + '_'  + date+'.p'
        elif cat =='crs_pol_30_2':
            GPATH = path_crs_30+'coloc_graph_' + 'allstdol' + '_'  + date+'.p'
        elif cat =='all':
            GPATH = path_all+'coloc_graph'+  "_" + date+'.p'    
            
        elif cat == "pr_pol":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT)+'_'+ date+'.p'
        elif cat == "pr_pol_1":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_1)+'_'+ date+'.p'
        elif cat == "pr_pol_2":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_2)+'_'+ date+'.p'

        elif cat == "pr_pol_exp":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp)+'_'+ date+'.p'
        elif cat == "pr_pol_exp_1":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp_1)+'_'+ date+'.p'
        elif cat == "pr_pol_exp_2":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp_2)+'_'+ date+'.p'
            
            
          
 
            
        elif cat == "ec_pol":
            GPATH = path_ec + 'coloc_graph_'+ 'ec' +'_'+ str(1)+'_'+ str(CONSTRAINT)+'_'+ date+'.p'
        elif cat == "ec_pol_1":
            GPATH = path_ec + 'coloc_graph_'+ 'ec' +'_'+ str(1)+'_'+ str(CONSTRAINT_1)+'_'+ date+'.p'
        elif cat == "ec_pol_2":
            GPATH = path_ec + 'coloc_graph_'+ 'ec' +'_'+ str(1)+'_'+ str(CONSTRAINT_2)+'_'+ date+'.p'

        elif cat == "ec_pol_exp":
            GPATH = path_ec + 'coloc_graph_'+ 'ec' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp)+'_'+ date+'.p'
        elif cat == "ec_pol_exp_1":
            GPATH = path_ec + 'coloc_graph_'+ 'ec' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp_1)+'_'+ date+'.p'
        elif cat == "ec_pol_exp_2":
            GPATH = path_ec + 'coloc_graph_'+ 'ec' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp_2)+'_'+ date+'.p'
            
            
            
        elif cat == "lc_pol":
            GPATH = path_lc + 'coloc_graph_'+ 'lc' +'_'+ str(1)+'_'+ str(CONSTRAINT)+'_'+ date+'.p'
        elif cat == "lc_pol_1":
            GPATH = path_lc + 'coloc_graph_'+ 'lc' +'_'+ str(1)+'_'+ str(CONSTRAINT_1)+'_'+ date+'.p'
        elif cat == "lc_pol_2":
            GPATH = path_lc + 'coloc_graph_'+ 'lc' +'_'+ str(1)+'_'+ str(CONSTRAINT_2)+'_'+ date+'.p'

        elif cat == "lc_pol_exp":
            GPATH = path_lc + 'coloc_graph_'+ 'lc' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp)+'_'+ date+'.p'
        elif cat == "lc_pol_exp_1":
            GPATH = path_lc + 'coloc_graph_'+ 'lc' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp_1)+'_'+ date+'.p'
        elif cat == "lc_pol_exp_2":
            GPATH = path_lc + 'coloc_graph_'+ 'lc' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp_2)+'_'+ date+'.p'            

            
            
            
        elif cat == "bc_pol":
            GPATH = path_bc + 'coloc_graph_'+ 'bc' +'_'+ str(1)+'_'+ str(CONSTRAINT)+'_'+ date+'.p'
        elif cat == "bc_pol_1":
            GPATH = path_bc + 'coloc_graph_'+ 'bc' +'_'+ str(1)+'_'+ str(CONSTRAINT_1)+'_'+ date+'.p'
        elif cat == "bc_pol_2":
            GPATH = path_bc + 'coloc_graph_'+ 'bc' +'_'+ str(1)+'_'+ str(CONSTRAINT_2)+'_'+ date+'.p'

        elif cat == "bc_pol_exp":
            GPATH = path_bc + 'coloc_graph_'+ 'bc' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp)+'_'+ date+'.p'
        elif cat == "bc_pol_exp_1":
            GPATH = path_bc + 'coloc_graph_'+ 'bc' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp_1)+'_'+ date+'.p'
        elif cat == "bc_pol_exp_2":
            GPATH = path_bc + 'coloc_graph_'+ 'bc' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp_2)+'_'+ date+'.p'            
            
##################            
# 2nd month

        
        elif cat =='2nd_crs_pol_30':
            GPATH = path_crs_30+'coloc_graph_'  + date+'.p'
        elif cat =='2nd_crs_pol_30_1':
            GPATH = path_crs_30+'coloc_graph_' + 'nonresol' + '_'  + date+'.p'
        elif cat =='2nd_crs_pol_30_2':
            GPATH = path_crs_30+'coloc_graph_' + 'allstdol' + '_'  + date+'.p'
        elif cat =='2nd_all':
            GPATH = path_all+'coloc_graph'+  "_" + date+'.p'    
            
        elif cat == "2nd_pr_pol":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT)+'_'+ date+'.p'
        elif cat == "2nd_pr_pol_1":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_1)+'_'+ date+'.p'
        elif cat == "2nd_pr_pol_2":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_2)+'_'+ date+'.p'

        elif cat == "2nd_pr_pol_exp":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp)+'_'+ date+'.p'
        elif cat == "2nd_pr_pol_exp_1":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp_1)+'_'+ date+'.p'
        elif cat == "2nd_pr_pol_exp_2":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp_2)+'_'+ date+'.p'


            
##################     


##################            
# 3nd month

        
        elif cat =='3rd_crs_pol_30':
            GPATH = path_crs_30+'coloc_graph_'  + date+'.p'
        elif cat =='3rd_crs_pol_30_1':
            GPATH = path_crs_30+'coloc_graph_' + 'nonresol' + '_'  + date+'.p'
        elif cat =='3rd_crs_pol_30_2':
            GPATH = path_crs_30+'coloc_graph_' + 'allstdol' + '_'  + date+'.p'
        elif cat =='3rd_all':
            GPATH = path_all+'coloc_graph'+  "_" + date+'.p'    
            
        elif cat == "3rd_pr_pol":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT)+'_'+ date+'.p'
        elif cat == "3rd_pr_pol_1":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_1)+'_'+ date+'.p'
        elif cat == "3rd_pr_pol_2":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_2)+'_'+ date+'.p'

        elif cat == "3rd_pr_pol_exp":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp)+'_'+ date+'.p'
        elif cat == "3rd_pr_pol_exp_1":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp_1)+'_'+ date+'.p'
        elif cat == "3rd_pr_pol_exp_2":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp_2)+'_'+ date+'.p'


            
##################   
# Static

        elif cat =='static_all':
            GPATH = path_all+'coloc_graph'+  "_" + date+'.p'    
            

##################

##################   
# Other schools
        elif cat =='uiuc_all':
            GPATH = path_all+'coloc_graph'+  "_" + date+'.p'    
            
        elif cat =='berkeley_all':
            GPATH = path_all+'coloc_graph'+  "_" + date+'.p' 
            
        elif cat =='texasAM_all':
            GPATH = path_all+'coloc_graph'+  "_" + date+'.p' 
            
        elif cat =='umich_all':
            GPATH = path_all+'coloc_graph'+  "_" + date+'.p' 
        elif cat =='purdue_all':
            GPATH = path_all+'coloc_graph'+  "_" + date+'.p' 
            
        elif cat =='uiuc_crs_pol_30':
            GPATH = path_crs_30+'coloc_graph_'  + date+'.p'
        elif cat =='uiuc_crs_pol_30_1':
            GPATH = path_crs_30+'coloc_graph_' + 'nonresol' + '_'  + date+'.p'
        elif cat =='uiuc_crs_pol_30_2':
            GPATH = path_crs_30+'coloc_graph_' + 'allstdol' + '_'  + date+'.p'
  
            
        elif cat == "uiuc_pr_pol":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT)+'_'+ date+'.p'
        elif cat == "uiuc_pr_pol_1":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_1)+'_'+ date+'.p'
        elif cat == "uiuc_pr_pol_2":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_2)+'_'+ date+'.p'

        elif cat == "uiuc_pr_pol_exp":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp)+'_'+ date+'.p'
        elif cat == "uiuc_pr_pol_exp_1":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp_1)+'_'+ date+'.p'
        elif cat == "uiuc_pr_pol_exp_2":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp_2)+'_'+ date+'.p'   
            
            
            
        elif cat =='berkeley_crs_pol_30':
            GPATH = path_crs_30+'coloc_graph_'  + date+'.p'
        elif cat =='berkeley_crs_pol_30_1':
            GPATH = path_crs_30+'coloc_graph_' + 'nonresol' + '_'  + date+'.p'
        elif cat =='berkeley_crs_pol_30_2':
            GPATH = path_crs_30+'coloc_graph_' + 'allstdol' + '_'  + date+'.p'
  
            
        elif cat == "berkeley_pr_pol":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT)+'_'+ date+'.p'
        elif cat == "berkeley_pr_pol_1":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_1)+'_'+ date+'.p'
        elif cat == "berkeley_pr_pol_2":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_2)+'_'+ date+'.p'

        elif cat == "berkeley_pr_pol_exp":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp)+'_'+ date+'.p'
        elif cat == "berkeley_pr_pol_exp_1":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp_1)+'_'+ date+'.p'
        elif cat == "berkeley_pr_pol_exp_2":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp_2)+'_'+ date+'.p'             
            

            
        elif cat =='texasAM_crs_pol_30':
            GPATH = path_crs_30+'coloc_graph_'  + date+'.p'
        elif cat =='texasAM_crs_pol_30_1':
            GPATH = path_crs_30+'coloc_graph_' + 'nonresol' + '_'  + date+'.p'
        elif cat =='texasAM_crs_pol_30_2':
            GPATH = path_crs_30+'coloc_graph_' + 'allstdol' + '_'  + date+'.p'
  
            
        elif cat == "texasAM_pr_pol":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT)+'_'+ date+'.p'
        elif cat == "texasAM_pr_pol_1":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_1)+'_'+ date+'.p'
        elif cat == "texasAM_pr_pol_2":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_2)+'_'+ date+'.p'

        elif cat == "texasAM_pr_pol_exp":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp)+'_'+ date+'.p'
        elif cat == "texasAM_pr_pol_exp_1":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp_1)+'_'+ date+'.p'
        elif cat == "texasAM_pr_pol_exp_2":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp_2)+'_'+ date+'.p'             

            
            
            
        elif cat =='umich_crs_pol_30':
            GPATH = path_crs_30+'coloc_graph_'  + date+'.p'
        elif cat =='umich_crs_pol_30_1':
            GPATH = path_crs_30+'coloc_graph_' + 'nonresol' + '_'  + date+'.p'
        elif cat =='umich_crs_pol_30_2':
            GPATH = path_crs_30+'coloc_graph_' + 'allstdol' + '_'  + date+'.p'
  
            
        elif cat == "umich_pr_pol":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT)+'_'+ date+'.p'
        elif cat == "umich_pr_pol_1":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_1)+'_'+ date+'.p'
        elif cat == "umich_pr_pol_2":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_2)+'_'+ date+'.p'

        elif cat == "umich_pr_pol_exp":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp)+'_'+ date+'.p'
        elif cat == "umich_pr_pol_exp_1":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp_1)+'_'+ date+'.p'
        elif cat == "umich_pr_pol_exp_2":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp_2)+'_'+ date+'.p'    
            
            
            
            
        elif cat =='purdue_crs_pol_30':
            GPATH = path_crs_30+'coloc_graph_'  + date+'.p'
        elif cat =='purdue_crs_pol_30_1':
            GPATH = path_crs_30+'coloc_graph_' + 'nonresol' + '_'  + date+'.p'
        elif cat =='purdue_crs_pol_30_2':
            GPATH = path_crs_30+'coloc_graph_' + 'allstdol' + '_'  + date+'.p'
  
            
        elif cat == "purdue_pr_pol":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT)+'_'+ date+'.p'
        elif cat == "purdue_pr_pol_1":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_1)+'_'+ date+'.p'
        elif cat == "purdue_pr_pol_2":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_2)+'_'+ date+'.p'

        elif cat == "purdue_pr_pol_exp":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp)+'_'+ date+'.p'
        elif cat == "purdue_pr_pol_exp_1":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp_1)+'_'+ date+'.p'
        elif cat == "purdue_pr_pol_exp_2":
            GPATH = path_pr + 'coloc_graph_'+ 'pr' +'_'+ str(1)+'_'+ str(CONSTRAINT_exp_2)+'_'+ date+'.p' 
##################
            
        elif cat =='netc_pol':
            GPATH = path_netc + 'coloc_graph_'+ 'netc' +'_'+ str(1)+'_'+ str(CONSTRAINT)+'_'+ date+'.p'             
            
        elif cat =='all_test':
            GPATH = path_all+'coloc_graph_test'+  "_" + date+'.p'   
        elif cat =='res':
            GPATH = path_res+'coloc_graph'+  "_" + date+'.p' 
         
        elif cat == 'mob':
            GPATH = path_mob+'mobil_graph'+  "_" + date+'.p' 

        elif cat == 'expI_1_netc':
            

            strings = cat.split('_')
           
            GPATH = path_netc+'coloc_graph_'+ 'exp1' +"_"+ strings[2]+'_'+ strings[1] +'_'+ date+'.p' 

        elif cat == 'expI_1_pr':
            
           
            strings = cat.split('_')
            GPATH = path_pr+'coloc_graph_'+ 'exp1' +"_"+ strings[2] +'_'+ strings[1] +'_'+ date+'.p' 
            
        elif cat == 'expI_2_netc':
            
            strings = cat.split('_')
           
            GPATH = path_netc+'coloc_graph_'+ 'exp1' +"_"+ strings[2]+'_'+ strings[1]  +'_'+ date+'.p' 


        elif cat == 'expI_2_pr':
            strings = cat.split('_')
            GPATH = path_pr+'coloc_graph_'+ 'exp1' +"_"+ strings[2] +'_'+ strings[1] +'_'+ date+'.p' 
        elif cat == 'expI_3_netc':
            
            strings = cat.split('_')
           
            GPATH = path_netc+'coloc_graph_'+ 'exp1' +"_"+ strings[2]+'_'+ strings[1]  +'_'+ date+'.p' 


        elif cat == 'expI_3_pr':
            strings = cat.split('_')
            GPATH = path_pr +'coloc_graph_'+ 'exp1' +"_"+ strings[2] +'_'+ strings[1]  +'_'+ date+'.p'
            
        elif cat == 'expI_4_netc':
            
            strings = cat.split('_')
           
            GPATH = path_netc+'coloc_graph_'+ 'exp1' +"_"+ strings[2]+'_'+ strings[1] +'_'+ date+'.p' 


        elif cat == 'expI_4_pr':
            strings = cat.split('_')
            GPATH = path_pr+'coloc_graph_'+ 'exp1' +"_"+ strings[2] +'_'+ strings[1]  +'_'+ date+'.p'   
            
 
        print(GPATH)
        G = pd.read_pickle(GPATH)
        G = nx.relabel_nodes(G, mapping)

        return G

        print(cat + " Data on " +start_time.strftime('%Y-%m-%d'))
        
    except:
        print(GPATH)
        print(cat +" No Data on " +start_time.strftime('%Y-%m-%d'))
        return None
