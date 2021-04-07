import socket
import random
import time
import struct
import threading
import re

host = 'localhost'
port = 5000


def send(client_socket, name, color, data):
    #packet format:
    #color(3)
    #len_name(1)
    #name(len_name)
    #len_content(4)
    #content(len_content)
    msg = int.to_bytes(color,3,'big')
    name = name.encode('utf-8')
    data = data.encode('utf-8')
    msg = msg + int.to_bytes(len(name),1,'big') + name
    msg = msg + int.to_bytes(len(data),4,'big') + data 
    client_socket.send(msg)
    return

def recv(client_socket):
    #packet format:
    #num_packet(1)
    #repeat num_packet times:
    #  color(3)
    #  len_name(1)
    #  name(len_name(max=256))
    #  time(8)
    #  len_conteant(4)
    #  content(len_content(max=65536))
    '''
    this code is not implemented yet. code down below is just a test code
    '''
    result = []
    try:
        num_packet = int.from_bytes(client_socket.recv(1),'big')
    except socket.timeout as e:
        raise e
    except ConnectionResetError:
        return
    if not num_packet:
        return
    for d in range(num_packet):
        color = '0x' + client_socket.recv(3).hex()
        len_name = int.from_bytes(client_socket.recv(1),'big')
        name = client_socket.recv(len_name).decode('utf-8')
        time = struct.unpack('d',client_socket.recv(8))[0]
        len_content = int.from_bytes(client_socket.recv(4),'big')
        contents = client_socket.recv(len_content).decode('utf-8')
        result.append([color, name, time, contents])
    return result

def recv_chat(client_socket):
    while(True):
        try:
           data = recv(client_socket)
        except socket.timeout:
            pass
        if not data:
            time.sleep(0.1)
            continue
        '''
        this code is not implemented yet. code down below is just a test code
        '''
        for d in data:
            #d[0]:color(in '0x000000' formatted str, ignored on termnal circmustance)
            #d[1]:name(in str)
            #d[2]:time(in gmt time.time() format)
            #d[3]:contents(in str)
            d[2] = time.localtime(d[2])
            tm_hr,tm_min,tm_sec=d[2].tm_hour, d[2].tm_min, d[2].tm_sec
            print('\n{:02}:{:02}:{:02}]{}:{}'.format(tm_hr,tm_min,tm_sec,d[1],d[3]))

def send_chat(client_socket, name, color):
    while(True):
        msg = input('')
        if not msg:
            break
        send(client_socket, name, color, msg)

def main():
    server = 'localhost'
    port = 5000
    try:
        with open('client.txt', 'rt') as f:
            host = f.readline().strip()
            port = int(f.readline().strip())
    except FileNotFoundError:
        pass
    color_re = re.compile('[0-9a-fA-F]{6}')
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
    except ConnectionRefusedError:
        print("Cannot connect to server... Quit.")
        return

    while(True):
        color = input('Set your color: #')
        if color.lower() == 'random':
            color = random.randint(0, 16**6)
            break
        if not color_re.match(color):
            print('invalid color')
            print('please input your color in: #000000 format')
            print('or type "random" to select random color')
            continue
        else:
            color = int(color.lower(),base=16)
            break

    while(True):
        name = input('Set your name:')
        if name:
            break

    inpt = threading.Thread(target=send_chat, args=(client_socket,name,color), daemon=True)
    outpt = threading.Thread(target=recv_chat, args=(client_socket,), daemon=True)
    inpt.start()
    outpt.start()
    inpt.join()
    client_socket.close()

if __name__ == '__main__':
    main()

