from hand_capture import capture_video

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit
from PIL import ImageGrab
from PIL import Image
from datetime import datetime

from tcp_connection import request_screenshot


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.success_login = False
        self.setStyleSheet("background-color: darkGray;")
        self.button2 = QPushButton("PASSWORD", self)

        # Create a button
        self.button = QPushButton("TAKE  A  SCREENSHOT!", self)
        self.image_label = QLabel(self)

        self.text_box = QLineEdit(self)
        self.text_box.setPlaceholderText("Enter your text here...")  # Placeholder text

        # Resize the button (optional)
        self.button.resize(200, 50)
        self.image_label.resize(800, 600)

        self.button2.setStyleSheet("background-color: cyan")
        self.button.setStyleSheet("background-color: cyan")

        # Connect the button's clicked signal to a method (command)
        self.button2.clicked.connect(self.on_button_click_password)
        self.button.clicked.connect(self.on_button_click)

        # Create a layout
        layout = QVBoxLayout()

        # Add the button and label to the layout
        layout.addWidget(self.button2)
        layout.addWidget(self.button)

        layout.addWidget(self.image_label)
        layout.addWidget(self.text_box)

        # Create a central widget and set the layout
        central_widget = QWidget(self)
        central_widget.setLayout(layout)

        # Set the central widget
        self.setCentralWidget(central_widget)

        # Set the window title and size
        self.setWindowTitle("Button Command Example")

    def on_button_click_password(self):
        capture_video()

    # Method that will be called when the button is clicked
    def on_button_click(self):
        if self.success_login:
            text = self.text_box.text()
            request_screenshot(text)

            now = datetime.now()
            self.setWindowTitle(now.strftime("%d/%m/%Y %H:%M:%S"))
            tmp_image = QPixmap('screenshot_small.png')
            self.image_label.setPixmap(tmp_image)
            self.image_label.resize(800, 600)
        else:
            print("failed to log in")



def start_gui():
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()

start_gui()