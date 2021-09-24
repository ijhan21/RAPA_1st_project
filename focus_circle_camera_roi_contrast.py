import numpy as np
import cv2,copy
 

orange, blue, cyan = (0, 165, 255), (255, 0, 0), (255, 255, 0)
white, black = (255, 255, 255), (0, 0, 0)         
# image = np.full((300, 500, 3), white, np.uint8)             # 컬러 영상 생성 및 초기화
# image = cv2.imread("../images/sunflower.jpg")  # 영상 읽기
# if image is None: raise Exception("영상파일 읽기 오류")

# cap = cv2.VideoCapture(mov) # 비디오 열기
cap = cv2.VideoCapture(0)

# fps = round(cap.get(cv2.CAP_PROP_FPS))
# delay = round(1000 / fps)
    
        

     		# 영상의 중심 좌표
# pt1, pt2 = (300, 50), (100, 220)
# shade = (pt2[0] + 2, pt2[1] + 2)                          # 그림자 좌표

# cv2.circle(image, center, 100, blue)                         # 원 그리기 

# cv2.circle(image, pt2   , 70 , cyan  , -1)                   # 원 내부 채움

# font = cv2.FONT_HERSHEY_COMPLEX;
# cv2.putText(image, "center_blue", center, font, 1.0, blue)
# cv2.putText(image, "pt1_orange", pt1, font, 0.8, orange)
# cv2.putText(image, "pt2_cyan",   shade, font, 1.2, black, 2)   # 그림자 효과
# cv2.putText(image, "pt2_cyan",   pt2, font, 1.2, cyan , 1)

ret, frame = cap.read()
        # print('ret : ', ret)
        
if ret == False:
    print('first frame open error')
   
center = (frame.shape[1]//2, frame.shape[0]//2)  
radius = 100 
moving_dist = 10
position = center
oldposition = center
color = white
# origin_image = copy.deepcopy(image)
# origin_image = frame.copy()
while True:
    ret, frame = cap.read()
        # print('ret : ', ret)
        
    if ret ==False:
        print('frame open error')
        break
    msk = np.zeros_like(frame)
 

# masked2 = cv2.bitwise_not(cv2.bitwise_and(dst,msk))

    # dst2 = cv2.copyTo(src, msk,dst)
    alpha = 0.9
    beta=0.5   
    cv2.circle(msk, position   ,radius , color, -1)
    inversed = ~msk # 반전
    frame_msk = cv2.bitwise_and(frame,msk)
    frame_inversed = cv2.bitwise_and(frame,inversed)
    # frame_inversed = int(frame_inversed/2)
    frame = cv2.add(frame_msk*alpha, frame_inversed*beta)
    # frame = cv2.add(frame_msk, frame_inversed)
    frame = np.clip(frame, 0,255).astype('uint8')
    title = "Draw circles"
    cv2.namedWindow(title)
    cv2.imshow(title, frame)
    key = cv2.waitKeyEx(100)
    print(f'key: {key}')
    if key == 27:  #esc
        print('esc key pressed')
        break
    elif key == 2490368: #up
        print('up')
        move = oldposition[1]-moving_dist
        print('moveup :', move)
        if move <=radius:
            print('move beyond 0')
            move = radius
        position = (oldposition[0], move)
    elif key == 2555904: #right
        print('right')
        move = oldposition[0]+moving_dist
        print('moveright :', move)
        if move >=frame.shape[1]-radius:
            print('move beyond image.shape[1]-radius')
            move = frame.shape[1]-radius
        position = (move, oldposition[1]) 
    elif key == 2621440: #down
        print('down')
        move = oldposition[1]+moving_dist
        print('movedown :', move)
        if move >=frame.shape[0]-radius:
            print('move beyond image.shape[0]-radius')
            move = frame.shape[0]-radius
        position = (oldposition[0], move)
    elif key == 2424832: #left
        print('left')
        move = oldposition[0]-moving_dist
        print('moveleft :', move)
        if move <=radius:
            print('move left beyond 0')
            move = radius
        position = (move, oldposition[1])
    if key != -1:
        oldposition =position
        # image = copy.deepcopy(origin_image)
        # image =  origin_image.copy()
cap.release()
cv2.destroyAllWindows()


        