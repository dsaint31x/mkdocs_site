# Color Space (Simple Version)

Color space에 대한 보다 자세한 내용은 다음 URL을 참고할 것 : [[DIP] Color Space or Color Model](https://dsaint31.tistory.com/348)

---

---

## Gray-scale

모든 색이 단일 채널에 의해 표현된다.

* `0` : black
* `max` : white (`1.` or `255`)

> intensity (or brightness) : pixel의 value임.

다음 코드로 일부 영역을 확대해서 표시하는 방법을 보임.

* `seaborn` 라이브러리를 이용.


```Python
import cv2
from skimage import data

#from skimage.color import rgb2gray

from skimage import img_as_ubyte,img_as_float
import matplotlib.pyplot as plt
import seaborn as sns

cat = data.chelsea() # take the test image of cat!

cat_cv   = cv2.cvtColor(cat,cv2.COLOR_RGB2BGR)
gray_cat = cv2.cvtColor(cat,cv2.COLOR_RGB2GRAY)

print(gray_cat.dtype)

plt.figure(figsize=(12,12))
sns.heatmap(gray_cat[:15, :15], annot=True, fmt="d", cmap=plt.cm.bone)
plt.axis("off")
plt.show()
```

* $15 \times 15$ 크기의 왼쪽 상단 patch를 크게 보여줌. 
* pixel intensity를 같이 숫자로 보여준다. `sns.heatmap`의 유용함을 확인 가능함.

---

### Note : URL에서 이미지 로드.

```Python
import requests
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('./tmp',exist_ok=True)
#alpha file
url = 'https://raw.githubusercontent.com/dsaint31x/OpenCV_Python_Tutorial/master/DIP/img/opencv_logo.png'

image_ndarray = np.asarray(bytearray(requests.get(url).content), dtype=np.uint8)
img = cv2.imdecode(image_ndarray, cv2.IMREAD_UNCHANGED)
cv2.imwrite('./tmp/opencv_logo.png', img)
```

---

---

## BGRA

BGRA의 경우, `cv2.imread`에서의 mode의 차이를 확인할 수 있다.

* 기본은 `cv2.IMREAD_COLOR`인 점을 잊지 말 것.

아래그림에서 검은색 글자의 출력이 어떻게 보이는지를 확인할 것!!

* `matplotlib`를 사용하는 경우 alpha channel이 있는 경우 고려를 잘 해야함.

```Python
import numpy as np
import matplotlib.pyplot as plt
import cv2

import os

img_path = './tmp/'
fstr = 'opencv_logo.png' 
fstr = os.path.join(img_path,fstr)


img = cv2.imread(fstr) # BGR (default)
img_bgr = cv2.imread(fstr, cv2.IMREAD_COLOR)      # BGR
img_bgra = cv2.imread(fstr, cv2.IMREAD_UNCHANGED) # BGRA

print(f'default:{img.shape}/imread_color:{img_bgr.shape}/imread_unchanged:{img_bgra.shape}')
print(f'range of alpha channel : [{np.min(img_bgra[:,:,-1])},{np.max(img_bgra[:,:,-1])}] ')

imgs = {'default':img[:,:,::-1], 'IMREAD_COLOR':img_bgr[:,:,::-1], 
        'IMREAD_UNCHANGED':img_bgra, r'$\alpha$':img_bgra[:,:,3]}

for idx, (title,img) in enumerate(imgs.items()):
  plt.subplot(2,2,idx+1)
  plt.title(title)
  if img.ndim == 3 : # num of dimension.
    if img.shape[2] == 4: # bgra
      plt.imshow(cv2.cvtColor(img_bgra,cv2.COLOR_BGRA2RGBA))
    else: # rgb! 
      plt.imshow(img)  
  else: # gray img.
    plt.imshow(img, cmap=plt.cm.gray)
  plt.axis('off')
plt.tight_layout()
plt.show()
```

다음 코드를 통해, alpha channel에 있는 값들을 살펴볼 수 있음.

```Python
a = img_bgra[...,-1].ravel()
print(img_bgra.shape[0]*img_bgra.shape[1],img_bgra.shape,a.shape)
value, counts = np.unique(a, return_counts=True)

for v,c in zip(value, counts):
  print(v,c)
```

* 주로 0,255 의 값을 가지나 경계상에서의 이들 사이의 값이 존재하는 것을 확인 가능함.

pixel intensity에 대한 Histogram (도수분포표)로 확인하면 보다 분명함.

```Python
print(a.shape)
tmp = plt.hist(a,bins=100)
```

---

---

## HSV

다음 코드는 Saturation이 0%, 20%, 100%경우, Hue-Value에 따른 색상을 보여준다.

* matplotlib에서는 RGB를 color space로 쓰므로 이미지로 확인하려면 변경해줘야 함.

```Python
from matplotlib.colors import hsv_to_rgb
import numpy as np

H, V = np.mgrid[0:1:360j, 0:1:100j]
S = np.ones_like(V)

print("Hue H's size        :",H.shape)
print("Saturation S's size :",S.shape)
print("Intnesity V's size  :",V.shape)

HSV_S100 = np.dstack((H, S * 1.0, V)) # depth 방향으로 배열을 합침. 가장 안쪽의 원소가 합쳐짐.
HSV_S20  = np.dstack((H, S * 0.2, V))
HSV_S0   = np.dstack((H, S * 0. , V))

# saturation = 1.0 (=100%) : pure color
RGB_S100 = hsv_to_rgb(HSV_S100)

# saturation = 0.2 (=20%)
RGB_S20  = hsv_to_rgb(HSV_S20)

# saturation = 0 (0%)
RGB_S0 = hsv_to_rgb(HSV_S0)

print("HSV_S20's shape:",HSV_S20.shape)

import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))
plt.subplot(131)
plt.imshow(RGB_S100,origin="upper",extent=[0,100,0,360])
plt.ylabel("Hue")
plt.xlabel("Value")
plt.title("Color Space : S=100")
plt.grid(False)

plt.subplot(132)
plt.imshow(RGB_S20, origin="upper",extent=[0,100,0,360])
plt.ylabel("Hue")
plt.xlabel("Value")
plt.title("Color Space : S=20")
plt.grid(False)

plt.subplot(133)
plt.imshow(RGB_S0, origin='upper', extent = [0,100,0,360])
plt.ylabel('Hue')
plt.xlabel('Value')
plt.title('Color Sapce : S=0')
plt.grid(False)

plt.tight_layout()
plt.show()
```

다음 코드는 red, green, yellow, blue 등의 원색에 대한 HSV 값을 출력해주는 코드임.

```Python
red_bgr    = np.array([[[  0,  0,255]]], dtype=np.uint8)
green_bgr  = np.array([[[  0,255,  0]]], dtype=np.uint8)
blue_bgr   = np.array([[[255,  0,  0]]], dtype=np.uint8)
yellow_bgr = np.array([[[  0,255,255]]], dtype=np.uint8)

red_hsv    = cv2.cvtColor(red_bgr   , cv2.COLOR_BGR2HSV)
green_hsv  = cv2.cvtColor(green_bgr , cv2.COLOR_BGR2HSV)
blue_hsv   = cv2.cvtColor(blue_bgr  , cv2.COLOR_BGR2HSV)
yellow_hsv = cv2.cvtColor(yellow_bgr, cv2.COLOR_BGR2HSV)

print(f'red:   {red_hsv}')    #   0 degree. In the case of opencv, the range of Hue is from 0 to 180.
print(f'green: {green_hsv}')  # 120 degree
print(f'blue:  {blue_hsv}')   # 240 degree
print(f'yellow:{yellow_hsv}')
```

결과는 다음과 같음.

```
red:   [[[  0 255 255]]]
green: [[[ 60 255 255]]]
blue:  [[[120 255 255]]]
yellow:[[[ 30 255 255]]]
```

* 원색이므로 saturation과 value는 모두 100%에 해당하는 255가 나옴.
* Hue는 color가 다르므로 다 다르고, red가 0도, green이 120도, blue가 240도, yellow가 60도임을 확인할 수 있음.

---

---

## YCbCr

* `Y` : Luma (밝기) : 많은 비트수를 할당. 4bit
* `Cb` (or `U`) : Chroma Blue (밝기와 파란색과의 색상차) : 둔감한 색상정보이므로 적은 비트수 할당. 2bit
* `V` (or `Cr`): Chroma Red (밝기와 붉은 색의 색상차) : 둔감한 색상정보이므로 적은 비트수 할당. 2bit

---

***RGB to YCbCr 변환공식***  

아래의 공식과 같으나 `cv2.cvtColor`등을 사용하길 권한다. (대략적인 값의 의미에 대해 이해하는 용도로 읽어봐도 충분하다.)

$$
\begin{aligned}
\text{Y} &= 0.29900\text{R} + 0.58700\text{G} + 0.11400\text{B} \\
\text{Cb} &= -0.16874\text{R} - 0.33126\text{G} + 0.50000\text{B} \\
\text{Cr} &= 0.50000\text{R} - 0.41869\text{G} - 0.08131\text{B} \\
\end{aligned}
$$

---

***YCbCr to RGB변환공식:***

아래의 공식과 같으나 `cv2.cvtColor`등을 사용하길 권한다. (대략적인 값의 의미에 대해 이해하는 용도로 읽어봐도 충분하다.)

$$\begin{aligned}
\text{R} = 1.00000\text{Y}  + 1.40200 \text{Cr} \\
\text{G} = 1.00000\text{Y}  - 0.34414 \text{Cb} - 0.71414 \text{Cr} \\
\text{B} = 1.00000\text{Y}  + 1.77200 \text{Cb}
\end{aligned}$$


다음은, 검정색에서 흰색으로 밝기만 변경한 경우의 YCbCr의 값을 확인한 코드조각임.

```Python
import numpy as np
import cv2

dark   = np.array([[[  0,  0,  0]]], dtype=np.uint8) #BGR
middle = np.array([[[127,127,127]]], dtype=np.uint8) #BGR
bright = np.array([[[255,255,255]]], dtype=np.uint8) #BGR

dark_yuv   = cv2.cvtColor(dark,   cv2.COLOR_BGR2YUV)
middle_yuv = cv2.cvtColor(middle, cv2.COLOR_BGR2YUV)
bright_yuv = cv2.cvtColor(bright, cv2.COLOR_BGR2YUV)

print(f'dark:   {dark_yuv}')   # Y = intensity!
print(f'middle: {middle_yuv}')
print(f'bright: {bright_yuv}')
```

결과는 다음과 같음.

```Json
dark:   [[[  0 128 128]]]
middle: [[[127 128 128]]]
bright: [[[255 128 128]]]
```

* numpy는 homogeneous data type으로 구성된 ndarray를 기본데이터로 하므로 bit절약이 로딩이후엔 의미가 없다. (각 채널당 8bit씩 할당됨.)
* 밝기에 해당하는 `Y`만 바뀌는 것을 확인 가능함.

> HSV에서는 3번째 채널에 해당하는 intensity가 YUV에서는 맨 앞에 있다보니 YUV를 종종 이용하는 코드들도 자주 보인다.

---

---

## OpenCV가 지원하는 Color space확인하기.

OpenCV의 경우, 150개 이상의 color-space conversion을 지원한다.

다음 코드는 ^^지원하는 color-space conversion^^ 를 보여준다.

```Python
cs = [i for i in dir(cv2) if i.startswith('COLOR_')]
print(cs)
print(len(cs))
```

---

---

## 관련 자료

* [관련 ipynb파일](https://github.com/dsaint31x/OpenCV_Python_Tutorial/blob/master/DIP/DIP_00_00_1_ColorSpace.ipynb)


