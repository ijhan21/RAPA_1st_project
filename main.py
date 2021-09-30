from threading import Thread
from utils_normal7 import *
import time
import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cap = cv2.VideoCapture(r'C:\python\rapa\opencv_class\videos\robot.mp4')

get_data = GetData()
motion_detect = Motion_Detect()
actionInstance = Action()
title = 'webcam'
while True:
    ret, frame = cap.read()
    if ret:
        # 이미지 분석해서 손동작과 손목 좌표를 받아온다
        state, coordinate = get_data.state_update(frame)
        # print(state, coordinate)
        # 손동작과 손목 좌표를 통해서 모션을 해석
        action, highlight = motion_detect.motion_to_action(state, coordinate)
        actionInstance.ReceiveFrame(frame)
        if highlight == False :            
            actionInstance.action(act='slideshow',direction=action)
        else:  
            actionInstance.action(act='spotlight',direction=action)
        

        print(f'action : {action}, highlight : {highlight}')
        cv2.putText(frame,str(action),(100,100),1,3,(255,100,0),2)
    

    # cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)  
    # cv2.setWindowProperty(title, cv2.WND_PROP_TOPMOST, 1)
    # cv2.imshow(title, frame)
    key = cv2.waitKey(20)
    if key ==27:
        break
    # else:
    #     print(frame)

