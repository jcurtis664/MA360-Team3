from mesa import Agent, Model
import enum

class LifeStage(Enum):
    Egg = 1
    Larva = 2
    Pupa = 3
    Adult = 4

class Mosquito:
    def __init__(self, sex, infected, mated, stage, model):
        self.sex = sex              # false = male, true = female
        self.infected = infected    
        self.mated = mated
        self.stage = stage
        self.model = model