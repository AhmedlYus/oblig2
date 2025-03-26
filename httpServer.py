from socket import *
import sys

#localhost config the server will be running on.
host = 'localhost'
port = 8080

#creating a TCP socket for the Http, and binding it. 
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((host, port))
serverSocket.listen(1)
# 2 Web server is created 
# 2.1 webserver task is is consolidated into this task, where the httpClient runs on TCP. 
print(f"server running on {host}:{port} and listening")

while True:
    connection, addr = serverSocket.accept()
    print(f"Connection from {addr}")

    try: #in the first instance we recive bytes from the client through the connection
        message = connection.recv(4096).decode()
        if not message:             # if there is no message from the client the connection closes, else it continues.
            connection.close()
            continue

        print("recived: \n", message) 

        filename = message.split()[1] #we extract the filename from the GET index.html the client sends here it is /index.html 

        f = open(filename[1:])                      # we open the filname and skips the first character / frm the filename
        output = f.read()                           # reads the content in the html file
        header = "HTTP/1.1 200 OK\r\n"              #creates header and content type that will be sendt back to the client 
        content = "Content-Type: text/html\r\n\r\n" #the content type tells the client to treat is as html file.
        packet = header.encode() + content.encode() + output.encode()
        connection.sendall(packet)

        #this loop sends each letter seperately to the client / requesting service. 
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


