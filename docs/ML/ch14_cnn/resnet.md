---
title: "ResNet: Deep Residual Learning for Image Recognition (2015)"
description: "ResNet의 residual learning, shortcut connection, residual unit 구조를 정리한 글"
date: 2026-07-07
categories:
  - Deep Learning
  - CNN
tags:
  - resnet
  - residual learning
  - skip connection
  - shortcut connection
  - image classification
  - computer vision
math: true
---

# ResNet: Deep Residual Learning for Image Recognition (2015)

ref.: original paper, [Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)

---

ILSVRC 2015 우승 모델이며, deep learning에서 “deep”의 의미를 크게 바꾼 모델임.

* Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun이 제안함.
* ImageNet classification에서 top-5 error 3.57%를 기록함.
* 152 layers라는, 당시로서는 매우 놀라운 깊이의 deep model을 제안함.

ResNet은 `skip connection` 또는 `shortcut connection`을 도입하여 매우 깊은 모델의 학습을 가능하게 함.

* ResNet은 identity mapping과 addition을 이용하는 `skip connection`을 통해 `residual learning`을 수행함.
* 최근에는 addition 연산 기반의 `residual learning`뿐 아니라, `concatenation`을 이용한 `skip connection`도 널리 사용됨.

> `residual learning`에서는 `skip connection`의 결과를 add 연산으로 연결함.  
> `concatenation`은 feature map을 channel 방향으로 이어 붙이는 방식임.  
> `concatenation` 기반 연결은 `DenseNet (2017)`을 통해 유용성을 보임.

참고로, `concatenation`을 사용한 `DenseNet (2017)`의 경우,

* low-level texture, edge, color pattern 같은 초기 feature가 뒤쪽 layer까지 직접 전달됨.
* 병변의 미세한 색 변화, 경계, 표면 질감처럼 low-level feature가 중요한 의료 영상 데이터에서는 ResNet보다 높은 성능을 보일 수 있음.
* 추가적으로 DenseNet-121은 parameter efficiency 측면에서 소량 데이터에 유리할 수 있음.
    * DenseNet-121은 대략 8M parameters 수준임.
    * ResNet-50은 대략 25M parameters 수준임.

---

## 구조

전반적인 구조는 다음과 같음.

* 매우 많은 수의 convolutional layer가 `residual unit (RU)` 단위로 반복되어 구성됨.
    * ResNet-18/34에서 사용하는 기본 `RU`는 보통 2개의 convolutional layers로 구성됨.
    * 첫 번째 convolutional layer는 BN과 ReLU로 이어짐.
    * 이후 두 번째 convolutional layer를 거치고, 그 결과는 BN을 통과함.
    * 이 결과는 skip connection으로 전달된 input과 addition을 수행하고, 해당 결과는 다시 ReLU를 거침.
* 각 `RU`는 main path와 shortcut path를 함께 가지며, `RU`의 input과 output은 skip connection을 통해 연결됨.

![](./img/resnet.png)

* ResNet의 기본 activation function은 `ReLU`이며, convolutional layer 뒤에서 BN과 함께 사용됨.
* 파선(dotted shortcut)으로 그려진 skip connection은 feature map의 spatial size나 channel 수가 바뀌어 $\mathbf{x}$와 $\mathcal{h}(\mathbf{x})$의 차원이 맞지 않는 경우를 의미함.
    * 논문에서는 이를 zero-padding shortcut과 projection shortcut의 두 가지 방식으로 구현하여 비교함.
    * zero-padding shortcut, 즉 Option A는 shortcut branch에서 identity mapping을 유지하되, channel 수가 늘어나는 부분을 0으로 padding함. 추가 parameter가 없음.
    * projection shortcut, 즉 Option B는 1x1 convolution을 사용하여 shortcut branch의 차원을 맞춤.
    * projection shortcut이 대체로 더 우수한 결과를 보임.
    * 현재 backbone으로 제공되는 대부분의 ResNet-18/34 basic block, ResNet-50/101/152 bottleneck block 구현은 차원이 바뀌는 지점에서 projection shortcut을 사용함.
* channel이 2배 늘어나는 경우에는 feature map의 width와 height가 각각 1/2로 줄어듦. 따라서 spatial area는 1/4이 됨.
* stage가 바뀌는 경우에는 pooling 대신 convolution에서 `stride=2`를 사용하여 spatial size를 줄이는 것이 일반적임.
    * 예를 들어 `RU (64ch)` stage, 즉 논문 표기의 `conv2_x`에서 `RU (128ch)` stage, 즉 `conv3_x`로 넘어갈 때,
    * spatial size는 $56 \times 56$에서 $28 \times 28$로 줄어듦.
    * channel 수는 $64$에서 $128$로 늘어남.

ResNet은 주로 convolutional layer와 fully-connected layer만 layer 수로 count함.  
즉, BN, ReLU, pooling layer 등은 layer 수에 포함하지 않음.

ResNet-34:

* `Conv (64ch)` - `RU (64ch, conv2_x)` $\times 3$ - `RU (128ch, conv3_x)` $\times 4$ - `RU (256ch, conv4_x)` $\times 6$ - `RU (512ch, conv5_x)` $\times 3$ - `FC (1000ch)`

ResNet-152:

* `Conv (64ch)` - `Bottleneck RU (256ch, conv2_x)` $\times 3$ - `Bottleneck RU (512ch, conv3_x)` $\times 8$ - `Bottleneck RU (1024ch, conv4_x)` $\times 36$ - `Bottleneck RU (2048ch, conv5_x)` $\times 3$ - `FC (1000ch)`

---

## Residual Block

다음은 ResNet-18/34에서 사용된 기본 `RU`와, 그보다 더 깊은 ResNet에서 사용된 `Bottleneck RU`의 구성임.

![](./img/residual_unit.png)

* 오른쪽의 `Bottleneck RU`는 ResNet-50/101/152에서 사용됨.
* 기본 `RU`는 2개의 3x3 convolution으로 구성됨.
* `Bottleneck RU`는 1x1, 3x3, 1x1 convolution으로 구성됨.
    * 첫 번째 1x1 convolution은 channel 수를 줄이는 역할을 함.
    * 3x3 convolution은 줄어든 channel 수에서 spatial feature를 추출함.
    * 마지막 1x1 convolution은 channel 수를 다시 확장함.

다음은 `Bottleneck RU`에서 identity shortcut과 projection shortcut을 보여줌.

![](./img/resnet_idblock_convblock.png)

---

## Residual Learning

기존 모델이 hypothesis $\mathcal{H}(\mathbf{x})$를 직접 학습하는 것과 달리, ResNet은 hypothesis와 input $\mathbf{x}$의 차이인 residual function을 학습함.

$$
\mathcal{F}(\mathbf{x}) = \mathcal{H}(\mathbf{x}) - \mathbf{x}
$$

따라서 최종 출력은 다음과 같이 표현됨.

$$
\mathcal{H}(\mathbf{x}) = \mathcal{F}(\mathbf{x}) + \mathbf{x}
$$

* skip connection을 통해 $\mathcal{F}(\mathbf{x})$에 $\mathbf{x}$를 더해 $\mathcal{H}(\mathbf{x})$를 구함.
* ResNet은 $\mathcal{H}(\mathbf{x})$를 직접 학습하는 것보다 residual인 $\mathcal{F}(\mathbf{x})$를 학습하는 것이 더 쉽다고 보았음.

---

## torchvision

최근 `torchvision`에서는 `pretrained=True` 대신 `weights` argument 사용이 권장됨.

```python
from torchvision.models import resnet50, ResNet50_Weights

model = resnet50(weights=ResNet50_Weights.DEFAULT)
````

다른 ResNet 계열 모델도 같은 방식으로 사용할 수 있음.

```python
from torchvision.models import resnet18, ResNet18_Weights
from torchvision.models import resnet34, ResNet34_Weights
from torchvision.models import resnet101, ResNet101_Weights
from torchvision.models import resnet152, ResNet152_Weights
from torchvision.models import wide_resnet50_2, Wide_ResNet50_2_Weights
from torchvision.models import wide_resnet101_2, Wide_ResNet101_2_Weights

model = resnet18(weights=ResNet18_Weights.DEFAULT)
model = resnet34(weights=ResNet34_Weights.DEFAULT)
model = resnet101(weights=ResNet101_Weights.DEFAULT)
model = resnet152(weights=ResNet152_Weights.DEFAULT)
model = wide_resnet50_2(weights=Wide_ResNet50_2_Weights.DEFAULT)
model = wide_resnet101_2(weights=Wide_ResNet101_2_Weights.DEFAULT)
```

---

## 같이 보면 좋은 자료들

* [ResNet Explained!](https://youtu.be/sAzL4XMke80?si=EjwNyuKMUlgAuB97)

```
```
