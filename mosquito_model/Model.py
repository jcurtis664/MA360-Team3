from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from Mosquito import Mosquito, LifeStage
import random
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

def compute_gini(model):
    return model.total_alive

class Model(Model):
    def __init__(self, N, number_of_infected, release_frequency, grid_width, grid_height):      # N = number of agents
        super().__init__()
        self.agents = N
        self.number_of_infected = number_of_infected
        self.grid = MultiGrid(grid_width, grid_height, True)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.killed_agents = []
        self.total_alive = N
        self.release_frequency = release_frequency
        self.day = 1
        self.datacollector = DataCollector(
            model_reporters={"Gini": compute_gini}
        )
        
        for i in range(N - number_of_infected):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            
            agent = Mosquito(i, self, False, [x, y], random.choice([1, 4]), random.randint(0, 1))
            
            self.schedule.add(agent)
            self.grid.place_agent(agent, (x, y))
            
        for i in range(N - number_of_infected, N):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            
            agent = Mosquito(i, self, True, [x, y], 4, 0)

            self.schedule.add(agent)
            self.grid.place_agent(agent, (x, y))
            
        
    def step(self):
        self.killed_agents = []
        
        self.datacollector.collect(self)
        self.schedule.step()
        
        for agent in self.killed_agents:
            self.grid.remove_agent(agent)
            self.schedule.remove(agent)
            self.total_alive -= 1
            
        if (self.day % self.release_frequency == 0):
            for i in range(self.agents, self.agents + self.number_of_infected):
                random_agent = self.random.choice(self.schedule.agents)
                
                if (random_agent.location[0] > 5 and random_agent.location[0] < self.grid.width - 5):
                    x = random_agent.location[0] + random.randint(-5, 5)
                else:
                    x = random_agent.location[0]
                    
                if (random_agent.location[1] > 5 and random_agent.location[1] < self.grid.height - 5):
                    y = random_agent.location[1] + random.randint(-5, 5)
                else:
                    y = random_agent.location[1]
                
                agent = Mosquito(i, self, True, [x, y], 4, 0)
                
                self.agents += 1
                self.total_alive += 1
    
                self.schedule.add(agent)
                self.grid.place_agent(agent, (x, y))
            
        self.day += 1
    
    '''
    def run_model(self, step_count=100):
        for i in range(step_count):
            self.killed_agents = []
            self.step()
            for agent in self.killed_agents:
                print("he dead")
                self.grid.remove_agent(agent)
                self.schedule.remove(agent)
                self.total_alive -= 1'''
            
            
    def add_agents(self, number_of_agents, location):
        for i in range(self.agents, self.agents + number_of_agents):
            x = location[0]
            y = location[1]
            
            agent = Mosquito(i, self, False, [x, y], 1, random.randint(0, 1))
            
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
