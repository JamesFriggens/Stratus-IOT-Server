import socket
from tinydb import TinyDB, Query
from datetime import datetime

database = TinyDB('IOT-Device-Information.json')
Device = Query()

if not database.contains(Device.name == 'Stratus-Server'):
    database.insert({'name': 'Stratus-Server', 'ip': '192.168.1.112', 'last-connected': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
if database.contains(Device.name == 'Stratus-Server'):
        database.update({'last-connected': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, Device.name == 'Stratus-Server')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('192.168.1.136', 10000))

server.listen(10)

while True:
    buffer = ''
    buffer_arr = []
    client, addr = server.accept()
    
    ip_address = addr[0]
    data = client.recv(1024).decode()
    buffer += data
    # print(buffer)
    # for x in range(2):
    buffer_arr = (buffer.split('\n', 1))
    
    # print(ip_address)
    # print(buffer_arr[0])
    # print(buffer_arr[1])

    if database.contains(Device.name == buffer_arr[0]):
        # print("found")
        # print("")
        client.send((database.search(Device.name == buffer_arr[0])[0]['ip']).encode())

    # client.send("hi".encode())
    client.close()

    if not database.contains(Device.name == buffer_arr[1]):
        database.insert({'name': buffer_arr[1], 'ip': ip_address, 'last-connected': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    if database.contains(Device.name == buffer_arr[1]):
        database.update({'ip': ip_address}, Device.name == buffer_arr[1])
        database.update({'last-connected': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, Device.name == buffer_arr[1])

