import socket

HOST, PORT = '', 1234
# HOST, PORT = '140.112.42.100', 7777

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    data = s.recv(1024).decode('utf-8')
    print('Receive server messages.')
    print(data)

    msg = input('SEND >> ')
    if msg == 'exit':
        s.close()
        break
    s.sendall(msg.encode('utf-8'))