import socket

server = 'localhost'
port = 5000

with open('host.txt', 'rt') as f:
    server = f.readline().strip()
    port = int(f.readline().strip())
    print(server,port)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server,port))
server_socket.listen(0)
client_socket, addr = server_socket.accept()
print("connected");
print("addr:",addr);
data = client_socket.recv(65535)
print("received:", data.decode())

