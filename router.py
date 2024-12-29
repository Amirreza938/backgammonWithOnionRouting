import socket
import threading

ROUTER_HOST = '127.0.0.1'
ROUTER_PORT = 6000

def forward_message(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"forwarded: {data.decode()}")
            
    except Exception as e:
        print(f"error: {e}")
    finally:
        client_socket.close()
def start_router():
    router_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    router_socket.bind((ROUTER_HOST, ROUTER_PORT))
    router_socket.listen(5)
    while True:
        client_socket, client_address = router_socket.accept()
        print(f"client connected: {client_address}")
        threading.Thread(target=forward_message, args=(client_socket,)).start()
if __name__ == "__main__": 
    start_router()