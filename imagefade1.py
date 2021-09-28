import cv2
import glob
import os
import numpy as np
import sys

def process():
    path = "pp"
    filenames = glob.glob(os.path.join(path, "*"))

    if not filenames:
        print("There are no jpg files in 'images' folder")
        sys.exit()

    idx = 0
    while True:
        img = cv2.imread(filenames[idx])
        cv2.namedWindow('Slideshow', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('Slideshow', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        h,w,c = img.shape    
        prev_image = np.zeros((h, w, c), np.uint8)
        print(h)
        print(w)
        print(c)

        # 이전 이미지 화면을 받기위한 빈공간 이미지 입력받기 

        cv2.imshow("Slideshow", img)

        for i in range(101):
            alpha = i/100
            beta = 1.0 - alpha
            dst1 = cv2.addWeighted(img, alpha, prev_image, beta, 0.0)
            cv2.imshow("Slideshow", dst1)
            
            if cv2.waitKey(1) == ord('p'):
                break
        prev_image = img

        if img is None:
            print('Image load failed!')
            break
        key = cv2.waitKey(0) & 0xFF
        
        if key == ord('d'):
            idx += 1
        elif key == ord('a'):
            idx -= 1
        elif key == ord('q') or key == 27:
            break


process()