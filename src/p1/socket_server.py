import socket
import re

# Specify the IP addr and port number 
# (use "127.0.0.1" for localhost on local machine)
# Create a socket and bind the socket to the addr
# TODO start
HOST, PORT = '', 1234
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
# TODO end

def calculate(data):
    reg = re.compile(r'[\d|(|)|\+|\-|\*|\/| ]*')
    if reg.fullmatch(data):
        try:
            return eval(data)
        except:
            return None

while(True):
    # Listen for any request
    # TODO start
    s.listen(100)
    # TODO end
    print("The Grading server for HW2 is running..")

    while(True):
        # Accept a new request and admit the connection
        # TODO start
        client, address = s.accept()
        # TODO end
        print(str(address)+" connected")
        try:
            while (True):
                client.sendall(b"Welcom to the calculator server. Input your problem ?\n")
                # Recieve the data from the client and send the answer back to the client
                # Ask if the client want to terminate the process
                # Terminate the process or continue
                # TODO start
                data = client.recv(1024).decode('utf-8')
                result = calculate(data)
                if result == None:
                    client.sendall(b'Error! Please input again!\n')
                else:
                    text = 'The answer is %s.\n' % result
                    client.sendall(text.encode('utf-8') + b'Do you have any question?(Y/N)\n')

                    data = client.recv(1024).decode('utf-8')
                    if data == 'y' or data == 'Y':
                        continue
                    else:
                        client.close()
                        break

                # TODO end
        except ValueError:
            print("except")
