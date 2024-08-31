import numpy as np
import keras
from keras import models
from keras import layers
import random


class Agent:
    def __init__(self, ID, pos_init, rscore_init, l_rate, d_rate):
        self.ID = ID
        self.current_pos = pos_init
        self.reward_score = rscore_init
        self.learning_rate = l_rate
        self.discount_rate = d_rate
        self.epsilon = 1
        self.current_actions = []
        self.action_history = []
        self.pos_history = [pos_init]
        self.NN_data = np.empty((0, 4))

    def make_move(self, choice, map):
        self.action_history.append(choice)
        if choice == 'up':
            v_pos = (self.current_pos[0], self.current_pos[1] - 1)
        elif choice == 'down':
            v_pos = (self.current_pos[0], self.current_pos[1] + 1)
        elif choice == 'left':
            v_pos = (self.current_pos[0] - 1, self.current_pos[1])
        else:
            v_pos = (self.current_pos[0] + 1, self.current_pos[1])
        if map[v_pos[1], v_pos[0]] == 0:
            self.current_pos = v_pos
        self.pos_history.append(self.current_pos)
        return v_pos
    """         Neural Network Functions            """
    def create_NN(self):
        self.model = models.Sequential()
        self.model.add(layers.Dense(6, input_dim=9, activation='softmax'))
        self.model.add(layers.Dense(6, activation='softmax'))
        self.model.add(layers.Dense(4, activation='softmax'))
        self.model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])

    def use_existing_model(self, file):
        self.model = models.load_model(file)

    def train_NN(self, data, rewards, directions, y_train):
        choices = np.array(['left', 'up', 'right', 'down'])
        for i in range(len(rewards)):
            v_i = 0
            if i + 5 > len(rewards):
                for n in range(len(rewards)-i):
                    v_i += rewards[i + n] * self.discount_rate ** (n)
            else:
                for n in range(5):
                    v_i += rewards[i + n] * self.discount_rate ** (n)
            # for c in range(len(choices)):
            #     if choices[c] == directions[i]:
            #         y_train[i, c] += v_i * self.learning_rate * np.log(y_train[i, c])
            #     else:
            #         y_train[i, c] -= v_i * self.learning_rate * np.log(y_train[i, c])/6
            if rewards[i] <= -0.5:
                y_train[i, np.where(choices == directions[i])[0][0]] = 0
            else:
                if directions[i] == 'left':
                    y_train[i, 0] += v_i * self.learning_rate * abs(np.log(y_train[i, 0]))
                elif directions[i] == 'up':
                    y_train[i, 1] += v_i * self.learning_rate * abs(np.log(y_train[i, 1]))
                elif directions[i] == 'right':
                    y_train[i, 2] += v_i * self.learning_rate * abs(np.log(y_train[i, 2]))
                else:
                    y_train[i, 3] += v_i * self.learning_rate * abs(np.log(y_train[i, 3]))

        self.model.fit(data, y_train, verbose=None)

    def get_NN_output(self, data):
        choices = ['left', 'up', 'right', 'down']
        action = self.model.predict(data, verbose = None)[0]
        self.NN_data = np.vstack((self.NN_data, action))
        primary_choice = choices[np.argmax(action)]
        alt_choice = np.random.choice(choices, p=action)
        # print(action)
        final_choice = np.random.choice([primary_choice, alt_choice], p=[0.8, 0.2])
        return final_choice

    def reset_episode_info(self):
        self.current_actions = []
        self.action_history = []
        self.pos_history = [(0, 0)]
        self.NN_data = np.empty((0, 4))






#
# class NPC:
#     def __init__(self, ID, pos):
#         self.IDs = ID  # 1xn array
#         self.current_pos = pos  # 1xn array
#         self.current_actions = {}
#         self.action_history = []
#         self.pos_history = [pos]
#
#     def first_move(self):
#         choice_bool = True
#         while choice_bool:
#             choice, value = random.choice(list(self.current_actions.items()))
#             if value == 1:
#                 self.data_update(choice)
#                 choice_bool = False
#
#     def move(self):
#         p_choice = np.zeros(4)
#         n_choices = sum(list(self.current_actions.values()))
#         index = np.where(np.array(list(self.current_actions.keys())) == self.action_history[-1])[0][0]
#         if n_choices == 1:
#             for key in self.current_actions:
#                 if self.current_actions[key] == 1:
#                     choice = key
#         else:
#             if n_choices == 2:
#                 if self.current_actions[self.action_history[-1]] == 1:
#                     p_choice[index] = 0.9
#                     p_choice[index-2] = 0.1
#                 else:
#                     d_list = np.array(list(self.current_actions.keys()))
#                     p_choice[index-2] = 0.1
#                     if self.current_actions[d_list[index-3]] == 1:
#                         p_choice[index-3] = 0.9
#                     else:
#                         p_choice[index-1] = 0.9
#             elif n_choices == 3:
#                 option = -2
#                 if self.current_actions[self.action_history[-1]] == 0:
#                     p_choice[index + option] = 0.1
#                     p_choice[index + option + 1] = 0.45
#                     p_choice[index + option - 1] = 0.45
#                 else:
#                     p_choice[index + option] = 0.1
#                     p_choice[index] = 0.45
#                     if list(self.current_actions.values())[index-1] == 1:
#                         p_choice[index-1] = 0.45
#                     else:
#                         if index > 2:
#                             p_choice[index-3] = 0.45
#                         else:
#                             p_choice[index+1] = 0.45
#             else:
#                 p_choice[index-2] = 0.1
#                 p_choice[index] = 0.3
#                 p_choice[index-1] = 0.3
#                 p_choice[index-3] = 0.3
#             choice = str(np.random.choice(list(self.current_actions.keys()), size=1, p=p_choice)[0])
#         self.data_update(choice)
#
#     def data_update(self, choice):
#         self.action_history.append(choice)
#         if choice == 'up':
#             self.current_pos = (self.current_pos[0], self.current_pos[1] - 1)
#         elif choice == 'down':
#             self.current_pos = (self.current_pos[0], self.current_pos[1] + 1)
#         elif choice == 'left':
#             self.current_pos = (self.current_pos[0] - 1, self.current_pos[1])
#         else:
#             self.current_pos = (self.current_pos[0] + 1, self.current_pos[1])
#         self.pos_history.append(self.current_pos)


