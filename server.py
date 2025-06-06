# server.py
from Crypto.Cipher import AES
import socket
import json
import threading
import random
import re
KEY3 = b'3456789012345678'
online_users = set()

def decrypt_message(encrypted_message, key):
    nonce = encrypted_message[:16]  # Extract the nonce (first 16 bytes)
    ciphertext = encrypted_message[16:]  # Remaining is the ciphertext
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(ciphertext).decode()  # Decode plaintext to a string

def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())  # Encode plaintext as bytes
    return nonce + ciphertext  # Combine nonce and ciphertext for transmission

def handle_client(client_socket, client_address):
    global online_users
    username = None
    try:
        while True:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                print(f"Server: Connection closed by {client_address}")
                break

            decrypted_message = decrypt_message(encrypted_message, KEY3)
            request = json.loads(decrypted_message)

            if request['request'] == 'register':
                username = request['username']
                pattern = r'^[a-zA-Z0-9]+$'
                if not re.match(pattern, username):
                    response = json.dumps({"status": "Invalid username"})
                else:
                    online_users.add(username)
                    response = json.dumps({"status": "registered"})
            elif request['request'] == 'get_online_users':
                response = json.dumps(list(online_users))
            elif request['request'] == 'get_dice':  # Handle dice request
                dice1, dice2 = random.randint(1, 6), random.randint(1, 6)
                response = json.dumps({"dice1": dice1, "dice2": dice2})
            else:
                response = json.dumps({"error": "Unknown request"})

            encrypted_response = encrypt_message(response, KEY3)
            client_socket.sendall(encrypted_response)

    except Exception as e:
        print(f"Server: Error occurred while handling {client_address}: {e}")
    finally:
        # if username:
        #     online_users.remove(username)
        client_socket.close()




def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('localhost', 5004))
        server_socket.listen()
        print("Server listening on port 5004...")
        while True:
            client_socket, client_address = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    main()