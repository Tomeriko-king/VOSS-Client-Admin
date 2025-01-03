from tcp_connection import start_tcp_connection
from hand_capture import capture_video


def main():
    start_tcp_connection()
    capture_video()


if __name__ == '__main__':
    main()
