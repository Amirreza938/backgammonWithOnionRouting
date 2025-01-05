from Crypto.Cipher import AES
import socket
import threading

KEY3 = b'3456789012345678'

def decrypt_message(encrypted_message, key):
    nonce = encrypted_message[:16]  # Extract nonce (first 16 bytes)
    ciphertext = encrypted_message[16:]  # Remaining is ciphertext
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(ciphertext).decode()

def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())  # Encode plaintext as bytes
    return nonce + ciphertext  # Combine nonce and ciphertext for transmission

def handle_client(client_socket):
    try:
        while True:  # Loop to handle multiple requests
            # Receive encrypted message from Router2
            message = client_socket.recv(1024)
            if not message:  # Break if the connection is closed
                print("Router3: Connection closed by client.")
                break

            print("Router3: Received encrypted message:", message)

            # Decrypt the message
            decrypted_message = decrypt_message(message, KEY3)
            print("Router3: Decrypted message:", decrypted_message)

            # Encrypt the decrypted message before sending to the server
            encrypted_message_for_server = encrypt_message(decrypted_message, KEY3)
            print("Router3: Forwarding encrypted message to server:", encrypted_message_for_server)

            # Send to server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.connect(('localhost', 5004))
                server_socket.sendall(encrypted_message_for_server)
                response = server_socket.recv(1024)
                print("Router3: Received response from server:", response)

            # Decrypt the response
            decrypted_response = decrypt_message(response, KEY3)
            print("Router3: Decrypted response from server:", decrypted_response)

            # Encrypt the decrypted response before sending back to Router2
            encrypted_response = encrypt_message(decrypted_response, KEY3)
            print("Router3: Forwarding encrypted response to Router2:", encrypted_response)
            client_socket.sendall(encrypted_response)

    except Exception as e:
        print(f"Router3: Error occurred: {e}")
    finally:
        client_socket.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('localhost', 5003))
        server_socket.listen()
        print("Router3 listening on port 5003...")
        while True:
            client_socket, _ = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    main()