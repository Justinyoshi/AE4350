import numpy as np
import Agents


class Map:
    def __init__(self, layout, n_npc):
        self.layout = layout
        self.height = layout.shape[0]
        self.width = layout.shape[1]
        self.mapsize = (self.width, self.height)
        self.positions = []
        self.v_position = []
        self.n_npc = n_npc
        self.data = np.empty((0, 9))
        self.goal = False
        self.lose = False
        self.run = True
        # self.lose_points = -0.5 * np.floor(np.sqrt(self.width*self.height))
        self.lose_points = -60
        self.rewards = []
        self.tot_reward = 0
        self.coordinates = []
        self.rings = 0
        for i in range(self.height):
            for j in range(self.width):
                self.coordinates.append((j, i))

    def get_direction(self, ID):
        IDpos = self.NPC_list[ID].current_pos
        temp_map = np.copy(self.layout)
        # Check if the NPCs are not within close proximity to crash into each other
        for i in range(self.n_npc):
            if i != ID:
                i_pos = self.NPC_list[i].current_pos
                temp_map[i_pos[1]-1:i_pos[1]+2, i_pos[0]-1:i_pos[0]+2] = np.ones(shape=(3, 3))
        directions = {'left': 0, 'up': 0, 'right': 0, 'down': 0}
        d_map = temp_map[IDpos[1]-1:IDpos[1]+2, IDpos[0]-1:IDpos[0]+2]
        if d_map[0, 1] == 0:
            directions['up'] = 1
        if d_map[1, 0] == 0:
            directions['left'] = 1
        if d_map[1, 2] == 0:
            directions['right'] = 1
        if d_map[2, 1] == 0:
            directions['down'] = 1
        return directions

    def gen_agent_positions(self, sections):
        choice = np.random.choice(np.arange(sections), 2, replace=False)
        sub_choice = np.random.choice([0, 1, 2, 3], 2)
        section_size = [self.height / np.floor(np.sqrt(sections)),
                        self.width / (sections / np.floor(np.sqrt(sections)))]  # y, x
        self.m_pos = []
        start_pos = False
        while not start_pos:
            r_int = [np.random.choice(np.arange(self.height)), np.random.choice(np.arange(self.width))]
            if self.layout[r_int[0], r_int[1]] == 0:
                self.m_pos.append(tuple(self.coordinates[r_int[0] * self.width + r_int[1]]))
                start_pos = True
        for i in range(len(choice)):
            pos_options = []
            y_row = np.floor(choice[i] / (sections / np.floor(np.sqrt(sections))))
            y_range = [int(y_row * np.floor(section_size[0])), int((y_row + 1) * np.floor(section_size[0]))]
            x_row = choice[i] % np.floor(np.sqrt(sections))
            x_range = [int(x_row * np.ceil(section_size[1])), int((x_row + 1) * np.ceil(section_size[1]))]
            if sub_choice[i] > 1:
                y_range[0] = int((y_range[1] - y_range[0]) / 2) + y_range[0]
            else:
                y_range[1] = int((y_range[1] - y_range[0]) / 2) + y_range[0]
            if sub_choice[i] % 2 > 0:
                x_range[0] = int((x_range[1] - x_range[0]) / 2) + x_range[0]
            else:
                x_range[1] = int((x_range[1] - x_range[0]) / 2) + x_range[0]
            for j in np.arange(y_range[0], y_range[1]):
                for k in np.arange(x_range[0], x_range[1]):
                    if self.layout[j, k] == 0:
                        pos_options.append(tuple(self.coordinates[j * self.width + k]))
            rand_int = np.random.choice(np.arange(len(pos_options)))
            self.m_pos.append(tuple(pos_options[rand_int]))

        self.start_pos = self.m_pos[0]
        self.pickup_pos = self.m_pos[1]
        self.delivery_pos = self.m_pos[2]
        self.current_objective = self.m_pos[1]

        self.positions = [self.start_pos]
        # self.NPC_list = []
        # for i in range(self.n_npc):
        #     cycle = True
        #     while cycle:
        #         npc_rand_int = [np.random.choice(np.arange(self.height)), np.random.choice(np.arange(self.width))]
        #         if self.layout[npc_rand_int[0], npc_rand_int[1]] == 0 and abs(npc_rand_int[1]-self.start_pos[0]) > 2 and abs(npc_rand_int[0]-self.start_pos[1]):
        #             self.positions.append(tuple(self.coordinates[npc_rand_int[0] * self.width + npc_rand_int[1]]))
        #             cycle = False
        #     self.NPC_list.append(Agents.NPC(i, self.positions[i+1]))

    def gen_non_random_position(self):
        self.m_pos = []
        start_pos = False
        while not start_pos:
            r_int = [np.random.choice(np.arange(self.height)), np.random.choice(np.arange(self.width))]
            if self.layout[r_int[0], r_int[1]] == 0:
                self.m_pos.append(tuple(self.coordinates[r_int[0] * self.width + r_int[1]]))
                start_pos = True
        # self.m_pos[0] = (8, 2)
        self.m_pos.append((8, 8))
        self.m_pos.append((8, 8))
        self.start_pos = self.m_pos[0]
        self.pickup_pos = (8, 8)
        self.delivery_pos = (8, 8)
        self.current_objective = (8, 8)
        self.positions = [self.start_pos, (1, 8)]
        # self.NPC_list = [Agents.NPC(0, self.positions[1])]


    def update_positions(self, v_pos, agent_pos):
        self.v_position = v_pos
        self.positions[0] = agent_pos
        # for i in range(self.n_npc):
        #     self.positions[i+1] = self.NPC_list[i].current_pos

    def check_goals(self):
        if self.positions[0] == self.current_objective:
            self.current_objective = self.delivery_pos
            self.goal = True
        elif self.current_objective == self.delivery_pos and self.positions[0] == self.current_objective:
            self.goal = True
        if self.tot_reward <= self.lose_points:
            self.lose = True
        if self.lose or self.goal:
            self.run = False

    def get_data(self):
        data = np.array([])
        i_pos = self.positions[0]
        data = np.append(data, [self.layout[i_pos[1], i_pos[0]-1], self.layout[i_pos[1]-1, i_pos[0]], self.layout[i_pos[1], i_pos[0]+1], self.layout[i_pos[1]+1, i_pos[0]]])
        data = np.append(data, [i_pos[0], i_pos[1]])
        data = np.append(data, [self.current_objective[0]/self.width, self.current_objective[1]/self.height])
        data = np.append(data, (abs(self.current_objective[0]-i_pos[0])+abs(self.current_objective[1]-i_pos[1])))
        npc_ref = self.height * self.width
        # for i in range(self.n_npc):
        #     npc_pos = self.NPC_list[i].current_pos
        #     npc_distance = abs(npc_pos[0]-i_pos[0]) + abs(npc_pos[1]-i_pos[1])
        #     if npc_distance < npc_ref:
        #         npc_ref = npc_distance
        #         npc_close_pos = npc_pos
        #     else:
        #         npc_close_pos = (0, 0)
        # data = np.append(data, [npc_close_pos[0]/self.width, npc_close_pos[1]/self.height, npc_ref / (self.height+self.width)])
        #
        # data = np.append(data, [0, 0, (i_pos[0]+i_pos[1])/(self.height+self.width)])
        self.data = np.vstack((self.data, data))

    def get_reward(self):
        wall = -0.75
        step = -0.05
        closer = 0.06
        goal = 2
        ring_reward = 0.5
        if self.layout[self.v_position[1], self.v_position[0]] == 1:
            r_t = step + wall
            self.v_position = self.positions[0]
        elif self.v_position in self.positions[1:]:
            r_t = step + self.lose_points
        elif self.v_position == self.current_objective:
            r_t = step + goal
        else:
            if self.data[-1, 8] < self.data[-2, 8]:
                r_t = step + closer
            else:
                r_t = step
        # if self.data[-1, 8] <= 0.5*self.width and np.count_nonzero(self.data[:, 8] <= 0.5*self.width) == 1:
        #     r_t += ring_reward
        #     self.rings += 1
        # elif self.data[-1, 8] <= 0.25*self.width and np.count_nonzero(self.data[:, 8] <= 0.25*self.width) == 1:
        #     r_t += ring_reward
        #     self.rings += 1
        self.tot_reward += r_t
        self.rewards.append(r_t)






















