import time
import struct
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

def dbg(name, param):
    print('{}={}{}'.format(name,param,type(param)))

def send(client_socket, addr, my_begin_idx):
    #packet format:
    #num_packet(1)
    #repeat num_packet times:
    #  color(3)
    #  len_name(1)
    #  name(len_name)
    #  time(8)
    #  len_content(4)
    #  content(len_content)
    num_success = 0
    if(my_begin_idx < begin_idx):
        my_begin_idx = begin_idx
    num_packet = len(log) + begin_idx - my_begin_idx
    if num_packet == 0:
        #nothing to send, quit.
        return 0

    try:
        client_socket.send(int.to_bytes(num_packet, 1, 'big'))
    except Exception as e:
        print('Error on sending the number of packet.')
        raise e

    from_idx = my_begin_idx - begin_idx
    end_idx = len(log)
    for d in range(from_idx, end_idx):
        data = log[d]
        msg = data[0] #color, bytes, len=3
        name = data[1].encode('utf-8')
        msg = msg + int.to_bytes(len(name),1,'big') + name
        msg = msg + struct.pack('d',data[2]) # time, double to bytes, len=8
        content = data[3].encode('utf-8')
        msg = msg + int.to_bytes(len(content),4,'big') + content
        try:
            client_socket.send(msg)
        except OSError as e:
            print('failed to send log:',log[d])
            raise e
        else:
            num_success += 1
    return num_success

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
    except ConnectionResetError:
        return
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
    dbg('msg',msg)
    return msg

def manage_sock(client_socket, addr, lock):
    begin_idx_each[addr] = begin_idx
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

        num_success = send(client_socket, addr,begin_idx_each[addr])
        begin_idx_each[addr] += num_success
    print('disconnected:',addr)
    client_socket.close()

def main():
    server = 'localhost'
    port = 5000
    try:
        with open('host.txt', 'rt') as f:
            server = f.readline().strip()
            port = int(f.readline().strip())
    except FileNotFoundError:
        pass
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
