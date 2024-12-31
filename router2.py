from Crypto.Cipher import AES
import socket
import threading

KEY2 = b'2345678901234567'

def decrypt_message(encrypted_message, key):
    nonce = encrypted_message[:16]
    ciphertext = encrypted_message[16:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(ciphertext).decode()

def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return nonce + ciphertext

def handle_client(client_socket):
    try:
        while True:  # Loop to handle multiple requests
            # Receive encrypted message
            message = client_socket.recv(1024)
            if not message:  # Break if the connection is closed
                print("Router2: Connection closed by client.")
                break

            print("Router2: Received encrypted message:", message)

            # Decrypt the message
            decrypted_message = decrypt_message(message, KEY2)
            print("Router2: Decrypted message:", decrypted_message)

            # Ensure the decrypted message is valid hex
            if not all(c in '0123456789abcdefABCDEF' for c in decrypted_message):
                raise ValueError(f"Decrypted message is not hex-encoded: {decrypted_message}")

            # Forward to Router3
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as router_socket:
                print("Router2: Connecting to Router3...")
                router_socket.connect(('localhost', 5003))  # Ensure this port matches Router3
                router_socket.sendall(bytes.fromhex(decrypted_message))
                response = router_socket.recv(1024)
                print("Router2: Received response from Router3:", response)

            # Encrypt the response
            encrypted_response = encrypt_message(response.hex(), KEY2)
            print("Router2: Encrypted response:", encrypted_response)
            client_socket.sendall(encrypted_response)

    except Exception as e:
        print(f"Router2: Error occurred: {e}")
    finally:
        client_socket.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('localhost', 5002))
        server_socket.listen()
        print("Router2 listening on port 5002...")
        while True:
            client_socket, _ = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    main()
