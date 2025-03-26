from socket import *
import sys
import argparse

#https://docs.python.org/3/library/argparse.html these are the commandline arguments passed to the function.
parse = argparse.ArgumentParser(prog="Client")
parse.add_argument('-i', '--server', type=str)
parse.add_argument('-p', '--port', type=int)
parse.add_argument('-f', '--file', type=str)
arg = parse.parse_args()

# function for the tcp client that will communicate with the server, takes inn server, port and ile fro the commandline
def client(server, port, file):
    # we create an socket that will handle TCP connection and connect to it through the host and port
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((server, port))

    #this sends a get request for the file from the server. 
    request = f"GET /{file} HTTP/1.1\r\nHost: {server}\r\n\r\n " . format(arg.file, arg.server)
    clientSocket.send(request.encode())

    #we recive a response from the cient and decodes it. before the client closes

    res = clientSocket.recv(4096)

    print(res.decode())
    
    clientSocket.close()

client(arg.server, arg.port, arg.file)


