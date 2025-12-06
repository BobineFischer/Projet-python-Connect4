import numpy as np
import time
from timed_smart_agent import SmartAgent
from pettingzoo.classic import connect_four_v3
env = connect_four_v3.env(render_mode="rdb_array") # ou render_mode="rdb_array" ou bien None
env.reset(seed=42)

# Détecter une victoire immédiate
board = np.zeros((6, 7, 2))
board[5, 0:3, 0] = 1  # Trois pièces alignées pour le joueur 0
agent = SmartAgent(env)
valid_actions = [3, 4, 5, 6]
winning_move = agent._find_winning_move(board, valid_actions, channel=0)
assert winning_move == 3

# Bloquer une victoire de l'adversaire
board = np.zeros((6, 7, 2))
board[5, 0:3, 1] = 1  # Trois pièces alignées pour le joueur 1
agent = SmartAgent(env)
valid_actions = [3, 4, 5, 6]
blocking_move = agent._find_winning_move(board, valid_actions, channel=1)
assert blocking_move == 3

# Jouer au centre si disponible
board = np.zeros((6, 7, 2))
board[5, 3, :] = 0  # Centre disponible
agent = SmartAgent(env)
valid_actions = [0, 1, 2, 3, 4, 5, 6]
center_move = agent.choose_action(board, action_mask=[1, 1, 1, 1, 1, 1, 1]) # on peut jouer partout
assert center_move == 3

# Jouer un coup aléatoire lorsque aucune autre règle ne s'applique
board = np.zeros((6, 7, 2))
board[5, 3, :] = 1  # Centre occupé
agent = SmartAgent(env)
valid_actions = [0, 1, 2, 4, 5, 6]
random_move = agent.choose_action(board, action_mask=[1, 1, 1, 0, 1, 1, 1]) # on peut jouer partout sauf au centre
assert random_move in valid_actions

# Test complet de jeu entre SmartAgent et un agent aléatoire    
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

print(game_smart_vs_random())