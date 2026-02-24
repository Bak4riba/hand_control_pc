   
import math


class GestureRecognizer:

    def __init__(self):
        self.last_gesture = None
        self.gesture_frames = 0
        self.confirmation_frames = 2  # exige 3 frames iguais

    # ======================================================
    # UTILIDADES
    # ======================================================

    def _distance(self, p1, p2):
        return math.sqrt(
            (p1[0] - p2[0]) ** 2 +
            (p1[1] - p2[1]) ** 2
        )

    def _hand_size(self, landmarks):
        wrist = landmarks[0]
        middle_mcp = landmarks[9]
        return self._distance(wrist, middle_mcp)

    # ======================================================
    # PINÇA (CLICK)
    # ======================================================

    def is_pinch(self, landmarks):
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]

        dist = self._distance(thumb_tip, index_tip)
        hand_size = self._hand_size(landmarks)

        return (dist / hand_size) < 0.3

    # ======================================================
    # INDICADOR LEVANTADO (MOVE)
    # ======================================================

    def is_index_only(self, landmarks):

        def finger_up(tip_id, base_id):
            return landmarks[tip_id][1] < landmarks[base_id][1]

        def finger_down(tip_id, base_id):
            return landmarks[tip_id][1] > landmarks[base_id][1]

        index_up = finger_up(8, 5)
        middle_down = finger_down(12, 9)
        ring_down = finger_down(16, 13)
        pinky_down = finger_down(20, 17)

        return index_up and middle_down and ring_down and pinky_down

    # ======================================================
    # PUNHO FECHADO (EXIT)
    # ======================================================

    def is_fist(self, landmarks):

        fingertip_ids = [8, 12, 16, 20]
        finger_base_ids = [5, 9, 13, 17]

        hand_size = self._hand_size(landmarks)

        closed = 0

        for tip_id, base_id in zip(fingertip_ids, finger_base_ids):
            tip = landmarks[tip_id]
            base = landmarks[base_id]

            dist = self._distance(tip, base)

            if (dist / hand_size) < 0.18:
                closed += 1

        return closed >= 3

    # ======================================================
    # CLICK COMPLETO (pinça + outros dedos abaixados)
    # ======================================================

    def is_click(self, landmarks):

        pinch = self.is_pinch(landmarks)

        middle_down = landmarks[12][1] > landmarks[9][1]
        ring_down = landmarks[16][1] > landmarks[13][1]
        pinky_down = landmarks[20][1] > landmarks[17][1]

        return pinch and middle_down and ring_down and pinky_down

    # ======================================================
    # RECONHECIMENTO COM CONFIRMAÇÃO TEMPORAL
    # ======================================================

    def recognize(self, landmarks):

        gesture = None

        # Ordem de prioridade
        if self.is_fist(landmarks):
            gesture = "EXIT"

        elif self.is_click(landmarks):
            gesture = "CLICK"

        elif self.is_index_only(landmarks):
            gesture = "MOVE_MOUSE"

        # ---------------- CONFIRMAÇÃO POR FRAMES ----------------
        if gesture == self.last_gesture:
            self.gesture_frames += 1
        else:
            self.gesture_frames = 0
            self.last_gesture = gesture

        if self.gesture_frames >= self.confirmation_frames:
            return gesture

        return None