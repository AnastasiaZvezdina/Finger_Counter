import cv2
import mediapipe as mp
cap=cv2.VideoCapture(0)
mp_Hands=mp.solutions.hands 
hands=mp_Hands.Hands(max_num_hands=10)
mpDraw=mp.solutions.drawing_utils

while cap.isOpened():
    succes, image = cap.read()
    if not succes:
        print('Не удалось получить кадр с web-камеры')
        continue
    image=cv2.flip(image, 1)
    RGB_image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result=hands.process(RGB_image)
    multiLandMarks=result.multi_hand_landmarks
    if multiLandMarks:
        print(len(multiLandMarks), 'рук в кадре')
    else:
        print('Рук в кадре нет')


    cv2.imshow('web-cam', image)
    
    if cv2.waitKey(1) & 0xFF==27:
        break 
cap.release()









