#Content of main.py; use as is
from tkinter import *
import multiprocessing

import client
import server

if __name__ == "__main__":
    server = multiprocessing.Process(target=server.main)
    client1 = multiprocessing.Process(target=client.main, name="Client1")
    client2 = multiprocessing.Process(target=client.main, name="Client2")
    client3 = multiprocessing.Process(target=client.main, name="Client3")
    client4 = multiprocessing.Process(target=client.main, name="Client4")
    client5 = multiprocessing.Process(target=client.main, name="Client5")
    server.start()
    client1.start()
    client2.start()
    client3.start()
    client4.start()
    client5.start()