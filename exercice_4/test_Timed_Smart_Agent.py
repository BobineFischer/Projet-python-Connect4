import numpy as np
import time
from timed_smart_agent import Timed_SmartAgent
from pettingzoo.classic import connect_four_v3
env = connect_four_v3.env(render_mode="rdb_array") # ou render_mode="rdb_array" ou bien None
env.reset(seed=42)



def game_smart_vs_random(time=False):
    env = connect_four_v3.env(render_mode="rdb_array")  # ou render_mode="rdb_array" ou bien None
    env.reset(seed=42)
    agents = env.agents
    p0 = agents[0]  # Smart Agent
    p1 = agents[1] 

    for agent in env.agent_iter():
        observation, reward, termination, truncation, info = env.last()


        if not (termination or truncation):
            if agent == p0:
                action = Timed_SmartAgent(env,agent).choose_action(observation["observation"], reward, termination, truncation, info, action_mask=observation["action_mask"], Time=time)

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

print(game_smart_vs_random(time=True))

def test_smart_vs_random_timed(num_games=100):
    win_p0 = 0
    win_p1 = 0
    draw = 0
    durations = []
    for _ in range(num_games):
        start = time.time()
        battle = game_smart_vs_random()
        end = time.time()
        durations.append((end - start)*1000)  # duration in milliseconds
        if battle=="player_0":
            win_p0+=1
        if battle=="player_1":
            win_p1+=1
        if battle=="draw":
            draw+=1
    
    dict_results = {
        "SmartAgent wins": win_p0,
        "RandomAgent wins": win_p1,
        "Draws": draw,
        "Duration (ms)": np.round(np.mean(durations),4)
    }
    return dict_results

print(" Results of (500) games Smart VS Random with timing : ", test_smart_vs_random_timed((500)))
