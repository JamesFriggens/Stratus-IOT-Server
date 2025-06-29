import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.1.136', 10000))

client.send("ip addr".encode())
print(client.recv(1024).decode())