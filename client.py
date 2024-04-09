# Group#: 12
# Student Names:Fatima Mushtaq and Ethan Watchorn

#Content of client.py; to complete/implement

JUSTIFICATION = 40

from tkinter import *
from tkinter.scrolledtext import ScrolledText
import socket
import threading
from multiprocessing import current_process #only needed for getting the current process name
import time
import random

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

        # TODO When both clients try connecting simultaneously, neither are able to connect
        time.sleep(random.random())

        # Connect to the server, and continually check the socket for received messages in a thread.
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('127.0.0.1', 1024))
        threading.Thread(target=self.receive_message, daemon=True).start() # daemon to True, since there is no join()

        # self.portname = self.sock.getsockname()

        self.window = window
        self.setup_gui()

    def setup_gui(self):
        # TODO: rename the port. Figure out how to get the port name from the server side.
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

        # Scrolling text box
        self.text_area = ScrolledText(self.window)
        self.text_area.pack(padx=20, pady=10, fill=X)
        self.text_area.config(state=DISABLED) # Deny any changes

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
                self.display_message(message)
            except:
                self.sock.close()

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

if __name__ == '__main__': # May be used ONLY for debugging
    main()