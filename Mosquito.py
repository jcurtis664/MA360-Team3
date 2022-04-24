from mesa import Agent, Model
from enum import Enum
import random


'''=======PARAMETERS======='''
egg_survival_chance = 0.9
larva_survival_chance = 0.8
pupa_survival_chance = 0.8
adult_survival_chance = 0.85
chance_of_mating = 0.9


class LifeStage(Enum):
    Egg = 1
    Larva = 2
    Pupa = 3
    Adult = 4


class Mosquito(Agent):
    def __init__(self, unique_id, model, infected):
        super().__init__(unique_id, model)
        self.sex = random.randint(0, 1)     # 0 = male, 1 = female
        self.infected = infected    
        #self.mated = False          
        self.stage = LifeStage.Egg          # from LifeStage enum class
        self.survival_chance = egg_survival_chance
        self.mating_chance = chance_of_mating
        self.days_til_advance = random.randint(8, 30)
        self.days_since_advance = 0

    def step(self):
        if (self.stage == LifeStage.Egg):
            print("Stage 1 - Egg")
            
            if (self.days_since_advance == self.days_til_advance):
                self.stage = LifeStage.Larva
                self.survival_chance = larva_survival_chance
                
                self.days_since_advance = 0
                self.days_til_advance = random.randint(5, 10)
                
        elif (self.stage == LifeStage.Larva):
            print("Stage 2 - Larva")
            
            if (self.days_since_advance == self.days_til_advance):
                self.stage = LifeStage.Pupa
                self.survival_chance = pupa_survival_chance
                
                self.days_since_advance = 0
                self.days_til_advance = random.randint(2, 3)
                
        elif (self.stage == LifeStage.Pupa):
            print("Stage 3 - Pupa")
            
            if (self.days_since_advance == self.days_til_advance):
                self.stage = LifeStage.Adult
                self.survival_chance = adult_survival_chance
                
                self.days_since_advance = 0
                self.days_til_advance = random.randint(5, 9)
                
        elif (self.stage == LifeStage.Adult):
            print("Stage 4 - Adult")
            
            if (self.days_since_advance == self.days_til_advance):
                self.survival_chance = 0
            else:
                if (self.mating_chance > random.random()):
                    self.mating_chance = self.mating_chance / 2
                    self.survival_chance = self.survival_chance / 2
                    if (self.sex == 1 and (self.model.number_of_infected / self.model.agents) < random.random()):
                        self.model.add_agents(random.randint(80, 100))
        
        #KILL AGENT
        if (self.survival_chance < random.random()):
            self.model.killed_agents.append(self)
            return
        else:
            self.days_since_advance += 1