#@author: metalcorebear


from mesa import Agent


#Agent class
class human(Agent):
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
        
        self.pos = unique_id
        
        self.model = model

        self.infected, self.susceptible, self.severe, self.exposed = False, True, False, False
        self.day = 0

        self.external_inf = False

        self.was_infected = False
        self.recovered = False
        self.alive = True
        
        self.induced_infections = 0
        self.infected_others = False

        ##SEIR
        self.symptomatic =False
        self.infectious = False
        self.E_I_days=0
        
        self.asymptomatic =False
        self.isolation = False
        
        self.internal_inf = False
        
        

    def step(self):
        #include outside infection
        
        if self.model.current_step ==1:
            
            self.infected, self.susceptible, self.infectious = self.model.SEIR_instance.initial_asym_infection()
            self.day = 6
        
        else:
            if self.alive == True:
                if self.infected ==False:
                    if self.susceptible == True:
                        if self.pos in self.model.grid.G.nodes():
                            self.infected, self.susceptible, self.severe, self.exposed = self.model.SEIR_instance.initial_infection()
                            
                            self.model.coin_flip +=1
                            self.day = 0
                            if self.infected == True:
                                self.external_inf = True

        self.model.SEIR_instance.interact(self)
        self.day += 1