import cv2
import time
import os
import hand_tracking_module as htm
import math

def distance(pt1, pt2):
    a = pt1[0]-pt2[0]    # 선 a의 길이
    b = pt1[1]-pt2[1]    # 선 b의 길이 
    c = math.sqrt((a * a) + (b * b))
    return c

cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)


# path="finger"
# myList=os.listdir(path)
# overlayList=[]

# for impath in myList:
#     image=cv2.imread(f'{path}/{impath}')
#     overlayList.append(image)
pTime=0

detector=htm.handDetector(detectionCon=0.75)
tipIds=[4,8,12,16,20,0]
while True:
    success,img=cap.read()
    if success:
        img=detector.findHands(img)
        # cv2.imshow("ImageAfterDectector",img)
        lmList=detector.findPosition(img,draw=False)

        # print('lmList:', lmList)
        if lmList:
            thumb =(lmList[tipIds[0]][1],lmList[tipIds[0]][2],lmList[tipIds[0] - 2][1],lmList[tipIds[0] - 2][2])
            index =(lmList[tipIds[1]][1],lmList[tipIds[1]][2],lmList[tipIds[1] - 2][1],lmList[tipIds[1] - 2][2])
            middle=(lmList[tipIds[2]][1],lmList[tipIds[2]][2],lmList[tipIds[2] - 2][1],lmList[tipIds[2] - 2][2])
            ring  =(lmList[tipIds[3]][1],lmList[tipIds[3]][2],lmList[tipIds[3] - 2][1],lmList[tipIds[3] - 2][2])
            pinky =(lmList[tipIds[4]][1],lmList[tipIds[4]][2],lmList[tipIds[4] - 2][1],lmList[tipIds[4] - 2][2])
            wrist =(lmList[tipIds[5]][1],lmList[tipIds[5]][2])

            finger_list = [thumb, index, middle, ring, pinky]
            
            if len(lmList) !=0:
                fingers=[]
                for i in range(5):
                    if i ==0 and (distance(finger_list[i][:2], [lmList[tipIds[3] - 3][1],lmList[tipIds[3] - 3][2]]) > distance(finger_list[i][2:], [lmList[tipIds[2] - 3][1],lmList[tipIds[2] - 3][2]]) or \
                        distance(finger_list[i][:2],index[2:]) > distance(finger_list[i][2:], index[2:])): # 엄지손가락일경우는 새끼손가락과의 거리로 계산
                        fingers.append(1)
                    elif distance(finger_list[i][:2], wrist) > distance(finger_list[i][2:], wrist):
                        fingers.append(1)
                    else:
                        fingers.append(0)

                # totalFingers=fingers.count(1)
                # print(totalFingers)
                action = {
                    str([1,1,0,0,1]):"peace",
                    str([1,1,0,0,0]):"Babo",
                    str([1,1,1,0,0]):"Victory",
                    str([1,1,1,1,1]):"Perfect"

                }

                txt = action[str(fingers)] if str(fingers) in action.keys() else "Nothing"
                # h,w,c=overlayList[totalFingers].shape
                # img[0:h,0:w]=overlayList[totalFingers]

                cv2.rectangle(img,(20,225),(170,425),(0,255,0),cv2.FILLED)
                cv2.putText(img,txt,(45,375),1,3,(255,100,0),2)
                cv2.putText(img,str(fingers),(45,275),1,3,(255,100,0),2)

            cTime=time.time()
            fps=1/(cTime-pTime)
            pTime=cTime

            cv2.putText(img,f'index x,y: ({wrist[0]},{wrist[1]})',(200,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("Image",img)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()