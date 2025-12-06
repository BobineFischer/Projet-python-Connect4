import numpy as np
import time
from smart_agent import SmartAgent
from pettingzoo.classic import connect_four_v3
env = connect_four_v3.env(render_mode="rdb_array") # ou render_mode="rdb_array" ou bien None
env.reset(seed=42)

# test _get_valid_actions
agent = SmartAgent(env)
mask = [1, 1, 1, 1, 1, 1, 1]  # All columns valid
assert agent._get_valid_actions(mask) == [0, 1, 2, 3, 4, 5, 6]

mask = [0, 1, 0, 1, 0, 1, 0]  # Only odd columns
assert agent._get_valid_actions(mask) == [1, 3, 5]

# test _get_next_row
# Empty board - piece goes to bottom
board = np.zeros((6, 7, 2))
assert agent._get_next_row( board, 3) == 5

# Column with one piece - next piece goes on top
board[5, 3, 0] = 1
assert agent._get_next_row(board, 3) == 4


# test _check_win_from_position
board = np.zeros((6, 7, 2))
# Horizontal win
board[5, 0:3, 0] = 1
assert agent._check_win_from_position(board, 5, 3, 0) == True

# test _winning_move
board = np.zeros((6, 7, 2))
board[5, 0:3, 0] = 1
valid_actions = [3, 4, 5, 6]
assert agent._find_winning_move(board, valid_actions, 0) == 3

# test _block_opponent_win
board = np.zeros((6, 7, 2))
board[5, 0:3, 1] = 1
valid_actions = [3, 4, 5, 6]
assert agent._find_winning_move(board, valid_actions, 1) == 3


def game_smart_vs_random():
    env = connect_four_v3.env(render_mode="rdb_array")  # ou render_mode="rdb_array" ou bien None
    env.reset(seed=42)
    agents = env.agents
    p0 = agents[0]  # Smart Agent
    p1 = agents[1] 

    for agent in env.agent_iter():
        observation, reward, termination, truncation, info = env.last()


        if not (termination or truncation):
            if agent == p0:
                action = SmartAgent(env,agent).choose_action(observation["observation"], reward, termination, truncation, info, action_mask=observation["action_mask"])

            else:
                mask = observation["action_mask"]
                action = env.action_space(agent).sample(mask)
            #print(f"{agent} plays column {action}")
        else:
            action = None
            if reward == 1:
                return agent
            elif reward == 0:
                return "draw"

        env.step(action)

    env.close()

print(" Result of one game Smart VS Random : ", game_smart_vs_random())

def test_smart_vs_random(num_games=100):
    win_p0 = 0
    win_p1 = 0
    draw = 0
    for _ in range(num_games):
        if game_smart_vs_random()=="player_0":
            win_p0+=1
        if game_smart_vs_random()=="player_1":
            win_p1+=1
        if game_smart_vs_random()=="draw":
            draw+=1
    
    dict_results = {
        "SmartAgent wins": win_p0,
        "RandomAgent wins": win_p1,
        "Draws": draw
    }
    return dict_results

print(f" Results after 100 games : {test_smart_vs_random(100)}")
