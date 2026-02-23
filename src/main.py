import cv2
import pyautogui
from hand_tracker import HandTracker
from gesture_recognizer import GestureRecognizer
from gesture_actions import GestureActions

pyautogui.FAILSAFE = False

cap = cv2.VideoCapture(0)

tracker = HandTracker(max_hands=2)
recognizer = GestureRecognizer()
actions = GestureActions()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    hands = tracker.process(frame)
    tracker.draw(frame, hands)

    for hand in hands:

        gesture = recognizer.recognize(hand["landmarks"])

        if gesture:
            actions.execute(gesture, hand["landmarks"])

            cv2.putText(
                frame,
                f"Gesto: {gesture}",
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