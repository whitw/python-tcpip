import socket
host = 'localhost'
port = 5000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
while(True):
    msg = input('Send:')
    if not msg:
        break
    try:
        client_socket.send(msg.encode())
    except Exception as e:
        print("exception occured:",e)
client_socket.close()

