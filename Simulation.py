import numpy as np
import Agents
import World
import Visual

"""     Episode Properties      """



def play_episode(player, map_layout):
    n_NPC = 1
    episode = World.Map(map_layout, n_NPC)
    episode.gen_agent_positions(sections=4)
    # episode.gen_non_random_position()
    # Assign agent position
    player.current_pos = episode.start_pos

    # NPCs make first move
    # for i in range(n_NPC):
    #     episode.NPC_list[i].current_actions = episode.get_direction(i)
    #     episode.NPC_list[i].first_move()
    # Update NPC positions
    episode.update_positions(episode.start_pos, episode.start_pos)
    episode.get_data()

    while episode.run:
        # Get state data for agent
        episode.get_data()
        # Agent makes move based on state data
        player_choice = player.get_NN_output(episode.data[-1].reshape((1, 9)))
        player_v_pos = player.make_move(player_choice, episode.layout)

        # NPC make moves
        # for i in range(n_NPC):
        #     episode.NPC_list[i].current_actions = episode.get_direction(i)
        #     episode.NPC_list[i].move()

        # Update all positions
        episode.update_positions(player_v_pos, player.current_pos)
        episode.get_reward()
        episode.check_goals()

    state = episode.data.copy()
    reward = episode.rewards
    player_ah = player.action_history
    player_nndata = player.NN_data.copy()
    player.reset_episode_info()

    feedback = [sum(episode.rewards), len(episode.rewards), episode.goal, episode.rings]

    episode = None
    return state, reward, player_ah, player_nndata, feedback

def epoch(n_epoch, player, map_layout, gen):
    winrate_history = []
    avg_reward = []
    n_episode = 20
    for n in range(n_epoch):
        win_history = []
        reward_history = []
        state_array = np.empty((0, 9))
        reward_array = np.array([])
        action_array = np.array([])
        nndata_array = np.empty((0, 4))
        ring_count = 0
        for nn in range(n_episode):
            ep_state, ep_r, p_ah, p_nnd, episode_results = play_episode(player, map_layout)
            ring_count += episode_results[-1]
            ep_state = np.delete(ep_state, 0, 0)
            if episode_results[2]:
                win_history.append(1)
            else:
                win_history.append(0)
            state_array = np.vstack((state_array, ep_state))
            reward_array = np.append(reward_array, ep_r)
            action_array = np.append(action_array, p_ah)
            nndata_array = np.vstack((nndata_array, p_nnd))
            reward_history.append(episode_results[0])
        player.train_NN(state_array, reward_array, action_array, nndata_array)
        player.model.save(f'./Keras_Weights/Simple_Map/{gen}weights{n}.keras')
        winrate = sum(win_history)/n_episode
        winrate_history.append(winrate)
        avg_reward.append(sum(reward_history)/n_episode)
        print(f"Epoch: {n}/{n_epoch} | Winrate: {winrate} | Average reward: {sum(reward_history)/n_episode} | Ring_count: {ring_count}")
        if winrate > 0.5:
            player.l_rate = 0.8
        if winrate > 0.75:
            player.l_rate = 0.5
        # if winrate > 0.9:
        #     # weight = player.model.get_weights()
        #     # np.savetxt('weight.csv', weight, fmt='%s', delimiter=',')
        #     # np.savetxt('winrate.csv', winrate_history, fmt='%s', delimiter=',')
        #     # np.savetxt('average_rewards.csv', avg_reward, fmt='%s', delimiter=',')
        #     break
    return winrate_history, avg_reward







# start episode
#   gen world!
#   gen NPC and agent positions!
#   gen objective positions!
#   Start game sequence
#       NPC makes move
#       collect state data
#       agent outputs choice
#       get reward
#       store data
#   End game sequence
#   Train Agent NN
#   End Episode
