#! /usr/bin/python3
import socket
import sys
import numpy as np
import matplotlib.pyplot as plt

HOST = '127.0.0.7'
# PORT = int(input('PORT = '))
PORT = 8800
STRING = 'From Server : '
CODE = 'utf-8'
MAX_BUFFER_SIZE = 65536


def Receive(Data, Client):
    DATA = Data.split("/")

    if eval(DATA[0]):
        Data = DATA[2]
        i = 0
        while i < eval(DATA[1]) - 1:
            Data += Client.recv(MAX_BUFFER_SIZE).decode(CODE)
            i += 1
            print(i)
    else:
        Data = DATA[1]

    return Data


def Convert_array(Data):
    Data = list(map(lambda a: eval(a), Data.split(",")))
    return np.array(Data)


def Visualization(XVector, YVector):
    plt.plot(Convert_array(XVector), Convert_array(YVector), color='r')
    plt.title("Visualization")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid()
    plt.show()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((HOST, PORT))
except socket.error:
    print('ERROR CONNECTION !!')
    sys.exit()

helloMessage = client.recv(1024).decode(CODE)
print(helloMessage)

while True:
    clientMessage = input('Give Massage : ')
    if clientMessage.upper() == 'END':
        print(f'Your Message : {clientMessage}')
        client.send(clientMessage.encode(CODE))
        break
    elif clientMessage == "":
        client.send("None".encode(CODE))
    client.send(clientMessage.encode(CODE))
    server_Message = client.recv(MAX_BUFFER_SIZE).decode(CODE)
    data = Receive(server_Message, client).split("|")
    if eval(data[0]):
        #print(STRING)
        #print("X Vector : {}".format(data[1].split(",")))
        #print("Y Vector : {}".format(data[2].split(",")))
        Visualization(data[1], data[2])
    else:
        print(STRING + data[1])

client.close()
print('The Connection is Finished !!')
