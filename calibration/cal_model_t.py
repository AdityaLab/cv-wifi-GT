# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 15:21:34 2020

@author: metalcorebear

Revised on Sun Jun 28 2020
@Jiajia Xie
"""
import os, sys
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector
import agent

parameters = {'progression_period':3, 
              'progression_sd':2, 'reinfection_rate':0.00, 'interactions':0.15,'death_rate':0.0006, 
              'exposed_duration':5, 'prob_symptoms':0.66, 'asym_duration':7, 'asym_sd': 0,
              'recovery_days':12, 'recovery_sd':2, 'severe':0.18}


import datetime
import pandas as pd 

# For relative imports of custom utilities
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
    
from mesa_SIR import SEIR
import mesa_SIR.calculations_and_plots as c_p

# For the graph
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import bipartite

import pickle


import numpy as np
from data_shaping import write_G



#from graph_utils import node_metrics, network_metrics, projections

class COVID_model(Model):
    
    def __init__(self, start_date, step_pol, p, I_asym, alpha , m, cat):
        super().__init__(Model)
        
        #self.Is0 = pd.read_csv('./fulton_data.csv')['Cases'].to_numpy() / 665
        self.I_asym = I_asym
        
        
         #the list of collocation networks
        self.susceptible = 0
        self.dead = 0
        self.recovered = 0
        self.infected = 0
        
        self.alpha= alpha
        
        self.current_step = 0

        self.cat =cat
        
        self.uiuc_cats = ['uiuc_all','uiuc_crs_pol_30',  'uiuc_crs_pol_30_1','uiuc_crs_pol_30_2',  "uiuc_pr_pol", "uiuc_pr_pol_1", "uiuc_pr_pol_2", 'uiuc_pr_pol_exp', 'uiuc_pr_pol_exp_1', 'uiuc_pr_pol_exp_2']


        self.berkeley_cats = ['berkeley_all','berkeley_crs_pol_30',  'berkeley_crs_pol_30_1','berkeley_crs_pol_30_2',  "berkeley_pr_pol", "berkeley_pr_pol_1", "berkeley_pr_pol_2", 'berkeley_pr_pol_exp', 'berkeley_pr_pol_exp_1', 'berkeley_pr_pol_exp_2']


        self.tamu_cats = ['texasAM_all','texasAM_crs_pol_30',  'texasAM_crs_pol_30_1','texasAM_crs_pol_30_2',  "texasAM_pr_pol", "texasAM_pr_pol_1", "texasAM_pr_pol_2", 'texasAM_pr_pol_exp', 'texasAM_pr_pol_exp_1', 'texasAM_pr_pol_exp_2']

        self.umich_cats = ['umich_all','umich_crs_pol_30',  'umich_crs_pol_30_1','umich_crs_pol_30_2',  "umich_pr_pol", "umich_pr_pol_1", "umich_pr_pol_2", 'umich_pr_pol_exp', 'umich_pr_pol_exp_1', 'umich_pr_pol_exp_2']
        
        self.purdue_cats = ['purdue_all','purdue_crs_pol_30',  'purdue_crs_pol_30_1','purdue_crs_pol_30_2',  "purdue_pr_pol", "purdue_pr_pol_1", "purdue_pr_pol_2", 'purdue_pr_pol_exp', 'purdue_pr_pol_exp_1', 'purdue_pr_pol_exp_2']
        
        
            
        if self.cat in self.uiuc_cats:
            cases_data = pd.read_csv('./county_cases.csv')['UIUC'].to_numpy()
            self.Is0 = cases_data / np.amax(cases_data)
        elif self.cat in self.berkeley_cats:
            cases_data = pd.read_csv('./county_cases.csv')['Berkeley'].to_numpy()
            self.Is0 = cases_data / np.amax(cases_data)    
        elif self.cat in self.tamu_cats:
            cases_data = pd.read_csv('./county_cases.csv')['Texas A&M'].to_numpy()
            self.Is0 = cases_data / np.amax(cases_data)        
            
        elif self.cat in self.umich_cats:
            cases_data = pd.read_csv('./county_cases.csv')['university of michigan'].to_numpy()
            self.Is0 = cases_data / np.amax(cases_data)  
        elif self.cat in self.purdue_cats:
            cases_data = pd.read_csv('./county_cases.csv')['Purdue University'].to_numpy()
            self.Is0 = cases_data / np.amax(cases_data)  
        else:
            self.Is0 = pd.read_csv('./fulton_data.csv')['Cases'].to_numpy() / 665
        

        
        self.cat_var = 'all'
        
        
        self.date_missing = []
        
        self.step_pol = step_pol
        
        self.coin_flips = [0]
        
        self.coin_flip = 0
      

        

        
        
        self.start_date =  datetime.datetime.strptime(start_date, '%Y-%m-%d')
        self.td = 1
        
        self.abs_cat ='all'
        self.steps  = m
        #interactions = model_params.parameters['interactions']
        
        self.week_idx = self.current_step // 7
        
        self.SEIR_instance = SEIR.Infection(self, ptrans = p,
                                          reinfection_rate = parameters['reinfection_rate'],
                                          I0= self.Is0[self.current_step]* self.alpha,
                                          I_asym = self.I_asym,
                                          severe = parameters["severe"],
                                          exposed_duration = parameters['exposed_duration'],
                                          prob_symptoms = parameters['prob_symptoms'],
                                          asym_duration= parameters['asym_duration'],
                                           asym_sd = parameters['asym_sd'] ,
                                          progression_period = parameters["progression_period"],
                                          progression_sd = parameters["progression_sd"],
                                          death_rate = parameters["death_rate"],
                                          recovery_days = parameters["recovery_days"],
                                          recovery_sd = parameters["recovery_sd"])


        #G = SIR.build_network(interactions, self.population)
        ## Here we initialize the G0 as the first time period collocation which cover all node_id but with no edges
        if self.cat == 'all':
            self.step_pol = self.steps
            
        if self.current_step ==0:
            print('Category: '+self.cat)
            
            get_path = '/cv19wifi/tmp/network_modeling/simulation_output/usr_sets/set_118'+'_' + start_date+ '_'+self.abs_cat+ '.p'
            print(get_path)
            usr_nodes = pickle.load(open(get_path, 'rb'))
                
           
        
            self.population = len(usr_nodes)
        
            self.mapping = {num: str(num) for num in range(1000001, 2000001)}

            print("Population size: " +str(self.population))
            self.asym = {}
            self.SIRD = {}

            G0 = nx.Graph()
            for ids in usr_nodes:
                self.asym[ids] = 0
                self.SIRD[ids] =0
                G0.add_node(str(ids))



        

            self.grid = NetworkGrid(G0)
            self.schedule = RandomActivation(self)
            
        
            self.dead_agents = []
            self.running = True
    
            for node in G0.nodes():

                new_agent = agent.human(node, self) #what was self.next_id()
                self.grid.place_agent(new_agent, node)
                self.schedule.add(new_agent)
        
     
        #self.meme = 0
            
            
            
        
        
        self.datacollector = DataCollector(model_reporters={"infected": lambda m: c_p.compute(m,'infected'),
                                                            "recovered": lambda m: c_p.compute(m,'recovered'),
                                                            "susceptible": lambda m: c_p.compute(m,"susceptible"),
                                                            "R0": lambda m: c_p.compute(m, "R0"),
                                                            "symptomatic": lambda m: c_p.compute(m,"symptomatic"),
                                                           "exposed": lambda m: c_p.compute(m,"exposed"),
                                                             "asymptomatic": lambda m: c_p.compute(m,"asymptomatic"),
                                                            "new asym": lambda m: c_p.compute(m,"new asym"),
                                                           "isolation": lambda m: c_p.compute(m,"isolation"),
                                                            "internal_inf": lambda m: c_p.compute(m,'internal_inf'),
                                                            "external_inf": lambda m: c_p.compute(m,'external_inf'),
                                                            "SIRD": lambda m: c_p.compute(m,"SIRD")})
        '''
        self.datacollector = DataCollector(model_reporters={
                                                            "R0": lambda m: c_p.compute(m, "R0"),
                                                            "new asym": lambda m: c_p.compute(m,"new asym"),
                                                            "SIRD": lambda m: c_p.compute(m,"SIRD"),
                                                            "internal_inf": lambda m: c_p.compute(m,'internal_inf'),
                                                            "external_inf": lambda m: c_p.compute(m,'external_inf'),
                                                            "recovered": lambda m: c_p.compute(m,'recovered')})'''
        self.datacollector.collect(self)

    def update(self):
        
        
        self.SEIR_instance.I0 = self.alpha * self.Is0[self.current_step]
        
        
        
        
        if self.current_step < self.steps:
            
            if self.current_step < self.step_pol:
                pass
            else:
                
                self.cat_var = self.cat
             
            G = None
            counter  = 0

            while G == None:
                
                if self.start_date in self.date_missing:
                    print(self.start_date)
                    G = None
                else:    
                    G = write_G(self.cat_var, self.start_date)
                
                self.start_date += datetime.timedelta(days = self.td)
                
                
                counter +=1
                
                if counter >=90:
                    G= 1
                
            
                
                

            self.grid.G = G
            self.current_step +=1
            
        


    
    def step(self):
        self.update()

        self.schedule.step()
        
        self.coin_flips.append(self.coin_flip)
        self.coin_flip = 0
        
        self.datacollector.collect(self)
        
        for a in self.schedule.agents:
            if a.asymptomatic ==  True:
                if self.asym[a.pos] == 0:
                    self.asym[a.pos] = 1
            elif (getattr(a, "recovered") ==True) or (getattr(a, "symptomatic") ==True) or (getattr(a, "isolation") ==True) or (getattr(a, "alive") ==False):
                if self.SIRD[a.pos]== 0:
                    self.SIRD[a.pos] = 1
         
        
        '''
        for a in self.schedule.agents:
            if a.alive == False:
                self.schedule.remove(a)
                self.dead_agents.append(a.unique_id)
        '''

        if self.dead == self.schedule.get_agent_count():
            self.running = False
        else:
            self.running = True
