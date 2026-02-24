import cv2  # type: ignore
import mediapipe as mp  # type: ignore


class HandTracker:

    def __init__(self, max_hands=1):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.9
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