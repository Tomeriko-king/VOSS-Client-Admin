import mediapipe as mp
import cv2
from google.protobuf.json_format import MessageToDict

from hand_side import HandSide
from tcp_connection import send_hand_side


def capture_video():
    # Initializing the Model
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(
        static_image_mode=False,
        model_complexity=1,
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75,
        max_num_hands=2)

    # Start capturing video from webcam
    cap = cv2.VideoCapture(0)
    motion_changed = True

    while True:
        # Read video frame by frame
        _, img = cap.read()

        # Flip the image(frame)
        img = cv2.flip(img, 1)

        # Convert BGR image to RGB image
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Process the RGB image
        results = hands.process(imgRGB)

        # If hands are present in image(frame)
        if results.multi_hand_landmarks:
            if motion_changed:
                motion_changed = False
                for i in results.multi_handedness:
                    # Return whether it is Right or Left Hand
                    label = MessageToDict(i)['classification'][0]['label']
                    send_hand_side(HandSide(label))

        else:
            motion_changed = True
