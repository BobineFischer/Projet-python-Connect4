"""
Smart, timed, and random agents for Connect Four.
Includes:
- SmartAgent
- TimedSmartAgent
- RandomAgent
- WeightedRandomAgent
"""

import time
import tracemalloc
import random
import numpy as np
from loguru import logger


# ======================================================================
#                               SMART AGENT
# ======================================================================

class SmartAgent:
    """
    A rule-based agent that plays strategically.
    """

    def __init__(self, env=None, player_name=None):
        self.player_name = player_name or "SmartAgent"

    def choose_action(self, observation, reward=0.0,
                      terminated=False, truncated=False,
                      info=None, action_mask=None):
        """
        Strategy priority:
        1. Win if possible
        2. Block opponent
        3. Prefer center
        4. Random valid move
        """
        if terminated or truncated:
            return None

        valid_actions = self._get_valid_actions(action_mask)

        # 1) Win
        move = self._find_winning_move(observation, valid_actions, channel=0)
        if move is not None:
            return move

        # 2) Block opponent
        move = self._find_winning_move(observation, valid_actions, channel=1)
        if move is not None:
            return move

        # 3) Prefer center
        if 3 in valid_actions:
            return 3

        # 4) Fallback random
        return random.choice(valid_actions)

    def _get_valid_actions(self, action_mask):
        return [i for i, valid in enumerate(action_mask) if valid == 1]

    def _find_winning_move(self, observation, valid_actions, channel):
        board = observation.copy()

        for col in valid_actions:
            row = self._get_next_row(board, col)
            if row is None:
                continue

            board[row, col, channel] = 1
            if self._check_win_from_position(board, row, col, channel):
                return col

        return None

    def _get_next_row(self, board, col):
        for row in range(5, -1, -1):
            if board[row, col, 0] == 0 and board[row, col, 1] == 0:
                return row
        return None

    def _check_win_from_position(self, board, row, col, channel):
        """
        Check horizontal / vertical / diagonal win.
        """
        # Horizontal →
        if col <= 3 and (board[row, col + 1:col + 4, channel] == 1).all():
            return True

        # Horizontal ←
        if col >= 3 and (board[row, col - 3:col, channel] == 1).all():
            return True

        # Vertical ↓
        if row <= 2 and (board[row + 1:row + 4, col, channel] == 1).all():
            return True

        # Diagonal /
        if row >= 3 and col <= 3:
            if all(board[row - i, col + i, channel] == 1 for i in range(1, 4)):
                return True
        if row <= 2 and col >= 3:
            if all(board[row + i, col - i, channel] == 1 for i in range(1, 4)):
                return True

        # Diagonal \
        if row <= 2 and col <= 3:
            if all(board[row + i, col + i, channel] == 1 for i in range(1, 4)):
                return True
        if row >= 3 and col >= 3:
            if all(board[row - i, col - i, channel] == 1 for i in range(1, 4)):
                return True

        return False


# ======================================================================
#                           TIMED SMART AGENT
# ======================================================================

class TimedSmartAgent(SmartAgent):
    """
    SmartAgent that measures execution time and memory usage.
    """

    def __init__(self, env=None, player_name="TimedSmartAgent"):
        super().__init__(env=env, player_name=player_name)
        tracemalloc.start()

    def choose_action(self, observation, reward=0.0,
                      terminated=False, truncated=False, info=None,
                      action_mask=None, Time=False):

        start_time = time.time()
        action = super().choose_action(observation, reward,
                                       terminated, truncated,
                                       info, action_mask)
        end_time = time.time()

        current, peak = tracemalloc.get_traced_memory()
        elapsed_ms = (end_time - start_time) * 1000

        if Time:
            print(
                f"Temps : {elapsed_ms:.3f} ms | "
                f"Mémoire : {current/1024:.2f} KB "
                f"(pic {peak/1024:.2f} KB)"
            )

        return action


# ======================================================================
#                               RANDOM AGENT
# ======================================================================

class RandomAgent:
    """
    A simple agent that plays randomly.
    """

    def __init__(self, env=None, player_name=None):
        self.player_name = player_name or "RandomAgent"

    def choose_action(self, observation, reward=0.0,
                      terminated=False, truncated=False,
                      info=None, action_mask=None):
        if terminated or truncated:
            return None

        valid_actions = [i for i, v in enumerate(action_mask) if v == 1]
        return random.choice(valid_actions)


# ======================================================================
#                         WEIGHTED RANDOM AGENT
# ======================================================================

class WeightedRandomAgent(RandomAgent):
    """
    Random agent that prefers center columns.
    """

    def choose_action(self, observation, reward=0.0,
                      terminated=False, truncated=False,
                      info=None, action_mask=None):

        if terminated or truncated:
            logger.info("Game over, no action to choose")
            return None

        if action_mask is None:
            logger.error("action_mask is None")
            return None

        weights = [1, 2, 3, 4, 3, 2, 1]
        valid_actions = [i for i, v in enumerate(action_mask) if v == 1]

        if not valid_actions:
            logger.warning("No valid actions available")
            return None

        choice = random.choices(valid_actions, weights=[weights[i] for i in valid_actions])[0]

        return choice

       