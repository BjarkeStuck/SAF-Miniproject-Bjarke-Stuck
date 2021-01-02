# !/usr/bin/env python3

import socket
import time


HOST = '192.168.56.1'                                                   # The server's hostname or IP address
PORT = 10000                                                             # The port used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:            #We define the socket connection as s
    s.connect((HOST, PORT))                                             #Connects to the host and port
    while True:
        data = s.recv(1024)
        print('Received', repr(data))                                   #Prints the data
        str_data = data.decode("utf-8")                                 #Decodes utf-8 and saves it as str_data

        float_data = float(str_data)/1000                               #Changes it to a float and divides it with 1000
        print(float_data)
        time.sleep(float_data)                                          #Delay
        print('sleep done')

        s.sendall(data)                                                 #Sends the data again



