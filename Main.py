import sys
import time

import pygame
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import Agents
import World
import Visual
import Maps



# Pygame Properties
black = 0, 0, 0
White = 255, 255, 255
gray = 180, 180, 180
red = 199, 30, 30
size_block = 32     # 16x16 pixels
n_NPC = 1


# Initialize World set-up
map_layout = Maps.simple_map()
episode = World.Map(map_layout, n_NPC)
episode.gen_non_random_position()

player = Agents.Agent(0, episode.start_pos, 0, 0.3, 0.8)
player.use_existing_model('./Keras_Weights/Complex_Map/36weights19.keras')
player.current_pos = episode.start_pos
# for i in range(n_NPC):
#     episode.NPC_list[i].current_actions = episode.get_direction(i)
#     episode.NPC_list[i].first_move()
episode.get_data()



# Initialize pygame
pygame.init()
clock = pygame.time.Clock()
screen_size = np.multiply(size_block, episode.mapsize)
screen = pygame.display.set_mode(screen_size)
r = pygame.Rect(100, 100, 50, 50)



run = True
while run:
    clock.tick(2)

    Visual.Map_setup(screen, episode.layout, episode.coordinates, size_block, episode.m_pos)
    Visual.Draw_agents(screen, episode.positions, size_block)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()





#
# run = True
# while run:
#     clock.tick(2)
#
#     Visual.Map_setup(screen, episode.layout, episode.coordinates, size_block, episode.m_pos)
#     Visual.Draw_agents(screen, episode.positions, size_block)
#
#     # new moves
#     # Get state data for agent
#     episode.get_data()
#     # Agent makes move based on state data
#     player_choice = player.get_NN_output(episode.data[-1].reshape((1, 9)))
#     player_v_pos = player.make_move(player_choice, episode.layout)
#
#     # NPC make moves
#     # for i in range(n_NPC):
#     #     episode.NPC_list[i].current_actions = episode.get_direction(i)
#     #     episode.NPC_list[i].move()
#
#     # Update all positions
#     episode.update_positions(player_v_pos, player.current_pos)
#     episode.get_reward()
#     episode.check_goals()
#
#
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#
#     pygame.display.update()
#
# pygame.quit()





"""Program Flow"""
# Initialize Agent
# Initialize simulation sequence
#   100-1000 game batches
#   start episode
#   gen world
#   gen NPC and agent positions
#   gen objective positions
#   Start game sequence
#       NPC makes move
#       collect state data
#       agent outputs choice
#       get reward
#       store data
#   End game sequence
#   Train Agent NN
#   End Episode
# End simulation sequence
# Present data with graphs
#   Win% per batch
#   Reward progress
#   Win% progress
#   Sensitivity analysis.




