from utils import *
import time
import cv2
import tkinter as tk
import win32com.client
import sys

tts = win32com.client.Dispatch("SAPI.SpVoice")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cap = cv2.VideoCapture(r'C:\python\rapa\opencv_class\videos\robot.mp4')

get_data = GetData()
motion_detect = Motion_Detect()
actionInstance = Action()
title = 'webcam'
ensemble = Ensemble(3)
while True:
    ret, frame = cap.read()
    action_list = list()
    highlight_list = list()
    if ret:       

        ### HSV YCrCb 인식 기능 추가        
        state, coordinate = get_data.state_update(frame)
        action, highlight = motion_detect.motion_to_action(state, coordinate)
        action_list.append(action)
        highlight_list.append(highlight)

        # HSV
        src_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv_planes = cv2.split(src_hsv)
        hsv_planes[2] = cv2.equalizeHist(hsv_planes[2])
        dst_hsv = cv2.merge(hsv_planes)
        dst_h = cv2.cvtColor(dst_hsv, cv2.COLOR_HSV2BGR)
        state, coordinate = get_data.state_update(dst_h)
        action, highlight = motion_detect.motion_to_action(state, coordinate)
        action_list.append(action)
        highlight_list.append(highlight)

        #Ycrcb
        src_ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
        ycrcb_planes = cv2.split(src_ycrcb)
        ycrcb_planes[0] = cv2.equalizeHist(ycrcb_planes[0])
        dst_ycrcb = cv2.merge(ycrcb_planes)
        dst = cv2.cvtColor(dst_ycrcb, cv2.COLOR_YCrCb2BGR)
        state, coordinate = get_data.state_update(dst)
        action, highlight = motion_detect.motion_to_action(state, coordinate)
        action_list.append(action)
        highlight_list.append(highlight)

        action = ensemble.get_ensemble_result(action_list)
        highlight = ensemble.get_ensemble_result(highlight_list)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",action)
        if action =="finish":        
            tts.Speak("감사합니다")
            sys.exit()

        #########################################################################################

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

