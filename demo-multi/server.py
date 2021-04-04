import socket
import threading

server = 'localhost'
port = 5000


#if you are running this on separate server...
#with open('host.txt', 'rt') as f:
#    server = f.readline().strip()
#    port = int(f.readline().strip())
#    print(server,port)

def manage_sock(client_socket, addr):
    print("addr:", addr)
    while(True):
        data = client_socket.recv(65536)
        if not data:
            break
        print("%s:%s" % (addr, data.decode()))
    print('%s: disconnected' % addr)
    client_socket.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server,port))
print('waiting for client...')
client_list = []
server_socket.listen(0)
while(True):
    client_socket, addr = server_socket.accept()
    print("connected, forking...")
    th = threading.Thread(target=manage_sock,
                     args=(client_socket,addr),
                     daemon=True)
    th.start()
    client_list.append(th)
server_socket.close()
