import socket
import random
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

def recv(client_socket, data):
    #packet format:
    #num_packet(1)
    #repeat num_packet times:
    #  color(3)
    #  len_name(1)
    #  name(len_name)
    #  time(4)
    #  len_conteant(4)
    #  content(len_content)
    return None
    data = 'testmsg'.encode('utf-8')
    return data.decode('utf-8')

def recv_chat():
    pass

def main():
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

    while(True):
        msg = input('Send:')
        if not msg:
            break
        send(client_socket, name, color, msg)
    client_socket.close()

if __name__ == '__main__':
    main()

