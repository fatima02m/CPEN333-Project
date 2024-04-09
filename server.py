# Group#: 12
# Student Names:Fatima Mushtaq and Ethan Watchorn

#Content of server.py; To complete/implement

from tkinter import *
import socket
import threading
from tkinter.scrolledtext import ScrolledText

class ChatServer:
    def __init__(self, window):
        self.window = window
        self.clients = []
        self.setup_gui()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('127.0.0.1', 1024))
        self.server_socket.listen()
        threading.Thread(target=self.accept_connections, daemon=True).start()

    def setup_gui(self):
        label = Label(self.window, text=f"Chat Server", anchor=W)
        label.pack(fill="both")
        label = Label(self.window, text="Chat history:", anchor=W)
        label.pack(fill="both")
        self.text_area = ScrolledText(self.window)
        self.text_area.pack(padx=20, pady=10)
        self.text_area.config(state=DISABLED)

    def accept_connections(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket, addr), daemon=True).start()

    def handle_client(self, client_socket, addr):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    self.display_message(f"{addr}: {message}")
                    self.broadcast_message(message, client_socket)
                else:
                    self.remove_client(client_socket)
                    break
            except Exception as e:
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

    def display_message(self, message):
        self.text_area.config(state=NORMAL)
        self.text_area.insert(END, message + '\n')
        self.text_area.config(state=DISABLED)
        self.text_area.yview(END)

def main():
    window = Tk()
    ChatServer(window)
    window.mainloop()

if __name__ == '__main__': # May be used ONLY for debugging
    main()