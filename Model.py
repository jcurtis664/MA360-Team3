from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from Mosquito import Mosquito, LifeStage

import random

class Model(Model):
    def __init__(self, N):      # N = number of agents
        self.agents = N
        self.schedule = SimultaneousActivation(self)
        for i in range(self.agents):
            agent = Mosquito(i, self)
            self.schedule.add(agent)

    def step(self):
        return self.schedule.step()