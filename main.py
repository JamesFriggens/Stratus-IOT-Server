# TODO
# handle ip and name from device and send most recent ips and names it needs to function
# store data into csv
# if connected device has the same name but different ip, then update the ip
# log all unique connections from devices
# create new thread for each device that connects
# move dataframe initialization out of return_data function

import socket
import datetime
import threading
import pandas
import os

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

    client_socket.close()

# defines pandas dataframe returns the device ip address the client is searching for
def return_data(device_name):
    value_names = ["device-name", "ip-address", "timestamp"]

    if(os.path.isfile("devices.csv")):
        dataframe = pandas.read_csv("devices.csv", names=value_names)
        dataframe["timestamp"] = pandas.to_datetime(dataframe["timestamp"])
    else:
        print("File not found or column names wrong")

    try:
        device_ip_address = dataframe.loc[dataframe["device-name"] == device_name, "ip-address"].value[0]
    
    except IndexError as i:
        print(i)

    return device_ip_address
    



def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Allow address reuse
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((ip_address, port))

    server.listen(5)  #queue 5 connections
    print(f"[*] Listening on {ip_address}:{port}")

    try:
        while True:
            client_socket, client_address = server.accept()

            # Start a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.daemon = True  # Allows program to exit even if threads are running
            client_thread.start()

    except KeyboardInterrupt:
        print("\n[!] Server is shutting down.")

    finally:
        server.close()


