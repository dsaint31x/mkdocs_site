# Template Matching : cv2.matchTemplate

template (대상 영상에서 찾고자 하는 object에 해당하는 patch image)을 input image(=target image, 대상영상)에서 찾아내는 기법.

convolution 기반의 spatial filtering의 동작 방식과 유사하게 template를 kernel로 삼아 target image에 sliding시키면서 matching을 정도를 평가하는 measure를 계산함.

> OpenCV 에서는 위 설명의 measure들을 `method` parameter로 6가지 정도를 지원함.

모든 pixel에 대해 measure를 계산하고 이들을 비교하여 matching이 잘 된 영역들의 위치와 measure score를 반환해준다.

> Signal processing의 관점에서 볼 때, Cross correlation을 2-Dimension으로 확장한 경우가 Template Matching에서 method를 `cross correlation`으로 사용한 경우와 동일함.

Matching에서 Template Matching은 가장 단순한 형태로, input image(=target image)와 template가 모두 image 형태 그대로가 사용된다.

단점은 template에 해당하는 image가 회전된 경우, pixel의 값이 전체적으로 밝아지거나 어두어진 경우, template과 matching 된 영역의 조명이 불균일한 경우, template 또는 matching 된 영역의 일부 패턴이 변형된 경우 등에서 성능이 떨어짐.

때문에 keypoint에서의 local feature 를 추출하고 이를 기반으로 하는 matching이 보다 더 선호됨. 하지만 template이 target image에서 추출되는 경우와 같이 단순한 경우엔 성능이 좋기 때문에 1차적으로 수행되는 경우가 많음.

## cv2.matchTemplate

```
cv2.matchTemplate(
    image,
    templ,
    method,
    result = None,
    mask = None
) -> result
```

* `image` : template 에 해당하는 patch image 위치를 찾기 위한 target image. `uint8` or `unit32`의 gray-scale image.
* `templ` : template. `image`보다 작거나 같은 크기를 가지면서 동시에 `dtype`이 같아야 함. 
* `method` : 넓은 의미에서 distance measure 또는 similarity measure function에 해당함. 보다 자세한 건 아래 참고.
* `result` : 결과 image로 `dtype`가 `np.float32`이며 $(W_\text{image}-W_\text{templ}+1) \times (H_\text{image}-H_\text{templ}+1)의 넓이와 높이를 가짐. 
    * 호출 시 argument는 `None`으로 해주고 return value로 설정하는 방식이 Python에선 일반적.
* `mask` : `image`에서 일부 영역에서만 template matching을 수행할 경우 입력됨.

## The matching methods available in OpenCV

### `TM_SQDIFF`

SQuared Difference로 difference vector의 squared L-2 norm을 사용. (Euclidean distance의 제곱)

$$R(x,y)= \sum _{x',y'} (T(x',y')-I(x+x',y+y'))^2$$

### `TM_SQDIFF_NORMED`

Normalized Square Difference임. pixel intensity의 평균이 template과 image의 matching 부위와 차이가 나는 경우에도 잘 동작함.

$$
R(x,y)= \frac{\sum_{x',y'} (T(x',y')-I(x+x',y+y'))^2}{\sqrt{\sum_{x',y'}T(x',y')^2 \cdot \sum_{x',y'} I(x+x',y+y')^2}}$$

### `TM_CCORR`

Cross correlation. Signal Processing에서 두 신호의 유사한 정도를 판별하는데 많이 사용되는 것으로 이를 2D로 확장함 : 이론적으로도 Correlation Coefficient (Fisher's Correlation Coefficient)보다 나쁜 성능을 보임.

$$R(x,y)= \sum _{x',y'} (T(x',y') \cdot I(x+x',y+y'))$$

### `TM_CCORR_NORMED`

Normalized Cross Correlation.

$$R(x,y)= \frac{\sum_{x',y'} (T(x',y') \cdot I(x+x',y+y'))}{\sqrt{\sum_{x',y'}T(x',y')^2 \cdot \sum_{x',y'} I(x+x',y+y')^2}}$$

### `TM_CCOEFF`

Cross Correlation에서 각각의 평균치에 대한 보정을 추가한 경우로 일종의 `Covariance`에 해당한다.

Cross Correlation에 비해서는 선호되는 편이나, 이 역시 normalization을 하지 않은 경우, 에러가 꽤 발생하는 편임.


$$R(x,y)= \sum _{x',y'} (T'(x',y') \cdot I'(x+x',y+y'))$$

where

$$\begin{array}{l} T'(x',y')=T(x',y') - 1/(w \cdot h) \cdot \sum _{x'',y''} T(x'',y'') \\ I'(x+x',y+y')=I(x+x',y+y') - 1/(w \cdot h) \cdot \sum _{x'',y''} I(x+x'',y+y'') \end{array}
$$

### `TM_CCOEF_NORMED`

일종의 Correlation Coefficient (Fisher's Correlation Coefficient)으로 볼 수 있음.

`templ`과 `image` 자체의 intensity variance를 구하고 이를 곱한 후 squared root를 취해주어 `templ`과 `image` 자체의 값이 퍼져 있는 정도를 구하고 이를 covariance(=`TM_CCOEFF`)에 나누어 줌.

> 수학적으로 covariance와 correlation은 arithmetic mean을 취해주지만, template matching에선 mean처리가 필요없음.

개인적으로 많이 이용하는 method임. `cv2.TM_SQDIFF_NORMED`와 함께 가장 기본으로 사용됨.

$$R(x,y)= \frac{ \sum_{x',y'} (T'(x',y') \cdot I'(x+x',y+y')) }{ \sqrt{\sum_{x',y'}T'(x',y')^2 \cdot \sum_{x',y'} I'(x+x',y+y')^2} }$$


### Example

OpenCV Tutorial에 있던 예제를 colab등에서 동작가능하도록 조금 수정한 예제임.

> Template Matching의 경우 가급적 원본 영상에서 template를 선택하여 사용하는게 가장 정확함. 그 외의 경우 그리 만족할만한 결과가 안나오는 경우가 많음.

예제로 사용할 수 있는 image 는 다음 URL에서 받을 것.

* [src image: Template_Matching_Original_Image.jpg](../../img/ch02/Template_Matching_Original_Image.jpg)
* [template image: Template_Matching_Template_Image.jpg](../../img/ch02/Template_Matching_Template_Image.jpg)

> 주석처리된 부분들을 해제하여 template를 원본영상의 일부가 아닌 비슷한 이미지(사이즈 다름)로 한 경우등의 성능을 확인해 볼 것.

```Python
import cv2
import matplotlib.pyplot as plt
import numpy as np

#match_method = cv2.TM_SQDIFF
# match_method = cv2.TM_SQDIFF_NORMED
# match_method = cv2.TM_CCORR
# match_method = cv2.TM_CCORR_NORMED
# match_method = cv2.TM_CCOEFF
match_method = cv2.TM_CCOEFF_NORMED
use_mask = False

mask  = None

# -------------------------------------------------------
# load src image
img_fstr  = 'Template_Matching_Original_Image.jpg'
img   = cv2.imread(img_fstr , cv2.IMREAD_COLOR)

# -------------------------------------------------------
# template matching은 scale 및 이미지 값에 영향을 크게 받음.
# 가급적 image에서 선택하여 잘라야 함.
templ = img[70:115,150:190,...].copy()
# templ_fstr  = 'Template_Matching_Template_Image.jpg'
# templ   = cv2.imread(templ_fstr , cv2.IMREAD_COLOR)


# plt.imshow(templ[...,::-1])

# -------------------------------------------------------
# generate mask
if use_mask:
  mask = np.ones(img.shape)

# -------------------------------------------------------
# matching!!
method_accepts_mask = (cv2.TM_SQDIFF == match_method or cv2.TM_CCORR_NORMED == match_method )
if (use_mask and method_accepts_mask):
  result = cv2.matchTemplate(img, templ, match_method, None, mask)
else:
  result = cv2.matchTemplate(img, templ, match_method)

# -------------------------------------------------------
# get the coordinate of matching point
cv2.normalize( result, result, 0, 1, cv2.NORM_MINMAX, -1 )
plt.imshow(result,cmap='gray')
_minVal, _maxVal, minLoc, maxLoc = cv2.minMaxLoc(result, None)
if (match_method == cv2.TM_SQDIFF or match_method == cv2.TM_SQDIFF_NORMED):
  print(match_method)
  matchLoc = minLoc
else:
  print(match_method)
  matchLoc = maxLoc

# -------------------------------------------------------
# display
print(matchLoc)
img_display = img.copy()
color_line = (255,0,0)
thickness = 2
line_type = 8

cv2.rectangle(img_display, matchLoc, (matchLoc[0] + templ.shape[1], matchLoc[1] + templ.shape[0]), color_line,thickness, line_type)

plt.imshow(img_display[...,::-1])
```


### References

* [OpenCV's Tutorial](https://docs.opencv.org/5.x/de/da9/tutorial_template_matching.html)