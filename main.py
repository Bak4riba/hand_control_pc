import cv2
import time
from hand_tracker import HandTracker, is_fist

cap = cv2.VideoCapture(0)
tracker = HandTracker(max_hands=2)

fist_start = None  # precisa estar fora do loop

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    hands = tracker.process(frame)

    # desenha landmarks
    tracker.draw(frame, hands)

    # 🔥 DETECÇÃO DO GESTO (AGORA NO LUGAR CERTO)
    for hand in hands:
        if is_fist(hand["landmarks"]):
            if fist_start is None:
                fist_start = time.time()
            elif time.time() - fist_start > 1.0:
                print("Punho mantido por 1 segundo. Fechando...")
                cap.release()
                cv2.destroyAllWindows()
                exit()
        else:
            fist_start = None

    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()