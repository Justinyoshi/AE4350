import numpy as np
import Agents
import World
import Visual
import Simulation
import Maps
import matplotlib.pyplot as plt

generation = 2
player = Agents.Agent(0, (0, 0), 0, 2, 0.25)
# player.create_NN()
player.use_existing_model('./Keras_Weights/9weights19.keras')

map_layout = Maps.simple_map()
w, r_a = Simulation.epoch(20, player, map_layout, generation)
np.savetxt(f'./Keras_Weights/Simple_Map/winrate_gen{generation}.csv', w, fmt='%s', delimiter=',')
np.savetxt(f'./Keras_Weights/Simple_Map/average_rewards_gen{generation}.csv', r_a, fmt='%s', delimiter=',')

plt.plot(np.arange(len(w)), w)
plt.show()
plt.plot(np.arange(len(r_a)), r_a)
plt.show()











