import sys
from game import BackgammonGame
from network import host_game, connect_to_game

def main():
    # Ask if hosting or connecting
    choice = input("Do you want to (h)ost or (c)onnect to a game? ").lower()
    is_host = choice == 'h'
    
    if is_host:
        conn, server = host_game()
        game = BackgammonGame(True)
    else:
        conn = connect_to_game()
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
            game.current_turn = not game.current_turn        
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