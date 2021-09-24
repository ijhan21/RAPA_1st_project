import cv2
import glob
import os
import numpy as np

def process():
    path = "pp"
    filenames = glob.glob(os.path.join(path, "*"))

    prev_image = np.zeros((500, 500, 3), np.uint8)
    for filename in filenames:
        print(filename)
        img = cv2.imread(filename)

        height, width, _ = img.shape
        if width < height:
            height = int(height*1000/width)
            width = 1000
            img = cv2.resize(img, (width, height))
            shift = height - 1000
            img = img[shift//2:-shift//2,:,:]
        else:
            width = int(width*1000/height)
            height = 1000
            shift = width - 1000
            img = cv2.resize(img, (width, height))
            img = img[:,shift//2:-shift//2,:]

        for i in range(101):
            alpha = i/100
            beta = 1.0 - alpha
            dst = cv2.addWeighted(img, alpha, prev_image, beta, 0.0)

            cv2.imshow("Slideshow", dst)
            if cv2.waitKey(1) == ord('q'):
                return

        prev_image = img

        if cv2.waitKey(1000) == ord('q'):
            return

process()