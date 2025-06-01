from threading import Thread

from UI import gui_loop
from email_sender import send_the_email
from client_connection import tcp_connection_loop
from hand_capture import capture_video


def main():
    ui_thread = Thread(target=gui_loop)
    connection_thread = Thread(target=tcp_connection_loop)

    ui_thread.start()
    connection_thread.start()

    ui_thread.join()
    connection_thread.join()


if __name__ == '__main__':
    main()
