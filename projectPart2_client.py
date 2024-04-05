# Group#: 12
# Student Names:Fatima Mushtaq and Ethan Watchorn

#Content of client.py; to complete/implement

JUSTIFICATION = 40

from tkinter import *
from tkinter.scrolledtext import ScrolledText
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
        self.window = window
        self.name = current_process().name
        self.setup_gui()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('127.0.0.1', 1024))
        threading.Thread(target=self.receive_message).start()

    def setup_gui(self):
        label = Label(self.window, text=f"{self.name} @port Fuck")
        label.pack()
        self.msg_entry = Entry(self.window)
        self.msg_entry.pack(padx=20, pady=10, fill=X)
        self.msg_entry.bind("<Return>", self.send_message)
        self.text_area = ScrolledText(self.window)
        self.text_area.pack(padx=20, pady=10)
        self.text_area.config(state=DISABLED)

    def send_message(self, event):
        message = self.msg_entry.get()
        self.display_message(f"{self.name}: {message}", 1)
        self.sock.send(f"{self.name}: {message}".encode())
        self.msg_entry.delete(0, END)

    def receive_message(self):
        while True:
            try:
                message = self.sock.recv(1024).decode()
                self.display_message(message)
            except OSError:  # Possibly client has left the chat.
                break

    def display_message(self, message, sent = 0):
        self.text_area.config(state=NORMAL)
        if sent:
            self.text_area.insert(END, ' ' * JUSTIFICATION + message + '\n')
        else:
            self.text_area.insert(END, message + '\n')
        self.text_area.config(state=DISABLED)
        self.text_area.yview(END)

def main():
    window = Tk()
    c = ChatClient(window)
    window.mainloop()

if __name__ == '__main__': # May be used ONLY for debugging
    main()