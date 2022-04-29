# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 17:17:55 2022

@author: jared
"""
from Model import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter


'''=======Sliders========'''

simulation_params = {
    "number_of_agents":UserSettableParameter(
        "slider",
        "Number of Agents",
        1000,     # default
        100,      # min
        3000,    # max
        100,      # step
        description="How many mosquitos should initially spawn"
    ),
    "number_of_infected":UserSettableParameter(
        "slider",
        "Number of Infected",
        50,      # default
        10,       # min
        500,     # max
        10,       # step
        description="How many mosquitos should initially be infected"
    ),
    "number_of_days":UserSettableParameter(
        "slider",
        "Number of Days",
        30,
        5,
        300,
        5,
        description="How many days the simulation will run for"
    ),
    "release_frequency":UserSettableParameter(
        "slider",
        "Release Frequency",
        7,
        1,
        30,
        1,
        description="How many days between infected release"
    ),
    "grid_width": 50,
    "grid_height": 50
}


def agent_portrayal(agent):
    if (agent.infected):
        portrayal = {"Shape": "circle",
                     "Color": "red",
                     "Filled": "true",
                     "Layer": 0,
                     "r": 0.5}
    else:
        portrayal = {"Shape": "D:\\Repos\\MA360\\mosquito_model\\resources\\mosquito3.png",
                     "Scale": 1,
                     "Layer": 1}
    return portrayal

grid = CanvasGrid(agent_portrayal, 50, 50, 750, 750)

chart = ChartModule([{"Label":"Gini", "Color":"Black"}], data_collector_name='datacollector')

server = ModularServer(Model,
                        [grid, chart],
                        "Mosquito Model",
                        simulation_params
                       )

server.port = 8521 # The default
server.launch()