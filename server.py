# Group#: 12
# Student Names:Fatima Mushtaq and Ethan Watchorn

#Content of server.py; To complete/implement

from tkinter import *
import socket
import threading
from tkinter.scrolledtext import ScrolledText

class ChatServer:
    def __init__(self, window):
        # Set up tkinter gui
        self.window = window
        self.clients: list[socket.socket] = [] # list of currently clients connected
        self.setup_gui()

        # Set up the server socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('127.0.0.1', 1024))
        self.sock.listen()

        # Start a thread to accept any new connections
        threading.Thread(target=self.accept_connections, daemon=True).start() # Daemon so that it closes when the program ends

    def setup_gui(self):
        # Server and Chat History labels
        label = Label(self.window, text=f"Chat Server", anchor=W)
        label.pack(fill="both")
        label = Label(self.window, text="Chat history:", anchor=W)
        label.pack(fill="both")

        # scrolling textbox
        self.text_area = ScrolledText(self.window)
        self.text_area.pack(padx=20, pady=10)
        self.text_area.config(state=DISABLED) # Deny any changes

    def accept_connections(self):
        # Continuously checks for if any clients request a connection
        # Starts a new thread for each client to manage incoming/outgoing messages
        while True:
            client_socket, addr = self.sock.accept()
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket, addr), daemon=True).start()

    def handle_client(self, client_socket: socket.socket, addr):
        # If the client disconnects, remove the client.
        while True:
            try:
                # Continuously checks a client socket for incoming message, decode it when it comes in
                message = client_socket.recv(1024).decode()
                
                # Once a message is received, display it, and broadcast it to the other client sockets
                if message:
                    self.display_message(f"{addr}: {message}")

                    for client in self.clients:
                        if client is not client_socket:
                            try:
                                client.send(message.encode())

                            # If the client can't be reached, remove the client
                            except:
                                self.remove_client(client)

                # If the client disconnects, remove the client.
                else:
                    self.remove_client(client_socket)
                    break
            except:
                self.remove_client(client_socket)
                break

    def remove_client(self, client_socket: socket.socket):
        # Closes the client socket and removes it from the client list

        if client_socket in self.clients:
            message = str(client_socket.getsockname())
            message = "Connection lost with " + message + ". Removing from client list"
            self.display_message(message)

            client_socket.close()
            self.clients.remove(client_socket)

    def display_message(self, message):
        # Print received messages onto the scrolling textbox
        self.text_area.config(state=NORMAL)
        self.text_area.insert(END, message + '\n')
        self.text_area.config(state=DISABLED)
        self.text_area.yview(END)

def main():
    window = Tk()
    c = ChatServer(window)
    window.mainloop()
    c.sock.close()
    print("Server HAS CLOSED")

if __name__ == '__main__': # May be used ONLY for debugging
    main()