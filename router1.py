from Crypto.Cipher import AES
import socket
import threading

# Global variable to store the key after the first handshake
stored_key = None

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
    global stored_key

    try:
        # First message is the key handshake
        key_message = client_socket.recv(1024)
        if not key_message:
            print("Router1: Connection closed by client during key handshake.")
            return

        # Decode the key (assuming it's sent as plaintext for simplicity)
        stored_key = key_message  # Store the key globally
        print(f"Router1: Key received and stored: {stored_key}")

        # Acknowledge the key handshake
        client_socket.sendall(b"Key received. Handshake complete.")

        # Now handle subsequent requests
        while True:
            # Receive encrypted message
            message = client_socket.recv(1024)
            if not message:  # Break if the connection is closed
                print("Router1: Connection closed by client.")
                break

            print("Router1: Received encrypted message:", message)

            # Decrypt the message using the stored key
            decrypted_message = decrypt_message(message, stored_key)
            print("Router1: Decrypted message:", decrypted_message)

            # Forward to router2
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as router_socket:
                router_socket.connect(('localhost', 5002))
                router_socket.sendall(bytes.fromhex(decrypted_message))
                response = router_socket.recv(1024)

            # Encrypt the response using the stored key
            encrypted_response = encrypt_message(response.hex(), stored_key)
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