# Contour Properties

object의 contour를 활용하여 구해지는 다양한 properties를 소개한다.

Centroid, Area, Perimeter 등은 이전에 다룸.

## Aspect Ratio

종횡비 (가로세로비)라고도 불림.

$$\text{AspectRatio} = \frac{\text{Width}}{\text{Height}}$$

```Python
x,y,w,h = cv2.boundingRect(cnt)
aspect_ratio = float(w)/h
```

> It is the ratio of width to height of bounding rect of the object.

## Extent

$$\text{Extent} = \frac{\text{ObjectArea}}{\text{BoundingRectangleArea}}$$

```Python
area    = cv2.contourArea(cnt)
x,y,w,h = cv2.boundingRect(cnt)
rect_area = w*h
extent = float(area)/rect_area
```

> Extent is the ratio of contour area to bounding rectangle area.

## Solidity

$$
\text{Solidity} = \frac{\text{ContourArea}}{\text{ConvexHullArea}}
$$

```Python
area      = cv2.contourArea(cnt)
hull      = cv2.convexHull(cnt)
hull_area = cv2.contourArea(hull)
solidity = float(area)/hull_area
```

> Solidity is the ratio of contour area to its convex hull area.

## Equivalent Diameter

Contour의 넓이와 동일한 넓이를 가진 원의 지름.

$$
\text{EquivalentDiameter} = \sqrt{\frac{4 \times \text{ContourArea}}{\pi}}
$$

> Equivalent Diameter is the diameter of the circle whose area is same as the contour area.

## Orientation

object가 향하고 있는 방향으로 object를 최적으로 표시하는 타원(`fitEllipse`)으로부터 구한 각도.

```Python
(x,y),(MA,ma),angle = cv2.fitEllipse(cnt)
```

* `MA` : Major Axis lengths. 
* `ma` : Minor Axis lengths.

## Mask and Pixel Point

Object를 구성하는 모든 point들의 좌표를 추출할 때 사용되는 코드는 다음과 같음.

```
mask = np.zeros(imgray.shape,np.uint8)
cv2.drawContours(mask,[cnt],0,255,-1)
pixelpoints = np.transpose(np.nonzero(mask))
#pixelpoints = cv2.findNonZero(mask)
```

* numpy의 `nonzero`를 사용하는 경우에는 (row, column) 의 형태이므로 x,y로 바꾸기 위해서 transpose가 필요함.
* `cv2.findNonZero`를 사용해도 같은 결과임.

## Maximum Value, Minimum Value and their locations

앞서 구함 mask 에 해당하는 영역(=object)에서의 최대, 최소값과 해당 위치의 좌표를 다음으로 구할 수 있음.

```Python
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(imgray,mask = mask)
```

### Mean Color or Mean Intensity

평균값들을 구할 수도 있음.

```Python
mean_val = cv2.mean(im,mask = mask)
```

## Extreme Points

object에서 topmost, bottommost, rightmost, and leftmost point를 extreme points라고 부름.

```Python
leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
```

`numpy`의 `ndarray`에서의 `argmax`, `argmin`을 활용함.

## References

* [OpenCV's tutorial : Contour Properties](https://docs.opencv.org/3.4/d1/d32/tutorial_py_contour_properties.html)
