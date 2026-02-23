import pyautogui # type: ignore
import sys


class GestureActions:

    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.prev_x = None
        self.prev_y = None

    def execute(self, gesture, landmarks=None):

        if gesture == "MOVE_MOUSE" and landmarks:

            tip = landmarks[8]

            current_x = tip[0] * self.screen_width
            current_y = tip[1] * self.screen_height

            if self.prev_x is not None and self.prev_y is not None:

                dx = current_x - self.prev_x
                dy = current_y - self.prev_y

                pyautogui.moveRel(dx, dy)

            self.prev_x = current_x
            self.prev_y = current_y

        elif gesture == "EXIT":
            print("Punho mantido por 1 segundo. Fechando...")
            sys.exit()

    def reset_mouse(self):
        self.prev_x = None
        self.prev_y = None