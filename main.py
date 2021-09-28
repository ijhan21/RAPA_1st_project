from threading import Thread
from utils import *
import time
import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cap = cv2.VideoCapture(r'C:\python\rapa\opencv_class\videos\robot.mp4')

get_data = GetData()
motion_detect = Motion_Detect()
tm = cv2.TickMeter()
time_checker = list()
while True:
    # 시간 측정
    tm.reset()
    tm.start()
    ret, frame = cap.read()
    if ret:
        # 이미지 분석해서 손동작과 손목 좌표를 받아온다
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        state, coordinate, frame = get_data.state_update(frame)
        # print(state, coordinate)
        # 손동작과 손목 좌표를 통해서 모션을 해석
        action = motion_detect.motion_to_action(state, coordinate)
        if action is not None:
            print(action)

        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)
        if key ==27:
            break        
    else:
        print(frame)
    tm.stop()
    ms = tm.getTimeMilli()
    time_checker.append(ms)
print("평균 처리 시간:",round(np.mean(np.array(time_checker)),2))

