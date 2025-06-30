import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.1.136', 10000))

client.send("Stratus-Server\narduino".encode())
print(client.recv(1024).decode())