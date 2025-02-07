import socket
import threading
from enum import Enum
from queue import Queue
from threading import Event
from time import sleep

from hand_side import HandSide

SERVER_IP = '10.76.107.250'  # Server IP address (localhost in this case)
SERVER_PORT = 12345  # Same port as the server

messages_queue = Queue()

authentication_finished_event = Event()

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

    session_thread = threading.Thread(target=handle_session, args=(client_socket,), daemon=True)
    session_thread.start()

    return session_thread


def send_hand_side(label: HandSide):
    messages_queue.put(label.value.encode())


def request_screenshot(ip_address: str):
    message = b'screenshot-' + ip_address.encode()
    messages_queue.put(message)


def handle_authentication(client_socket):
    while True:
        if not messages_queue.empty():
            label = messages_queue.get()
            client_socket.send(label)
            response = client_socket.recv(64)
            if response == AuthenticationStatus.RECEIVED_OK.value:
                continue
            elif response == AuthenticationStatus.RECEIVED_FAILED.value:
                return False
            elif response == AuthenticationStatus.RECEIVED_PASSED.value:
                return True


def handle_screenshot(client_socket, command: bytes):
    client_socket.send(command)
    response = client_socket.recv(64)
    'screenshot-is-ready:{filename}'


def handle_session(client_socket):
    succeeded = handle_authentication(client_socket)
    print(f"Authentication succeeded: {succeeded}")
    authentication_finished_event.set()
    while True:
        if not messages_queue.empty():
            command = messages_queue.get()
            if command.startswith(b'screenshot-'):
                handle_screenshot(client_socket, command)

    # Close the socket connection
    client_socket.close()
