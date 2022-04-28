from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from Mosquito import Mosquito, LifeStage
import random
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


'''=======PARAMETERS======='''
num_of_mosquitoes = 550
num_of_infected = 50
num_of_days = 10

def compute_gini(model):
    return model.total_alive

class Model(Model):
    def __init__(self, N, number_of_infected, grid_width, grid_height):      # N = number of agents
        super().__init__()
        self.agents = N
        self.number_of_infected = number_of_infected
        self.grid = MultiGrid(grid_width, grid_height, True)
        self.schedule = SimultaneousActivation(self)
        
        for i in range(N - number_of_infected):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            
            agent = Mosquito(i, self, False, [x, y], 4)
            
            self.schedule.add(agent)
            self.grid.place_agent(agent, (x, y))
            
        for i in range(N - number_of_infected, N):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            
            agent = Mosquito(i, self, True, [x, y], 4)

            self.schedule.add(agent)
            self.grid.place_agent(agent, (x, y))
            
        self.running = True
        self.killed_agents = []
        self.total_alive = N
        
        self.datacollector = DataCollector(
            model_reporters={"Gini": compute_gini}
        )

    def step(self):
        self.killed_agents = []
        
        self.datacollector.collect(self)
        self.schedule.step()
        
        for agent in self.killed_agents:
            self.grid.remove_agent(agent)
            self.schedule.remove(agent)
            self.total_alive -= 1
    
    def run_model(self, step_count=100):
        for i in range(step_count):
            self.killed_agents = []
            self.step()
            for agent in self.killed_agents:
                print("he dead")
                self.grid.remove_agent(agent)
                self.schedule.remove(agent)
                self.total_alive -= 1
            
    def add_agents(self, number_of_agents, location):
        for i in range(self.agents, self.agents + number_of_agents):
            x = location[0]
            y = location[1]
            
            agent = Mosquito(i, self, False, [x, y], 1)
            
            self.schedule.add(agent)
            self.agents += 1
            self.total_alive += 1

            self.grid.place_agent(agent, (x, y))
    
#RUN THE MODEL
'''
model = Model(num_of_mosquitoes, num_of_infected)
model.run_model(num_of_days)
print(model.total_alive)
'''
