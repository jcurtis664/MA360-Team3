from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from Mosquito import Mosquito, LifeStage
import random
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


'''=======PARAMETERS======='''
num_of_mosquitoes = 10000
num_of_infected = 200
num_of_days = 50


class Model(Model):
    def __init__(self, N, number_of_infected):      # N = number of agents
        super().__init__()
        self.agents = N
        self.number_of_infected = number_of_infected
        self.schedule = SimultaneousActivation(self)
        for i in range(N - number_of_infected):
            agent = Mosquito(i, self, False)
            self.schedule.add(agent)
        for i in range(N - number_of_infected, N):
            agent = Mosquito(i, self, True)
            self.schedule.add(agent)
            
        self.running = True
        self.killed_agents = []
        self.total_alive = N

    def step(self):
        return self.schedule.step()
    
    def run_model(self, step_count=100):
        for i in range(step_count):
            self.killed_agents = []
            self.step()
            for agent in self.killed_agents:
                self.schedule.remove(agent)
                self.total_alive -= 1
                #self.grid.remove_agent(agent)
            
    def add_agents(self, number_of_agents):
        for i in range(self.agents, self.agents + number_of_agents):
            agent = Mosquito(i, self, False)
            self.schedule.add(agent)
            self.agents += 1
            self.total_alive += 1
    
#RUN THE MODEL
model = Model(num_of_mosquitoes, num_of_infected)
model.run_model(num_of_days)

print(model.total_alive)

'''
def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                "Filled": "true",
                "Layer": 0,
                "Color": "red",
                "r": 0.5}
    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(Model,
                [grid],
                "My Model",
                {'N': 50})

server.launch()
'''