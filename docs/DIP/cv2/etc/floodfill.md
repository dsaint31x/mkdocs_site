# cv2.floodfill

연결된 component를 `newVal`에 해당하는 새로운 color (or intensity)로 채우는 함수.

```Python
num_pixels, ret_img, ret_mask,ret_rect = cv2.floodFill(
        image,     # input image
        mask,      # uint8 mask, image보다 2pixel씩 width, height가 커야함.
        seedPoint, # starting point
        newVal,    # 채워질 color
        loDiff,    # 같은 component로 인식하기 위한 아래쪽 차이.
        upDiff,    # 같은 component로 인식하기 위한 위쪽 차이. 
        flags      # floodfill의 동작모드를 결정하는 flag
)
``` 

**Returned Values**

* `num_pixels` : 채우기가 적용된 pixel들의 수.
* `ret_img` : 결과 image (h x w x c) = `image`
* `ret_mask`: 결과 mask  ( h+2 x w+2) = `mask`

**Parameters**

* `loDiff` : 생략되는 경우, 0이 주어진 것으로 아래쪽으로 차이가 없어야 함. (즉 이웃 pixel의 값이 `loDiff`를 뺀 경우보다는 크거나 같아야함.)
* `upDiff` : 생략되는 경우, 0이 주어진 것으로 위쪽으로 차이가 없어야 함. (즉 이웃 pixel의 값이 `upDiff`를 더한 경우보다는 작거나 같아야함.)
* `mask` : None인 경우 모든 image 영역에 대해 처리가 이루어짐. 주어질 경우, mask에서 0이 아닌 pixel을 만나게 될 경우, 채우기가 더이상 진행되지 않음(즉, 채워질 최대 영역을 제한함)
* `flags` : 초기 8bit는 connectivity를 결정하는 수로, `4`가 default로 four-nearest neighbor로 동작하며, `8`인 경우 eight-nearest neighbor로 동작한다. 그다음 8bit는 1~255의 값중 하나가 되며 `ret_mask`에서 새로 채워넣을 값에 해당 (`ret_img`에서의 `newVal`의 관계와 같음)한다. 기본값은 `1`임. `4+(255<<9)`인 경우, four-nearest neighbor이면서 `255`로 채워진 mask를 반환한다.
    * `cv2.FLOODFILL_MASK_ONLY` : mask에만 채우기 수행.
    * `cv2.FLOODFILL_FIXED_RANGE` : 이웃한 pixel간의 차이로 connected component인지를 결정하지 않고, seed point의 pixel과의 비교로 connected component를 결정.

다음은 `flags`를 설정하는 방법에 대한 예제 코드임.

```Python
```

## Example

```Python
import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('../images/taekwonv1.jpg')
rows, cols = img.shape[:2]
# 마스크 생성, 원래 이미지 보다 2픽셀 크게
mask = np.zeros((rows+2, cols+2), np.uint8)
# 채우기에 사용할 색
newVal = (255,255,255)
# 연결될 component를 결정하기 위한 최대 차이 값 (아래쪽, 위쪽)
loDiff, upDiff = (10,10,10), (10,10,10)

# 마우스 이벤트 처리 함수
def onMouse(event, x, y, flags, param):
    global mask, img
    if event == cv2.EVENT_LBUTTONDOWN:
        seed = (x,y)
        # 색 채우기 적용 
        retval = cv2.floodFill(img, mask, seed, newVal, loDiff, upDiff)
        
        # 채우기 변경 결과 표시 
        cv2.imshow('img', img)
        
        print(f'num of pixels changed : {retval[0]}')
        print(f'shape of the changed img : {retval[1].shape}')
        print(f'shape of the returned mask : {retval[2].shape}')
        
        plt.imshow(retval[2],cmap='gray')
        plt.show()
        print(f'returned rectanble : {retval[3]}')

# 화면 출력
cv2.imshow('img', img)
cv2.setMouseCallback('img', onMouse)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

## References

* [OpenCV's Document](https://docs.opencv.org/4.x/d7/d1b/group__imgproc__misc.html#ga366aae45a6c1289b341d140839f18717)