from cv2 import cv2
import mediapipe as mp

mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
camera = cv2.VideoCapture(0)

with mp_hands.Hands() as hands:
    while True:
        ret, image = camera.read()

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        result = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # showing hand landmarks
        if result.multi_hand_landmarks:
            for hand_landmark in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(image, hand_landmark, mp_hands.HAND_CONNECTIONS)

        cv2.imshow('Hill Climbing', image)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

camera.realease()
cv2.destroyAllWindows()
