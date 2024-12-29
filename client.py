import socket
import threading
import random
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000

def listen_message(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if message:
                print(message)
        except Exception as e:
            print(f"error: {e}")
            break
def start_game():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    player_name = input("enter your name")
    client_socket.send(player_name.encode())
    active_users = client_socket.recv(1024).decode()
    print(f"active users: {active_users}")
    opponent_name = input("enter opponent's name")
    client_socket.send(opponent_name.encode())
    response = client_socket.recv(1024).decode()
    print(f"response: {response}")
    threading.Thread(target=listen_message, args=(client_socket,)).start()
    while True:
        input("please enter to roll the dice...")
        dice_roll = random.randint(1, 6)
        print(f"dice roll: {dice_roll}")
        client_socket.send(f"Dice roll: {dice_roll}".encode())
        message = input("enter your message")
        client_socket.send(message.encode())
    
if __name__ == "__main__": 
    start_game()