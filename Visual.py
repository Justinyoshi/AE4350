import numpy as np
import pygame

black = 0, 0, 0
white = 255, 255, 255
gray = 180, 180, 180
lblue = 64, 119, 207
red = 199, 30, 30
oker  = 105, 93, 16
green = 0, 128, 0


# Pickup Shape
def get_pickup_shape(b, c):
    return [(b/2, b/2-c), (b/2+c, b/2), (b/2, b/2+c), (b/2-c, b/2)]


def get_finish_shape(b, d, l):
    return [(b/2-d/2, b/2+l/3+d/2), (b/2+d/2, b/2+l/3+d/2), (b/2+d/2, b/2+l/3), (b/2, b/2+l/3), (b/2, b/2-l*2/3),
            (b/2-d/2, b/2-l/2), (b/2, b/2-l/3), (b/2, b/2+l/3), (b/2-d/2, b/2+l/3)]


# Set up Map
def Map_setup(surface, map, positions, block_size, pos_goals):
    for y in range(map.shape[0]):
        for x in range(map.shape[1]):
            block = pygame.Rect(np.multiply(block_size, positions[map.shape[1]*y + x]), (block_size, block_size))
            if map[y, x] == 0:
                pygame.draw.rect(surface, color=gray, rect=block)

            else:
                pygame.draw.rect(surface, color=black, rect=block)
    pickup_points = get_pickup_shape(block_size, block_size/2)
    pickup_coords = np.add(np.multiply(pos_goals[1], block_size), pickup_points)
    pygame.draw.polygon(surface, color=oker, points=pickup_coords)
    goal_points = get_finish_shape(block_size, 10, 20)
    goal_coords = np.add(np.multiply(pos_goals[2], block_size), goal_points)
    pygame.draw.polygon(surface, color=lblue, points=goal_coords)


def Draw_agents(surface, pos_agents, block_size):
    for i in range(len(pos_agents)):
        if i == 0:
            pygame.draw.circle(surface, color=green, center=(block_size*(1/2+pos_agents[i][0]), block_size*(1/2+pos_agents[i][1])), radius=block_size/3)
        # else:
        #     NPC_rect = pygame.Rect((block_size*(1/4+pos_agents[i][0]), block_size*(1/4+pos_agents[i][1])), (block_size/2, block_size/2))
        #     pygame.draw.rect(surface, color=red, rect=NPC_rect)



def Simulation():
    return



