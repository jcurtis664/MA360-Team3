# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 17:17:55 2022

@author: jared
"""
from Model import *
from Mosquito import LifeStage
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

def agent_portrayal(agent):
    if (agent.infected):
        portrayal = {"Shape": "circle",
                     "Color": "red",
                     "Filled": "true",
                     "Layer": 0,
                     "r": 0.5} 
    elif (agent.stage == LifeStage.Egg):
        portrayal = {"Shape": "C:\\Users\\12032\\embry_riddle\\ma360\\mosquito_model\\resources\\eggs.png",
                     "Scale": 1,
                     "Layer": 1}   
    elif (agent.stage == LifeStage.Adult):
        portrayal = {"Shape": "C:\\Users\\12032\\embry_riddle\\ma360\\mosquito_model\\resources\\mosquito3.png",
                     "Scale": 1,
                     "Layer": 1}
        
    return portrayal

grid = CanvasGrid(agent_portrayal, 50, 50, 750, 750)

chart = ChartModule([{"Label":"Gini", "Color":"Black"}], data_collector_name='datacollector')

server = ModularServer(Model,
                       [grid, chart],
                       "Mosquito Model",
                       {"N":750, "number_of_infected":0, "grid_width":50, "grid_height":50})

server.port = 8521 # The default
server.launch()