#Content of main.py; use as is
from tkinter import *
import multiprocessing

import projectPart2_client as client
import projectPart2_server as server

if __name__ == "__main__":
    server1 = multiprocessing.Process(target=server.main)
    client1 = multiprocessing.Process(target=client.main, name="Client1")
    client2 = multiprocessing.Process(target=client.main, name="Client2")
    server1.start()
    client1.start()
    client2.start()