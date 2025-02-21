import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import os
from email.mime.image import MIMEImage
from security_picture import security_picture
from datetime import datetime


class EmailSender:
    def __init__(self, sender: str, password: str):
        self.sender = sender
        self.password = password


    def send_email(self, subject: str, body: str, image_path: str, recipients: list[str]) -> None:
        msg = MIMEMultipart()

        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = ', '.join(recipients)

        msg.attach(MIMEText(body, 'plain'))
        if image_path:
            with open(image_path, 'rb') as img_file:
                img = MIMEImage(img_file.read())
            msg.attach(img)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(self.sender, self.password)
            smtp_server.sendmail(self.sender, recipients, msg.as_string())



def send_the_email():
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%Y-%m-%d")
    formatted_time = current_datetime.strftime("%H:%M:%S")

    security_picture()
    image_path = 'security_picture.jpg'

    # Your email credentials
    sender_email = 'tomerklein9@gmail.com'
    sender_password = os.getenv('GMAIL_APP_PASSWORD')

    # Receiver's email address
    receiver_email = 'tomerklein9@gmail.com'
    king = EmailSender(sender_email, sender_password)

    # Create the email content
    subject = 'Hacking attempt alert'
    body = f'Someone tried to hack in the app and failed to log in after 3 attempts. \n Date: {formatted_date} \n Time: {formatted_time}'
    king.send_email(subject, body, image_path, [receiver_email])