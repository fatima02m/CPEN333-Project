# Group#: 12
# Student Names:Fatima Mushtaq and Ethan Watchorn

#Content of client.py; to complete/implement

JUSTIFICATION = 40

from tkinter import *
import socket
import threading
from multiprocessing import current_process #only needed for getting the current process name

class ChatClient:
    """
    This class implements the chat client.
    It uses the socket module to create a TCP socket and to connect to the server.
    It uses the tkinter module to create the GUI for the chat client.
    """
    # To implement
    def __init__(self, window: Tk):
        # gui setup
        self.name = current_process().name

        # Connect to the server, and continually check the socket for received messages in a thread.
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Persistently try to connect to server
        successful_connection = False
        while not successful_connection:
            # If the socket can't connect because other clients are trying, connection refused exception is thrown
            # If that happens, reset the socket and try again.
            try:
                self.sock.connect(('127.0.0.1', 1024)) # not all clients connect when using 1024 or 1025
                successful_connection = 1
            except ConnectionRefusedError as e:
                successful_connection = 0
                self.sock.close()
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        threading.Thread(target=self.receive_message, daemon=True).start() # daemon to True, since there is no join()

        self.window = window
        self.gui()

    def gui(self):
        # Port number label
        label = Label(self.window, text=f"{self.name} @port {self.sock.getsockname()[1]}", justify="left", anchor=W)
        label.pack(fill=X, padx=(0, 0))

        # Chat message + entry frame
        chat_message_frame = Frame(self.window)
        chat_message_frame.pack(fill=X, padx=10, pady=2)

        # Chat message
        label = Label(chat_message_frame, text="Chat message:", anchor=W)
        label.pack(side=LEFT, padx=(0, 10))

        # Entry
        self.msg_entry = Entry(chat_message_frame)
        self.msg_entry.pack(side=LEFT, fill=X, expand=True)
        self.msg_entry.bind("<Return>", self.send_message)

        # Chat history label
        label = Label(self.window, text="Chat history:", anchor=W)
        label.pack(fill=X)

        # Create Scrollbar, associate it with a Text widget
        self.text_area = Text(self.window, height=10, state=DISABLED)
        self.text_area.pack(side=LEFT, padx=20, pady=10, fill=X, expand=True)
        
        scrollbar = Scrollbar(self.window, command=self.text_area.yview)
        scrollbar.pack(side=LEFT, fill=Y)
        
        self.text_area['yscrollcommand'] = scrollbar.set

    def send_message(self, event):
        message = self.msg_entry.get() # Takes the string from the text entry box
        self.display_message(f"{self.name}: {message}", 1) # Displays the sent message
        self.sock.send(f"{self.name}: {message}".encode()) # Encodes the message, sends it through the socket.
        self.msg_entry.delete(0, END) # Clears the text entry box

    def receive_message(self):
        # Continually check for a message from the server
        # Once it receves the message, decode it + display it in the scrolling text box.
        while True:
            try:
                message = self.sock.recv(1024).decode()
                if message:
                    self.display_message(message)
                
                # If the server disconnects, close the socket
                else:
                    message = "Connection to server lost"
                    self.display_message(message)
                    self.sock.close()
                    break
            except:
                message = "Connection to server lost"
                self.display_message(message)
                self.sock.close()
                break

    def display_message(self, message, sent = 0):
        self.text_area.config(state=NORMAL) # Enable editing in the scrolling text box
        # Display the text on the "right" if it's a sent message, left if it's received.
        if sent:
            self.text_area.insert(END, ' ' * JUSTIFICATION + message + '\n')
        else:
            self.text_area.insert(END, message + '\n')
        self.text_area.config(state=DISABLED) # Disable editing in the scrolling text box
        self.text_area.yview(END) # return the view to the bottom (scroll with the messages)

def main():
    window = Tk()
    c = ChatClient(window)
    window.mainloop()
    print(c.name, "HAS CLOSED")

if __name__ == '__main__': # May be used ONLY for debugging
    main()