import cv2 # type: ignore
import pyautogui # type: ignore

from hand_tracker import HandTracker
from gesture_recognizer import GestureRecognizer
from gesture_actions import GestureActions

#########################Variaveis para calibração do mouse (ajustável)#########################
calibrating = False
calibration_start = None
open_hand_start = None

calib_points_x = []
calib_points_y = []

calib_min_x = 0
calib_max_x = 1
calib_min_y = 0
calib_max_y = 1
###########################################################################################################


pyautogui.FAILSAFE = False

def main():

    cap = cv2.VideoCapture(0)

    tracker = HandTracker(max_hands=1)
    recognizer = GestureRecognizer()
    actions = GestureActions()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        hands = tracker.process(frame)
        tracker.draw(frame, hands)

        gesture_detected = None

        for hand in hands:
            gesture = recognizer.recognize(hand["landmarks"])
            if gesture:
                gesture_detected = gesture
                actions.execute(gesture, hand["landmarks"])

        # Se nenhum gesto ativo → resetar movimento
        if not gesture_detected:
            actions.reset_mouse()

        if gesture_detected:
            cv2.putText(
                frame,
                f"Gesto: {gesture_detected}",
                (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

        cv2.imshow("Hand Control PC", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()