from socket import *
import threading
import _thread as thread
import sys

# this function establishes the client connection. 
def client(connection):
    try:
        req = connection.recv(4096).decode()
        print("recived: " + req)

        #client will send back HTTP/1.1 200 OK
        res = "HTTP/1.1 200 OK\r\n"
        connection.sendall(res.encode())
        #if it cant connect to the client it will send exception error.
    except Exception:
        print(f"Client error: {Exception}")
    finally:     # and close the connection when its done
        connection.close()

# this creates the socket and deligates the client to its own socket thread. 
def main():
    # here we establish the socket connection. 
    serverSocket = socket(AF_INET, SOCK_STREAM)
    server = 'localhost'
    port = 8080
    try:
        serverSocket.bind((server, port))   #bind the server or throws an error if it cannot bind. 
    except:
        print('cant bind socket')
        sys.exit()
    serverSocket.listen(10)                 # we tell the server to listen for upto 10 connections

    # when a new client request a tcp connection it will open a new seperate thread for it.
    while True:
        connection, addr = serverSocket.accept()
        print('server running on: ', addr)
        threading.Thread(target=client, args=(connection, )).start()
    serverSocket.close()
if __name__ == '__main__':
    main()