"""
My Smart Agent for Connect Four

This agent uses rule-based heuristics to play strategically.
"""

import random


class SmartAgent:
    """
    A rule-based agent that plays strategically
    """

    def __init__(self, env, player_name=None):
        """
        Initialize the smart agent

        Parameters:
            env: PettingZoo environment
            player_name: Optional name for the agent
        """
        self.env = env
        self.action_space = env.action_space(env.agents[0])
        self.player_name = player_name or "SmartAgent"

    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        """
        Choose an action using rule-based strategy

        Strategy priority:
        1. Win if possible
        2. Block opponent from winning
        3. Play center if available
        4. Random valid move
        """
        if terminated or truncated:
            return None
        
        # Get valid actions
        valid_actions = self._get_valid_actions(action_mask)

        # Rule 1: Try to win
        winning_move = self._find_winning_move(observation, valid_actions, channel=0)
        if winning_move is not None:
            return winning_move

        # Rule 2: Block opponent
        blocking_move = self._find_winning_move(observation, valid_actions, channel=1)
        if blocking_move is not None:
            return blocking_move

        # Rule 3: Prefer center
        if 3 in valid_actions:
            return 3

        # Rule 4: Random fallback
        return random.choice(valid_actions)

    def _get_valid_actions(self, action_mask):
        """
        Get list of valid column indices

        Parameters:
            action_mask: numpy array (7,) with 1 for valid, 0 for invalid

        Returns:
            list of valid column indices
        """
        return [i for i, valid in enumerate(action_mask) if valid == 1]

    def _find_winning_move(self, observation, valid_actions, channel):
        """
        Find a move that creates 4 in a row for the specified player

        Parameters:
            observation: numpy array (6, 7, 2) - current board state
            valid_actions: list of valid column indices
            channel: 0 for current player, 1 for opponent

        Returns:
            column index (int) if winning move found, None otherwise
        """
        
        board = observation.copy()
        for col in valid_actions:
            row = self._get_next_row(board, col)
            if row is not None:
                # Simulate placing the piece
                board[row, col, channel] = 1
                if self._check_win_from_position(board, row, col, channel):
                    return col
        return None
    

    def _get_next_row(self, board, col):
        """
        Find which row a piece would land in if dropped in column col

        Parameters:
            board: numpy array (6, 7, 2)
            col: column index (0-6)

        Returns:
            row index (0-5) if space available, None if column full
        """
        for row in range(5, -1, -1):  # Start from bottom (row 5)
            if board[row, col, 0] == 0 and board[row, col, 1] == 0:
                return row  # This position is empty
        return None  # Column is full
        

    
    def _check_win_from_position(self, board, row, col, channel):
        """
        Check if placing a piece at (row, col) would create 4 in a row

        Parameters:
            board: numpy array (6, 7, 2)
            row: row index (0-5)
            col: column index (0-6)
            channel: 0 or 1 (which player's pieces to check)

        Returns:
            True if this position creates 4 in a row/col/diag, False otherwise
        """
        # TODO: Check all 4 directions: horizontal, vertical, diagonal /, diagonal \
        # Hint: Count consecutive pieces in both directions from (row, col)

        # Check horizontal
        # droite
        if col in range(4): # piece falls in the first half so the row of 3 has to be on the right
            if (board[row, col + 1:col + 4, channel] == 1).all():
                return True

        # gauche
        if col in range(3,7): # piece falls in the second half so the row of 3 has to be on the left
            if (board[row, col - 3:col, channel] == 1).all():
                return True
        
        # Check vertical
        # verticale descendante
        if row in range(3): # piece falls in the first half so the row of 3 has to be on the right
            if (board[row + 1:row + 4, col, channel] == 1).all():
                return True
        # verticale montante
        if col in range(3,6): # piece falls in the second half so the row of 3 has to be on the left
            if (board[row - 3:row, col, channel] == 1).all():
                return True
        
        # Check diagonal /
        #diagonal montante
        if row in [3,4,5] and col in [0,1,2,3]:
            if all([board[row - 1, col + 1, channel] == 1, board[row - 2, col + 2, channel] == 1, board[row - 3, col + 3, channel] == 1]):
                return True
        #diagonale descendante
        if row in [0,1,2] and col in [3,4,5,6]:
            if all([board[row + 1, col - 1, channel] == 1, board[row + 2, col - 2, channel] == 1, board[row + 3, col - 3, channel] == 1]):
                return True

        # Check diagonal \
        # diagonal descendante
        if row in [0,1,2] and col in [0,1,2,3]:
            if all([board[row + 1, col + 1, channel] == 1, board[row + 2, col + 2, channel] == 1, board[row + 3, col + 3, channel] == 1]):
                return True
        # diagonal montante
        if row in [3,4,5] and col in [3,4,5,6]:
            if all([board[row - 1, col - 1, channel] == 1, board[row - 2, col - 2, channel] == 1, board[row - 3, col - 3, channel] == 1]):
                return True
        
        return False

        