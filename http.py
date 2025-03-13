from socket import *
import sys

serverSocket = socket(AF_INET, SOCK_STREAM)

port = 8080;
serverSocket.bind(('', port))
serverSocket.listen(1)
# 2 Web server is created
# 2.1
while True:
    print(f"server running on {port} and listening")
    connection, addr = serverSocket.accept()
    print(f"Connection from {addr}")

    try:
        message = connection.recv(1024).decode()
        print("recived: \n", message)

        filename = message.split()[1]
        f = open(filename[1:])
        output = f.read()
        connection.send("HTTP/1.1 200 OK\r\n".encode())

        for i in range(0, len(output)):
            connection.send(output[i].encode())
            connection.send("\r\n".encode())
        connection.close()
    except IOError:
        connection.send("HTTP/1.1 404 Not Found \r\n\r\n".encode())
        connection.send("<html><head><body><h1>404 Not Found</h1></body></head></html>")
        connection.close()
    serverSocket.close()
    sys.exit()


