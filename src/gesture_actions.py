import time
import pyautogui # type: ignore
import sys


class GestureActions:

    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.prev_x = None
        self.prev_y = None
        self.last_click_time = 0
        self.alpha = 0.35
        self.dead_zone = 3 #pixels

    def execute(self, gesture, landmarks=None):

        if gesture == "MOVE_MOUSE" and landmarks:

            tip = landmarks[8]

            ############ DEfinindo a área de controle do mouse (ajustável) ############
            # zona ativa (ajuste fino depois)
            x_min, x_max = 0.2, 0.8
            y_min, y_max = 0.2, 0.8

            # normalização
            x_norm = (tip[0] - x_min) / (x_max - x_min)
            y_norm = (tip[1] - y_min) / (y_max - y_min)

            # limitar entre 0 e 1
            x_norm = max(0, min(1, x_norm))
            y_norm = max(0, min(1, y_norm))

            current_x = x_norm * self.screen_width
            current_y = y_norm * self.screen_height

            #########################################################################
            # Inicializa as posições anteriores na primeira detecção
            if self.prev_x is None or self.prev_y is None:
                self.prev_x = current_x
                self.prev_y = current_y
                pyautogui.moveTo(current_x, current_y)
                return

            # aplica suavização exponencial
            smooth_x = self.alpha * current_x + (1 - self.alpha) * self.prev_x
            smooth_y = self.alpha * current_y + (1 - self.alpha) * self.prev_y

            # verifica dead zone
            if (
                abs(smooth_x - self.prev_x) > self.dead_zone or
                abs(smooth_y - self.prev_y) > self.dead_zone
            ):
                pyautogui.moveTo(smooth_x, smooth_y)

                self.prev_x = smooth_x
                self.prev_y = smooth_y

        if gesture == "EXIT":
            sys.exit()

        elif gesture == "CLICK":
            current_time = time.time()
            if current_time - self.last_click_time > 0.8:
                pyautogui.click()
                self.last_click_time = current_time
        if self.is_open_hand(landmarks):
            return "CALIBRATE"
    def reset_mouse(self):
        self.prev_x = None
        self.prev_y = None