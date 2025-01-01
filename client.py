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
    username = input("Enter your username: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('localhost', 5001))

        # Register username
        register_message = json.dumps({'request': 'register', 'username': username})
        encrypted_message = encrypt_message(register_message, KEY3)
        encrypted_message = encrypt_message(encrypted_message.hex(), KEY2)
        encrypted_message = encrypt_message(encrypted_message.hex(), KEY1)
        client_socket.sendall(encrypted_message)

        response = client_socket.recv(1024)
        response = decrypt_message(response, KEY1)
        response = decrypt_message(bytes.fromhex(response), KEY2)
        response = decrypt_message(bytes.fromhex(response), KEY3)
        print("Server response:", response)

        while True:
            # Request online users
            print("\nChoose an option:")
            print("1. Get online users")
            print("2. Roll dice")
            print("3. Exit")
            option = input("Enter your option(1/2/3): ")

            if option == '1':
                # Get the list of online users
                request_message = json.dumps({'request': 'get_online_users'})
                encrypted_message = encrypt_message(request_message, KEY3)
                encrypted_message = encrypt_message(encrypted_message.hex(), KEY2)
                encrypted_message = encrypt_message(encrypted_message.hex(), KEY1)
                client_socket.sendall(encrypted_message)

                response = client_socket.recv(1024)
                response = decrypt_message(response, KEY1)
                response = decrypt_message(bytes.fromhex(response), KEY2)
                response = decrypt_message(bytes.fromhex(response), KEY3)
                print("Online users:", response)


            elif option == '2':  # Roll dice
                # Request dice numbers
                dice_message = json.dumps({'request': 'get_dice'})
                encrypted_message = encrypt_message(dice_message, KEY3)
                encrypted_message = encrypt_message(encrypted_message.hex(), KEY2)
                encrypted_message = encrypt_message(encrypted_message.hex(), KEY1)
                client_socket.sendall(encrypted_message)

                response = client_socket.recv(1024)
                response = decrypt_message(response, KEY1)
                response = decrypt_message(bytes.fromhex(response), KEY2)
                response = decrypt_message(bytes.fromhex(response), KEY3)
                print("Dice roll:", response)


            elif option == '3':
                print("Exiting client...")
                break
            else:   
                print("Invalid option")


if __name__ == "__main__":
    main()
