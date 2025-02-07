from tcp_connection import start_tcp_connection
from hand_capture import capture_video


def main():
    session_thread = start_tcp_connection()

    capture_video()
    # TODO start ui

    session_thread.join()


if __name__ == '__main__':
    main()
