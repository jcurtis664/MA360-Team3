from mesa import Agent, Model
from enum import Enum
import random

class LifeStage(Enum):
    Egg = 1
    Larva = 2
    Pupa = 3
    Adult = 4

class Mosquito(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.sex = random.getrandbits(1)    # false = male, true = female
        self.infected = False    
        self.mated = False          
        self.stage = LifeStage.Egg          # from LifeStage enum class

    def step(self):
        # TODO method for time keeping fopr each mosquito
        print("TODO")