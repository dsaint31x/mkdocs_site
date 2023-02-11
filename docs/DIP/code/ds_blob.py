import cv2
import numpy as np
import os

path_by_file = os.path.realpath(__file__)
img_path = os.path.dirname(path_by_file)
img = cv2.imread(os.path.join(img_path,"../img/ch02/blob.jpg"))
img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)



params = cv2.SimpleBlobDetector_Params()

print(params.minThreshold, params.maxThreshold)

# Change thresholds
print('minThreshold:',params.minThreshold)
print('maxThreshold:',params.maxThreshold)
params.minThreshold = 10;  # 50. #default
params.maxThreshold = 250; #220. #default
 
# Filter by Area.
params.filterByArea = False #True
params.minArea = 1500
 
# Filter by Circularity
params.filterByCircularity = False #True
params.minCircularity = 0.1
 
# Filter by Convexity
print('filter by Convexity:',params.filterByConvexity)
print('minConvexity:',params.minConvexity)
print('maxConvexity:',params.maxConvexity)
params.filterByConvexity = False # True #default
params.minConvexity = 0.6 # .95 # default #0.86, 0.89, 0.96
params.maxConvexity = 1. 
 
# Filter by Inertia
print('filter by Inertia:', params.filterByInertia)
print('minInertiaRatio:',params.minInertiaRatio) 
print('maxInertiaRatio:',params.maxInertiaRatio) 
params.filterByInertia = True # True
params.minInertiaRatio = .01 # .1 # default
params.maxInertiaRatio = 1. # .1 # default


# Blob Detector 생성
ver = (cv2.__version__).split('.')
if int(ver[0]) < 3 :
  detector = cv2.SimpleBlobDetector(params)
else : 
  detector = cv2.SimpleBlobDetector_create(params)
  

key_points = detector.detect(img_g)
img = cv2.drawKeypoints (img_g, key_points, 
                         None, (0,0,255), 
                        #  flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
                         flags = cv2.DRAW_MATCHES_FLAGS_DEFAULT,
                         )

for k in key_points:
    print("===============")
    print('pt:      ',k.pt)
    print('size:    ',k.size)
    print('angle:   ',k.angle)
    print('response:',k.response)
    print('octave:  ',k.octave)
    print('class_id:',k.class_id)

cv2.imshow("blob", img)
cv2.waitKey()

