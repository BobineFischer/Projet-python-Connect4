from pettingzoo.classic import connect_four_v3
import numpy as np


### Tâche 2.2 : Analyse de l'espace d'observation
# TODO: Create environment
env = connect_four_v3.env()
env.reset(seed=42)

# TODO: Get first observation
for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:
        break

    # TODO: Print the observation structure
    print("Agent:", agent)
    print("Observation keys:", observation.keys())
    print("Observation shape:", observation['observation'].shape)
    print("Observation type:", type(observation['observation']))
    print("Action mask:", observation['action_mask'], type(observation['action_mask']))
    #print("Observation:", observation['observation'])

    # TODO: Take a random action (column 3)
    env.step(3)
    break

env.close()


### Tâche 2.3 : Comprendre la représentation du plateau


from pettingzoo.classic import connect_four_v3
import numpy as np

def print_board(observation):
    """
    Print a human-readable version of the board

    observation: numpy array of shape (6, 7, 2)
        observation[:,:,0] = current player's pieces
        observation[:,:,1] = opponent's pieces
    """
    # TODO: Implement this function
    # Hint: Loop through rows and columns
    # Use symbols like 'X', 'O', and '.' for current player, opponent, and empty
    board = np.full((6, 7), ".", dtype=str)
    X = observation[:, :, 0]
    O = observation[:, :, 1]
    board[X == 1] = "X"
    board[O == 1] = "O"

    for row in board:
        print(" ".join(row))

# Test your function
env = connect_four_v3.env()
env.reset(seed=42)

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:
        break

    print(f"\nAgent: {agent}")
    print_board(observation['observation'])

    # Make a few moves to see the board change
    env.step(3)
    if agent == env.agents[1]:
        break

env.close()


### Tâche 2.4 : Créer une boucle de jeu simple

# simple_game.py
from pettingzoo.classic import connect_four_v3

env = connect_four_v3.env(render_mode="rdb_array")  # ou render_mode="rdb_array" ou bien None
env.reset(seed=42)

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:
        action = None
        if reward == 1:
            print(f"{agent} wins!")
        elif reward == 0:
            print("It's a draw!")
    else:
        # Take a random valid action
        mask = observation["action_mask"]
        action = env.action_space(agent).sample(mask)
        print(f"{agent} plays column {action}")

    env.step(action)

input("Press Enter to close...")
env.close()


import numpy as np
mask = np.array([1, 0, 1, 1, 0, 1, 1])
action = env.sample(mask)