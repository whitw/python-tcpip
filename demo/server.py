import socket

server = 'localhost'
port = 5000

#if you are running this on separate server...
#with open('host.txt', 'rt') as f:
#    server = f.readline().strip()
#    port = int(f.readline().strip())
#    print(server,port)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server,port))
print('waiting for client...')
server_socket.listen(0)
while(True):
    client_socket, addr = server_socket.accept()
    print("connected")
    print("addr:",addr)
    while(True):
        data = client_socket.recv(65535)
        if not data:
            break
        print("%s:%s" % (addr, data.decode()))
    print("disconnected")
    client_socket.close()
server_socket.close()
