# TODO
# handle ip and name from device and send most recent ips and names it needs to function
# store data into csv
# handle csv data with pandas data frame
# if connected device has the same name but different ip, then update the ip
# log all unique connections from devices
# create new thread for each device that connects

import socket
import datetime
import threading
import pandas

ip_address = "0.0.0.0"
port = 10002

def handle_client(client_socket, address):

    while True:
        try:
            data = client_socket.recv(1024)

            if not data:
                break

            message = data.decode('utf-8').strip()

        except ConnectionResetError:
            # Handle abrupt client disconnect
            print(f"[-] Connection reset by {address[0]}:{address[1]}")
            break

        except Exception as e:
            print(f"[!] Error: {e}")
            break

