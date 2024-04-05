# Group#: 12
# Student Names:Fatima Mushtaq and Ethan Watchorn

#Content of server.py; To complete/implement

from tkinter import *
import socket
import threading

class ChatServer:
    def __init__(self, host='127.0.0.1', port=1024):
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen()
        print("Server listening on port", port)

    def handle_client(self, client_socket, addr):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    print(f"Message from {addr}: {message}")
                    self.broadcast_message(message, client_socket)
                else:
                    self.remove_client(client_socket)
                    break
            except Exception as e:
                print(f"Error handling message from {addr}: {e}")
                self.remove_client(client_socket)
                break

    def broadcast_message(self, message, sender_socket):
        for client in self.clients:
            if client is not sender_socket:
                try:
                    client.send(message.encode())
                except:
                    self.remove_client(client)

    def remove_client(self, client_socket):
        if client_socket in self.clients:
            self.clients.remove(client_socket)

    def run(self):
        print("Server is running...")
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr} established.")
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket, addr)).start()

def main():
    ChatServer().run()

if __name__ == '__main__': # May be used ONLY for debugging
    main()