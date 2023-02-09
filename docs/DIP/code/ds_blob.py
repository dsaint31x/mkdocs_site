import cv2
import numpy as np
import os

path_by_file = os.path.realpath(__file__)
img_path = os.path.dirname(path_by_file)
img = cv2.imread(os.path.join(img_path,"../img/ch02/blob.jpg"))
img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# Blob Detector 생성
detector = cv2.SimpleBlobDetector_create()

key_points = detector.detect(img_g)

img = cv2.drawKeypoints (img, key_points, None, (0,0,255), flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.imshow("blob", img)
cv2.waitKey()

