"""
Random-based agents for Connect Four.

This module defines:
- RandomAgent: chooses valid actions uniformly at random.
- WeightedRandomAgent: prefers center columns when selecting moves.
"""

import random
from loguru import logger


class RandomAgent:
    """
    A simple agent that plays randomly among valid actions.
    """

    def __init__(self, env, player_name=None):
        """
        Initialize the random agent.

        Parameters:
            env: PettingZoo environment instance.
            player_name: Optional name for the agent.
        """
        self.env = env
        self.player_name = player_name or "RandomAgent"

    def choose_action(
        self,
        observation,
        reward=0.0,
        terminated=False,
        truncated=False,
        info=None,
        action_mask=None
    ):
        """
        Choose a random valid action using the PettingZoo `.sample(mask)` API.

        Parameters:
            observation: dict containing board state and "action_mask".
            action_mask: numpy array (7,) indicating valid actions.
            Other params unused but kept for compatibility.

        Returns:
            int: selected column (0–6), or None if game ended.
        """
        if terminated or truncated:
            return None

        mask = observation["action_mask"]
        action_space = self.env.action_space(self.player_name)
        return action_space.sample(mask)

    def choose_action_manual(
        self,
        observation,
        reward=0.0,
        terminated=False,
        truncated=False,
        info=None,
        action_mask=None
    ):
        """
        Same as choose_action(), but implemented manually
        without relying on `.sample(mask)`.

        Returns:
            int: selected column (0–6), or None if game ended.
        """
        if terminated or truncated:
            return None

        mask = observation["action_mask"]
        valid_actions = [i for i, valid in enumerate(mask) if valid == 1]

        if not valid_actions:
            return None

        return random.choice(valid_actions)


class WeightedRandomAgent(RandomAgent):
    """
    Random agent that prefers center columns using weighted sampling.
    """

    def choose_action(
        self,
        observation,
        reward=0.0,
        terminated=False,
        truncated=False,
        info=None,
        action_mask=None
    ):
        """
        Choose an action with weighted probability favoring the center column.

        Returns:
            int: selected column (0–6), or None if game ended.
        """
        if terminated or truncated:
            logger.info("Game over, no action to choose")
            return None

        mask = action_mask if action_mask is not None else observation["action_mask"]

        # Center-favoring weights
        weights = [1, 2, 3, 4, 3, 2, 1]

        valid_actions = [i for i, valid in enumerate(mask) if valid == 1]

        if not valid_actions:
            logger.warning("No valid actions available")
            return None

        valid_weights = [weights[i] for i in valid_actions]
        return random.choices(valid_actions, weights=valid_weights, k=1)[0]
