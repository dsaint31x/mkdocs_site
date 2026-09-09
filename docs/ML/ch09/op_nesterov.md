# Nesterov Accelerated Gradient

Yurii Nesterov가 1983년 momentum을 개선한 Nesterov Accelerated Gradient를 제안함.  
`NAG`로 많이 불림.

Momentum과 비교하면 다음의 차이를 보임:
![](https://github.com/user-attachments/assets/4a3999db-05df-4509-9586-367e499e88ab){style="display: block; margin: 0 auto; width: 500px"}

* Gradient를 구할 때,
  다음 step으로 우선 momentum에 따라 inertia의 방향으로 먼저 이동한 후
  이동한 위치에서 gradient를 구하여 이를 momentum과 같이 고려하여
  실제 파라미터의 이동이 이루어짐.
    * 기존의 momentum : $\nabla_{\boldsymbol{\theta}}J(\boldsymbol{\theta}_t)$
    * NAG : $\nabla_{\boldsymbol{\theta}}J(\boldsymbol{\theta}_t+\gamma \textbf{m}_{t})$
* 이 같은 gradient를 ***look-ahead gradient*** 라고 부름.
* 이경우 최적값에 해당하는 minimum에서 기존 Momentum 방법이 요동치는 단점이 줄어드는 효과를 가져옴.

수식으로 살펴보면 다음과 같음:

1. 우선 momentum이 다음과 같이 변경됨.

$$\begin{aligned} \textbf{m}_0 &= \textbf{0} \\ \textbf{m}_{t+1}&=\gamma \textbf{m}_t - \eta\nabla_{\boldsymbol{\theta}}J(\boldsymbol{\theta}_t+\gamma \textbf{m}_t)\end{aligned}$$

2. model의 parameter vector의 업데이트는 다음과 같음:

$$
\boldsymbol{\theta}_{t+1} = \boldsymbol{\theta}_{t} + \textbf{m}_{t+1} 
$$

3. 이를 그림으로 다시 표현하면 다음과 같음:

![](https://github.com/user-attachments/assets/8402499e-c1e2-4c7c-bbf5-049d6a6d5206){style="display: block; margin: 0 auto; width: 500px"}

앞서 살펴본 식은  

* Nesterov가 제안한 accelerated gradient의 look-ahead 방식을
* momentum notation으로 표기한 것으로,  
* NAG의 look-ahead 동작을 직접 보여주는 형태이며
* [Sebastian Ruder 등의 자료](https://www.ruder.io/optimizing-gradient-descent/#nesterovacceleratedgradient)에서 NAG의 동작을 설명할 때 사용됨  
    * 사실 Ruder 역시 기호를 $\textbf{m}$대신에 $\textbf{v}$로 씀.
    * 이후 다룰 Sutskever의 식과 구분하기 위해 이 문서에선 이 방식에선 $\textbf{m}$을 사용했음.  

개인적으로도 NAG의 동작을 이해하기에는 이 표현이 가장 직관적임.  
(Bengio도 위의 식의 index에 맞춰 Sutskever의 식을 다시 표기하기도 함).
  
하지만, 

* $\textbf{m}_t = -\textbf{v}_{t-1}$의 관계를 이용하여  
* 다음과 같이 $\textbf{v}_t$를 이용한 식으로 표현할 수도 있음:  
$$
\textbf{v}_{t} = \gamma \textbf{v}_{t-1} + \eta \nabla_\theta J (\boldsymbol{\theta}_t - \gamma \textbf{v}_{t-1}) \\
\boldsymbol{\theta_{t+1}} = \boldsymbol{\theta_{t}} - \textbf{v}_{t}$$

* 위의 식은 널리 알려진 Sutskever 등의 자료 및 CS231n에서 사용하는 형태)  
* 위의 식과 앞서 식의 차이는 lookahead로 이동할 moment를 $\textbf{m}_t$ 로 표현하느냐, $-\textbf{v}_{t-1}$로 표현하느냐의 차이임.

다만 실제 library 구현에서는 

* look-ahead parameter를 별도로 만든 뒤 그 위치에서 gradient를 다시 계산하는 방식보다는,  
* 현재 parameter에서 계산한 gradient와 momentum buffer를 조합하는 형태가 주로 사용됨.

PyTorch의 `SGD(..., nesterov=True)`도 다음과 같은 방식임.

```python
buf = momentum_buffer_list[i]
if buf is None:
    buf = grad.detach().clone()  # <-- 361라인: 최초 버퍼에 첫 grad 복사
    momentum_buffer_list[i] = buf
else:
    buf.mul_(momentum).add_(grad, alpha=1 - dampening)

if nesterov:
    grad = grad.add(buf, alpha=momentum)  # <-- 368라인: nesterov=True 일 때 grad 중첩 갱신
else:
    grad = buf
```

PyTorch에서는 먼저 momentum buffer를 다음과 같이 갱신함.

$$
\mathbf v_t = \gamma \mathbf v_{t-1} + \nabla_\theta J(\boldsymbol{\theta}_t)
$$

`nesterov=True`이면 parameter update는 다음과 같음.

$$
\boldsymbol{\theta}_{t+1} = \boldsymbol{\theta}_t - \eta \left[ \nabla_\theta J(\boldsymbol{\theta}_t) + \gamma \mathbf v_t \right]
$$

즉, PyTorch에서는 

* look-ahead 위치에서 gradient를 직접 계산하지 않고,
* **현재 parameter에서 계산한 gradient와 momentum buffer를 조합하여 NAG를 구현함**.
* 그리고, 첫 momentum buffer를 zero vector로 시작하지 않고 첫 gradient로 초기화함.

```python
if buf is None:
    buf = grad.detach().clone()
```

따라서 첫 step에서 momentum buffer에 gradient가 바로 들어가도록 구현됨.  
이는 [PyTorch 공식 문서](https://docs.pytorch.org/docs/main/generated/torch.optim.SGD.html?utm_source=chatgpt.com)에도 명시되어 있음
  
> 실제로 Sutskever의 식에서도,
> 앞서 $\textbf{m}_t$ 을 사용하여 전개한 NAG 식과 맞추려면,
> 첫 velocity 가 $\textbf{v}_1 = \eta \nabla_theta J(\boldsymbol{\theta}_1}$ 이어야 함.  
> PyTorch 구현(NAG의 원래 식보다는 Sutskever의 식에 가까움)에서는
> learning rate를 momentum buffer에 포함시키지 않고,  
> 첫 momentum buffer에 gradient 자체를 복사해 넣는 방식으로 처리함.
> 
> [https://github.com/pytorch/pytorch/blob/main/torch/optim/sgd.py](https://github.com/pytorch/pytorch/blob/main/torch/optim/sgd.py) 의 360-367라인 참고


## Keras에서의 구현.

`tf.keras.optimizers.SGD` optimizer를 생성할 때,  
`momentum` parameter에 momentum coef.를 지정하고,  
`nesterov` parameter에 `True`를 넘겨주면 NAG optimizer를 생성함.  
(이를 모델의 `fit`에 넘겨주면 됨.)

> SGD optimizer에서 Nesterov momentum을 활성화하는 것으로도 볼 수 있음.

```Python
optimizer = tf.keras.optimizers.SGD(learning_rate=0.001, 
                                    momentum=0.9,
                                    nesterov=True)
```

## PyTorch에서의 구현

`torch.optim.SGD` optimizer를 생성할 때,  
`momentum` parameter에 momentum coefficient를 지정하고,  
`nesterov=True`를 설정하면 NAG를 사용할 수 있음.

```python
optimizer = torch.optim.SGD(
    model.parameters(),
    lr=0.001,
    momentum=0.9,
    nesterov=True
)
```

- `lr`: learning rate
- `momentum`: momentum coefficient
- `nesterov=True`: Nesterov momentum 사용

PyTorch에서는 생성한 optimizer를 학습 loop에서 사용함.

```python
optimizer.zero_grad()
loss.backward()
optimizer.step()
```
