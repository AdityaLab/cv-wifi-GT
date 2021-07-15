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
        
        self.Is0 = pd.read_csv('./fulton_data.csv')['Cases'].to_numpy() / 665
        
        #self.degree_list = pd.read_pickle("/cv19wifi/tmp/network_modeling/degree_distribution_small_world_gt.p") 
        self.I_asym = I_asym
        
        
         #the list of collocation networks
        self.susceptible = 0
        self.dead = 0
        self.recovered = 0
        self.infected = 0
        
        self.alpha= alpha
        
        self.current_step = 0

        self.cat =cat
        

        
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
        #if self.cat == 'all':
        self.step_pol = self.steps
            
        if self.current_step ==0:
            print('Category: '+self.cat)
            
 
                
           
        
            #self.population = len(usr_nodes)
        
            #self.mapping = {index: a for index, a in enumerate(usr_nodes)}

            #print("Population size: " +str(self.population))
            self.asym = {}
            self.SIRD = {}

            G0 = pd.read_pickle('path_to_staic_network/static_network.p')
            
            usr_nodes = G0.nodes()
            #G0 = nx.relabel_nodes(G0, self.mapping)
            for ids in usr_nodes:
                self.asym[ids] = 0
                self.SIRD[ids] =0
                #G0.add_node(str(ids))



        

            self.grid = NetworkGrid(G0)
            self.schedule = RandomActivation(self)
            
        
            self.dead_agents = []
            self.running = True
    
            for node in G0.nodes():

                new_agent = agent.human(node, self) #what was self.next_id()
                self.grid.place_agent(new_agent, node)
                self.schedule.add(new_agent)
        
     
        #self.meme = 0
            
            
            
        
        '''
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
                                                            "SIRD": lambda m: c_p.compute(m,"SIRD")})'''
        
        self.datacollector = DataCollector(model_reporters={ "R0": lambda m: c_p.compute(m, "R0"),
                                                            "infected": lambda m: c_p.compute(m,'infected'),
                                                            "internal_inf": lambda m: c_p.compute(m,'internal_inf'),
                                                            "external_inf": lambda m: c_p.compute(m,'external_inf'),
                                                            "recovered": lambda m: c_p.compute(m,'recovered')})
        self.datacollector.collect(self)

    def update(self):
        
        
        self.SEIR_instance.I0 = self.alpha * self.Is0[self.current_step]
        
        
        
        
        if self.current_step < self.steps:
            
            if self.current_step < self.step_pol:
                pass
            else:
                
                self.cat_var = self.cat
             
            
            #self.grid.G = G
            self.current_step +=1
            
        


    
    def step(self):
        self.update()

        self.schedule.step()
        
        '''
        self.coin_flips.append(self.coin_flip)
        self.coin_flip = 0'''
        
        self.datacollector.collect(self)
        '''
        for a in self.schedule.agents:
            if a.asymptomatic ==  True:
                if self.asym[a.pos] == 0:
                    self.asym[a.pos] = 1
            elif (getattr(a, "recovered") ==True) or (getattr(a, "symptomatic") ==True) or (getattr(a, "isolation") ==True) or (getattr(a, "alive") ==False):
                if self.SIRD[a.pos]== 0:
                    self.SIRD[a.pos] = 1'''
         
        
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
