from socket import *
import sys

#local host config for server
host = 'localhost'
port = 8080

#creating a TCP socket for the Http. 
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((host, port))
serverSocket.listen(1)
# 2 Web server is created 
# 2.1 webserver task is is consolidated into this task, where the httpClient runs on TCP. 
print(f"server running on {host}:{port} and listening")

while True:
    connection, addr = serverSocket.accept()
    print(f"Connection from {addr}")

    try:
        message = connection.recv(4096).decode()
        if not message:
            connection.close()
            continue

        print("recived: \n", message)

        filename = message.split()[1]

        f = open(filename[1:])
        output = f.read()
        header = "HTTP/1.1 200 OK\r\n"
        content = "Content-Type: text/html\r\n\r\n"
        packet = header.encode() + content.encode() + output.encode()
        connection.sendall(packet)

        #this loop sends each letter seperately. 
        for i in range(0, len(output)):
            connection.send(output[i].encode())
            connection.send("\r\n".encode())

        connection.close()
    except IOError:     #if no file is found it will return an 404 not found response with the html.
        connection.send("HTTP/1.1 404 Not Found \r\n\r\n".encode())
        connection.send("<html><head><body><h1>404 Not Found</h1></body></head></html>")
    
    # after data is sent the connection closes until the server is restarted and called again.    
    finally:
        connection.close()
    serverSocket.close()
    sys.exit()


