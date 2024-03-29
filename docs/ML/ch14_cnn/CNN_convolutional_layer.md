# Convolutional Layer

Locality of Pixel Dependency 와Stationarity of Statstics 에 기반한 cnn의 주요 구성 요소.

* CNN은 convolutional layer를 통해 feature(특징)을 추출함.
* Convolutional layer의 출력인 feature map은 추출된 feature의 위치와 강도를 가지고 있음.

하나의 kernel (폭과 높이, 그리고 depth로 dimension이 결정됨)과 bias를 이용한 convolution을 수행하여 하나의 feature map을 얻어냄.

* 작은 크기의 kernel (=filter라고도 불림)을 사용
	* 이전 layer의 일부 neurons만이 연결됨 (전체가 연결되는 dense와 다름)
	* kernel 크기에 따라 receptive field가 결정됨.
* sliding을 통해 입력 layer의 모든 neurons에 적용함.
	* 입력 layer에서 위치에 상관없이 현재 kernel에 대한 반응강도를 얻어냄.
	* feature map은 이들 반응강도를 각receptive field의 위치에 따라 2D로 배치한 것임 (feature vector는 특징을 1차원으로 나타낸 vector임. feature map은 특정 kernel에 대한 response를 feature 값으로 하여 2차원으로 배치한 map임.)
* 하나의 입력에 대해 여러 kernels를 적용하여 여러 feature map을 얻게 되며, 이들을 다시 입력으로 삼아 다른 여러 kernels를 적용하도록 계층으로 쌓음.
	* 이같은 구조는 여러 feature maps로 구성된 hierarchicy를 얻음.
	* lower layer에서는 low level feature maps 를 얻음 (edge, corner, texture 등)
	* intermediate layer에서는low level feature maps를 조합한 intermediate feature를 추출해 냄.
	* higher layer에서는 task와 밀접하게 관련되며 이들 intermediate features를 조합하여 구성되는 high level feature를 추출해냄.

![](../img/ch00/dl_hiearchy_rep.png)

* 만약 input의 depth가 10인 경우, kernel의 depth도 10이 된다.

---

## Correlation과Convolution.

Signal Processing에서는 Convolution과 Cross Correlation은 용도가 분명히 다른 연산이지만, DL에서는 대부분의 Convolution은 Cross Correlation으로 구현된다.

다음 URL 참고.

참고 : [Cross Correlation](https://dsaint31.tistory.com/382) 

---

## 주요 hyper-parameters

### kernel size

feature map의 **한 pixel의 값** 을 결정하는데 참여하는 input의 pixels의 수를 결정.

* kernel size가 클수록 receptive field가 커짐.
* kernel size가 클수록 parameters 의 수가 커짐.
* 일반적으로 kernel size는 홀수이며, kernel의 정가운데 pixel의 위치를 anchor라고 부름.

![](./img/kernel.gif)

> kernel의 weights를 cnn에서는 데이터로부터 DL의 training과정 중에 알아서 설정됨.  
> Digital Image Processing 에서의 spatial filtering의 경우, 사람이 kernel의 weight를 설정하는 것과 달리 DL에서는 Task에 적합한 Kernel의 weights를 데이터로부터 구해냄.

### stride

convolution에서 sliding을시킬 때 건너뛰는 pixel의 수.

* stride가 클수록 convolutional layer의 출력인 feature map의 넓이와 높이가 작음.
* receptive field가 겹치지 않도록 조정하는게 일반적임.

![](./img/Stride.png)

### padding

convolution의 경우, 출력이 입력보다 작은 크기(폭과 높이)가 되게 된다.

이를 방지하기 위해, 입력을 padding하여 좀 더 큰 크기로 만들어서 convolution의 출력이 padding 전의 입력과 같은 크기가 되도록 처리하는 게 일반적임.

TensorFlow의 경우, `padding` 파라메터를 `same`으로 지정하면 zero-padding을 수행하여 입력과 같은 크기의 출력이 나오도록 할 수 있음.

---

### Note

Convolutional Layer는 Dense Layer에 비해서는 메모리 사용량이 적지만, 적다고 보기는 어려운 수준의 메모리 사용량을 가짐.

때문에 훈련과정에서 out of memory가 발생할 경우, batch size를 줄이거나 stride를 크게 하는 등의 처리가 필요함.
