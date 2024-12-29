import threading
import socket
Host = '127.0.0.1'
Port = 5000
active_users = {}

def handle_client(client_socket, client_address):
    global active_users
    try:
        player_name = client_socket.recv(1024).decode()
        active_users[player_name] = client_socket
        client_socket.send(str(list(active_users.keys())).encode())
        opponent_name = client_socket.recv(1024).decode()
        if opponent_name in active_users:
            opponent_socket = active_users[opponent_name]
            client_socket.send(f"connected to {opponent_name}".encode())
            opponent_socket.send(f"connected to {player_name}".encode())
        else:
            client_socket.send("no such player".encode())
    except Exception as e:
        print(f"error: {e}")
    finally:
        client_socket.close()
        del active_users[player_name]
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((Host, Port))
    server_socket.listen(5)
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"client connected: {client_address}")
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()   

if __name__ == "__main__":
    start_server()
