import cv2
import mediapipe as mp
import time
from time import sleep

class HandTracker:
    def __init__(self, max_hands=2):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

    def process(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        hands_data = []

        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):

                label = results.multi_handedness[idx].classification[0].label

                landmarks = []
                for lm in hand_landmarks.landmark:
                    landmarks.append((lm.x, lm.y, lm.z))

                hands_data.append({
                    "label": label,
                    "landmarks": landmarks,
                    "mp_landmarks": hand_landmarks
                })

        return hands_data

    def draw(self, frame, hands_data):
        for hand in hands_data:
            self.mp_draw.draw_landmarks(
                frame,
                hand["mp_landmarks"],
                self.mp_hands.HAND_CONNECTIONS
            )

import math

def is_fist(landmarks):

    fingertip_ids = [8, 12, 16, 20]
    finger_base_ids = [5, 9, 13, 17]

    # mede tamanho aproximado da mão
    wrist = landmarks[0]
    middle_base = landmarks[9]

    hand_size = math.sqrt(
        (middle_base[0] - wrist[0])**2 +
        (middle_base[1] - wrist[1])**2
    )

    closed_fingers = 0

    for tip_id, base_id in zip(fingertip_ids, finger_base_ids):

        tip = landmarks[tip_id]
        base = landmarks[base_id]

        dist = math.sqrt(
            (tip[0] - base[0])**2 +
            (tip[1] - base[1])**2
        )
        print(dist)
        if dist < hand_size * 0.25:  # proporcional ao tamanho da mão
            closed_fingers += 1

    return closed_fingers >= 3