import numpy as np
import cv2,copy
 

orange, blue, cyan = (0, 165, 255), (255, 0, 0), (255, 255, 0)
white, black = (255, 255, 255), (0, 0, 0)         
# image = np.full((300, 500, 3), white, np.uint8)             # 컬러 영상 생성 및 초기화
image = cv2.imread("../images/sunflower.jpg")  # 영상 읽기
if image is None: raise Exception("영상파일 읽기 오류")

center = (image.shape[1]//2, image.shape[0]//2)         		# 영상의 중심 좌표
pt1, pt2 = (300, 50), (100, 220)
shade = (pt2[0] + 2, pt2[1] + 2)                          # 그림자 좌표

# cv2.circle(image, center, 100, blue)                         # 원 그리기 

# cv2.circle(image, pt2   , 70 , cyan  , -1)                   # 원 내부 채움

# font = cv2.FONT_HERSHEY_COMPLEX;
# cv2.putText(image, "center_blue", center, font, 1.0, blue)
# cv2.putText(image, "pt1_orange", pt1, font, 0.8, orange)
# cv2.putText(image, "pt2_cyan",   shade, font, 1.2, black, 2)   # 그림자 효과
# cv2.putText(image, "pt2_cyan",   pt2, font, 1.2, cyan , 1)

 
radius = 50 
moving_dist = 10
position = center
oldposition = center
color = orange
# origin_image = copy.deepcopy(image)
origin_image = image.copy()
while True: 
    cv2.circle(image, position   ,radius , color, 2)
    title = "Draw circles"
    cv2.namedWindow(title)
    cv2.imshow(title, image)
    key = cv2.waitKeyEx(1000)
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
        if move >=image.shape[1]-radius:
            print('move beyond image.shape[1]-radius')
            move = image.shape[1]-radius
        position = (move, oldposition[1]) 
    elif key == 2621440: #down
        print('down')
        move = oldposition[1]+moving_dist
        print('movedown :', move)
        if move >=image.shape[0]-radius:
            print('move beyond image.shape[0]-radius')
            move = image.shape[0]-radius
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
        image =  origin_image.copy()
cv2.destroyAllWindows()


        