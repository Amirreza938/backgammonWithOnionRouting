import socket
import sys
import random
import time
from typing import List, Tuple, Optional

class BackgammonBoard:
    def __init__(self):
        # Initialize the board with starting positions
        # Positive numbers represent white pieces, negative represent black
        self.board = [
            2, 0, 0, 0, 0, -5,  # 1-6
            0, -3, 0, 0, 0, 5,  # 7-12
            -5, 0, 0, 0, 3, 0,  # 13-18
            5, 0, 0, 0, 0, -2   # 19-24
        ]
        self.bar = [0, 0]  # [white, black]
        self.off = [0, 0]  # [white, black]
        
    def draw(self):
        """Draw the beautiful ASCII board"""
        print("\n" + "=" * 57)
        # Top numbers
        print("║", end=" ")
        for i in range(13, 19):
            print(f"{i:2}", end=" ")
        print("║BAR║", end=" ")
        for i in range(19, 25):
            print(f"{i:2}", end=" ")
        print("║")
        
        # Upper board
        for row in range(5):
            print("║", end=" ")
            # Print pieces for positions 13-18
            for pos in range(12, 18):
                pieces = self.board[pos]
                if abs(pieces) > row:
                    print(" ○ " if pieces > 0 else " ● ", end="")
                else:
                    print(" │ ", end="")
            print("║", end="")
            # Bar area
            if abs(self.bar[0]) > row:
                print(" ○ ", end="")
            else:
                print(" │ ", end="")
            print("║", end=" ")
            # Print pieces for positions 19-24
            for pos in range(18, 24):
                pieces = self.board[pos]
                if abs(pieces) > row:
                    print(" ○ " if pieces > 0 else " ● ", end="")
                else:
                    print(" │ ", end="")
            print("║")
        
        # Middle section
        print("║" + "═" * 17 + "║" + "═" * 3 + "║" + "═" * 17 + "║")
        print("║     WHITE (○) DIRECTION →    ║   ║                      ║")
        print("║" + "─" * 17 + "║" + "─" * 3 + "║" + "─" * 17 + "║")
        print("║     BLACK (●) DIRECTION →    ║   ║                      ║")
        print("║" + "═" * 17 + "║" + "═" * 3 + "║" + "═" * 17 + "║")
        
        # Lower board
        for row in range(5):
            print("║", end=" ")
            # Print pieces for positions 1-6
            for pos in range(0, 6):
                pieces = self.board[pos]
                if abs(pieces) > row:
                    print(" ○ " if pieces > 0 else " ● ", end="")
                else:
                    print(" │ ", end="")
            print("║", end="")
            # Bar area
            if abs(self.bar[1]) > row:
                print(" ● ", end="")
            else:
                print(" │ ", end="")
            print("║", end=" ")
            # Print pieces for positions 7-12
            for pos in range(6, 12):
                pieces = self.board[pos]
                if abs(pieces) > row:
                    print(" ○ " if pieces > 0 else " ● ", end="")
                else:
                    print(" │ ", end="")
            print("║")
        
        # Bottom numbers
        print("║", end=" ")
        for i in range(1, 7):
            print(f"{i:2}", end=" ")
        print("║BAR║", end=" ")
        for i in range(7, 13):
            print(f"{i:2}", end=" ")
        print("║")
        print("=" * 57)
        
        # Show pieces on bar and off the board
        print(f"Bar - White: {self.bar[0]} Black: {abs(self.bar[1])}")
        print(f"Off - White: {self.off[0]} Black: {self.off[1]}\n")
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

def main():
    # Ask if hosting or connecting
    choice = input("Do you want to (h)ost or (c)onnect to a game? ").lower()
    is_host = choice == 'h'
    
    if is_host:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', 5000))
        server.listen(1)
        print("Waiting for opponent to connect...")
        conn, addr = server.accept()
        game = BackgammonGame(True)
    else:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(('localhost', 5000))
        game = BackgammonGame(False)
    
    print("\nWelcome to Backgammon!")
    print("You are", "White" if game.is_white else "Black")
    
    while True:
        game.board.draw()
        
        if game.current_turn == game.is_white:
            # Your turn
            dice = game.roll_dice()
            print(f"You rolled: {dice[0]}, {dice[1]}")
            
            # Show valid moves
            valid_moves = game.get_valid_moves(dice, game.is_white)
            print("Valid moves:")
            for move in valid_moves:
                print(f"From {move[0] + 1} to {move[1] + 1}")
            
            moves_left = list(dice)
            while moves_left:
                print(f"Moves left: {moves_left}")
                try:
                    start = int(input("Enter start position (1-24): ")) - 1
                    end = int(input("Enter end position (1-24): ")) - 1
                    
                    move_distance = abs(end - start)
                    if move_distance in moves_left:
                        if game.make_move(start, end, game.is_white):
                            moves_left.remove(move_distance)
                            # Send move to opponent
                            conn.send(f"{start},{end}".encode())
                        else:
                            print("Invalid move!")
                    else:
                        print("Move doesn't match dice roll!")
                except ValueError:
                    print("Please enter valid numbers!")
                    
        else:
            # Opponent's turn
            print("Waiting for opponent's move...")
            data = conn.recv(1024).decode()
            if not data:
                break
                
            start, end = map(int, data.split(','))
            game.make_move(start, end, not game.is_white)
            
        game.current_turn = not game.current_turn
        
    conn.close()
    if is_host:
        server.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame ended by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    sys.exit(0)