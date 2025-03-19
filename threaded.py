from socket import *
import threading
server = 'localhost'
port = '8080'

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(1)
serverSocket.listen(1)

def client(connection):
    req = connection.recv(1024)
    print("recived: " + req.decode())
    #client will send back HTTP/1.1 200 OK
    res = "HTTP/1.1 200 OK\r\n"

    clientSocket.send(res.encode())
    clientSocket.close()

def server():
