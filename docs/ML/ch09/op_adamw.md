---
title: AdamW Optimizer
tags: [optimizer, adam, adamw, gradient, moment, weight-decay, transformer ]
---

# AdamW

**Adam with decoupled Weight Decay** 는 Transformer 학습에서 가장 널리 사용되는 optimizer 임:

* 기존 Adam의 구조적 문제점 개선:
   * L2 regularization이 gradient 기반 업데이트에 섞여 들어가
   * adaptive learning rate와 weight decay가 결합되어 의도한 정규화 효과가 왜곡됨
* AdamW의 핵심 아이디어:
   * Weight decay를 gradient 업데이트와 완전히 분리(decoupled)
   * Parameter 업데이트 이후에 별도로 decay 적용
* 결과:
   * 정규화 효과가 이론적으로 명확해짐
   * 일반화 성능 향상
   * 현재 Transformer 계열 및 HuggingFace Trainer의 기본 optimizer

> moment, momentum, 그리고 weight decay의 정확한 이해 필요

## 1. Adam 의 등장

### 1.1. 출발점: SGD와 최적화의 기본 문제

[SGD (Stochastic Gradient Descent)](https://dsaint31.tistory.com/633) 은 다음과 같이 정의됨:

$$
\theta_{t+1} = \theta_t - \eta g_t,
\quad
g_t = \nabla_\theta \mathcal{L}(\theta_t)
$$

[SGD](https://dsaint31.tistory.com/633)의 구조적 한계는 다음과 같음:

* gradient 를 매순간 일부 샘플로 구함: 안정적인 gradient의 방향을 구하기 어려움.
* 현재 iteration에 적절한 learning ratio를 구할 수 없음 (고정)

이 한계를 해결하기 위해 **크게 두 종류의 개선책들** 이 등장.

1. 방향을 안정화하는 방법 : `Momentum`
2. 적절한 learning ratio (~step size)를 찾는 방법: [`Adagrad`](./op_adagrad.md), [`RMSProp`](./op_rmsprop.md)


두 방향으로 개발되던 중, [`Momentum`](./op_momentum.md)과 [`RMPProp`](./op_rmsprop.md) 를 1st moment와 2nd moment 를 통해 합쳐서 높은 성능 개선을 이룬 것이 Adam 임.

### 1.2. 참고: 핵심 용어 정리: moment, momentum

#### 1.2.1 momentum: 운동량 (물리적 개념)

물리학에서 momentum은 운동량 : $p = m v$

* 방향성과 관성을 가진 물리량
* **$m$ 이나 $v$가 크면 쉽게 바뀌지 않는다 (관성)**

이를 optimization 에 도입한 것이 [**Momentum SGD (줄여서 Momentum)**](./op_momentum.md) :

$$ \begin{aligned}v_t &= \beta v_{t-1} + (1-\beta) g_t \\ 
\theta_{t+1} &= \theta_t - \eta v_t \end{aligned}$$

여기서:

* $v_t$ 는 velocity 로 parameters 가 최적화 되기 위한 방향 과 크기를 가진 벡터를 의미: 이를 통해 parameter vector 가 변경됨.
* $g_t$ 는 gradient 로 가속도 처럼 현재 parameter vector가 최적화되기 위해 변해야하는 방향을 가리키는 벡터.
* $\beta$ 는 일종의 관성의 정도로 현재의 gradient 를 velocity에 반영할지를 결정함

> [Momentum SGD](./op_momentum.md)는  
> **의도적으로 운동량 모델을 이용하여  
> Loss를 높이(height)라고 생각해서  
> 중력에 의해 낮은 지점으로 내려오는 방법을 최적화라고 생각하여 구현한 방식**

#### 1.2.2 moment: 통계적 모멘트

통계에서 [moment](https://dsaint31.tistory.com/256)는 **확률분포의 요약 통계량**.

확률변수 $X$에 대해:

* 1차 moment: $\mathbb{E}[X]$ (mean)
* 2차 moment: $\mathbb{E}[X^2]$ (에너지, 스케일)
* 분산: $\mathbb{E}[X^2] - (\mathbb{E}[X])^2$ 로 일종의 2nd moment

### 1.3. Adam의 핵심 아이디어

[Adam](./op_adam.md)은 이름 그대로 **Adaptive Moment Estimation** 즉,

* Adam은 momentum을 "그대로 쓰는" 알고리즘이 아니라,
* **1st moment와 2nd moment를 adaptive 하게  추정하는 알고리즘** 이다.

1st moment는 EMA를 통한 Momentum 알고리즘의 효과를 가져오고,  
2nd moment는 지금까지 적용된 parameter 각각의 변화의 정도를 고려하여 adaptive하게 각 parameter에 적용되는 step size 를 결정하게 함.

#### 1.3.1. 1차 모멘트: gradient 평균 추정

Adam의 1st moment 는 다음을 추정하는 것임:

$$
m_t \approx \mathbb{E}[g_t]
$$

이를 **[지수 이동 평균(EMA)](https://dsaint31.tistory.com/860)** 으로 계산.

$$
m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t
$$

이 의미는 결국, 

* 지금까지의 여러 iteration에서의 gradient의 평균(EMA)적 방향을 의미함(Momentum처럼 과거 gradients의 방향을 고려)
* 결국 수식 상 **[Momentum SGD](./op_momentum.md)의 velocity 업데이트와 형태가 동일** 해짐.

#### 1.3.2. 2차 모멘트: gradient 에너지 추정

Adam의 2nd moment는 다음을 추정한다.

$$v_t \approx \mathbb{E}[g_t^2]$$

이의 MA 형태는 다음과 같다.

$$v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2$$

이 의미는 다음과 같음:

* gradient 크기의 평균 제곱. (gradient 벡터의 제곱)
* gradient 벡터에서의 각 요소별로 제곱을 하여 각 요소(~parameter별 축)에서의 **크기(scale)** 를 구함. 
* 이들을 EMA로 처리하면 지금까지 parameter에 대해 가해진 변화량을 가늠할 수 있기 때문에 Parameter별로 다른 adaptive step size 들을 결정하는데 사용 가능. 

이를 다음과 같이 적용한다 (`RMSProp`의 아이디어)

* gradient 벡터에서 제곱한 요소가 큰 축에 해당하는 parameter: step size 감소
* gradient 벡터에서 제곱한 요소가 작은 축에 해당하는 parameter : 변화될 step size 증가

parameter 별 adaptive learning rate 제공

> 지금까지 gradient의 변화량을 적용했던 Adagrad의 경우 매우 불안정했던 단점을 가짐.  
>    
> 이를 개선하기 위해 RMSProp에선  
> gradient 벡터의 2nd moment에 대해 EMA를 통해 대처함.
> 이를 `Adam`도 채택.

#### 1.3.3. Adam 업데이트의 구조적 해석

Bias correction을 적용하면,

$$
\hat{m}_t = \frac{m_t}{1-\beta_1^t}
\quad
,
\quad
\hat{v}_t = \frac{v_t}{1-\beta_2^t}
$$

최종 업데이트는 다음과 같음:

$$
\theta_{t+1} =  \theta_t - \eta \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon}
$$

* 분자 $\hat{m}_t$: **어디로 가야 하는가 (방향)**
* 분모 $\sqrt{\hat{v}_t}$: **얼마나 조심해서 가야 하는가 (step size)**

> Adam은  
> **방향은 1차 moment**,  
> **step size는 2차 moment** 로 제어.

### 2. Weight Decay

#### 2.1. 정의

**Weight decay는 파라미터의 크기를 현재 크기에 따라 일정 비율로 지속적으로 줄이는 L2-Regularization 을 구현하는 기법** 임.

Model의 over-fitting을 막고 general performance 를 향상시키기 위해 모델의 parameter가 지나치게 커지지 않게 해주는 방법을 Regularization 이라고 하는데, Weight decay는 이 중 L2 Regularization 을 구현하는 방법임.

#### 2.2. L2 regularization과의 관계

가장 전통적인 Regularization인 L2 regularization 은 loss에 다음 항을 추가하는 것임:

$$
\mathcal{L}'(\theta) = \mathcal{L}(\theta) + \frac{\lambda}{2}|\theta|^2
$$

이에 따른 gradient는

$$
\nabla_\theta \mathcal{L}'=g_t + \lambda \theta_t
$$

이는 SGD에서의 업데이트를 다음과 같이 표현하게 함:
$$
\theta_{t+1}= (1 - \eta \lambda)\theta_t - \eta g_t
$$

* 매 step마다 parameter 가 일정 비율로 감소함.

즉, [SGD](https://dsaint31.tistory.com/633)에선 L2 regularization이나 **weight decay** 는 동일하다.

> AdamW 이전의 대부분이 Adam variants들은 weight decay를 L2 regularization처럼 loss에 parameter의 L2-norm 을 더하는 형태를 채택함.

#### 2.3. Adam에서 Weight decay가 문제가 되는 이유

Adam에서 위 gradient를 그대로 사용하면,

$$
\theta_{t+1} = \theta_t - \eta \frac{g_t + \lambda \theta_t}{\sqrt{v_t} + \epsilon}
$$

여기서 문제는 분모 임:

* $\sqrt{v_t}$  는 각 parameter 별로 다름
* 이는 $\displaystyle \lambda \theta_t$ 도 $\displaystyle \frac{\lambda \theta_t}{\sqrt{v_t}}$ 로 스케일링됨을 의미.

즉, 그 결과로

* weight decay 강도가 각 parameters 마다 달라지는 효과가 발생함.
* regularization이 원하는 단순한 "크기 억제" 가 아닌, "gradient vector" 가 가리키는 방향 자체에 대한 왜곡이 일어나는 셈임.


## 2. AdamW: Regularization 을 분리

AdamW의 핵심 아이디어는 다음과 같음:

* **"moment 기반 최적화"** 와 **"L2-Regularization"**은 서로 다른 역할임.
* 그러므로 분리하여 `Adam` step과 `Weight decay` step으로 나눈다.

### 2.1. Adam step (moment 기반 최적화)

$$
\theta_t' = \theta_t - \eta \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon}
$$

* 순수하게 loss 감소만 담당
* moment 추정 그대로 유지

### 2.2 Weight decay step 

$$
\theta_{t+1} = \theta_t' - \eta \lambda \theta_t
$$

* adaptive scaling과 완전히 독립
* 파라미터 크기에 직접 일관되게 적용

### 2.3. 최종 수식

$$
\theta_{t+1} =  \theta_t - \eta \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon} - \eta \lambda \theta_t
$$

## 3. AdamW의 개념적 위치

`Adam`:

* gradient 분포의 moment 추정
* optimization dynamics 설계

`AdamW`:

* moment 기반 최적화 유지
* regularization  분리

---

---


## 4. Notes

**Q1. L2 regularization과 weight decay는 완전히 같은가?**

**`SGD`에서는 사실상 동일함.**
**`Adam` 같은 adaptive optimizer에서는 달라짐.**

* L2 regularization: loss에 항을 추가
* Weight decay: 파라미터를 직접 감쇠

AdamW는 **weight decay를 통해 L2 regularization의 원래 동작을 non-adaptive optimizer와 같이 정확히 구현한 방식** 임.

---

**Q2. 왜 bias나 LayerNorm에는 weight decay를 적용하지 않는가?**

* `bias`와 `LayerNorm` 파라미터는 **스케일을 조정하는 역할**
* 크기를 줄이면 표현력이 직접적으로 손상됨
* 일반화(or Generalization Performance)와 거의 무관

그래서 다음이 성립:

* `weight` 행렬 : decay 적용
* `bias` / `LayerNorm` : decay 제외

---

**Q3. Weight decay는 일반화에 어떤 영향을 주는가?**

* 파라미터 크기를 억제
* 결정 경계를 단순화
* 입력 변화에 대한 민감도 감소

즉, 다음이 성립:

> weight decay는
> **최적화를 돕는 기법이 아니라,
> 모델의 형태를 제한하여 일반화를 유도하는 구현기법**.

---

---

## 5. 요약 (1)

* `Adam`은 gradient의 adaptive moment 를 추정하는 알고리즘이고,
* `AdamW`는 여기에 `weight decay`를 분리하여
* `L2 regularization`의 의미를 회복한 variant임.

---

---

## 6. HF 및 PyTorch 에서 사용.

* **PyTorch**:
    * `torch.optim.AdamW` 를 직접 사용
* **Hugging Face Transformers**:
    * `Trainer` 사용 시 : 내부에서 `AdamW` 자동 구성
    * 커스텀 학습 루프 : PyTorch `AdamW` 직접 사용 추천(for Transformers 모델)

> 둘 다 **동일한 AdamW (decoupled weight decay)** 임.

### 6.2. PyTorch 사용법

#### 6.2.1 기본형

```python
import torch

optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=5e-5,
    betas=(0.9, 0.999),
    eps=1e-8,
    weight_decay=0.01
)
```

* `lr` : learning rate
* `betas` :
    * $\beta_1$ : 1차 moment EMA
    * $\beta_2$ :  2차 moment EMA
* `weight_decay` : **decoupled weight decay 계수**

> 여기서 `weight_decay` 는  
> gradient에 섞이지 않고 **파라미터 감쇠로 직접 적용** 됨.


#### 6.2.2 중요 포인트 (`bias` / `LayerNorm` 제외)

Transformer 계열에서는 보통 다음과 같이 사용됨:

```python
decay_params = []
no_decay_params = []

for name, param in model.named_parameters():
    if param.requires_grad:
        if name.endswith(".bias") or "LayerNorm.weight" in name:
            no_decay_params.append(param)
        else:
            decay_params.append(param)

optimizer = torch.optim.AdamW(
    [
        {"params": decay_params, "weight_decay": 0.01},
        {"params": no_decay_params, "weight_decay": 0.0},
    ],
    lr=5e-5
)
```

* `bias`, `LayerNorm` scale 파라미터는
* 크기를 줄여도 일반화에 거의 도움 없음
* 오히려 표현력만 손상

> 이 방법이 **HF 공식 레시피** 임.

### 6.3. HF 에서 AdamW 사용법

#### 6.3.1 Trainer 사용 (권장)

```python
from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir="./results",
    learning_rate=5e-5,
    weight_decay=0.01, # AdamW의 기본 decoupled weight decay 는 0.0 으로 꺼진상태.
    per_device_train_batch_size=8,
    num_train_epochs=3,
    logging_steps=500,
    save_steps=500,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

trainer.train()
```

* `Trainer`는 내부적으로
    * **AdamW**
    * `bias` / `LayerNorm` weight decay 제외
      를 자동으로 처리.
* 사용자는 `weight_decay` 만 지정하면 충분.

> **대부분의 HF 파인튜닝은 이걸로 충분**.

#### 6.3.2 Trainer 내부 동작.

HF Trainer는 내부적으로 대략 다음을 수행:

* Optimizer: `torch.optim.AdamW`
* Parameter grouping:
    * `weight`  : decay
    * `bias` / `LayerNorm` : no decay
* Learning rate scheduler:
    * linear / cosine / warmup 등

즉, **직접 `AdamW`를 쓰는 것과 동일한 결과**.

### 6.4. HF에서 Custom Optimizer 쓰기

Trainer를 쓰되 `optimizer`를 직접 지정할 수도 있음.

```python
optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=3e-5,
    weight_decay=0.01
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    optimizers=(optimizer, None),
)
```

* `scheduler`를 직접 쓰고 싶다면 `(optimizer, scheduler)` 형태로 전달
* 연구용, 실험용으로 자주 사용

### 6.5. HF / PyTorch의 구현

> 앞서 살펴본 내용과 같음: 코드만 보는 경우를 위해 다시 반복.

PyTorch와 HF에서 실제로 수행되는 update는 개념적으로 다음과 같음:

**1.Adam step (moment 기반)**

$$   
\theta_t' = \theta_t - \eta \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon}
$$

**2.Weight decay step (decoupled)**

$$
\theta_{t+1} = \theta_t' - \eta \lambda \theta
$$ 

* 구현에서는 보통 $\theta_t'$ 기준으로 `decay`를 적용하지만,
* 차이는 $\mathcal{O}(\eta^2)$  이므로 거의 차이 없음.

### 6.6. PyTorch vs. HF

| 상황                  | 추천                      |
| :---:  | :---: |
| 표준 Transformer 파인튜닝 | HF `Trainer`              |
| 실험적 optimizer 수정    | PyTorch `AdamW`           |
| 논문 재현               | PyTorch 직접              |
| 대규모 분산 학습          | HF `Trainer` + `Accelerate` |

### 6.7. 체크리스트

* `AdamW` 쓸 때
    * `weight_decay` ≠ 0 확인
* `bias` / `LayerNorm` decay 제외
* ***learning rate warmup*** 함께 사용 (HF 기본)
    * `Adam` 계열은 2nd moment 추정이 초반에 안정이 잘 안됨.
    * 때문에 극초반에는 작은 `lr`로 출발하고 
    * 2nd moment 가 안정되면 점진적으로 증가하다가,
    * parameters가 최적화에 가까워지면 step size가 줄어들어야 함.
    * 때문에 `learning rate warmup`과 궁합이 좋음.
* `Adam` 대신 `AdamW` 인지 확인 (특히 옛 코드)

---

---

## 요약 (2)

* **PyTorch `AdamW`** 와 **HF `AdamW`는 동일**
* HF `Trainer`는
    * `AdamW`
    * parameter grouping
    * `scheduler`
    를 자동으로 처리
* AdamW의 핵심은
    * **moment 추정과 weight decay의 분리**
