import cv2
from hand_tracker import HandTracker

cap = cv2.VideoCapture(0)
tracker = HandTracker(max_hands=2)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    hands = tracker.process(frame)

    for hand in hands:
        print(hand["label"])  # só pra testar

    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()