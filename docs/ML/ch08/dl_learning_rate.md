---
title: Learning Rate Tuning and Scheduling
tags: [Learning Rate, Hyperparameter, Optimization, Deep Learning, Training]
---

# Learning Rate Range Test

> Learning rate는  
> 모델 학습 과정에서 
> **parameter를 얼마나 크게 업데이트할지를 결정** 하는  
> 중요한 hyperparameter임. 

Learning rate가 

* 너무 작으면 학습이 매우 느려지고, 
* 너무 크면 loss가 불안정하게 증가하거나 발산할 수 있음. 
* 따라서 효율적이고 안정적인 학습을 위해 적절한 learning rate를 선택하는 것이 중요함.

참고자료: [Learning rate 의 중요성](https://dsaint31.tistory.com/633#Learning%20rate%20%EC%9D%98%20%EC%A4%91%EC%9A%94%EC%84%B1-1-7)

또한 하나의 learning rate를 처음부터 끝까지 고정해서 사용하는 것은 일반적으로 최선의 방법이라고 보기 어려움.

일반적으로 다음과 같은 방식이 권장됨:

* 초반에는 비교적 큰 learning rate를 사용하여 빠르게 좋은 영역으로 이동하고,
* 후반에는 learning rate를 줄여 parameter가 optimum 근처에 안정적으로 settle down 하도록 조정.

위와 같이,  

> training 중 learning rate를 일정한 규칙에 따라 조절하는 전략을
> **Learning Rate Schedule** 또는 **Learning Rate Scheduling** 이라고 함.

---

---

## Learning rate range test

아래에서 기술된 Learning rate range test는 ***적절한 learning rate 범위를 찾기 위한 실험적 방법*** 임. 

* 이 방법의 목적은 최종 모델을 학습시키는 것이 아니라, 
* learning rate 변화에 따라 loss가 어떻게 반응하는지 관찰하고
* 이를 통해 **적절한 초기 learning rate를 찾는 것** 임.

---

### 절차

1. 모델을 랜덤 초기화함.
2. 매우 매우 작은 learning rate에서 학습을 시작함.
3. 학습의 매 iteration마다 learning rate를 일정 비율로 증가시킴.
4. 매우 큰 learning rate 에 이르면 학습 종료.
4. 각 iteration 에서의 loss를 기록함.
5. loss (y축)를 learning rate(x축)에 대한 함수로 시각화함.
6. loss가 감소하다가 **다시 증가( or 발산) 하기 시작하는 지점 (=Turning point)** 을 찾음.
7. 해당 turning point 에서의 learning rate 보다 약간 작은 (1/10 정도로 경험적인 정도를 언급한 문헌 있음) learning rate를 최적의 초기 learning rate로 선택.
8. 모델을 다시 초기화한 뒤, 선택된 초기 learning rate로 정상적인 학습을 수행함.

> 위에서 다룬 Learning rate range test는
> ***1cycle scheduling*** 에서 maximum learning rate $\eta_1$을 정할 때 자주 사용됨.

---

---

## Learning rate range test의 원리

1. Learning rate가 너무 작으면 parameter update가 매우 작아 loss가 거의 감소하지 않음.
2. Learning rate가 적절한 범위에 들어가면 parameter가 효과적으로 update되어 loss가 빠르게 감소함.
3. Learning rate가 지나치게 커지면 update 폭이 과도해져 loss가 증가하거나 발산함.
4. 따라서 loss가 감소하다가 다시 증가하기 시작하는 지점을 통해 학습이 불안정해지는 learning rate 범위를 추정할 수 있음.

> 일반적으로 최종 학습에는 해당 지점보다 약간 1/10 정도 작은 learning rate를 사용함.

---

---

## Learning rate range test 사용 시 주의사항

* 이는 Learning rate마다 별도의 모델을 생성하여 각각 수 iteration씩 학습하는 방식이 아님.
    * 엄밀하게는 이 방식이 공정하다고 볼 수 있으나, 실제 적용하기에 비효율적임. 
    * 하나의 모델을 사용해 수백 iteration 동안 학습하면서 learning rate를 점진적으로 증가시키는 방식으로도 충분함.
    * 이는 초기 학습이 매우 적은 Learning rate로 이루어지기 때문이므로, 반드시 매우 작은 Learning rate 로 시작해야 함.
* Learning rate는 보통 선형 증가보다 매 iteration마다 일정 비율을 곱하는 지수적 증가 방식을 사용함.
    * 예를 들어 $10^{-5}$에서 시작하여 500 iteration 동안 $10$까지 증가시키려면, 매 iteration마다 다음 값을 learning rate에 곱함.

$$
\left(\frac{10}{10^{-5}}\right)^{1/500}
$$

---

---

## Learning rate range test 의  한계

* 엄밀히 애기하면, Learning rate range test로 얻은 결과는 특정 모델, 데이터셋, optimizer, batch size 설정에 대해서만 유효함.
    * Batch size가 크게 변경되면 gradient의 분산과 update 특성이 달라지므로 적절한 learning rate 범위도 달라질 수 있음.
    * Optimizer를 SGD에서 Adam으로 변경하거나 momentum 등의 hyperparameter를 변경한 경우에도 결과가 달라질 수 있음.
    * 모델 구조나 심지어 데이터 전처리가 크게 바뀐 경우에도 다시 수행하는 것이 바람직함.

즉, 학습 설정이 크게 변경되었다면 learning rate range test를 다시 수행하여 적절한 learning rate 범위를 재탐색하는 것이 좋음.

> 다만
> batch size나 기타 설정이 소폭 변경된 경우에는
> 기존 결과를 초기값으로 활용한 뒤, 필요할 때만 추가 실험을 수행할 수 있음.

---

---

---

# Learning Rate Scheduling 의 중요성

Constant learning rate는 학습 전체 과정에서 같은 step size를 사용함.

* 예를 들어 learning rate를 \$\eta = 0.01$로 설정하면,
* training이 시작될 때도 $\eta = 0.01$, training이 끝날 때도 $\eta = 0.01$ 임.

문제는 training의 초반과 후반에서 필요한 learning rate의 성격이 다르다는 점임.

* 초반에는 parameter가 optimum에서 멀리 떨어져 있을 가능성이 큼.
    * 이때는 비교적 큰 learning rate를 사용해야 loss를 빠르게 줄일 수 있음.
* 반대로 후반에는 parameter가 optimum 근처에 도달해 있을 가능성이 큼.
    * 이때도 learning rate가 크면 optimum 주변을 계속 지나치면서 진동할 수 있음.
    * 따라서 후반에는 learning rate를 줄여야 parameter가 더 정밀하게 조정될 수 있음.
 
이를 반영한 **Learning Rate Scheduling의 핵심 아이디어** 는 다음과 같음.

* 처음에는 빠르게 움직이고,
* 나중에는 조심스럽게 움직이도록
* learning rate를 조절하는 것.

---

---

## Learning Rate Scheduling의 분류

Learning Rate Scheduling은 training 중 learning rate를 고정하지 않고, 학습 단계에 맞게 조절하는 방법임.

* 중요한 것은 learning rate가 training 전체에서 항상 같은 값일 필요가 없다는 점임.
* 초반에는 exploration을 위해 크게, 후반에는 convergence를 위해 작게 사용하는 것이 기본 원리임.
   * 필요하다면 초반에는 warm-up으로 안정화하고,
   * 전체 schedule 안에서는 decay를 통해 안정적으로 수렴시키며,
   * plateau가 문제가 될 때는 cyclic 또는 restart 방식을 사용할 수 있음.


대표적인 learning rate schedule은 다음과 같이 분류할 수 있음.

| 분류                            | 핵심 기준                                             | 대표 기법                                                    |
| ----------------------------- | ------------------------------------------------- | -------------------------------------------------------- |
| Monotonic Decay Scheduling    | training이 진행될수록<br/>learning rate를 전반적으로 감소시킴       | Exponential Decay, Power Decay,<br/>Piecewise Constant,<br/>Cosine Annealing |
| Adaptive Decay Scheduling<br/>Performance Scheduling  | validation metric 등<br/>학습 결과를 보고 learning rate를 감소시킴 | ReduceLROnPlateau                |
| Warm-up + Decay Scheduling    | 초반에는 learning rate를 증가시키고,<br/>이후에는 다시 감소시킴           | Warm-up + decay,<br/>1cycle                                  |
| Cyclical / Restart Scheduling | learning rate 증가와 감소를<br/>여러 번 반복하거나 restart 시켜<br/> plateau나 local optimum 탈출 유도 | Cyclical LR,<br/>Cosine Annealing with Warm Restarts         |

**Monotonic Decay Scheduling**

* learning rate를 시간이 지남에 따라 전반적으로 줄이는 GD에서부터 사용된 고전적인 방식.
* 다음의 대표적인 방법들이 여기에 속함:
* Exponential Scheduling, Power Scheduling, Piecewise Constant Scheduling, Cosine Annealing
* 이들 모두 감소되는 방식에서 각각 차이가 잇으나모두 전체적으로는 learning rate를 낮추는 schedule임.

**Adaptive Decay Scheduling** 

* 이 방식에서는 감소 시점이 미리 정해져 있지 않음.
* Validation loss나 validation accuracy 같은 metric을 보고,
* 성능 개선이 정체되면 learning rate를 줄임.

**Warm-up + Decay Scheduling**

* 초반에는 learning rate를 작은 값에서 시작해 증가시키고,
* 이후에는 다시 감소시키는 방식임.
* Warm-up은 단독 schedule이라기보다는 보통 전체 schedule의 초반 phase로 사용됨.

대표적으로 1cycle Scheduling 이 있음.

* 이는 반복 cycle이라기보다
* 훈련 전체를 1cycle 로 보고,
* 이를 하나의 큰 warm-up + decay schedule로 구성시킴.

**Cyclical / Restart Scheduling** 

* learning rate를 한 번 줄이고 끝내는 방식이 아님.
* Learning rate를 여러 번 다시 키우거나,
* 증가와 감소를 반복함
* 이는 optimizer가 plateau나 local optimum에서 효과적으로 벗어날 수 있게 해 줌.

---

### Monotonic Decay Scheduling

Monotonic Decay Scheduling은 training이 진행될수록 learning rate를 전반적으로 감소시키는 방식임.

> 초반에는 큰 learning rate로 빠르게 이동하고,
> 후반에는 작은 learning rate로 안정적으로 수렴시킴.

이 계열에는 다음 방식들이 포함됨.

* Exponential Scheduling
* Power Scheduling
* Piecewise Constant Scheduling
* Cosine Annealing

이들은 모두 learning rate를 줄이는 방식이라는 점에서 decay schedule임.

차이는 learning rate를 어떤 모양으로 줄이는가에 있음.

| 기법                            | 감소 방식                   |
| ----------------------------- | ----------------------------- |
| Exponential Scheduling        | 일정 비율로 계속 감소           |
| Power Scheduling              | 초반에는 빠르게 감소하고, 후반에는 점점 느리게 감소 |
| Piecewise Constant Scheduling | 특정 시점마다 계단식으로 감소           |
| Cosine Annealing              | cosine curve를 따라 부드럽게 감소      |

#### 1. Exponential Decay Scheduling

Exponential Scheduling은 learning rate를 일정한 비율로 계속 감소시키는 방식임.
$$
\eta(t) = \eta_0 \cdot 0.1^{t/s}
$$
where,

* $\eta_0$: initial learning rate
* $t$: 현재 step 또는 epoch
* $s$: learning rate가 10분의 1로 줄어드는 주기

PyTorch에서는 `torch.optim.lr_scheduler.ExponentialLR`을 사용할 수 있음.

```python
optimizer = torch.optim.SGD(model.parameters(), lr=0.05)

scheduler = torch.optim.lr_scheduler.ExponentialLR(
    optimizer,
    gamma=0.9,
)
```

* `gamma`는 learning rate에 매 epoch 곱해지는 값임.
* `gamma=0.9`이면 epoch가 끝날 때마다 learning rate가 이전 값의 90%가 됨.

주로, `scheduler.step()`은 epoch 마다 한번 호출됨.

#### 2. Power Decay Scheduling

Power Scheduling은 iteration number $t$에 따라 learning rate를 다음과 같이 감소시키는 방식임.
$$
\eta(t) = \frac{\eta_0}{(1 + t/s)^c}
$$

where,

* $\eta_0$: initial learning rate
* $t$: 현재 iteration (=step, single mini-batch update)
* $s$: learning rate 감소 속도를 조절하는 step scale
* $c$: power 값

보통 $c = 1$로 설정하는 경우가 많음.

#### 3. Piecewise Constant Scheduling

Piecewise Constant Scheduling은 일정 구간마다 learning rate를 직접 지정하는 방식임.

예를 들어 다음과 같이 설정할 수 있음.

* 처음 5 epoch 동안 $\eta = 0.1$
* 이후 50 epoch 동안 $\eta = 0.001$
* 이후 나머지 epoch 동안 $\eta = 0.0001$

즉, learning rate를 연속적으로 줄이는 것이 아니라, 특정 시점에서 계단식으로 줄임.

수식으로 쓰면 다음과 같음:
$$
\eta(t) =
\begin{cases}
0.1 & \text{if } 0 \le t < 5 \
0.001 & \text{if } 5 \le t < 55 \
0.0001 & \text{if } 55 \le t
\end{cases}
$$

이 방식은 Step Decay 또는 Step-based Scheduling이라고도 부름.

* 장점은 단순하다는 것임.
* 단점은 언제 learning rate를 낮출지, 얼마나 낮출지를 사람이 직접 정해야 한다는 것임.

PyTorch에선 `MultiStepLR` 로 지원함.

#### 4. Cosine Annealing

Cosine Annealing은 cosine function을 이용하여 learning rate를 부드럽게 감소시키는 방식.
$$
\eta(t) = \eta_{\min} + \frac{1}{2}(\eta_{\max} - \eta_{\min})
\left(1 + \cos\left(\frac{t}{T_{\max}}\pi\right)\right)
$$
where,

* $\eta_{\max}$: maximum learning rate
* $\eta_{\min}$: minimum learning rate
* $T_{\max}$: cosine schedule이 한 번 끝나는 총 step 수. learning rate가 최댓값에서 최솟값까지 내려가는 데 필요한 `scheduler.step()` 호출 횟수
* $t$: 현재 epoch 또는 step

> 보통 epoch 단위로 감소시키는 처리가 일반적임

Cosine Annealing은 

* 초반과 중반에는 learning rate를 비교적 높게 유지하다가,
* 후반부에 minimum learning rate에 가까워지도록 부드럽게 감소시킴.

PyTorch에서는 `CosineAnnealingLR`을 사용할 수 있음.

```python
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
    optimizer,
    T_max=20,
    eta_min=0.001,
)
```

참고로  

* Cosine Annealing 자체는 단일 cosine curve로 learning rate를 줄이는 방식이나,
* Ilya Loshchilov와 Frank Hutter가 2016년에 제안한 SGDR, 즉 Stochastic Gradient Descent with Warm Restarts 논문에서는
* cosine decay 후 learning rate를 다시 올리는 warm restart까지 포함하는 응용버전도 있음

---

### Adaptive Decay Scheduling

Adaptive Decay Scheduling은 learning rate의 감소 시점이 미리 고정되어 있지 않은 방식임.
(Performance Scheduling 이라고도 불림)

* 즉, epoch 또는 step 번호만으로 learning rate가 결정되지 않음.
* 대신 validation loss, validation accuracy 같은 training 결과를 관찰하고,
* 이를 확인한 결과 model의 성능 개선이 정체되면 learning rate를 줄임.

예를 들어 validation loss를 기준으로 한다면 다음과 같이 동작함.

1. 매 epoch마다 validation loss를 계산함.
2. validation loss가 계속 감소하면 learning rate를 유지함.
3. validation loss가 일정 기간 개선되지 않으면 learning rate를 줄임.

PyTorch에서는 `torch.optim.lr_scheduler.ReduceLROnPlateau` 가 대표적인 Performance Scheduling의 구현물임:

```python
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer,
    mode="min",
    patience=2,
    factor=0.1,
)
```

* `mode` : metric을 maximize할지 minimize할지 결정
    * validation loss를 기준으로 하면 loss는 작을수록 좋으므로 `mode="min"`을 사용함.
    * validation accuracy를 기준으로 하면 accuracy는 클수록 좋으므로 `mode="max"`를 사용함.
* `patience` : metric이 개선되지 않아도 기다릴 epoch 수 
* `factor`   : learning rate를 줄일 때 곱하는 값

PyTorch의 Performance Scheduling에서는 scheduler의 `step()`을 통해 validation metric을 넘겨줌:

```python
for epoch in range(n_epochs):
    model.train()

    for X_batch, y_batch in train_loader:
        # training code
        pass

    model.eval()

    val_loss = evaluate_loss(model, valid_loader)

    scheduler.step(val_loss)
```

`ReduceLROnPlateau`는 

* 일반적인 scheduler처럼 단순히 `scheduler.step()`만 호출하는 것이 아니라,
* 반드시 monitoring할 metric을 인자로 전달해야 한다는 점임.

---

### Warm-up + Decay Scheduling

Warm-up + Decay Scheduling은 

* training 초반에 learning rate를 작은 값에서 시작해 점진적으로 증가시킨 뒤,
* 이후에는 다시 감소시키는 방식임.

$$
\text{low LR} \rightarrow \text{high LR} \rightarrow \text{low LR}
$$

* warm-up은 초반 phase 를 가리킴.

#### 1. Learning Rate Warm-up

Warm-up은 training 초반에 learning rate를 바로 크게 사용하지 않고, 작은 값에서 시작해 점진적으로 증가시킴

이는 다음과 같은 상황에서 특히 유용함.

* training 초반 loss가 불안정한 경우
* gradient descent가 초반에 튀는 경우
* 매우 큰 batch size를 사용하는 경우
* recurrent neural network처럼 학습이 불안정하기 쉬운 경우
* ***Transformer 계열 model처럼 초반 안정화가 중요*** 한 경우

DL의 경우 초기 parameter 상태에서는 loss landscape의 불안정한 영역에 있을 수 있음.

* 이때 처음부터 큰 learning rate를 사용하면 parameter가 안정적인 방향으로 내려가지 못하고 크게 흔들릴 수 있음.
* Warm-up은 작은 learning rate로 시작해 gradient descent가 안정적인 영역에 들어갈 시간을 준 뒤, 이후 더 큰 learning rate를 사용하게 함.

이같은 warm-up 이후에는 cosine decay, linear decay, exponential decay, performance scheduling 등을 붙여 learning rate를 다시 낮춤.

PyTorch에서는 `LinearLR`을 사용하여 warm-up을 구현할 수 있음.

```python
warmup_scheduler = torch.optim.lr_scheduler.LinearLR(
    optimizer,
    start_factor=0.1,
    end_factor=1.0,
    total_iters=3,
)
```

* 원래 learning rate의 10%에서 시작(`start_factor`)
* 3 epoch (`total_iters`) 동안
* 100% (`end_factor`)까지 선형적으로 증가시킴.

Warm-up 이후에는 다른 scheduler (주로 monotonic decay scheduling)를 사용하는 방식임.

#### 2. 1cycle Scheduling

1cycle Scheduling은 training 동안 하나의 큰 learning rate cycle 로 처리함.

* 이름에 cycle이 들어가지만, Cyclical Learning Rates처럼 여러 cycle을 반복하는 방식은 아님.
* 구조적으로는 Cyclical / Restart Scheduling보다는 Warm-up + Decay Scheduling에 더 가까움.

전체 흐름은 다음과 같음.

1. 작은 learning rate $\eta_0$에서 시작함.
2. training의 절반 이하 (보통 2-30%)까지 learning rate를 선형적으로 증가시켜 maximum learning rate $\eta_1$에 도달함.
3. 이후 다시 learning rate를 $\eta_0$까지 선형적으로 감소시킴.

여기서 maximum learning rate $\eta_1$ 은 앞서 다룬 learning rate range test를 통해 찾는 경우가 많음.

그리고 보통 initial learning rate $\eta_0$는 보통 $\eta_1$보다 10배 정도 작게 설정함:
$$
\eta_0 \approx \frac{\eta_1}{10}
$$

1cycle Scheduling에서는 momentum도 함께 조절하는 경우가 많음.

* learning rate가 증가할 때는 momentum을 낮추고,
* learning rate가 감소할 때는 momentum을 다시 높임.
* learning rate와 momentum은 대체로 반대 방향으로 움직임.

1cycle Scheduling은 Leslie N. Smith가 제안한 learning rate scheduling 기법임.

* 관련 아이디어는 Smith가 2015년에 제안한 Cyclical Learning Rates에서 출발했고,
* Leslie N. Smith와 Nicholay Topin이 2017년에 발표한 Super-Convergence 논문에서
* 큰 learning rate와 하나의 learning rate cycle을 이용한 빠른 학습 전략으로 본격적으로 다루어짐.

PyTorch에서는 `OneCycleLR` 으로 지원하고 있음:

```python
scheduler = torch.optim.lr_scheduler.OneCycleLR(
    optimizer,
    max_lr=0.1,
    epochs=n_epochs,
    steps_per_epoch=len(train_loader),
)
```

주의할 점은 `OneCycleLR`은 보통 epoch 단위가 아니라 batch 단위로 `scheduler.step()`을 호출한다는 점임.

```python
for epoch in range(n_epochs):
    model.train()

    for X_batch, y_batch in train_loader:
        optimizer.zero_grad()

        pred = model(X_batch)
        loss = criterion(pred, y_batch)

        loss.backward()
        optimizer.step()

        scheduler.step()
```

즉, `OneCycleLR`은 매 batch마다 learning rate를 바꾸는 scheduler로 이해하는 것이 좋음.

---

### Cyclical / Restart Scheduling

Cyclical / Restart Scheduling은 

* learning rate를 한 번 증가시키고 감소시키는 데서 끝나지 않고
* Learning rate의 증가와 감소를 여러 번 반복하거나,
* 감소한 learning rate를 다시 큰 값으로 restart 시킴.

> 이 계열의 핵심 아이디어는  
> learning rate를 다시 크게 만들어 optimizer가 plateau나 local optimum에서 벗어나도록 하는 것임.

이 계열에는 다음 방식들이 포함됨.

* Cyclical Learning Rates
* Cosine Annealing with Warm Restarts


> 참고로
> 1cycle Scheduling은 제외하는 것이 더 자연스러움.  
> 1cycle은 이름상 cycle을 포함하지만 반복 cycle이나 restart를 사용하지 않기 때문임.

---

#### 1 Cyclical Learning Rates

Cyclical Learning Rates는 

* learning rate를 단조롭게 감소시키지 않고,
* 일정 범위 안에서 주기적으로 증가와 감소를 반복시키는 방식임.

이는 Leslie N. Smith가 2015년에 제안한 방법으로

* 핵심 아이디어는 learning rate를 계속 줄이기만 할 필요가 없다는 것임.
* 오히려 learning rate를 일정 범위 안에서 주기적으로 커지도록 만들면,
* optimizer가 sharp local minimum이나 plateau에서 벗어나 더 좋은 영역을 탐색할 수 있음을 보임.
* 또한 Smith는 learning rate range test를 통해 적절한 lower bound와 upper bound를 찾는 방법도 함께 제안함.

PyTorch에서는 `CyclicLR`을 통해 지원함:

```python
scheduler = torch.optim.lr_scheduler.CyclicLR(
    optimizer,
    base_lr=0.001,
    max_lr=0.1,
    step_size_up=2000,
)
```

* `base_lr` : cycle에서 가장 낮은 learning rate
* `max_lr` : cycle에서 가장 높은 learning rate
* `step_size_up` : `base_lr`에서 `max_lr`까지 올라가는 데 필요한 training step 수.
* `step_size_down` :  `max_lr` 에서 `base_lr`까지 내려가는데 필요한 training step 수.
    * 지정하지 않을 경우, `step_size_down=step_size_up` 임.

> `OneCycleLR`이나 `CyclicLR`은 batch 단위로 `scheduler.step()`이 이루어짐

#### 2 Cosine Annealing with Warm Restarts

Cosine Annealing with Warm Restarts는 

* cosine annealing을 한 번만 수행하지 않고
* 여러 번 반복하는 방식임.

이 방식은 Ilya Loshchilov와 Frank Hutter가 2016년에 제안한 SGDR에서 제안됨.

* 각 cycle에서는 cosine curve를 따라 learning rate를 낮추어짐.
* cycle이 끝나면 다시 높은 learning rate로 돌아가고 cycle이 반복됨.
* 이렇게 learning rate가 주기적으로 다시 커지면 gradient descent가 local optimum이나 plateau에서 빠져나올 가능성이 커짐.

<img width="640" height="480" alt="image" src="https://github.com/user-attachments/assets/59c15747-fa6e-4103-9d97-fb54da421579" />

다음의 참고 자료를 같이 볼 것

* [SGDR: Stochastic Gradient Descent with Warm Restarts](https://arxiv.org/abs/1608.03983)

PyTorch에서는 `CosineAnnealingWarmRestarts`를 사용할 수 있음.

```python
scheduler = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(
    optimizer,
    T_0=2,
    T_mult=2,
    eta_min=0.001,
)
```

* `T_0`  : 첫 번째 cosine cycle의 길이 (epoch를 주로 사용)
* `T_mult` : cycle이 반복될 때 cycle 길이를 몇 배로 늘릴지 결정
* `eta_min` : minimum learning rate
* 참고로 maximum learning rate는 CosineAnnealingWarmRestarts의 인자로 직접 지정하지 않음.
  Optimizer에 설정된 초기 learning rate가 각 cycle 시작 시의 maximum learning rate 역할을 함.

예를 들어 `T_0=2`, `T_mult=2`이면 첫 번째 cycle은 2 epoch, 두 번째 cycle은 4 epoch, 세 번째 cycle은 8 epoch처럼 점점 길어짐.

이 방식은 초반에는 짧은 cycle로 빠르게 탐색하고, 후반에는 긴 cycle로 더 정밀하게 최적화하는 효과를 가짐.

---

### PyTorch에서 Scheduler를 사용할 때의 주의점

PyTorch에서 learning rate scheduler를 사용할 때는 `scheduler.step()`을 언제 호출해야 하는지가 중요함.

scheduler는 크게 다음 세 가지 방식으로 나눌 수 있음.

| 방식                  | 호출 위치                  | 예                                    |
| ------------------- | ---------------------- | ------------------------------------ |
| epoch 단위 scheduler  | epoch 끝                | `ExponentialLR`, `CosineAnnealingLR` |
| batch 단위 scheduler  | batch마다                | `OneCycleLR`, `CyclicLR`             |
| metric 기반 scheduler | validation metric 계산 후 | `ReduceLROnPlateau`                  |

일반적인 epoch 단위 scheduler는 보통 epoch이 끝난 뒤 호출함.

```python
for epoch in range(n_epochs):
    model.train()

    for X_batch, y_batch in train_loader:
        optimizer.zero_grad()
        pred = model(X_batch)
        loss = criterion(pred, y_batch)

        loss.backward()
        optimizer.step()

    scheduler.step()
```

batch 단위 scheduler는 매 batch마다 호출함.

```python
for epoch in range(n_epochs):
    for X_batch, y_batch in train_loader:
        optimizer.zero_grad()
        pred = model(X_batch)
        loss = criterion(pred, y_batch)

        loss.backward()
        optimizer.step()
        scheduler.step()
```

metric 기반 scheduler는 validation metric을 계산한 뒤 호출함.

```python
val_loss = evaluate_loss(model, valid_loader)

scheduler.step(val_loss)
```

즉, scheduler마다 호출 위치와 방식이 다를 수 있음.

따라서 scheduler를 사용할 때는 반드시 해당 scheduler가 epoch 단위인지, batch 단위인지, metric 기반인지 확인해야 함.

---

---

## 어떤 Scheduler를 선택해야 하는가?

Learning Rate Scheduling은 다음 기준으로 선택하면 됨.

| 상황                               | 권장 방식                                    |
| -------------------------------- | ---------------------------------------- |
| 단순하고 안정적인 training<br/>별다른 특수 요구사항이 없는 기본선택| Exponential Scheduling, Cosine Annealing |
| 직접 epoch별 감소 시점을 정하고 싶음          | Piecewise Constant Scheduling            |
| validation 성능이 정체될 때<br/>자동으로 줄이고 싶음 | Performance Scheduling                   |
| 초반 training이 불안정함                | Warm-up + Decay                          |
| 빠른 학습과 좋은 일반화 성능을<br/>동시에 노림(전체 step 수를 미리 아는 경우) | 1cycle Scheduling                        |
| plateau나 local optimum에서<br/>벗어나고 싶음 | Cyclical LR, Cosine Warm Restarts        |

실무적으로는 다음과 같이 생각할 수 있음:

* 먼저 기본 scheduler가 필요하다면 Cosine Annealing이나 Exponential Scheduling을 사용할 수 있음.
    * 이 둘은 특수한 요구사항이 없을 때 가장 널리 쓰이는 기본 선택임! 
* Validation metric을 기준으로 자동 조절하고 싶다면 `ReduceLROnPlateau`가 적절함.
    * 이 방식은 전체 학습 step 수를 사전에 정해 두지 않아도 사용할 수 있음. 
* 초반 loss가 불안정하다면 warm-up을 추가하는 것이 좋음.
* Training 전체에서 빠르게 학습한 뒤 마지막에 매우 작은 learning rate로 fine-tuning하고 싶다면 1cycle Scheduling을 고려할 수 있음.
    * 학습 전에 정해진 epoch 수 또는 step 수로 진행하는 경우.
* Training이 plateau에 자주 걸린다면 Cosine Annealing with Warm Restarts 또는 Cyclical Learning Rates를 고려할 수 있음.

