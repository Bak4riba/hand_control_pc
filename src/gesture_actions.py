import pyautogui
import sys

class GestureActions:

    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()

    def execute(self, gesture, landmarks=None):

        if gesture == "MOVE_MOUSE" and landmarks:

            tip = landmarks[8]

            screen_x = tip[0] * self.screen_width
            screen_y = tip[1] * self.screen_height

            pyautogui.moveTo(screen_x, screen_y)

        elif gesture == "EXIT":
            print("Punho mantido por 1 segundo. Fechando...")
            sys.exit()