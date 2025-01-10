import random
from typing import List, Tuple
from board import BackgammonBoard

class BackgammonGame:
    def __init__(self, is_host: bool):
        self.board = BackgammonBoard()
        self.is_host = is_host
        self.is_white = is_host
        self.current_turn = True  # True for white, False for black
        
    def roll_dice(self) -> Tuple[int, int]:
        """Roll two dice"""
        return (random.randint(1, 6), random.randint(1, 6))
        
    def is_valid_move(self, start: int, end: int, player_is_white: bool) -> bool:
        """Check if a move is valid"""
        if start < 0 or start > 23 or end < 0 or end > 23:
            return False
            
        # Check if moving in the correct direction
        if player_is_white and end < start:
            return False
        if not player_is_white and end > start:
            return False
            
        # Check if landing on opponent's single piece or own pieces
        target = self.board.board[end]
        if (player_is_white and target < -1) or (not player_is_white and target > 1):
            return False
            
        return True
        
    def make_move(self, start: int, end: int, player_is_white: bool) -> bool:
        """Make a move if valid"""
        if not self.is_valid_move(start, end, player_is_white):
            return False
            
        # Handle hitting an opponent's piece
        if self.board.board[end] == (-1 if player_is_white else 1):
            if player_is_white:
                self.board.bar[1] += 1
            else:
                self.board.bar[0] += 1
            self.board.board[end] = 0
            
        # Update board
        if player_is_white:
            self.board.board[start] -= 1
            self.board.board[end] += 1
        else:
            self.board.board[start] += 1
            self.board.board[end] -= 1
        return True

    def get_valid_moves(self, dice_roll: Tuple[int, int], player_is_white: bool) -> List[Tuple[int, int]]:
        """Get all valid moves for the current dice roll"""
        valid_moves = []
        for start in range(24):
            if (player_is_white and self.board.board[start] > 0) or (not player_is_white and self.board.board[start] < 0):
                for die in dice_roll:
                    end = start + die if player_is_white else start - die
                    if self.is_valid_move(start, end, player_is_white):
                        valid_moves.append((start, end))
        return valid_moves