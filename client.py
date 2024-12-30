# client.py
from Crypto.Cipher import AES
import socket
import json
import sys

# Shared keys
KEY1 = b'1234567890123456'
KEY2 = b'2345678901234567'
KEY3 = b'3456789012345678'

def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce  # Randomly generated nonce
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    # Combine nonce and ciphertext for transmission
    return nonce + ciphertext



def decrypt_message(encrypted_message, key):
    nonce = encrypted_message[:16]  # Extract the nonce (first 16 bytes)
    ciphertext = encrypted_message[16:]  # Remaining is the ciphertext
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(ciphertext).decode()


def main():
    if len(sys.argv) != 2:
        print("Usage: python client.py <username>")
        return

    username = sys.argv[1]

    # Connect to router1
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('localhost', 5001))
        
        # Register username
        register_message = json.dumps({'request': 'register', 'username': username})
        encrypted_message = encrypt_message(register_message, KEY3)
        encrypted_message = encrypt_message(encrypted_message.hex(), KEY2)
        encrypted_message = encrypt_message(encrypted_message.hex(), KEY1)
        client_socket.sendall(encrypted_message)
        print("Client: Waiting for server response...")
        # Wait for registration response
        response = client_socket.recv(1024)
        print("Client: Server response:", response)
        response = decrypt_message(response, KEY1)
        print("Client: Decrypted server response:", response)
        response = decrypt_message(bytes.fromhex(response), KEY2)
        print("Client: Decrypted server response:", response)
        response = decrypt_message(bytes.fromhex(response), KEY3)
        print("Client: Decrypted server response:", response)

        print("Server response:", response)

        # Request online users
        get_users_message = json.dumps({'request': 'get_online_users'})
        encrypted_message = encrypt_message(get_users_message, KEY3)
        encrypted_message = encrypt_message(encrypted_message.hex(), KEY2)
        encrypted_message = encrypt_message(encrypted_message.hex(), KEY1)
        client_socket.sendall(encrypted_message)

        # Wait for users response
        print("Client: Waiting for server response...")
        response = client_socket.recv(1024)
        print("Client: Server response:", response)
        response = decrypt_message(response, KEY1)
        print("Client: Decrypted server response:", response)
        response = decrypt_message(bytes.fromhex(response), KEY2)
        print("Client: Decrypted server response:", response)
        response = decrypt_message(response, KEY3)
        print("Online users:", response)

if __name__ == "__main__":
    main()
