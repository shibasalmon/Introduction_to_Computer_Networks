#import socket module
from socket import *
import time
import sys # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
# TODO start
HOST, PORT = '', 2345
serverSocket.bind((HOST, PORT))
serverSocket.listen(3)
# TODO in end
while True:
    #Establish the connection
    print('Ready to serve...')
    # TODO start
    connectionSocket, address = serverSocket.accept()
    # TODO end
    try:
        # Receive http request from the clinet
        # TODO start
        message = connectionSocket.recv(4096)
        # TODO end
        print(message)

        if len(message.split()) >= 2:
            filename = message.split()[1]
        else:
            continue
        if filename == b'/':
            filename = b'/index.html'
        print(filename)
        f = open(filename[1:])
        
        # Read data from the file that the client requested
        # Split the data into lines for future transmission 
        # TODO start
        outputdata = f.read()
        # TODO end
        print(outputdata)

        #Send one HTTP header line into socket
        # TODO start
        
        # send HTTP status to client
        connectionSocket.sendall(b'HTTP/1.1 200 OK\r\n')
        # send content type to client
        connectionSocket.sendall(b'Content-Type: text/html; charset=UTF-8\n\n')
        # TODO end
        
        # Send the content of the requested file to the client  
        for i in range(0, len(outputdata)):
            connectionSocket.sendall(outputdata[i].encode())
        connectionSocket.sendall("\r\n".encode())

        connectionSocket.close()
    except IOError:
        #Send response message for file not found
        # TODO start
        connectionSocket.sendall(b'HTTP/1.1 404 Not Found\r\n')
        connectionSocket.sendall(b'Content-Type: text/html; charset=UTF-8\n\n')
        connectionSocket.sendall(b'404 Not found')
        # TODO end

        #Close client socket
        # TODO start
        connectionSocket.close()
        # TODO end
serverSocket.close()
sys.exit() #Terminate the program after sending the corresponding data
