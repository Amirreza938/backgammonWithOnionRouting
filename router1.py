# router1.py
from Crypto.Cipher import AES
import socket
import threading

KEY1 = b'1234567890123456'

def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce  # Random nonce generated during encryption
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    # Combine nonce and ciphertext for transmission
    return nonce + ciphertext


def decrypt_message(encrypted_message, key):
    nonce = encrypted_message[:16]  # Extract the nonce (first 16 bytes)
    ciphertext = encrypted_message[16:]  # Remaining is the ciphertext
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(ciphertext).decode()

def handle_client(client_socket):
    try:
        # Receive encrypted message
        message = client_socket.recv(1024)
        print("Router1: Received encrypted message:", message)

        # Decrypt the message
        decrypted_message = decrypt_message(message, KEY1)
        print("Router1: Decrypted message:", decrypted_message)

        # Forward to router2
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as router_socket:
            router_socket.connect(('localhost', 5002))
            router_socket.sendall(bytes.fromhex(decrypted_message))
            response = router_socket.recv(1024)

        # Encrypt the response
        encrypted_response = encrypt_message(response.hex(), KEY1)
        print("Router1: Encrypted response:", encrypted_response)
        client_socket.sendall(encrypted_response)

    except Exception as e:
        print(f"Router1: Error occurred: {e}")
    finally:
        client_socket.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('localhost', 5001))
        server_socket.listen()
        print("Router1 listening on port 5001...")
        while True:
            client_socket, _ = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    main()
