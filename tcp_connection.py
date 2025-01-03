import socket
from time import sleep

SERVER_IP = '127.0.0.1'  # Server IP address (localhost in this case)
SERVER_PORT = 12345  # Same port as the server


def start_client():
    # Server configuration

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print(f"Connected to server at {SERVER_IP}:{SERVER_PORT}")

    handle_session(client_socket)

    # Close the socket connection
    client_socket.close()


def handle_session(client_socket):
    # TODO
    ...
