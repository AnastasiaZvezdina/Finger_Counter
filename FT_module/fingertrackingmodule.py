import cv2
import mediapipe as mp
import time
import math

class handDetector():
    def __init__(self, mode=False, maxHands=2, complexity=0, detectionCon=0.75, trackingCon=0.75):
        self.mpHands = mp.solutions.hands  # говорим, что хотим распознавать руки
        self.hands = self.mpHands.Hands(mode, maxHands, complexity, detectionCon, trackingCon)  # характеристики для распознавания
        self.mpDraw = mp.solutions.drawing_utils # инициализация утилиты для рисования
        self.fingertips = [4, 8, 12, 16, 20] # кончики пальцев
        self.pointPosition = {}
        self.fingers = {} 

    def findHands(self, img, draw=False):
        RGB_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img.flags.writeable = False
        self.result = self.hands.process(RGB_image)  # ищем руки на изображении
        img.flags.writeable = True
        if draw:
            multiLandMarks = self.result.multi_hand_landmarks  # извлекаем коллекцию (список) найденных рук
            if multiLandMarks:
                for handLms in multiLandMarks:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
    
    def findFingersPosition(self, img, draw=False):
        mhl = self.result.multi_hand_landmarks
        if mhl:
            for idx, handLms in enumerate(mhl):
                xList = []
                yList = []
                self.pointPosition[idx] = []
                for lm in handLms.landmark:
                    h, w, c = img.shape
                    x, y = int(lm.x * w), int(lm.y * h) 
                    self.pointPosition[idx].append((x, y))
                    xList.append(x)
                    yList.append(y)
                if draw:
                    offset = 20
                    xmin, xmax = min(xList), max(xList)
                    ymin, ymax = min(yList), max(yList)
                    cv2.rectangle(img, (xmin - offset, ymin - offset), (xmax + offset, ymax + offset), (0, 255, 0), 2)

    def fingersUp(self, draw=False):
        mhl = self.result.multi_hand_landmarks
        if mhl:
            handCount = len(mhl)
            for i in range(handCount):
                self.fingers[i] = []
                side = 'left'

                if self.pointPosition[i][5][0] > self.pointPosition[i][17][0]:
                    side = 'right'

                if side == 'left': 
                    if self.pointPosition[i][self.fingertips[0]][0] < self.pointPosition[i][self.fingertips[0]-2][0]:
                        self.fingers[i].append(1)
                    else:
                        self.fingers[i].append(0)
                else:
                    if self.pointPosition[i][self.fingertips[0]][0] > self.pointPosition[i][self.fingertips[0]-2][0]:
                        self.fingers[i].append(1)
                    else:
                        self.fingers[i].append(0)

                for id in range(1, 5):
                    if self.pointPosition[i][self.fingertips[id]][1] < self.pointPosition[i][self.fingertips[id]-2][1]:
                        self.fingers[i].append(1)
                    else:
                        self.fingers[i].append(0)
                
                if draw:
                    print(self.fingers[i])

    def findDistance(self, p1, p2, handNumber=0, draw=False, img=None, r=10, t=3):
        x1, y1 = self.pointPosition[handNumber][p1][0], self.pointPosition[handNumber][p1][1]
        x2, y2 = self.pointPosition[handNumber][p2][0], self.pointPosition[handNumber][p2][1]
        cx, cy = (x1+x2) // 2,  (y1+y2) // 2
        
        lenght = math.sqrt((x2-x1)**2+(y2-y1)**2)

        if draw:            
            cv2.circle(img, (x1, y1), r, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), t)
            if lenght > 30:
                cv2.circle(img, (cx, cy), r, (0, 255, 255), cv2.FILLED)
            else:
                cv2.circle(img, (cx, cy), r, (255, 255, 0), cv2.FILLED)
            print(lenght)
def main():
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    prevTime = time.time()
    while cap.isOpened():  # пока камера "работает"        
        success, image = cap.read()  # получение кадра с камеры
        if not success:  # если не удалось получить кадр
            print('Не удалось получить кадр с web-камеры')
            continue  # возвращаемся к ближайшему циклу
        image = cv2.flip(image, 1)  # зеркально отражаем изображение        
        detector.findHands(image, True)
        detector.findFingersPosition(image, True)
        detector.fingersUp()
        mhl = detector.result.multi_hand_landmarks
        if mhl:
            handCount = len(mhl)
            for i in range(handCount):
                detector.findDistance(4, 8, i, True, image)
        currentTime = time.time()
        fps = 1 / (currentTime - prevTime)
        prevTime = currentTime
        cv2.putText(image, f"FPS: {fps}", (200, 100), cv2.FONT_ITALIC, 2, (255, 255, 255), 2)
        cv2.imshow('web-cam', image)

        if cv2.waitKey(1) & 0xFF == 27:  # Ожидаем нажатие ESC 
            break

main()