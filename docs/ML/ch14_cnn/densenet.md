---

title: "DenseNet의 구조와 특징"
description: "DenseNet의 dense connectivity, Dense Layer, growth rate, bottleneck, transition layer, compression 및 DenseNet-121의 구조와 특징을 정리한 문서"

categories:

* Deep Learning
* Computer Vision

tags:

* densenet
* densenet-121
* cnn
* dense-connectivity
* dense-layer
* growth-rate
* bottleneck
* transition-layer
* feature-reuse
* image-classification

toc: true
math: true
draft: false
------------

# DenseNet

## 1. 개요

**DenseNet(Dense Convolutional Network)** 은 Huang 등이 2017년 CVPR에서 제안한 CNN 구조임.

DenseNet은 하나의 **Dense Block** 안에서 이전 모든 layer의 feature map을 이후의 모든 layer로 전달하는 구조임.

* 즉, 각 layer가 이전 layer들의 feature를 반복해서 새로 학습하기보다,
* 이미 생성된 feature를 직접 재사용하도록 설계된 모델임.

DenseNet의 핵심 목적은 다음과 같음.

* feature reuse를 통한 학습 효율 향상
* gradient flow 개선
* vanishing gradient 완화
* 적은 parameter를 이용한 높은 성능 달성
* 저수준 feature와 고수준 feature의 직접적인 연결

---

## 2. Dense Connectivity

일반적인 CNN에서는 $l$번째 layer가 바로 이전 layer의 출력만 입력으로 사용함.

$$
\mathbf{x}_l = H_l(\mathbf{x}_{l-1})
$$

여기서 $H_l(\cdot)$은 convolution, normalization, activation 등으로 구성된 transformation임.

반면 DenseNet에서는 (l)번째 layer가 이전의 모든 feature map을 입력으로 사용함.

$$
\mathbf{x}_l = H_l \left(
[\mathbf{x}_0,\mathbf{x}*1,\ldots,\mathbf{x}*{l-1}]
\right)
$$

여기서 대괄호 $[\cdot]$는 feature map을 **channel dimension으로 concatenation하는 연산**임.

따라서 DenseNet에서는 다음과 같은 연결 구조가 형성됨.

$$
\mathbf{x}_0
\rightarrow
\mathbf{x}_1
\rightarrow
\mathbf{x}_2
\rightarrow
\mathbf{x}_3
$$

동시에 각 layer 사이에 다음과 같은 직접 연결이 추가됨.

$$
\mathbf{x}_0
\rightarrow
\mathbf{x}_2,
\qquad
\mathbf{x}_0
\rightarrow
\mathbf{x}_3,
\qquad
\mathbf{x}_1
\rightarrow
\mathbf{x}_3
$$

이처럼 

* 하나의 Dense Block 안에서
* 각 layer가 이후의 모든 layer와 연결되는 구조를
* **dense connectivity**라고 부름.

---

## 3. ResNet과의 차이

DenseNet의 연결 방식은 ResNet의 residual connection과 구분됨.

ResNet은 이전 feature map과 새로운 feature map을 element-wise addition으로 결합함.

$$
\mathbf{x}_l =

H_l(\mathbf{x}*{l-1})
+
\mathbf{x}*{l-1}
$$

반면 DenseNet은 이전 feature map들을 channel dimension으로 concatenation함.

$$
\mathbf{x}_l =

H_l
\left(
[\mathbf{x}_0,\mathbf{x}*1,\ldots,\mathbf{x}*{l-1}]
\right)
$$

따라서 두 모델의 핵심 차이는 다음과 같음.

| 구분            | ResNet                           | DenseNet                   |
| ------------- | -------------------------------- | -------------------------- |
| 연결 방식         | element-wise addition            | channel-wise concatenation |
| 이전 feature 처리 | 기존 feature와 새로운 feature를 더함      | 기존 feature를 그대로 보존하여 누적함   |
| channel 수     | 일반적으로 유지                         | layer가 추가될수록 증가            |
| 핵심 개념         | residual learning                | feature reuse              |
| 연결 목적         | identity mapping을 통한 gradient 전달 | 모든 이전 feature에 대한 직접 접근    |

* ResNet에서는 새로운 feature가 기존 feature에 더해지는 반면,
* DenseNet에서는 기존 feature와 새로운 feature가 각각 독립된 channel로 유지됨.

---

## 4. Dense Layer

Dense Block 내부의 각 layer는 일반적으로 다음과 같은 구조를 가짐.

$$
\text{BN}
\rightarrow
\text{ReLU}
\rightarrow
1\times1\text{ Conv}
\rightarrow
\text{BN}
\rightarrow
\text{ReLU}
\rightarrow
3\times3\text{ Conv}
$$

* convolution을 먼저 수행한 뒤 normalization과 activation을 적용하는 당시 전통적인 구조와 달리,
* normalization과 activation을 convolution 앞에 배치하는 **pre-activation 구조**임.

### $1\times1$ convolution

DenseNet의 $1\times1$ convolution은 뒤따르는 $3\times3$ convolution의 입력 channel 수를 $4k$로 제한하는 bottleneck 역할을 수행함.

* 여기서 $k$는 growth rate(성장률) 라고 부름.
* growth rate는 DenseNet에서는 각 Dense Layer가 새롭게 추가하는 feature map의 수를 의미함.
* DenseNet에서 이러한 bottleneck 구조를 사용하는 모델을 **DenseNet-B**라고 부름.

일반적으로 $3\times3$ convolution이 growth rate인 $k$개의 새로운 feature map을 생성할 때, 앞의 $1\times1$ convolution은 $4k$개의 intermediate feature map을 생성함.

$$
C_{\text{input}} \xrightarrow{1\times1} 4k \xrightarrow{3\times3} k
$$

따라서 $C_{\text{input}}>4k$인 경우에는 channel 수를 감소시키지만, 초기 Dense Layer처럼 $C_{\text{input}}<4k$인 경우에는 오히려 channel 수를 증가시킬 수 있음.

핵심 목적은 channel 감소 자체가 아니라, 계속 증가하는 Dense Layer의 입력 channel을 $4k$로 제한하여 $3\times3$ convolution의 연산량을 제어하는 것임.

---

## 5. Growth Rate

DenseNet의 각 layer가 새롭게 생성하여 Dense Block에 추가하는 feature map의 수를 **growth rate**라고 부름.

Growth rate는 일반적으로 $k$로 표기함.

각 layer가 $k$개의 새로운 feature map을 생성할 경우, $l$개의 layer를 통과한 뒤의 channel 수는 다음과 같음:

$$
C_l =
C_0
+
kl
$$

여기서

* $C_0$: Dense Block의 초기 입력 channel 수
* $k$: growth rate
* $l$: Dense Block 내부 layer 수

예를 들어 초기 channel 수가 64이고 growth rate가 $k=32$인 경우, 6개의 layer를 지난 뒤의 channel 수는 다음과 같음.

$$
64 + 6\times32 = 256
$$

따라서 DenseNet에서는 각 layer가 많은 channel을 새로 생성할 필요가 없음.

각 layer가 소수의 새로운 feature만 생성하고, 이전 feature는 concatenation을 통해 계속 재사용하는 방식임.

DenseNet-121, DenseNet-169, DenseNet-201에서는 일반적으로 $k=32$가 사용됨.

---

## 6. Dense Block

Dense Block은 dense connectivity가 적용되는 핵심 구간임.

Dense Block 안에서는 spatial resolution이 유지되므로, 서로 다른 layer에서 생성된 feature map을 channel dimension으로 직접 concatenation할 수 있음.

Dense Block 내부의 처리 과정은 다음과 같음.

$$
\mathbf{x}_0
\rightarrow
\mathbf{x}_1
\rightarrow
\mathbf{x}_2
\rightarrow
\cdots
\rightarrow
\mathbf{x}_L
$$

각 layer의 실제 입력은 다음과 같음.

$$
\mathbf{x}_1 = H_1([\mathbf{x}_0]) \\\\
\mathbf{x}_2 =H_2([\mathbf{x}_0,\mathbf{x}_1]) \\\\
\mathbf{x}_3= H_3([\mathbf{x}_0,\mathbf{x}_1,\mathbf{x}_2])
$$

따라서 Dense Block의 뒤쪽 layer일수록 더 많은 이전 feature를 입력으로 사용함.

초기 layer에서 생성된 edge, texture와 같은 저수준 feature가 깊은 layer까지 직접 전달되며, 깊은 layer는 이를 이용하여 더 복잡한 semantic feature를 생성함.

---

## 7. Transition Layer

Dense Block 사이에서는 feature map의 spatial resolution과 channel 수를 조절하기 위해 **Transition Layer**를 사용함.

Transition Layer의 일반적인 구성은 다음과 같음.

$$
\text{BN}
\rightarrow
\text{ReLU}
\rightarrow
1\times1\text{ Conv}
\rightarrow
2\times2\text{ Average Pooling}
$$

각 구성 요소의 역할은 다음과 같음.

* $1\times1$ convolution을 통한 channel 수 감소
* $2\times2$ average pooling을 통한 spatial resolution 절반 감소
* 다음 Dense Block으로 전달되는 feature의 크기 조절
* Dense Block에서 증가한 channel 수의 압축

Transition Layer는 CNN의 pooling layer와 유사한 downsampling 역할을 수행하되, pooling 이전에 $1\times1$ convolution을 적용하여 channel 수까지 함께 조절하는 구조임.

---

## 8. Compression

Transition Layer에서 channel 수를 감소시키는 비율을 **compression factor**라고 부름.

Compression factor는 일반적으로 $\theta$로 표기하며 다음 범위를 가짐.

$$
0 < \theta \leq 1
$$

Dense Block의 출력 channel 수가 (C)일 경우 Transition Layer의 출력 channel 수는 다음과 같음.

$$
C_{\text{out}} =

\lfloor
\theta C
\rfloor
$$

예를 들어 Dense Block의 출력 channel 수가 512이고 $\theta=0.5$인 경우 다음과 같음.

$$
C_{\text{out}} = 512\times0.5 = 256
$$

Compression을 적용한 DenseNet을 **DenseNet-C**라고 부름.

Bottleneck과 compression을 모두 적용한 구조를 **DenseNet-BC**라고 부르며, 일반적으로 사용되는 DenseNet-121, DenseNet-169, DenseNet-201이 이에 해당함.

---

## 9. DenseNet-121 구조

DenseNet-121은 총 4개의 Dense Block으로 구성되며, 각 Dense Block의 layer 수는 다음과 같음.

$$
[6,\ 12,\ 24,\ 16]
$$

전체 구조는 다음과 같음.

$$
\text{Input}
\rightarrow
\text{Stem}
\rightarrow
\text{Dense Block 1}
\rightarrow
\text{Transition 1}
\rightarrow
\text{Dense Block 2}
\rightarrow
\text{Transition 2}
\rightarrow
\text{Dense Block 3}
\rightarrow
\text{Transition 3}
\rightarrow
\text{Dense Block 4}
\rightarrow
\text{Classifier}
$$

ImageNet용 DenseNet-121의 세부 구조는 다음과 같음.

| Stage               | 구성                                    | 출력 spatial size |
| ------------------- | ------------------------------------- | --------------: |
| Input               | $224\times224$ RGB image              |  $224\times224$ |
| Stem                | $7\times7$ Conv, stride 2             |  $112\times112$ |
| Stem                | $3\times3$ Max Pooling, stride 2      |    $56\times56$ |
| Dense Block 1       | Dense Layer $\times6$                 |    $56\times56$ |
| Transition 1        | $1\times1$ Conv + $2\times2$ Avg Pool |    $28\times28$ |
| Dense Block 2       | Dense Layer $\times12$                |    $28\times28$ |
| Transition 2        | $1\times1$ Conv + $2\times2$ Avg Pool |    $14\times14$ |
| Dense Block 3       | Dense Layer $\times24$                |    $14\times14$ |
| Transition 3        | $1\times1$ Conv + $2\times2$ Avg Pool |      $7\times7$ |
| Dense Block 4       | Dense Layer $\times16$                |      $7\times7$ |
| Classification Head | Global Average Pooling + Linear       |    class logits |

DenseNet-121이라는 이름의 121은 convolution layer와 classification layer 등을 포함한 전체 layer 수를 의미함.

---

## 10. DenseNet 종류

대표적인 DenseNet 모델의 Dense Block 구성은 다음과 같음.

| 모델           | Dense Block별 layer 수 | Growth rate |
| ------------ | -------------------- | ----------: |
| DenseNet-121 | $[6,12,24,16]$       |          32 |
| DenseNet-169 | $[6,12,32,32]$       |          32 |
| DenseNet-201 | $[6,12,48,32]$       |          32 |
| DenseNet-264 | $[6,12,64,48]$       |          32 |

모델 이름의 숫자가 클수록 일반적으로 Dense Block 내부의 layer 수와 모델 깊이가 증가함.

DenseNet-121, DenseNet-169, DenseNet-201은 모두 일반적으로 $224\times224$ 입력 이미지를 사용할 수 있음.

---

## 11. DenseNet의 주요 특징

### 11.1 Feature Reuse

각 layer가 이전 모든 layer의 feature map을 직접 입력으로 사용하므로, 이미 학습된 feature를 반복해서 새로 생성할 필요가 없음.

초기 layer에서 생성된 edge와 texture feature가 깊은 layer에서도 직접 사용되는 구조임.

### 11.2 Improved Gradient Flow

Loss에서 발생한 gradient가 여러 개의 짧은 경로를 통해 초기 layer로 전달될 수 있음.

깊은 network에서 발생할 수 있는 vanishing gradient 문제를 완화하는 효과가 있음.

### 11.3 Parameter Efficiency

각 layer가 적은 수의 새로운 feature map만 생성하고 기존 feature를 재사용하므로, 비슷한 성능의 일반적인 CNN보다 적은 parameter로 높은 성능을 달성할 수 있음.

DenseNet-121은 깊이가 121 layer이지만 약 8 million개의 parameter를 사용하여, 약 25 million개의 parameter를 사용하는 ResNet-50보다 parameter 수가 적음.

### 11.4 Implicit Deep Supervision

초기 layer의 feature가 classification head까지 비교적 짧은 경로로 전달되므로, 중간 layer도 최종 loss의 영향을 직접적으로 받는 효과가 발생함.

별도의 auxiliary classifier 없이도 deep supervision과 유사한 효과를 제공하는 구조임.

### 11.5 Multi-level Feature Integration

저수준 feature와 고수준 semantic feature가 지속적으로 concatenation되므로, 서로 다른 abstraction level의 feature를 함께 사용하는 구조임.

작은 패턴, 경계, texture 정보가 중요한 image classification과 segmentation 문제에서 유리할 수 있음.

---

## 12. DenseNet의 장점

* 이전 feature를 직접 재사용하는 효율적인 구조
* 깊은 network에서도 안정적인 gradient 전달
* 비교적 적은 parameter 수
* 저수준 feature와 고수준 feature의 효과적인 결합
* 작은 객체나 미세한 texture 정보를 보존하는 데 유리한 구조
* transfer learning과 fine-tuning에 널리 사용되는 backbone
* (224\times224) 입력을 사용하는 일반적인 image classification pipeline에 적용 가능

---

## 13. DenseNet의 한계

DenseNet은 parameter 수가 적지만 반드시 memory 사용량과 연산 시간이 적은 모델은 아님.

각 layer의 출력 feature map을 이후의 모든 layer에서 사용하기 위해 보존해야 하므로, 학습 중 activation memory 사용량이 증가할 수 있음.

또한 concatenation이 반복되면서 channel 수가 지속적으로 증가하므로, 다음과 같은 문제가 발생할 수 있음.

* 중간 feature map 저장에 필요한 memory 증가
* concatenation 연산에 따른 memory access 비용 증가
* 깊은 Dense Block에서의 연산 복잡도 증가
* 병렬 처리 효율 저하 가능성
* ResNet이나 최신 CNN에 비해 실제 inference 속도가 느릴 가능성

따라서 DenseNet의 parameter 효율성과 실제 실행 속도는 구분하여 평가해야 함.

---

## 14. 핵심 정리

DenseNet은 각 layer가 이전 모든 layer의 feature map을 channel dimension으로 concatenation하여 사용하는 CNN 구조임.

Dense Block에서는 spatial resolution을 유지하면서 feature를 누적하고, Transition Layer에서는 $1\times1$ convolution과 average pooling을 이용하여 channel 수와 spatial resolution을 감소시킴.

각 layer는 growth rate $k$만큼의 새로운 feature를 생성하며, 기존 feature를 지속적으로 재사용함으로써 적은 parameter로 높은 표현력을 확보함.

DenseNet의 가장 중요한 특징은 다음과 같이 요약 가능함.

> DenseNet은 이전 layer의 feature를 단순히 전달하거나 더하는 것이 아니라,
> 모든 이전 feature를 보존한 상태로 concatenation하여 재사용함으로써
> gradient flow와 parameter efficiency를 개선한 CNN 구조임.
