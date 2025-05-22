from dataclasses import dataclass
from typing import Optional

import mediapipe as mp
import cv2
from google.protobuf.json_format import MessageToDict

from tcp_connection import send_hand_side, get_auth_status
from voss_socket import HandSide, AuthenticationStatus


def init_hands_model():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        model_complexity=1,
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75,
        max_num_hands=2)

    return hands


@dataclass
class HandCaptureResult:
    motion_detected: bool
    raised_hand_side: Optional[HandSide]

    @classmethod
    def from_model_result(cls, model_result):
        motion_detected = bool(model_result.multi_hand_landmarks)
        if motion_detected:
            raised_hand_side = MessageToDict(model_result.multi_handedness[0])['classification'][0]['label']
            raised_hand_side = HandSide(raised_hand_side.encode())
        else:
            raised_hand_side = None

        return cls(motion_detected, raised_hand_side)


def process_image(img):
    img_dup = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img_dup, cv2.COLOR_BGR2RGB)
    return img_rgb


def capture_video() -> None:
    # Initializing the Model
    hands = init_hands_model()

    # Start capturing video from webcam
    cap = cv2.VideoCapture(0)
    motion_changed = True

    while get_auth_status() == AuthenticationStatus.RECEIVED_OK:
        _, img = cap.read()
        img = process_image(img)
        cv2.imshow('Camera', img)

        hand_capture_result = HandCaptureResult.from_model_result(hands.process(img))

        if hand_capture_result.motion_detected:
            if motion_changed:
                motion_changed = False
                print(hand_capture_result.raised_hand_side)
                send_hand_side(hand_capture_result.raised_hand_side)

        else:
            motion_changed = True
