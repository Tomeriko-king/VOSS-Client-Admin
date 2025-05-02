import socket
from email_sender import send_the_email
from enum import Enum
from threading import Event, Lock, Condition
from time import sleep
# from hand_side import HandSide
from queue import Queue

from voss_socket import VOSSSocketClientAdmin, HandSide, AuthenticationStatus

SERVER_IP = '127.0.0.1'  # Server IP address (localhost in this case)

hands_to_send = Queue()
target_ips_to_send = Queue()

current_auth_status = AuthenticationStatus.RECEIVED_OK
# Lock for synchronization
auth_status_lock = Lock()


def tcp_connection_loop():
    # TODO create class
    def process_hand_side(client_socket: VOSSSocketClientAdmin, hand_side: HandSide) -> AuthenticationStatus:
        client_socket.send_hand_side_auth_request(hand_side)

        return client_socket.recv_hand_side_auth_response()

    def process_target_ip_screenshot(client_socket: VOSSSocketClientAdmin, target_ip: str) -> str:
        client_socket.send_screenshot_from_target_request(target_ip)
        client_socket.recv_screenshot_from_target_response('screenshot.jpg')
        return 'screenshot.jpg'

    # Create a socket object
    client_socket = VOSSSocketClientAdmin()

    # Connect to the server
    client_socket.connect(SERVER_IP)
    print(f"Connected to server at {SERVER_IP}")

    # Start authentication
    while True:
        hand_side = hands_to_send.get()
        auth_status = process_hand_side(client_socket, hand_side)
        set_auth_status(auth_status)

        if auth_status == AuthenticationStatus.RECEIVED_OK:
            continue
        elif auth_status == AuthenticationStatus.RECEIVED_PASSED:
            break
        elif auth_status == AuthenticationStatus.RECEIVED_FAILED:
            client_socket.close()
            sleep(0.1)  # Let authentication camera shutdown
            send_the_email()
            return
        else:
            continue

    while True:
        target_ip = target_ips_to_send.get()
        filename = process_target_ip_screenshot(client_socket, target_ip)
        set_target_screenshot(filename)


# Function to export
def send_hand_side(hand_side: HandSide):
    hands_to_send.put(hand_side)


# Function to export
def send_target_ip(target_ip: str):
    target_ips_to_send.put(target_ip)


def set_auth_status(new_status: AuthenticationStatus):
    """Writer function: safely updates the auth status."""
    global current_auth_status
    with auth_status_lock:
        current_auth_status = new_status


def get_auth_status() -> AuthenticationStatus:
    """Reader function: returns the current auth status."""
    with auth_status_lock:
        return current_auth_status


target_screenshot_filename: str = ''
screenshot_filename_lock = Lock()
screenshot_filename_condition = Condition(screenshot_filename_lock)


def set_target_screenshot(result: str):
    global target_screenshot_filename
    with screenshot_filename_condition:
        target_screenshot_filename = result
        screenshot_filename_condition.notify_all()  # Wake up the waiting thread


def wait_for_target_screenshot() -> str:
    with screenshot_filename_condition:
        screenshot_filename_condition.wait_for(lambda: target_screenshot_filename != '')
        return target_screenshot_filename
