import socket

def host_game():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5000))
    server.listen(1)
    print("Waiting for opponent to connect...")
    conn, addr = server.accept()
    return conn, server

def connect_to_game():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(('localhost', 5000))
    return conn