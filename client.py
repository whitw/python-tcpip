import socket
host = 'localhost'
port = 5000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
while(True):
    msg = input('Send:')
    client_socket.send(msg.encode())
