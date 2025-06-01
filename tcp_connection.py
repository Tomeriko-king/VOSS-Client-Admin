import socket

from Lib.test.test_linecache import EMPTY

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
    def process_hand_side(client_socket: VOSSSocketClientAdmin, hand_side: HandSide) -> AuthenticationStatus:
        try:
            client_socket.send_hand_side_auth_request(hand_side)
            return client_socket.recv_hand_side_auth_response()

        #todo
        except Exception as e:
            print(f"[ERROR] Failed to process hand side auth: {e}")
            return AuthenticationStatus.RECEIVED_FAILED


    def process_target_ip_screenshot(client_socket: VOSSSocketClientAdmin, target_ip: str) -> str:
        try:
            client_socket.send_screenshot_from_target_request(target_ip)
            client_socket.recv_screenshot_from_target_response('screenshot.jpg')
            return 'screenshot.jpg'

        #todo
        except Exception as e:
            print(f"[ERROR] Failed to get screenshot from {target_ip}: {e}")
            return ''

    try:
        # Create a socket object
        client_socket = VOSSSocketClientAdmin()
        # Connect to the server
        client_socket.connect(SERVER_IP)
        print(f"Connected to server at {SERVER_IP}")

    #todo
    except Exception as e:
        print(f"[ERROR] Could not connect to server: {e}")
        return

    try:

        # Start authentication
        while True:
            hand_side = hands_to_send.get(timeout= 2)
            auth_status = process_hand_side(client_socket, hand_side)
            set_auth_status(auth_status)

            if auth_status == AuthenticationStatus.RECEIVED_OK:
                continue
            elif auth_status == AuthenticationStatus.RECEIVED_PASSED:
                break
            elif auth_status == AuthenticationStatus.RECEIVED_FAILED:
                try:
                    client_socket.close()

                #todo
                except Exception as e:
                    print(f"[WARN] Failed to close socket: {e}")

                sleep(0.1)  # Let authentication camera shutdown
                try:
                    send_the_email()

                #todo
                except Exception as e:
                    print(f"[ERROR] Failed to send email: {e}")

                return
            else:
                continue

        while True:
            try:
                target_ip = target_ips_to_send.get()
            except EMPTY:
                continue

            filename = process_target_ip_screenshot(client_socket, target_ip)
            set_target_screenshot(filename)


    except:
            print(f"[FATAL] Unexpected error in main loop")
            try:
                client_socket.close()
            except:
                pass


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
    global target_screenshot_filename
    with screenshot_filename_condition:
        screenshot_filename_condition.wait_for(lambda: target_screenshot_filename != '')
        screenshot_filename = target_screenshot_filename
        target_screenshot_filename = ''
        return screenshot_filename
