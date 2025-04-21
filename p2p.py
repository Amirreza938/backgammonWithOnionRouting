import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog

def receive_messages(sock, text_area):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if message:
                text_area.config(state=tk.NORMAL)
                text_area.insert(tk.END, f"{peer_name}: {message}\n")
                text_area.config(state=tk.DISABLED)
                text_area.yview(tk.END)
            else:
                break
        except:
            break

def send_messages(sock, entry, text_area):
    message = entry.get()
    entry.delete(0, tk.END)
    sock.sendall(message.encode('utf-8'))
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, f"{my_name}: {message}\n")
    text_area.config(state=tk.DISABLED)
    text_area.yview(tk.END)

def main():
    global my_name, peer_name

    root = tk.Tk()
    root.title("P2P Chat")

    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    entry = tk.Entry(root)
    entry.pack(padx=10, pady=10, fill=tk.X, expand=True)

    def on_send():
        send_messages(client_sock, entry, text_area)

    send_button = tk.Button(root, text="Send", command=on_send)
    send_button.pack(padx=10, pady=10)

    my_name = simpledialog.askstring("Name", "Enter your name:")
    choice = simpledialog.askstring("Choice", "Do you want to host (h) or connect (c) to a chat?")

    if choice == 'h':
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.bind(('0.0.0.0', 12345))
        server_sock.listen(1)
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, "Waiting for a connection...\n")
        text_area.config(state=tk.DISABLED)
        conn, addr = server_sock.accept()
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, f"Connected by {addr}\n")
        text_area.config(state=tk.DISABLED)

        peer_name = conn.recv(1024).decode('utf-8')
        conn.sendall(my_name.encode('utf-8'))

        threading.Thread(target=receive_messages, args=(conn, text_area)).start()
        client_sock = conn

    elif choice == 'c':
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_ip = simpledialog.askstring("Server IP", "Enter the server IP address:")
        client_sock.connect((server_ip, 12345))
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, "Connected to the server\n")
        text_area.config(state=tk.DISABLED)

        client_sock.sendall(my_name.encode('utf-8'))
        peer_name = client_sock.recv(1024).decode('utf-8')

        threading.Thread(target=receive_messages, args=(client_sock, text_area)).start()

    root.mainloop()

if __name__ == "__main__":
    main()