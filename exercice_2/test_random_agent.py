from pettingzoo.classic import connect_four_v3
from random_agent import RandomAgent, WeightedRandomAgent
from loguru import logger

env = connect_four_v3.env(render_mode="rdb_array") # ou render_mode="rdb_array" ou bien None
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

env.close()


def test_random_agent(num_games):
    '''
    Test the RandomAgent by playing num_games games against itself.

    Parameters:
         num_games: int, number of games to play

    Returns : 
    - wins: dict with number of wins for each agent
    - draws: number of draws
    - avg_moves: average number of moves per game

    '''
    env = connect_four_v3.env(render_mode="rdb_array") # ou render_mode="rdb_array" ou bien None
    env.reset(seed=42)

    pr_wins = {agent: 0 for agent in env.agents}
    num_draws = 0
    avg_moves = {agent: 0 for agent in env.agents}
    minimax = []

    for _ in range(num_games):
        env.reset(seed=42)
        count = 0
        
        for agent in env.agent_iter():
            observation, reward, termination, truncation, info = env.last()

            if termination or truncation:
                action = None
                minimax.append(count)
                if reward == 1:
                    pr_wins[agent] += 1
                elif reward == 0:
                    num_draws += 1
            else:
                # Take a random valid action
                
                action = RandomAgent(env, agent).choose_action(observation, reward, termination, truncation, info, action_mask=observation["action_mask"])

                avg_moves[agent] += 1
                count += 1

            env.step(action)

    env.close()
    for agent in avg_moves:
        avg_moves[agent] /= num_games
    
    avg_moves["total"] = round(sum(avg_moves.values()), 2)

    for agent in pr_wins:
        pr_wins[agent] /= (num_games/100)
    
    print("random agent results :")
    print("win pourcentage : ", pr_wins)
    print("total of drawns : ", num_draws) 
    print("minimum of moves : " , min(minimax))
    print("maximum of moves : " , max(minimax))
    print("average number of moves : " ,avg_moves) 

print(test_random_agent(100))





def test_weigted_random_agent(num_games):
    '''
    Test the Weighted—RandomAgent by playing num_games games against itself.

    Parameters:
         num_games: int, number of games to play

    Returns : 
    - wins: dict with number of wins for each agent
    - draws: number of draws
    - avg_moves: average number of moves per game

    '''
    env = connect_four_v3.env(render_mode="rdb_array") # ou render_mode="rdb_array" ou bien None
    env.reset(seed=42)

    pr_wins = {agent: 0 for agent in env.agents}
    num_draws = 0
    avg_moves = {agent: 0 for agent in env.agents}
    minimax = []

    for _ in range(num_games):
        env.reset(seed=42)
        count = 0
        
        for agent in env.agent_iter():
            observation, reward, termination, truncation, info = env.last()

            if termination or truncation:
                action = None
                minimax.append(count)
                if reward == 1:
                    pr_wins[agent] += 1
                elif reward == 0:
                    num_draws += 1
            else:
                # Take a random valid action
                
                action = WeightedRandomAgent(env, agent).choose_action(observation, reward, termination, truncation, info, action_mask=observation["action_mask"])

                avg_moves[agent] += 1
                count += 1

            env.step(action)

    env.close()
    for agent in avg_moves:
        avg_moves[agent] /= num_games
    
    avg_moves["total"] = round(sum(avg_moves.values()), 2)

    for agent in pr_wins:
        pr_wins[agent] /= (num_games/100)
    
    print("weigted random agent results :")
    print("victory pourcentage : ", pr_wins)
    print("total of drawns : ", num_draws) 
    print("minimum of moves : " , min(minimax))
    print("maximum of moves : " , max(minimax))
    print("average number of moves : " ,avg_moves) 

print(test_weigted_random_agent(100))