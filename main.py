# TODO
# handle ip and name from device and send most recent ips and names it needs to function
# store data into csv
# log all unique connections from devices
# create new thread for each device that connects

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
def return_data(dataframe, device_name):
    try:
        device_ip_address = dataframe.loc[dataframe["device-name"] == device_name, "ip-address"].value[0]
    except IndexError as i:
        print(i)
    return device_ip_address


#checks for if the ip address stored in the dataframe equals the current one
#if it doesn't then update it to the current one
def replace_device_ip(device_ip_address, device_name, dataframe):
    if(device_ip_address == dataframe.loc[dataframe["device-name"] == device_name, "ip-address"]):
        pass
    else:
        dataframe.loc[dataframe["device-name"] == device_name, "ip-address"] = device_ip_address



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




if __name__ == "__main__":
    value_names = ["device-name", "ip-address", "timestamp"]

    if(os.path.isfile("devices.csv")):
        dataframe = pandas.read_csv("devices.csv", names=value_names)
        dataframe["timestamp"] = pandas.to_datetime(dataframe["timestamp"])
    else:
        print("File not found or column names wrong")

    