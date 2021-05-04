import mediapipe as mp

from cv2 import cv2
from directkeys import PressKey, right_key_hex, left_key_hex

mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
camera = cv2.VideoCapture(0)
finger_tips = [4, 8, 12, 16, 20]

with mp_hands.Hands(max_num_hands=1) as hands:
    while True:
        _, image = camera.read()

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        result = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        lm_List = []

        # showing hand landmarks
        if result.multi_hand_landmarks:
            for hand_landmark in result.multi_hand_landmarks:
                my_hand = result.multi_hand_landmarks[0]
                for index, lm in enumerate(my_hand.landmark):
                    height, width, _ = image.shape
                    x, y = int(lm.x * width), int(lm.y * height)
                    lm_List.append([index, x, y])
                mp_draw.draw_landmarks(image, hand_landmark, mp_hands.HAND_CONNECTIONS)

        if len(lm_List):
            fingers_opened = 0

            # thumb
            if lm_List[finger_tips[0]][1] < lm_List[finger_tips[0] - 1][1]:
                fingers_opened += 1

            # index, middle, ring, pinky
            for finger_tip in finger_tips[1:]:
                if lm_List[finger_tip][2] < lm_List[finger_tip - 2][2]:
                    fingers_opened += 1

            if fingers_opened == 5:
                PressKey(right_key_hex)
                print('Gas')
            elif fingers_opened == 0:
                PressKey(left_key_hex)
                print('brake')
        cv2.imshow('Hill Climbing', image)

        # closing the app
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

cv2.destroyAllWindows()
