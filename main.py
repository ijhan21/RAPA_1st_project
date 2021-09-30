from threading import Thread
from utils import *
import time
import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cap = cv2.VideoCapture(r'C:\python\rapa\opencv_class\videos\robot.mp4')

get_data = GetData()
motion_detect = Motion_Detect()
actionInstance = Action()
title1 = 'webcam'
transaction=True
while True:
    ret, frm = cap.read()
    if ret:
        # 이미지 분석해서 손동작과 손목 좌표를 받아온다
        state, coordinate, frm = get_data.state_update(frm)
        # print(state, coordinate)
        # 손동작과 손목 좌표를 통해서 모션을 해석
        action, highlight = motion_detect.motion_to_action(state, coordinate, transaction=transaction)
        if action in ['toDown',"toUp","toLeft","toRight"]:
            print(action, highlight)
        if highlight == False :
            transaction = True
            frame = actionInstance.action(act='slideshow',direction=action)
        else:  
            transaction = False
            actionInstance.action(act='spotlight',direction=action)
        

        # print(f'action : {action}, highlight : {highlight}')
        frm = cv2.putText(frm,str(action),(100,100),1,3,(255,100,0),2)
        h, w, c = frm.shape
        frame[0:h, 0:w,:] = frm
        frm = frame
            
    cv2.namedWindow(title1, cv2.WINDOW_NORMAL)  
    cv2.setWindowProperty(title1, cv2.WND_PROP_TOPMOST, 1)
    cv2.imshow(title1, frm)
    key = cv2.waitKey(50)
    if key ==27:
        break
    # else:
    #     print(frame)

