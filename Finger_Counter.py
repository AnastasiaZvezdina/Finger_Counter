import cv2
import mediapipe as mp 

cap=cv2.VideoCapture(0)  # подключение к web-камере
mp_Hands=mp.solutions.hands  # говорим, что хотим распознавать руки
hands=mp_Hands.Hands(max_num_hands=10)  # задаём характеристики для распознавания
mpDraw=mp.solutions.drawing_utils  # инициализация (создание) утилиты для рисования
fingers_coord=[(8, 6), (12, 10), (16, 14), (20,18)] # ключевые точки всех пальцев, кроме большого
thumb_coord=(4, 2)  # ключевые точки для большого пальца

while cap.isOpened():  # пока камера работает
    succes, image = cap.read()  # получение кадра с камеры
    if not succes:  # если не удалось получить кадр (если succes==False)
        print('Не удалось получить кадр с web-камеры')
        continue  # возвращаемся к ближайшему циклу
    image=cv2.flip(image, 1)  # зеркально отражаем изображение
    RGB_image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
    result=hands.process(RGB_image)  # ищем руки на изображении
    multiLandMarks=result.multi_hand_landmarks  # извлекаем коллекцию (список) найденных рук 
    upCount=0
    if multiLandMarks:
        for idx, handLms in enumerate(multiLandMarks): 
            lbl=result.multi_handedness[idx].classification[0].label
            print(lbl)
            mpDraw.draw_landmarks(image, handLms, mp_Hands.HAND_CONNECTIONS)
            fingersList=[]
            for lm in handLms.landmark:
                h, w, c = image.shape
                x, y = int(lm.x*w), int(lm.y*h)
                fingersList.append((x,y))
            for coord in fingers_coord:
                if fingersList[coord[0]][1]<fingersList[coord[1]][1]:
                    upCount+=1
            if fingersList[thumb_coord[0]][0]<fingersList[thumb_coord[1]][0]:
                upCount+=1

    cv2.putText(image, str(upCount), (100, 150), cv2.FONT_ITALIC, 5, (0, 255, 0), 5)
    cv2.imshow('web-cam', image)
    
    if cv2.waitKey(1) & 0xFF==27: # Ожидаем нажатие клавиши Esc 
        break 
cap.release()









