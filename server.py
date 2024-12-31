# server.py
from Crypto.Cipher import AES
import socket
import json
import threading

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
    try:
        while True:  # Loop to allow multiple requests from the same client
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                print(f"Server: Connection closed by {client_address}")
                break

            print(f"Server: Received encrypted message from {client_address}: {encrypted_message}")

            # Decrypt the message
            decrypted_message = decrypt_message(encrypted_message, KEY3)
            print(f"Server: Decrypted message from {client_address}: {decrypted_message}")

            # Parse the JSON request
            request = json.loads(decrypted_message)
            print(f"Server: Parsed request: {request}")

            # Process the request
            if request['request'] == 'register':
                username = request['username']
                online_users.add(username)
                print(f"Server: {username} registered. Online users: {online_users}")
                response = json.dumps({"status": "registered"})
            elif request['request'] == 'get_online_users':
                response = json.dumps(list(online_users))
                print(f"Server: Online users list sent: {response}")
            else:
                response = json.dumps({"error": "Unknown request"})

            # Encrypt the response
            encrypted_response = encrypt_message(response, KEY3)
            print("Server: Encrypted response sent:", encrypted_response)
            client_socket.sendall(encrypted_response)

    except Exception as e:
        print(f"Server: Error occurred while handling {client_address}: {e}")
    finally:
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
