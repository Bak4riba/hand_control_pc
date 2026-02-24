import cv2  # type: ignore
import pyautogui  # type: ignore

from hand_tracker import HandTracker
from gesture_recognizer import GestureRecognizer
from gesture_actions import GestureActions

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
        h, w, _ = frame.shape

        box_w = actions.nav_box_width
        box_h = actions.nav_box_height

        x_min = 0.5 - box_w / 2
        x_max = 0.5 + box_w / 2
        y_min = 0.5 - box_h / 2
        y_max = 0.5 + box_h / 2

        start_x = int(x_min * w)
        end_x = int(x_max * w)
        start_y = int(y_min * h)
        end_y = int(y_max * h)

        cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)


        hands = tracker.process(frame)
        tracker.draw(frame, hands)

        gesture_detected = None

        for hand in hands:
            gesture = recognizer.recognize(hand["landmarks"])
            if gesture:
                gesture_detected = gesture
                actions.execute(gesture, hand["landmarks"])

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