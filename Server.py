import socket                       #For TCP connection
import pandas as pd                 #To read data
import numpy as np                  #To save data
import time                         #To make a delay in the code (Despite a PLC not requiring one)
HOST = '192.168.56.1'
PORT = 10000


df = pd.read_csv('processing_times_table.csv')          #Reads the information on the named file. We save it as df
#c1 = df['Station#01']
#r1 = ['Carrier#1']
#str_c1 = str(c1).encode()

# connection
serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       #Here we create a TCP socket
serv_sock.bind((HOST, PORT))                                        # bind socket with server
str_data_old = ''

while True:
    print("Waiting to establish connection.....")
    serv_sock.listen()                                          #We are listening if a client want to connect to the server
    conn, addr = serv_sock.accept()                             #here we check if it is acceptable
    with conn:
        print('Connection by: ', addr)
        i = 0
        while i < 16:                                            #16 is the number of data frames we recieve

            dframe = df.iloc[i,1]                                 #We create an object. iloc looks for a specific number from this table
            dframe_byte = str(dframe).encode()                     #Changes the table from string to bytes to send it over a TCP connection
            conn.sendall(dframe_byte)                              #Sends the whole data frame

            print('send: ')
            print(dframe)
            float_data = float(dframe) / 1000

            time.sleep(float_data)
            data = conn.recv(1024)                                   #Recieves the data frame and stores it as data
            str_data = data.decode("utf-8")

            print('recieve: ')
            print(str_data)
            if i >=1:                                                #Adds the old data to the new data
                str_data = str_data_old + "\n" + str_data

            a_dataframe = pd.DataFrame([str_data])
            numpy_array = a_dataframe.to_numpy()
            np.savetxt("decoded_info.txt", numpy_array, fmt="%s")

            str_data_old = str_data
            i += 1

conn.close()                                             #Closes the connection
serv_sock.close()                                       #The TCP gets closed