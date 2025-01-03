import socket
import threading
from enum import Enum
from queue import Queue
from time import sleep

from hand_side import HandSide

SERVER_IP = '127.0.0.1'  # Server IP address (localhost in this case)
SERVER_PORT = 12345  # Same port as the server

messages_queue = Queue()


class AuthenticationStatus(Enum):
    RECEIVED_OK = b'OK'
    RECEIVED_FAILED = b'FAILED'
    RECEIVED_PASSED = b'PASSED'


def start_tcp_connection():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print(f"Connected to server at {SERVER_IP}:{SERVER_PORT}")

    session_thread = threading.Thread(target=handle_session, args=(client_socket,))
    session_thread.start()


def send_hand_side(label: HandSide):
    messages_queue.put(label.value.encode())


def handle_authentication(client_socket):
    while True:
        if not messages_queue.empty():
            label = messages_queue.get()
            client_socket.send(label.value.encode())
            response = client_socket.recv(64)
            if response == AuthenticationStatus.RECEIVED_OK:
                continue
            elif response == AuthenticationStatus.RECEIVED_FAILED:
                return False
            elif response == AuthenticationStatus.RECEIVED_PASSED:
                return True


def handle_session(client_socket):
    succeeded = handle_authentication(client_socket)
    print(f"Authentication succeeded: {succeeded}")
    ...

    # Close the socket connection
    client_socket.close()
