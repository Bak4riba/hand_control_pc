import time
import pyautogui  # type: ignore


class GestureActions:

    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()

        self.prev_x = None
        self.prev_y = None

        self.last_click_time = 0
        self.click_cooldown = 0.8

        self.block_move_until = 0

        self.base_alpha = 0.25
        self.fast_alpha = 0.6

        self.dead_zone = 3  # pixels

        self.invert_y = True  # inverter eixo Y se necessário

    # ======================================================
    # EXECUTOR PRINCIPAL
    # ======================================================

    def execute(self, gesture, landmarks=None):

        if gesture == "MOVE_MOUSE" and landmarks:
            self._move_mouse(landmarks)

        elif gesture == "CLICK":
            self._click()

        elif gesture == "EXIT":
            raise SystemExit  # saída limpa

    # ======================================================
    # MOVIMENTO DO MOUSE
    # ======================================================

    def _move_mouse(self, landmarks):

        # Bloqueia movimento logo após clique
        if time.time() < self.block_move_until:
            return

        tip = landmarks[8]

        # ---------------- ZONA ATIVA ----------------
        x_min, x_max = 0.2, 0.8
        y_min, y_max = 0.2, 0.8

        if (
            tip[0] < x_min or tip[0] > x_max or
            tip[1] < y_min or tip[1] > y_max
        ):
            self.reset_mouse()
            return

        # ---------------- NORMALIZAÇÃO ----------------
        x_norm = (tip[0] - x_min) / (x_max - x_min)
        y_norm = (tip[1] - y_min) / (y_max - y_min)

        if self.invert_y:
            y_norm = 1 - y_norm

        current_x = x_norm * self.screen_width
        current_y = y_norm * self.screen_height

        current_y = self.screen_height - (y_norm * self.screen_height)

        # Primeira leitura
        if self.prev_x is None or self.prev_y is None:
            self.prev_x = current_x
            self.prev_y = current_y
            pyautogui.moveTo(current_x, current_y)
            return

        # ---------------- ALPHA ADAPTATIVO ----------------
        velocity = abs(current_x - self.prev_x) + abs(current_y - self.prev_y)

        if velocity > 60:
            alpha = self.fast_alpha
        else:
            alpha = self.base_alpha

        smooth_x = alpha * current_x + (1 - alpha) * self.prev_x
        smooth_y = alpha * current_y + (1 - alpha) * self.prev_y

        # ---------------- DEAD ZONE ----------------
        if (
            abs(smooth_x - self.prev_x) > self.dead_zone or
            abs(smooth_y - self.prev_y) > self.dead_zone
        ):
            pyautogui.moveTo(smooth_x, smooth_y)
            self.prev_x = smooth_x
            self.prev_y = smooth_y

    # ======================================================
    # CLICK
    # ======================================================

    def _click(self):

        current_time = time.time()

        if current_time - self.last_click_time > self.click_cooldown:
            pyautogui.click()
            self.last_click_time = current_time

            # Bloqueia movimento por 200ms após clique
            self.block_move_until = current_time + 0.2

    # ======================================================
    # RESET
    # ======================================================

    def reset_mouse(self):
        self.prev_x = None
        self.prev_y = None