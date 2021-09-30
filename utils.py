
import cv2
import time
import os,sys,glob
import hand_tracking_module as htm
import math
import numpy as np
from collections import Counter
import tkinter as tk

# UI 클래스
class UI:
    def __init__(self):
        # tkinter or Web 구현
        pass
    
# 백엔드 클래스
class Motion_Detect: #카메라로부터 데이터 받아서 동작과 연결
    def __init__(self):
        self.pre_state = "init"
        self.pre_coor = (0,0)
        self.ready_state = False
        self.state = None
        self.LIMIT_DISTANCE = 50
        self.w_diff_sum = 0
        self.h_diff_sum = 0
        self.highlight = False #하이라이트 저장 변수(이상철 추가) 
    
    def motion_to_action(self, state, coordinate,transaction=True):
        action=None
        # if A조건: A행동
        if self.pre_state =="init" and state == 'ready':
            self.ready_state = True
            self.pre_coor = coordinate
            self.pre_state = 'ready'
            action = "입력 대기 상태"
        elif state=="init":
            action = "입력종료"
            self.initiate(transaction)
        elif self.ready_state:
            if state == "move":
                w_diff = coordinate[0]-self.pre_coor[0]
                h_diff = coordinate[1]-self.pre_coor[1]
                if self.pre_coor==(0,0):
                    w_diff=0
                    h_diff=0
                self.w_diff_sum += w_diff
                # print(self.w_diff_sum)
                self.h_diff_sum += h_diff
                if abs(self.w_diff_sum) > self.LIMIT_DISTANCE:
                    if self.w_diff_sum > 0:
                        action = "좌측이동"
                    else:
                        action = "우측이동"
                    self.initiate(transaction)

                elif abs(self.h_diff_sum) > self.LIMIT_DISTANCE:
                    # 수직 이동 모드
                    if self.h_diff_sum > 0:
                        action = "아래이동"
                    else:
                        action = "위로이동"                
                    self.initiate(transaction)
                else:
                    action = None
                self.pre_coor = coordinate
            
            else:
                action=None
        else:
            action=None

        if state == 'highlight_on':
                self.highlight = True
        elif state == "highlight_off":
                self.highlight = False
        # peace 초기상태로
    # 어떤 알고리즘으로 연계되는 행동을 인식하여 반영할 것인지 고민 
        # print('action : %s, highlight : %s in motion_to_action'%( action, self.highlight))   
        if state =="finish":
            action =state
        return action, self.highlight
    def initiate(self, transaction):
        self.ready_state = False
        if transaction:
            self.pre_state ="init"
        self.w_diff_sum = 0
        self.h_diff_sum = 0
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
                    str([1,1,0,0,0]):"finish",
                    str([1,0,0,0,0]):"ready",
                    str([0,1,1,1,0]):"highlight_on",  #하이라이트 저장 변수(이상철 추가)
                    str([0,0,0,0,1]):"highlight_off",  #하이라이트 저장 변수(이상철 추가)
                    str([1,1,1,0,0]):"None",
                }

                state = action[str(fingers)] if str(fingers) in action.keys() else "Nothing"
                # h,w,c=overlayList[totalFingers].shape
                # img[0:h,0:w]=overlayList[totalFingers]

                cv2.rectangle(img,(20,225),(170,425),(0,255,0),cv2.FILLED)
                cv2.putText(img,state,(45,375),1,3,(255,100,0),2)
                cv2.putText(img,str(fingers),(45,275),1,3,(255,100,0),2)

            cTime=time.time()
            fps=1/(cTime-pTime)
            pTime=cTime
        return state, wrist

    # 안정적인 손가락 정보 인식 전달 목표
    # 손가락 이외의 기능 추가 여부 검토    

# Action 클래스# Action 클래스
class Action:
    orange, blue, cyan = (0, 165, 255), (255, 0, 0), (255, 255, 0)
    white, black = (255, 255, 255), (0, 0, 0) 
    path = None
    act= None
    direction= None         
    filenames = None
    idx = 0
    

    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    size = (screen_width, screen_height)    
            
    # image = np.full((300, 500, 3), white, np.uint8)             # 컬러 영상 생성 및 초기화
    image = None
     

    center = None         		# 영상의 중심 좌표
    pt1, pt2 = None, None
    shade = None                         # 그림자 좌표

    # cv2.circle(image, center, 100, blue)                         # 원 그리기 

    # cv2.circle(image, pt2   , 70 , cyan  , -1)                   # 원 내부 채움

    # font = cv2.FONT_HERSHEY_COMPLEX;
    # cv2.putText(image, "center_blue", center, font, 1.0, blue)
    # cv2.putText(image, "pt1_orange", pt1, font, 0.8, orange)
    # cv2.putText(image, "pt2_cyan",   shade, font, 1.2, black, 2)   # 그림자 효과
    # cv2.putText(image, "pt2_cyan",   pt2, font, 1.2, cyan , 1)

    multiple=2
    radius = 50*multiple 
    moving_dist = 50*multiple
    position = None
    oldposition = None
    color = white
    origin_image = None
       
    title = ['slideshow','spotlight']
    frm=None
    def __init__(self):
        Action.path = 'images'
        Action.act='slideshow'
        Action.direction='입력종료'
         
        Action.filenames = glob.glob(os.path.join(Action.path, "*"))
        print(Action.filenames)

        if not Action.filenames:
            print("There are no jpg files in 'images' folder")
            sys.exit()

        Action.idx = 0

            # image = np.full((300, 500, 3), white, np.uint8)             # 컬러 영상 생성 및 초기화
        Action.image = cv2.imread(Action.filenames[Action.idx])  # 영상 읽기
        if Action.image is None: raise Exception("영상파일 읽기 오류")

        center = (Action.image.shape[1]//2, Action.image.shape[0]//2)         		# 영상의 중심 좌표
        # pt1, pt2 = (300, 50), (100, 220)
        # shade = (pt2[0] + 2, pt2[1] + 2)   
        position = center
        oldposition = center

        
         # origin_image = copy.deepcopy(image)
        Action.origin_image =Action.image.copy()
    
    def action(self, act='slideshow', direction='입력종료'): # 이전 화면으로 전환
        self.direction=direction
        self.act=act
        if(act == 'slideshow'):
            try:
                cv2.destroyWindow(Action.title[1])
                # cv2.destroyAllWindows()
            except:
                pass
            # cv2.namedWindow(act, cv2.WINDOW_NORMAL)
            # cv2.imshow(act, Action.image)
            # cv2.setWindowProperty('Slideshow', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

            # h,w,c = img.shape    
            # prev_image = np.zeros((h, w, c), np.uint8)
            # print(h)
            # print(w)
            # print(c)

            # 이전 이미지 화면을 받기위한 빈공간 이미지 입력받기 

           

            # for i in range(101):
            #     alpha = i/100
            #     beta = 1.0 - alpha
            #     dst1 = cv2.addWeighted(img, alpha, prev_image, beta, 0.0)
            #     cv2.imshow("Slideshow", dst1)
                
            #     if cv2.waitKey(1) == ord('p'):
            #         break
            # prev_image = img

            if Action.image is None:
                print('Image load failed in action func')
                sys.exit()
            # key = cv2.waitKey(0) & 0xFF
            
            n=30
            if self.direction =="우측이동":
                img1 = cv2.imread(Action.filenames[Action.idx])
                img2 = cv2.imread(Action.filenames[Action.idx+1])
                
                #크기 변경
                dst1 = cv2.resize(img1, Action.size, 0,0,cv2.INTER_NEAREST) 
                dst2 = cv2.resize(img2, Action.size, 0,0,cv2.INTER_NEAREST) 
            
                h1, w1,c1 = dst1.shape
                h2, w2,c1 = dst2.shape
                frame = np.zeros((max(h1, h2),max(w1,w2),3), np.uint8)

                for i in range(1,n+1):
                    frame[:h1, :round(w1*(i)/n)] = dst1[:,:round(w1*(i)/n)] - np.array((-50,0,100), dtype=np.uint8) #############
                    frame[:h2, round(w1*(i)/n):round(w1*(i)/n)+round(w2*(n-i)/n)] = dst2[:,:round(w2*(n-i)/n)]
                    # cv2.imshow(Action.title[0],frame)                    
                    self.DoDisplay(Action.title[0],frame, False)                     
                    cv2.waitKey(50)
                Action.idx += 1
            elif self.direction =="좌측이동":
                img1 = cv2.imread(Action.filenames[Action.idx])
                img2 = cv2.imread(Action.filenames[Action.idx-1])
                
                #크기 변경
                dst1 = cv2.resize(img1, Action.size, 0,0,cv2.INTER_NEAREST) 
                dst2 = cv2.resize(img2, Action.size, 0,0,cv2.INTER_NEAREST) 
            
                h1, w1,c1 = dst1.shape
                h2, w2,c1 = dst2.shape
                frame = np.zeros((max(h1, h2),max(w1,w2),3), np.uint8)

                for i in range(1,n+1):
                    frame[:h1, :round(w1*(n-i)/n)] = dst1[:,:round(w1*(n-i)/n)]
                    frame[:h2, round(w1*(n-i)/n):round(w1*(n-i)/n)+round(w2*(i)/n)] = dst2[:,:round(w2*(i)/n)] - np.array((100,100,-50), dtype=np.uint8) #############
                    # cv2.imshow(Action.title[0],frame)                    
                    self.DoDisplay(Action.title[0],frame, False)                    
                    cv2.waitKey(50)
                Action.idx -= 1

            # elif self.direction =='입력종료' or key == 27:
            # elif key == 27:
            #     sys.exit()
            
            print('self.idx = ', Action.idx)
            Action.image = cv2.imread(Action.filenames[Action.idx])
            Action.origin_image=Action.image.copy()
            Action.position= (Action.image.shape[1]//2, Action.image.shape[0]//2)
            Action.oldposition = (Action.image.shape[1]//2, Action.image.shape[0]//2)         		# 영상의 중심 좌표
            cv2.namedWindow(Action.title[0], cv2.WINDOW_NORMAL) # WINDOW_NORMAL 로 만들어야 전체화면 가능

            # cv2.setWindowProperty 함수를 사용하여 속성 변경
            # cv2. WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN을 이용하여 전체화면 속성으로 변경
            cv2.setWindowProperty(Action.title[0], cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            # cv2.imshow(Action.title[0], Action.image)
            self.DoDisplay(Action.title[0], Action.image)

        elif act == 'spotlight':
            # print('spotlight is chosun') cv.WND_PROP_VISIBLE
            if cv2.getWindowProperty(Action.title[0],cv2.WND_PROP_VISIBLE):
                cv2.destroyWindow(Action.title[0]) 
                # cv2.destroyAllWindows()
            
            msk = np.zeros_like(Action.image)
 

            # masked2 = cv2.bitwise_not(cv2.bitwise_and(dst,msk))

            # dst2 = cv2.copyTo(src, msk,dst)
            cv2.namedWindow(Action.title[1], cv2.WINDOW_NORMAL) # WINDOW_NORMAL 로 만들어야 전체화면 가능

            # cv2.setWindowProperty 함수를 사용하여 속성 변경
            # cv2. WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN을 이용하여 전체화면 속성으로 변경
            cv2.setWindowProperty(Action.title[1], cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.circle(msk, Action.position   ,Action.radius , Action.color, -1)  
            alpha = 0.9
            beta=0.5   
             
            inversed = ~msk # 반전
            frame_msk = cv2.bitwise_and(Action.image,msk)
            frame_inversed = cv2.bitwise_and(Action.image,inversed)
            # frame_inversed = int(frame_inversed/2)
            frame = cv2.add(frame_msk*alpha, frame_inversed*beta)
            # frame = cv2.add(frame_msk, frame_inversed)
            frame = np.clip(frame, 0,255).astype('uint8')
                        
            # cv2.imshow(Action.title[1], frame)
            self.DoDisplay(Action.title[1], frame)
            
            
            if self.direction =="위로이동": #up
                print('up')
                move = Action.oldposition[1]-Action.moving_dist
                print('moveup :', move)
                if move <=Action.radius:
                    print('move beyond 0')
                    move = Action.radius
                Action.position = (Action.oldposition[0], move)
            elif self.direction =="우측이동": #right
                print('right')
                move = Action.oldposition[0]+Action.moving_dist
                print('moveright :', move)
                if move >=Action.image.shape[1]-Action.radius:
                    print('move beyond image.shape[1]-radius')
                    move = Action.image.shape[1]-Action.radius
                Action.position = (move, Action.oldposition[1]) 
            elif self.direction =='아래이동': #down
                print('down')
                move = Action.oldposition[1]+Action.moving_dist
                print('movedown :', move)
                if move >=Action.image.shape[0]-Action.radius:
                    print('move beyond image.shape[0]-radius')
                    move = Action.image.shape[0]-Action.radius
                Action.position = (Action.oldposition[0], move)
            elif self.direction =='좌측이동': #left
                print('left')
                move = Action.oldposition[0]-Action.moving_dist
                print('moveleft :', move)
                if move <=Action.radius:
                    print('move left beyond 0')
                    move = Action.radius
                Action.position = (move, Action.oldposition[1])
            if self.direction != None and self.direction.find('입력') == -1:
                print('self.direction', self.direction)
                Action.oldposition =Action.position
                # image = copy.deepcopy(origin_image)
                Action.image =  Action.origin_image.copy()

    def ReceiveFrame(self, frm):
        Action.frm=frm

    def DoDisplay(self, title, frame, show=True):############
        
        h,w,_ = Action.frm.shape
        dst1 = cv2.resize(frame, Action.size, 0,0,cv2.INTER_NEAREST) 
        if show:
            frH, frW, _ = dst1.shape
            dst1[round(frH-h):,round(frW-w):] =Action.frm[:,:]
        cv2.imshow(title, dst1)  


    # 다양한 프로그램 연결이 가능하도록 구성
    
class Action_ppt:
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
    # print(f'pt_a : {pt_a}, pt_b :{pt_b}, cos_theta : {cos_theta}')
    area = mag(pt_a)*mag(pt_b)*math.sin(math.acos(cos_theta))*0.5
    return area

def img_multi_detection(func, frame):    
    # hsv
    src_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_planes = cv2.split(src_hsv)
    hsv_planes[2] = cv2.equalizeHist(hsv_planes[2])
    dst_hsv = cv2.merge(hsv_planes)
    dst_h = cv2.cvtColor(dst_hsv, cv2.COLOR_HSV2BGR)
    state, coordinate = get_data.state_update(frame)

    action, highlight = func(state, coordinate)


# 인식 정확도 개선을 위한 앙상블 알고리즘 적용
class Ensemble:
    def __init__(self, limit_num):
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
    def get_ensemble_result(self, datas):
        cnt = Counter(datas)
        mode = cnt.most_common(2)
        print(mode)
        if mode[0][0] == None and len(mode)>1:
            return mode[1][0]
        return mode[0][0] # 최빈값 리턴
    def initialize(self):
        self.data_pack = list()
