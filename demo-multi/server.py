import time
import socket
import threading

server = 'localhost'
port = 5000

max_storage_size = 300
#very first index of the log(to set maximum storage size)
begin_idx = 0
#chatting log, log[i] = (color, name, time, content)
log = []

#begin_idx_each: {client_addr:begin_idx}
begin_idx_each = {}

#if you are running this on separate server...
#with open('host.txt', 'rt') as f:
#    server = f.readline().strip()
#    port = int(f.readline().strip())
#    print(server,port)

def dbg(name, param):
    print('{}={}{}'.format(name,param,type(param)))

def send(client_socket, addr):
    
    #packet format:
    #num_packet(1)
    #repeat num_packet times:
    #  color(3)
    #  len_name(1)
    #  name(len_name)
    #  time(4)
    #  len_content(4)
    #  content(len_content)

    return None

def recv(client_socket, addr):
    #packet format:
    #color(3)
    #len_name(1)
    #name(len_name)
    #len_content(4)
    #content(len_content)
    try:
        data = client_socket.recv(4)
    except socket.timeout as e:
        raise e
    if not data:
        return
    color = data[:3]
    len_name = data[3]
    name = client_socket.recv(len_name).decode('utf-8')
    len_content = client_socket.recv(4)
    len_content = int.from_bytes(len_content, 'big')
    content = client_socket.recv(len_content).decode('utf-8')
    tm = time.time()
    msg = (color, name, tm, content)
    print(msg)
    return msg

def manage_sock(client_socket, addr, lock):
    begin_idx_each[addr] = 0
    print("connected:", addr)
    while(True):
        try:
            data = recv(client_socket, addr)
        except socket.timeout:
            pass
        else:
            if not data:
                break
            else:
                lock.acquire()
                log.append(data)
                lock.release()

        send(client_socket, addr)
    print('disconnected:',addr)
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((server,port))
    print('waiting for client...')
    client_list = []
    server_socket.listen(0)
    _lock = threading.Lock()
    while(True):
        client_socket, addr = server_socket.accept()
        client_socket.settimeout(1)
        print("connected, forking...")
        th = threading.Thread(target=manage_sock,
                         args=(client_socket,addr,_lock),
                         daemon=True)
        th.start()
        client_list.append(th)
    server_socket.close()

if __name__ == '__main__':
    main()
