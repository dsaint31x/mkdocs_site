---
title: Adam Optimizer
tags: [optimizer, rmsprop, momentum, adam, gradient ]
---

# ADAptive Moment Estimation (Adam)

**Adaptive Moment Estimation (Adam)** 은 다음이 결합된 Gradient 기반 최적화 알고리즘이다.

* [`RMSProp`](./op_rmsprop.md) 의 **적응적 학습률(adaptive learning rate)** 과
* [`Momentum`](./op_momentum.md) 기법의 **업데이트 방향 누적(momentum-based update)** 을

Adam은 다양한 변형(variants)을 가지며,
현대 딥러닝에서 **가장 널리 사용되는 optimizer** 중 하나이다.

> HuggingFace 의 `Trainer`의 기본 optimizer가 `AdamW` 임.

## Adam 알고리즘 개요

Adam은 **1st moment** 와 **2nd moment** 를 동시에 추정하여,
모델 파라미터 업데이트 시

* gradient 방향의 안정성 확보 (`Momentum`)
* 파라미터별 학습률 자동 조정 (`RMSProp`)

을 함께 반영한다.

여기서 moment 는 확률과 통계 분야에서 사용되는 용어임:

* 확률변수의 분포가 가지는 **형태적 특성 [e.g 중심(mean), 분산(var) 등]** 을 요약하여 표현하는 지표를 의미
* 보다 자세한 건 다음을 참고 [링크](https://dsaint31.tistory.com/256)

## Adam 알고리즘 절차.

$t$번째 iteration에서 Adam의 업데이트는 다음과 같이 정의된다.

1.**1차 모멘트 추정 (Momentum)**

$$
\mathbf{m}_t = \beta_1 \mathbf{m}_{t-1} + (1-\beta_1)\nabla_\theta J(\theta)
$$

2.**2차 모멘트 추정 (RMSProp)**

$$
\mathbf{s}_t = \beta_2 \mathbf{s}_{t-1} + (1-\beta_2)\left(\nabla_\theta J(\theta)\otimes\nabla_\theta J(\theta)\right)
$$

3.**1차 모멘트 bias correction**

$$
\hat{\mathbf{m}}_t = \frac{\mathbf{m}_t}{1-\beta_1^t}
$$

4.**2차 모멘트 bias correction**

$$
\hat{\mathbf{s}}_t = \frac{\mathbf{s}_t}{1-\beta_2^t}
$$

5.**parameters 업데이트**

$$
\theta_{t+1} = \theta_{t} - \eta \frac{\hat{\mathbf{m}}_t}{\sqrt{\hat{\mathbf{s}}_t}+\epsilon}
$$


### 각 단계에 대한 해설

**1번과 2번, 5번 단계** 는 Adam이 `Momentum`과 `RMSProp`를 결합한 알고리즘임을 명확히 보여줌.

* $t$는 iteration number이며, $t=1$부터 시작한다.

#### 1차 모멘트 (Momentum)

* 1번 식은 gradient의 **방향 정보** 를 누적하여 반영.
* 이는 `Momentum` 기법과 동일한 목적을 가지며,
  gradient의 **지수 이동 평균(Exponentially Moving Average, EMA)** 을 사용.
* 여기서 $\beta_1$은 Momentum에서의 감쇠 계수 $\gamma$에 대응.
* 즉, exponentially decaying sum과 exponentially decaying average는  
  상수배 차이만 있을 뿐, 본질적으로 동일한 방향 누적 효과를 가짐.

Momentum의 누적합 표현과 비교하면

$$
\gamma = \frac{\beta_1}{1-\beta_1}
$$
에 해당.

#### 2차 모멘트 (RMSProp)

* 2번 식은 gradient의 제곱을 누적하여 각 파라미터의 **변화 크기(scale)**를 추정.
* 이를 통해 파라미터별로 서로 다른 학습률을 적용하는 
  **adaptive learning rate**가 구현됨.
* $\beta_2$는 `RMSProp`에서 사용되는 decay 계수와 동일한 역할을 수행.

#### Bias 보정 (Bias Correction)

* $\mathbf{m}_0=\mathbf{0}$, $\mathbf{s}_0=\mathbf{0}$으로 초기화되기 때문에,
  학습 초반($t$가 작은 경우)에는 추정된 모멘트들이 **0에 편향(bias)**되는 문제가 발생.
* 이를 보정하기 위해 **3번과 4번의 bias correction 항**이 도입됨.
    * 학습 초기에는 $1-\beta_1^t$, $1-\beta_2^t$가 작아
      $\hat{\mathbf{m}}_t$, $\hat{\mathbf{s}}_t$가 크게 보정됨.
    * 학습이 진행되면서($t$가 커질수록)
      분모가 1에 가까워져 보정 효과는 점차 사라짐.
* 결과적으로,
    * 초기 단계에서는 과도한 0-bias를 상쇄하고
    * 후반 단계에서는 원래의 모멘트 추정값에 기반한 안정적인 업데이트가 이루어짐.

이와 같이 Adam은
**방향 안정성(`Momentum`)** 과 **스케일 적응성(`RMSProp`)** 을 동시에 확보하여,
다양한 문제에서 강건하고 효율적인 최적화 성능을 제공.

## References

[Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980)

---

---

## PyTorch에서의 구현

* PyTorch에서는 `torch.optim.Adam` 클래스를 사용.
* Keras와 마찬가지로 `learning_rate`, `beta_1`, `beta_2`를 명시적으로 지정할 수 있다.

```python
import torch

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001,
    betas=(0.9, 0.999),
    eps=1e-8
)
```

### 주요 파라미터 설명

* `lr`
    * 학습률(learning rate)
    * Keras의 `learning_rate`와 동일
* `betas=(beta_1, beta_2)`
    * 1차 모멘트와 2차 모멘트의 EMA 계수
    * Keras의 `beta_1`, `beta_2`에 각각 대응
* `eps`
    * 분모가 0에 가까워지는 것을 방지하기 위한 작은 상수
    * `Adam` 수식의 $\epsilon$에 해당

## Hugging Face Transformers에서의 구현

Hugging Face의 `Trainer`를 사용할 경우,

* **기본 optimizer는 `AdamW` (Adam with decoupled Weight Decay)** 이며, 
* 일반적으로 직접 `Adam` 객체를 생성하지 않는다.

### 1. Trainer 기본 설정 (권장 방식)

```python
from transformers import TrainingArguments

training_args = TrainingArguments(
    output_dir="./outputs",
    learning_rate=5e-5,
    adam_beta1=0.9,   # AdamW 임을 잊지 말 것
    adam_beta2=0.999,
    adam_epsilon=1e-8,
)
```

* `Trainer` 내부에서 자동으로 `AdamW` optimizer가 생성됨
* weight decay가 decoupled된 Adam 변형을 사용

### 2. Optimizer를 명시적으로 생성하는 경우

`Trainer`에 optimizer를 직접 생성하여 전달할 수 있음.

```python
from transformers import AdamW

optimizer = AdamW(
    model.parameters(),
    lr=5e-5,
    betas=(0.9, 0.999),
    eps=1e-8,
    weight_decay=0.01
)
```

이 경우 `Trainer` 생성 시 다음과 같이 전달한다.

```python
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    optimizers=(optimizer, None)
)
```

### 참고: Adam vs. AdamW (정리)

* **PyTorch의 `Adam`**
    * 전통적인 Adam 알고리즘 구현
    * weight decay가 L2 regularization 형태로 결합됨
* **Hugging Face의 기본 `AdamW`**
    * **weight decay** 를 **gradient 업데이트와 분리** (decoupled) 
    * "loss function에 더해지는 L2 regularization" 과 달리 weight decay를 분리하여 적용 (직접 parameters를 감쇠시킴) 
  * **Transformer 계열 모델에서 일반적으로 더 안정적인 성능 제공**

따라서,

* 단순 실험이나 직접 학습 루프 작성 시에는 `torch.optim.Adam` 을 사용할 수 있으나, 
* Hugging Face `Trainer` 기반 학습에서는 기본 설정의 `AdamW` 를 사용하는 것이 일반적인 선택이다.


## Keras에서의 구현.

아래와 같이 `Adam` optimizer 객체를 생성하여 `fit`에 넘겨주면 됨.

```Python
optimizer = tf.keras.optimizers.Adam(learning_rate=0.001, 
                                     beta_1=0.9,
                                     beta_2=0.999)
```

* momentum decay hyperparameter $\beta_1$ : `0.9`
* scaling decay hyperparameter $\beta_2$ : `0.999`
* the smoothing term $\epsilon$ : `1e-7`
