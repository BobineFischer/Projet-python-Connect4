# tournoi d'agents

def tournament(agents, env_fn, num_games=100):
    """
    Conduct a tournament among multiple agents in a given environment.

    Parameters:
        agents: List of agent instances
        env_fn: Function that creates a new environment instance
        num_games: Number of games each pair of agents plays
    Returns:
        results: Dictionary with win counts for each agent
    """

    results = {agent.player_name: 0 for agent in agents}

    for i in range(len(agents)):
        for j in range(len(agents)):
            if i != j:

                agent_1 = agents[i]
                agent_2 = agents[j]

                for _ in range(num_games):

                    env = env_fn()
                    env.reset()

                    # Save the ordering of agents before the game starts
                    agents_list = env.agents.copy()
                    winner = None

                    for agent in env.agent_iter():
                        observation, reward, termination, truncation, info = env.last()

                        if termination or truncation:
                            # Determine the winner at the moment of termination
                            if reward == 1:
                                winner = agent
                            elif reward == 0:
                                winner = "draw"

                            env.step(None)
                            continue

                        # Select appropriate agent controller
                        if agent == agents_list[0]:
                            action = agent_1.choose_action(
                                observation["observation"],
                                reward,
                                termination,
                                truncation,
                                info,
                                action_mask=observation["action_mask"]
                            )
                        else:
                            action = agent_2.choose_action(
                                observation["observation"],
                                reward,
                                termination,
                                truncation,
                                info,
                                action_mask=observation["action_mask"]
                            )

                        env.step(action)

                    # Update results after game finishes
                    if winner == agents_list[0]:
                        results[agent_1.player_name] += 1
                    elif winner == agents_list[1]:
                        results[agent_2.player_name] += 1

                    env.close()

    return results

if __name__ == "__main__":
    from pettingzoo.classic import connect_four_v3
    from timed_smart_agent import SmartAgent, RandomAgent, WeightedRandomAgent

    def create_env():
        return connect_four_v3.env(render_mode="rdb_array")

    env = create_env()
    env.reset(seed=42)

    agents = [
        SmartAgent(env, player_name="SmartAgent"),
        RandomAgent(env, player_name="RandomAgent"),
        WeightedRandomAgent(env, player_name="WeightedRandomAgent")
    ]

    tournament_results = tournament(agents, create_env, num_games=10)
    print("Tournoi Simple", "\t", tournament_results)




############################# tournoi plus complet #############################



def full_tournament(agents, env_fn, num_games=100):
    """
    Tournoi complet pairwise entre tous les agents.
    Alternance du premier joueur.
    Retourne un dictionnaire de résultats détaillés.
    """

    results = {}

    for i in range(len(agents)):
        for j in range(i + 1, len(agents)):
            agent1_class = type(agents[i])
            agent2_class = type(agents[j])

            print(f"\n Match: {agents[i].player_name} vs {agents[j].player_name}")

            # On crée des **nouveaux agents pour chaque match** afin d'éviter
            # les problèmes de PettingZoo liés à l'env stocké dans les classes
            agent1 = agent1_class(env=None, player_name=agents[i].player_name)
            agent2 = agent2_class(env=None, player_name=agents[j].player_name)

            match_result = {"wins": 0, "losses": 0, "draws": 0}

            for game in range(num_games):
                env = env_fn()
                env.reset()

                # Alternance du premier joueur
                if game % 2 == 0:
                    order = [agent1, agent2]
                else:
                    order = [agent2, agent1]

                agents_list = env.agents.copy()
                winner = None

                for agent_name in env.agent_iter():
                    observation, reward, terminated, truncated, info = env.last()

                    if terminated or truncated:
                        if reward == 1:
                            winner = agent_name
                        elif reward == 0:
                            winner = "draw"
                        env.step(None)
                        continue

                    # Détermine quel agent doit jouer
                    acting_agent = order[0] if agent_name == agents_list[0] else order[1]

                    action = acting_agent.choose_action(
                        observation["observation"],
                        reward,
                        terminated,
                        truncated,
                        info,
                        action_mask=observation["action_mask"]
                    )

                    env.step(action)

                # Mise à jour des stats
                if winner == "draw":
                    match_result["draws"] += 1
                elif winner == agents_list[0]:
                    match_result["wins" if order[0] == agent1 else "losses"] += 1
                elif winner == agents_list[1]:
                    match_result["wins" if order[1] == agent1 else "losses"] += 1

                env.close()

            results[(agent1.player_name, agent2.player_name)] = match_result
            print(f"Résultats ({agent1.player_name}): {match_result}")

    return results

if __name__ == "__main__":
    from pettingzoo.classic import connect_four_v3
    from timed_smart_agent import SmartAgent, RandomAgent, WeightedRandomAgent

    def create_env():
        return connect_four_v3.env(render_mode="rdb_array")

    agents = [
        SmartAgent(env=None, player_name="SmartAgent"),
        RandomAgent(env=None, player_name="RandomAgent"),
        WeightedRandomAgent(env=None, player_name="WeightedRandomAgent")
    ]

    results = full_tournament(agents, create_env, num_games=100)
    print("\n===== RESULTATS DU TOURNOI =====")
    for k, v in results.items():
        print(f"{k}: {v}")
