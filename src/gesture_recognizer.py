import math


class GestureRecognizer:

    # ---------------- PINÇA (CLICK) ----------------
    def is_pinch(self, landmarks):

        thumb_tip = landmarks[4]
        index_tip = landmarks[8]

        dist = math.sqrt(
            (thumb_tip[0] - index_tip[0])**2 +
            (thumb_tip[1] - index_tip[1])**2
        )

        return dist < 0.04


    # ---------------- INDICADOR LEVANTADO ----------------
    def is_index_only(self, landmarks):

        index_tip = landmarks[8]
        index_base = landmarks[5]

        middle_tip = landmarks[12]
        middle_base = landmarks[9]

        ring_tip = landmarks[16]
        ring_base = landmarks[13]

        pinky_tip = landmarks[20]
        pinky_base = landmarks[17]

        index_up = index_tip[1] < index_base[1]
        middle_down = middle_tip[1] > middle_base[1]
        ring_down = ring_tip[1] > ring_base[1]
        pinky_down = pinky_tip[1] > pinky_base[1]

        return index_up and middle_down and ring_down and pinky_down


    # ---------------- PUNHO FECHADO ----------------
    def is_fist(self, landmarks):

        fingertip_ids = [8, 12, 16, 20]
        finger_base_ids = [5, 9, 13, 17]

        wrist = landmarks[0]
        middle_mcp = landmarks[9]

        hand_size = math.sqrt(
            (wrist[0] - middle_mcp[0])**2 +
            (wrist[1] - middle_mcp[1])**2
        )

        closed_fingers = 0

        for tip_id, base_id in zip(fingertip_ids, finger_base_ids):

            tip = landmarks[tip_id]
            base = landmarks[base_id]

            dist = math.sqrt(
                (tip[0] - base[0])**2 +
                (tip[1] - base[1])**2
            )

            dist_norm = dist / hand_size

            if dist_norm < 0.09:
                closed_fingers += 1

        return closed_fingers >= 3


    # ---------------- PRIORIDADE DOS GESTOS ----------------
    def recognize(self, landmarks):

        if self.is_fist(landmarks):
            return "EXIT"

        if self.is_pinch(landmarks) and self.is_index_only(landmarks):
            return "CLICK"

        if self.is_index_only(landmarks):
            return "MOVE_MOUSE"

        return None