#! /usr/bin/python3
import socket
import sys
from threading import Thread
from math import *

HOST = '127.0.0.7'
# PORT = int(input('PORT : '))
PORT = 8800
CODE = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server.bind((HOST, PORT))
except socket.error:
    print('BIND ERROR !!')
    sys.exit()


# example : cos 0 1 10
def Calculate(expr):
    expM = expr.split(',')
    if len(expM) < 4:
        return False, None, None
    try:
        func, left, step, nb = eval(expr)
        ResX, ResY = [], []
        x = left
        for i in range(nb):
            y = round(func(x), 4)
            ResX.append(x)
            ResY.append(y)
            x += step
            x = round(x, 4)
        return True, str(ResX), str(ResY)
    except:
        return False, None, None


def new_client(client, address):
    message = 'Hello You are Connecting to Hicham Server !!'
    STRING = f'From Client {address} : '
    client.send(message.encode(CODE))
    print(f'Client {address} is Connecting !!')
    while True:
        clientMessage = client.recv(1024).decode(CODE)
        check, XX, YY = Calculate(clientMessage)
        print(STRING + clientMessage)
        if clientMessage.upper() == 'END':
            print(f'Connection With Client {address} is Closed !!')
            client.close()
            break
        elif check:
            data = "1" + "|" + XX[1:len(XX) - 1] + "|" + YY[1:len(YY) - 1]
            size = sys.getsizeof(data)
            if size > 64536:
                nb = (size // 64536) + 1
                print(f" Nb = {nb}")
                print(f"Size : {size}")
                data = "1" + "/" + str(nb) + "/" + "1" + "|" + XX[1:len(XX) - 1] + "|" + YY[1:len(YY) - 1]
                print(f"Size of Message in Bytes : {sys.getsizeof(data)}")
                i = 0
                while i < nb:
                    if i == 0:
                        response = data[0:len(data) // nb]
                    else:
                        response = data[i * len(data) // nb:(i + 1) * len(data) // nb]
                    client.send(response.encode(CODE))
                    i += 1
                    print(i)

            else:
                data = "0" + "/" + "1" + "|" + XX[1:len(XX) - 1] + "|" + YY[1:len(YY) - 1]
                client.send(data.encode(CODE))
        else:
            data = "0" + "/" + "0" + "|" + clientMessage
            client.send(data.encode(CODE))


def waiting():
    while True:
        print('Server Listen .....')
        server.listen(2)
        client, address = server.accept()
        T = Thread(target=new_client, args=(client, address))
        T.start()


if __name__ == '__main__':
    waiting()
