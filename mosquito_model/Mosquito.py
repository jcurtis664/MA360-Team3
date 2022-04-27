from mesa import Agent, Model
from enum import Enum
import random


'''=======PARAMETERS======='''
egg_survival_chance = 0.99
larva_survival_chance = 0.9
pupa_survival_chance = 0.9
adult_survival_chance = 0.9
chance_of_mating = 0.9


class LifeStage(Enum):
    Egg = 1
    Larva = 2
    Pupa = 3
    Adult = 4


class Mosquito(Agent):
    def __init__(self, unique_id, model, infected, location, stage):
        super().__init__(unique_id, model)
        self.sex = random.randint(0, 1)     # 0 = male, 1 = female
        self.infected = infected       
        self.stage = LifeStage(stage)          # from LifeStage enum class
        self.mated = False
        
        self.survival_chance = egg_survival_chance
        self.mating_chance = random.uniform(0.6, 0.9)
        self.days_til_advance = random.randint(10, 20)
        self.days_since_advance = 0
        self.days_til_mate = 0
        
        self.location = [location[0], location[1]]

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=True)
        new_position = self.random.choice(possible_steps)
        self.location = new_position
        self.model.grid.move_agent(self, new_position)
        
    def mate(self):
        neighbors = self.model.grid.get_cell_list_contents([self.pos])
        #print(neighbors)
        if (len(neighbors) > 1):
            for chosen_neighbor in neighbors:
                if (self.mating_chance > random.random() and \
                        chosen_neighbor.mating_chance > random.random() and \
                        self.sex != chosen_neighbor.sex and \
                        not self.mated and not chosen_neighbor.mated):
                    
                    self.mating_chance = self.mating_chance / 2
                    self.survival_chance = self.survival_chance / 2
                    self.mated = True
                    self.days_til_mate = ((self.days_til_advance - self.days_since_advance) / 2) + 1
                    
                    chosen_neighbor.mating_chance = chosen_neighbor.mating_chance / 2
                    chosen_neighbor.survival_chance = chosen_neighbor.survival_chance / 2
                    chosen_neighbor.mated = True
                    
                    if not (chosen_neighbor.infected or self.infected):
                        self.model.add_agents(random.randint(15, 20))     
                if (len(neighbors) > 10):
                    self.survival_chance = self.survival_chance / 2

    def step(self):
        if (self.stage == LifeStage.Egg):
            #print("Stage 1 - Egg")
            
            if (self.days_since_advance == self.days_til_advance):
                self.stage = LifeStage.Adult
                self.survival_chance = adult_survival_chance
                
                self.days_since_advance = 0
                self.days_til_advance = random.randint(7, 9)
        
        elif (self.stage == LifeStage.Adult):
            #print("Stage 4 - Adult")
            
            if (self.days_since_advance == self.days_til_advance):
                self.survival_chance = 0
            else:
                if (self.days_til_mate < 1):
                    self.mate()
                self.days_til_mate += 1
                self.move()
                self.mated = False
                
        #KILL AGENT
        if (self.survival_chance < random.random()):
            self.model.killed_agents.append(self)
        else:
            self.days_since_advance += 1
                
        '''        
        elif (self.stage == LifeStage.Larva):
            #print("Stage 2 - Larva")
            
            if (self.days_since_advance == self.days_til_advance):
                self.stage = LifeStage.Pupa
                self.survival_chance = pupa_survival_chance
                
                self.days_since_advance = 0
                self.days_til_advance = random.randint(2, 2)
                
        elif (self.stage == LifeStage.Pupa):
            #print("Stage 3 - Pupa")
            
            if (self.days_since_advance == self.days_til_advance):
                self.stage = LifeStage.Adult
                self.survival_chance = adult_survival_chance
                
                self.days_since_advance = 0
                self.days_til_advance = random.randint(7, 7)
        '''
    