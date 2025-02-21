from ftplib import FTP

SERVER_IP = '127.0.0.1'
SERVER_PORT = 21

# TODO Create a user that have only upload permissions
FTP_USER = 'dori'
FTP_PASSWORD = 'avmybaby'


def download_file():
    ftp = FTP()
    ftp.connect(SERVER_IP, SERVER_PORT)
    ftp.login(FTP_USER, FTP_PASSWORD)

    remote_filepath = '/path/to/your/image.jpg'  # Replace with the file path on the FTP server
    local_filepath = 'image_from_ftp.jpg'  # This will save the image in the same directory as your Python script

    # Open the local file to save the image
    with open(local_filepath, 'wb') as local_file:
        # Retrieve the file from the FTP server
        ftp.retrbinary(f'RETR {remote_filepath}', local_file.write)

    # Close the connection
    ftp.quit()


