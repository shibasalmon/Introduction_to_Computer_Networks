from socket import *
import sys
import threading

if len(sys.argv) <= 1:
	print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
	sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# TODO start.
HOST, PORT = '', 3456
tcpSerSock.bind((HOST, PORT))
tcpSerSock.listen(100)
# TODO end.

def routine(tcpCliSock, addr):
	# Receive request from the client
	# TODO start.
	message = tcpCliSock.recv(4096).decode('utf-8')
	# while len(message.split()) <= 1:
	# 	message = tcpCliSock.recv(4096).decode('utf-8')
	# TODO end.
	
	# Extract the filename from the given message
	if len(message.split()) >= 2:
		print(message.split()[1])
		filename = message.split()[1].partition("/")[2]
		print(filename)
		fileExist = "false"
		filetouse = "/" + filename
		print(filetouse)
	else:
		return
	try:
		# Check wether the file exist in the cache
		f = open(filetouse[1:], "r")
		outputdata = f.read()
		fileExist = "true"
		
		# ProxyServer finds a cache hit and generates a response message
		# Send the file data to the client
		tcpCliSock.sendall(b"HTTP/1.0 200 OK\r\n")
		tcpCliSock.sendall(b"Content-Type:text/html\r\n")
		# TODO start.
		for i in range(0, len(outputdata)):
			tcpCliSock.sendall(outputdata[i].encode('utf-8'))
		# TODO end.

		print('Read from cache')
	# Error handling for file not found in cache
	except IOError:
		if fileExist == "false":
			# Create a socket on the proxyserver
			c = socket(AF_INET, SOCK_STREAM)# Fill in start.		# Fill in end.
			hostn = filename.replace("www.","",1)
			print(hostn)
			try:
				# Connect to the socket to port 80
				# TODO start.
				if len(sys.argv) == 3:
					c.connect((sys.argv[1], int(sys.argv[2])))
				else:
					c.connect((sys.argv[1], 80))
				c.sendall(message.encode('utf-8'))
				# TODO end.

				# Create a temporary file on this socket and ask port 80 for the file requested by the client
				# fileobj = c.makefile('r', 0)
				# fileobj.write("GET "+"http://" + filename + " HTTP/1.0\n\n")
				
				# Read the response into buffer
				# TODO start.
				# c.sendall(fileobj.encode('utf-8'))
				buffer = b''
				b = c.recv(4096)
				while b != b'':
					buffer += b
					b = c.recv(4096)
				# TODO end.

				# Create a new file in the cache for the requested file.
				# Also send the response in the buffer to client socket and the corresponding file in the cache
				tmpFile = open("./" + filename,"wb")
				# TODO start.
				tmpFile.write(buffer)
				tmpFile.close()
				tcpCliSock.sendall(buffer)
				# TODO end.
			except:
				print("Illegal request")
			c.close()
		else:
			# HTTP response message for file not found
			# Fill in start.
			# Fill in end.
			tcpCliSock.sendall(b'HTTP/1.1 404 Not Found\r\n')
			tcpCliSock.sendall(b'Content-Type: text/html; charset=UTF-8\n\n')
			tcpCliSock.sendall(b'404 Not found')
	# Close the client sockets
	tcpCliSock.close()

while 1:
	# Strat receiving data from the client
	print('Ready to serve...')
	tcpCliSock, addr = tcpSerSock.accept()
	print('Received a connection from:', addr)
	threading.Thread(target=routine, args=(tcpCliSock, addr)).start()
	
# Close the server socket
# TODO start.
tcpSerSock.close()
# TODO end.
