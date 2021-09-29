import cv2
import time
import os
import hand_tracking_module as htm
import math
import numpy as np
from collections import Counter

# UI 클래스
class UI:
    def __init__(self):
        # tkinter or Web 구현
        pass
    
# 백엔드 클래스
class Motion_Detect: #카메라로부터 데이터 받아서 동작과 연결
    def __init__(self):
        self.pre_state = "init"
        self.pre_action =""
        self.pre_coor = (0,0)
        self.ready_state = False
        self.state = None
        self.LIMIT_DATA_LEN =80
        self.LIMIT_DISTANCE = 50
        self.w_diff_sum = list()
        self.h_diff_sum = list()   
        self.ensemble = self.Ensemble(limit_num = 5)
    # 인식 정확도 개선을 위한 앙상블 알고리즘 적용
    class Ensemble:
        def __init__(self, limit_num) -> None:
            self.data_pack = list()            
            self.limit_num = limit_num
        def update(self, new_data):
            self.data_pack.append(new_data)
            if len(self.data_pack)>self.limit_num:
                self.data_pack.pop(0)
            # 최빈값 받아오기
            cnt = Counter(self.data_pack)
            mode = cnt.most_common(1)
            return mode[0][0] # 최빈값 리턴
        def initialize(self):
            self.data_pack = list()
        
    def motion_to_action(self, state, coordinate,transaction=True):
        # if A조건: A행동
        # if self.pre_state =="init" and state == 'ready':
        if state == 'ready':
            self.ready_state = True
            self.pre_coor = coordinate
            self.pre_state = 'ready'
            action = "입력 대기 상태"
            self.w_diff_sum =list()
            self.h_diff_sum =list()
            # self.initiate(transaction)

        elif state=="init":
            action = "입력 종료"
            self.initiate(transaction=True)
            self.ready_state = False

        elif self.ready_state:
            if state == "move":
                # print("move 대기")
                w_diff = coordinate[0]-self.pre_coor[0]
                h_diff = coordinate[1]-self.pre_coor[1]
                if self.pre_coor==(0,0):
                    w_diff=0
                    h_diff=0                
                self.w_diff_sum.append(w_diff)
                self.h_diff_sum.append(h_diff)

                if len(self.w_diff_sum)>self.LIMIT_DATA_LEN:
                    self.w_diff_sum.pop(0)
                w_diff_sum_tmp = np.sum(self.w_diff_sum)
                if len(self.h_diff_sum)>self.LIMIT_DATA_LEN:
                    self.h_diff_sum.pop(0)
                h_diff_sum_tmp = np.sum(self.h_diff_sum)                    

                if abs(w_diff_sum_tmp) > self.LIMIT_DISTANCE:
                    if w_diff_sum_tmp > 0:
                        action = "좌측이동"
                    else:
                        action = "우측이동"
                    # if transaction:
                    #     self.ready_state = False
                    # self.initiate(transaction)

                elif abs(h_diff_sum_tmp) > self.LIMIT_DISTANCE:
                    # 수직 이동 모드
                    if h_diff_sum_tmp > 0:
                        action = "아래이동"
                    else:
                        action = "위로이동"                
                    # if transaction:
                    #     self.ready_state = False
                else:
                    action = None
                self.pre_coor = coordinate
            else:action=None
        else:
            action=None
        # peace 초기상태로
        # 어떤 알고리즘으로 연계되는 행동을 인식하여 반영할 것인지 고민    
        ensemble_action = self.ensemble.update(action)
        if transaction and self.pre_action != ensemble_action and ensemble_action in ['아래이동',"위로이동","좌측이동","우측이동"]:
            print('check', state)
            self.ready_state = False
            self.ensemble.initialize()
            # self.initiate(transaction=True)
        self.pre_action = ensemble_action
        return ensemble_action

    def initiate(self, transaction):
        self.ready_state = False
        if transaction:
            self.pre_state ="init"
            self.ready_state = False
            
        self.w_diff_sum = list()
        self.h_diff_sum = list()
        self.pre_coor = (0,0)
class GetData:
    def __init__(self):               
        # 데이터 수집        
        self.detector=htm.handDetector(detectionCon=0.75)
        # self.detector=htm.handDetector(detectionCon=0.2,trackCon=0.3)
        self.tipIds=[4,8,12,16,20,0]

        self.state = None
        self.coordinate = 0,0

    def state_update(self, frame):
        pTime=0
        img=self.detector.findHands(frame)
        lmList=self.detector.findPosition(img,draw=False)
        state = None
        wrist = None
        if lmList:
            thumb =(lmList[self.tipIds[0]][1],lmList[self.tipIds[0]][2],lmList[self.tipIds[0] - 2][1],lmList[self.tipIds[0] - 2][2])
            index =(lmList[self.tipIds[1]][1],lmList[self.tipIds[1]][2],lmList[self.tipIds[1] - 2][1],lmList[self.tipIds[1] - 2][2])
            middle=(lmList[self.tipIds[2]][1],lmList[self.tipIds[2]][2],lmList[self.tipIds[2] - 2][1],lmList[self.tipIds[2] - 2][2])
            ring  =(lmList[self.tipIds[3]][1],lmList[self.tipIds[3]][2],lmList[self.tipIds[3] - 2][1],lmList[self.tipIds[3] - 2][2])
            pinky =(lmList[self.tipIds[4]][1],lmList[self.tipIds[4]][2],lmList[self.tipIds[4] - 2][1],lmList[self.tipIds[4] - 2][2])
            wrist =(lmList[self.tipIds[5]][1],lmList[self.tipIds[5]][2])

            #엄지손가락 인식을 위한 삼각형 알고리즘
            pt1 = wrist
            pt2 = (lmList[self.tipIds[0] - 2][1],lmList[self.tipIds[0] - 2][2])
            pt3 = (lmList[self.tipIds[1] - 3][1],lmList[self.tipIds[1] - 3][2])
            area = tri_area(pt1, pt2, pt3)

            # Compare Tri
            pt1 = (lmList[self.tipIds[0]][1],lmList[self.tipIds[0]][2])
            pt2 = (lmList[self.tipIds[0] - 2][1],lmList[self.tipIds[0] - 2][2])
            pt3 = lmList[self.tipIds[4] - 2][1],lmList[self.tipIds[4] - 2][2]
            area_compare = tri_area(pt1, pt2, pt3)
            area_rate = area/area_compare
            # print(round(area/area_compare,2)) #area, area_compare, 

            finger_list = [thumb, index, middle, ring, pinky]
            
            if len(lmList) !=0:
                fingers=[]
                for i in range(5):
                    if i ==0:
                        if area_rate < 1:
                            fingers.append(1)
                        else:fingers.append(0)
                    else:
                        if distance(finger_list[i][:2], wrist) > distance(finger_list[i][2:], wrist):
                            fingers.append(1)
                        else:
                            fingers.append(0)

                # totalFingers=fingers.count(1)
                # print(totalFingers)
                action = {
                    str([1,1,0,0,1]):"init",
                    str([1,1,1,1,1]):"move",
                    str([1,1,0,0,0]):"choise",
                    str([1,0,0,0,0]):"ready",
                    str([1,1,1,0,0]):"None",
                }

                state = action[str(fingers)] if str(fingers) in action.keys() else "Nothing"
                # h,w,c=overlayList[totalFingers].shape
                # img[0:h,0:w]=overlayList[totalFingers]

                cv2.rectangle(img,(20,225),(170,425),(0,255,0),cv2.FILLED)
                cv2.putText(img,state,(45,375),1,3,(255,100,0),2)
                cv2.putText(img,str(fingers),(45,275),1,3,(255,100,0),2)

            frame = img # 불분명한 코드 수정

            cTime=time.time()
            fps=1/(cTime-pTime)
            pTime=cTime
        return state, wrist, frame

    # 안정적인 손가락 정보 인식 전달 목표
    # 손가락 이외의 기능 추가 여부 검토    

# Action 클래스
class Action:
    def __init__(self):
        # ppt 초기화
        # ppt 관련 행동 정의
        pass
    
    def action_left(self): # 이전 화면으로 전환
        raise NotImplementedError
    def action_move_next(self): # 다음 화면으로 전환
        raise NotImplementedError

    # 다양한 프로그램 연결이 가능하도록 구성
    
class Action_ppt(Action):
    def __init__(self):
        super().__init__()
        pass

def distance(pt1, pt2):
    a = pt1[0]-pt2[0]    # 선 a의 길이
    b = pt1[1]-pt2[1]    # 선 b의 길이 
    c = math.sqrt((a * a) + (b * b))
    return c

# 요소의 squre root
def mag(x): 
    return math.sqrt(sum(i**2 for i in x))

# 엄지손가락 인식 개선을 위한 삼각형 넓이 알고리즘
def tri_area(pt1, pt2, pt3):
    pt1 = np.array(pt1)
    pt2 = np.array(pt2)
    pt3 = np.array(pt3)
    pt_a = pt2-pt1
    pt_b = pt3-pt1
    cos_theta = (np.dot(pt_a, pt_b))/(mag(pt_a)*mag(pt_b))
    area = mag(pt_a)*mag(pt_b)*math.sin(math.acos(cos_theta))*0.5
    return area