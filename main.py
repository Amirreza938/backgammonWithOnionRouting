import sys
import threading
from tkinter import Tk, Text, Entry, Button, Scrollbar, END
from game import BackgammonGame
from network import host_game, connect_to_game
import client

def setup_chat_interface(conn, player_name, opponent_name):
    def send_message():
        message = input_box.get()
        if message.strip():
            chat_display.insert(END, f"{player_name}: {message}\n")
            conn.send(f"CHAT:{message}".encode())
            input_box.delete(0, END)

    def receive_messages():
        while True:
            try:
                data = conn.recv(1024).decode()
                if data.startswith("CHAT:"):
                    chat_display.insert(END, f"{opponent_name}: {data[5:]}\n")
                else:
                    incoming_messages.append(data)  # Store game-related messages
            except Exception as e:
                chat_display.insert(END, f"Error: {e}\n")
                break

    root = Tk()
    root.title("Backgammon Chat")

    chat_display = Text(root, height=20, width=50, state='normal')
    chat_display.pack(side='top', fill='both', expand=True)

    scrollbar = Scrollbar(chat_display)
    chat_display.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    input_box = Entry(root, width=40)
    input_box.pack(side='left', fill='x', expand=True)

    send_button = Button(root, text="Send", command=send_message)
    send_button.pack(side='right')

    threading.Thread(target=receive_messages, daemon=True).start()

    return root

def main():
    def game_loop():
        while True:
            game.board.draw()

            if game.current_turn == game.is_white:
                # Your turn
                dice = game.roll_dice()
                print(f"You rolled: {dice[0]}, {dice[1]}")

                valid_moves = game.get_valid_moves(dice, game.is_white)
                if not valid_moves:
                    print("No valid moves! Turn skipped.")
                    conn.send("TURN_SWITCH".encode())
                    game.current_turn = not game.current_turn
                    continue

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
                                conn.send(f"{start},{end}".encode())
                            else:
                                print("Invalid move!")
                        else:
                            print("Move doesn't match dice roll!")
                    except ValueError:
                        print("Please enter valid numbers!")

                conn.send("TURN_SWITCH".encode())
                game.current_turn = not game.current_turn
            else:
                # Opponent's turn
                print("Waiting for opponent's move...")
                while not incoming_messages:
                    chat_root.update()  # Keep the chat interface responsive

                data = incoming_messages.pop(0)
                if data == "TURN_SWITCH":
                    game.current_turn = not game.current_turn
                else:
                    start, end = map(int, data.split(','))
                    if not game.make_move(start, end, not game.is_white):
                        print("Invalid move received from opponent!")

    while True:
        username = client.register()
        if username is not None:
            break
    global incoming_messages
    while True:
         # Request online users
            print("\nChoose an option:")
            print("1. Get online users")
            print("2. Play game")
            print("3. Exit")
            option = input("Enter your option(1/2/3): ")
            
            if option == '1':
                client.get_online_users()
            elif option == '2':
                choice = input("Do you want to (h)ost or (c)onnect to a game? ").lower()
                is_host = choice == 'h'
                if is_host:
                    conn, server = host_game()
                    game = BackgammonGame(True)
                    opponent_name = conn.recv(1024).decode()
                    # conn.send(player_name.encode())
                    accepting = input(f"Do you want to play against {opponent_name}? (y/n)")
                    if accepting.lower() == 'y':
                        conn.send("ACCEPT".encode())
                        print("\nWelcome to Backgammon!")
                        print("You are", "White" if game.is_white else "Black")

                        
                        incoming_messages = []  # Buffer for incoming game messages

                        chat_root = setup_chat_interface(conn, username, opponent_name)
                        threading.Thread(target=game_loop, daemon=True).start()
                        chat_root.mainloop()
                    else:
                        conn.send("DECLINE".encode())
                else:
                    online_users = client.get_online_users()
                    opponent_name = input("Enter opponent's name: ")
                    if opponent_name not in online_users or opponent_name == username:
                        print("Invalid opponent name")
                        continue
                    conn = connect_to_game()
                    game = BackgammonGame(False)
                    conn.send(username.encode())
                    message = conn.recv(1024).decode()
                    if message == "ACCEPT":
                        print("\nWelcome to Backgammon!")
                        print("You are", "White" if game.is_white else "Black")

                        incoming_messages = []  # Buffer for incoming game messages

                        chat_root = setup_chat_interface(conn, username, opponent_name)
                        threading.Thread(target=game_loop, daemon=True).start()
                        chat_root.mainloop()
                    else:
                        continue
            elif option == '3':
                break
            else:
                print("Invalid option")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame ended by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    sys.exit(0)
