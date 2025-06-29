import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('192.168.1.136', 10000))

server.listen(10)

while True:
    client, addr = server.accept()
    print(client.recv(1024).decode())
    client.send("192.168.1.112".encode())
    client.close()