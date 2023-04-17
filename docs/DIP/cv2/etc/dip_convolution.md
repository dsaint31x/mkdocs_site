# Convolution

> 이 문서에서의 conovlution은 digital image processing등에서의 convolution을 다루고 있음. 
> signal processing의 discrete convolution에 대한 건 다음 문서를 참고할 것:  
> [Discrete Convolution](https://dsaint31.tistory.com/entry/SS-Discrete-Convolution-Linear-Discrete-Convolution), [Circular Convolution](https://dsaint31.tistory.com/entry/SS-Circular-Convolution)

image filtering에서 spatial domain filtering은 주로 **filter** 또는 **kernel** 또는 **window** 라고 하는 행렬과 입력 영상의 Convolution으로 이루어짐.

> Convolution은 기호 ⊗ or ∗ 등으로 표기되지만 통일된 기호는 없음.

* 어찌보면, spatial operation의 끝판왕이라고 봐도 됨.

convoluton의 수식은 다음과 같음.

$$
\begin{aligned}
g(x,y) &= \int^\infty_{-\infty}\int^\infty_{-\infty}f(\xi,\eta)h(x-\xi,y-\eta)d\xi d\eta
\\
&= h(x,y)*f(x,y)\\
&= f(x,y)*h(x,y)\end{aligned}
$$

where

- $h(x,y)$ : filter or kernel
- $f(x,y)$ : original image
- $g(x,y)$ : output imagewhere

convoluton은 cross-correlation과 달리 ^^교환법칙이 성립^^ 하며, impulse response(영상에선 point spread function)와 입력 신호를 이용하여 ***시스템의 response를 구하는 연산*** 임.

* cross-correlation과 달리 입력 함수 중 하나가 reflection이 이루어진다는 차이가 있음.
* cross-correlation에 대한 보다 자세한 내용은 다음 url을 참고 : [Cross correlation](https://dsaint31.tistory.com/entry/SS-Cross-Correlation)

> 하지만, 이미지 처리에서는 대부분 kernel을 대칭적인 것을 사용하다 보니 cross-correlation과 차이가 없는 경우가 많고, 특히 ML(기계학습)이나 DL(딥러닝)에서 kernel이 이미 상하좌우로 flip하여 입력하면 된다는 가정 하에 convolution의 구현이 실제로는 cross-correlation인 경우가 대다수임.

## Kernel (or Mask, Window)

- 유한한 크기의 `impulse response` (or point spread function)의 특성 계수
- 시스템 응답 특성 계수를 가지고 있는 matrix 혹은 tensor임.

![](../../img/etc/kernel.png)

## Convolution 수행 방식

![](../../img/etc/convolution.png)

위의 그림에서 Kernel matrix는 상하좌우로 뒤집힌(reflection) 상태임. (Cross correlation과 차이)

- 다시 강조하지만, DIP나 ML, DL에서는 cross-correlation과 거의 구분하지 않음.

아래 그림은 다채널의 입력에 대해, 2개의 filter (or kernel)이 주어져서 convolution이 이루어지는 과정을 보여주고 있음.

![](../../img/etc/convolution_how.gif)

* $5 \times 5 \times 3$ image를 상하좌우로 1씩 padding을 수행하고, 
* $3 \times 3$ kernel을(엄밀하게는 $3\times 3\times 3$) 통해 convolution을 수행하여 $3 \times 3 \times 2$ image를 얻어냄. 
* Kernel은 2 pixel의 stride로 사용하여 이동함.
* 결과 영상의 depth $2$는 kernel (or filter)이 2개 (W0, W1) 사용됨을 의미함. 

## OpenCV

OpenCV 는 filter2D를 통해 convolution을 제공.

```Python
dst = cv2.filter2D(
    src, 
    ddepth, 
    kernel, 
    dst,
    anchor,
    delta, 
    borderType
)
```

- `src` : input image
- `ddepth` : output imaget dtype : -1 입력과 동일 / `CV_8U`,`CV_16U`, `CV16S`, `CV_32F`, `CV_64F`
- `kernel` : kernel or window or mask or filter matrix
- `dst` : output image
- `anchor` : kernel의 기준점. 결과값이 치환될 위치. default (-1,-1) 로 kernel의 중앙을 의미
- `delta` : 결과값에 추가할 값.
- `borderType` : padding 형태 (기본으로 `BORDER_REFLECT_101`임).

간단한 예제 코드는 다음과 같음.

```Python
#img = cv2.imread('./data/lena.jpg')
img = astro_noise.copy() # 아래 예는 poisson noise를 가함.
print(img.dtype, img.shape)

k_size = 10
kernel = np.full((k_size,k_size),1./(k_size**2))
blured = cv2.filter2D(img, -1, kernel)
print(f'from {img.shape} to {blured.shape}')

plt.figure(figsize=(10,20))
plt.imshow(np.concatenate((img,blured),axis=1))
plt.axis('off')
plt.show()
```

결과는 다음과 같음.

![](../../img/etc/box_filtered.png)
