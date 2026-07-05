# Max-Norm Regularization

## 1. 핵심 개념

`Max-Norm Regularization`은 

* 각 neuron 또는 filter의 weight vector가
* 너무 커지지 않도록 $\ell_2$ norm의 상한을 두는 regularization 기법임.

$$
|\mathbf{w}|_2 \le r
$$

여기서,

* $\mathbf{w}$ : 하나의 neuron 또는 filter에 해당하는 weight vector
* $|\mathbf{w}|_2$ : weight vector의 $\ell_2$ norm
* $r$ : 허용되는 최대 norm 값
* `max_norm` : PyTorch 구현에서의 $r$

즉, weight가 학습 중 커지는 것은 허용하되, 정해진 크기 $r$ 을 넘으면 다시 $r$로 줄이는 방식임.


> `L2 Regularization`처럼
> loss에 penalty를 추가하는 것이 아니라,
> 학습 후 weight를 feasible region 안으로 다시 넣는 방식에 가까움.

따라서 구현에서 가장 중요한 점은 다음임.

* bias에는 보통 적용하지 않음.
* `Linear`에서는 `dim=(1,)` 사용.
* `Conv` 계열에서는 `dim=tuple(range(1, weight.ndim))` 사용.
* `BatchNorm`, `LayerNorm`의 affine weight 같은 1D parameter에는 보통 적용하지 않음.
* `optimizer.step()` 직후 적용함.
* `max_norm`은 반드시 tuning 대상임.

## 2. 적용 방식

Max-Norm Regularization은 loss function에 다음과 같은 항을 추가하지 않음.

$$
\lambda |\mathbf{w}|_2^2
$$

대신 training step 이후 weight를 직접 검사함.

* weight norm이 $r$ 이하이면 그대로 유지함.
* weight norm이 $r$ 보다 크면 $r$ 크기로 rescale함.
* weight vector의 방향은 유지하고 크기만 줄임.

수식으로 쓰면 다음과 같음.

$$
\mathbf{w}
\leftarrow
\mathbf{w}
\cdot
\min\left(1, \frac{r}{|\mathbf{w}|_2 + \epsilon}\right)
$$

여기서 $\epsilon$ 은 division by zero를 피하기 위한 작은 값임.

## 3. 효과

`max_norm` 값인 $r$ 을 작게 잡을수록 regularization이 강해짐.

* $r$ 이 작음: weight 크기 제한이 강함.
* $r$ 이 큼: weight 크기 제한이 약함.
* 너무 작으면 underfitting 가능성 증가.
* 너무 크면 regularization 효과 감소.

따라서 `max_norm`은 직접 tuning해야 하는 hyperparameter임.

Max-Norm Regularization은 특히 다음 상황에서 의미가 있음.

* weight가 지나치게 커지는 것을 막고 싶은 경우
* overfitting을 줄이고 싶은 경우
* Batch Normalization이나 Layer Normalization 없이 학습 안정성을 높이고 싶은 경우
* exploding gradient의 영향을 간접적으로 완화하고 싶은 경우

다만 gradient 자체를 clip하는 것은 아니므로, `Gradient Clipping`과는 구분해야 함.

## 4. PyTorch에서 중요한 점

중요한 것은 `dim`을 아무렇게나 고정하면 안 된다는 점임.

`dim`은 **어느 축을 따라 norm을 계산할지**를 의미함.
즉, 제한하고 싶은 단위가 neuron인지, filter인지에 따라 달라져야 함.

### `nn.Linear`

`nn.Linear`의 weight shape은 다음과 같음.

```python
[out_features, in_features]
```

하나의 output neuron은 weight matrix의 한 row에 해당함.

따라서 각 neuron의 incoming weight vector 전체에 대해 norm을 계산하려면 다음처럼 해야 함.

```python
dim=1
```

즉,

```python
weight.norm(p=2, dim=1, keepdim=True)
```

은 각 output neuron마다 하나의 norm을 계산함.

### `nn.Conv2d`

`nn.Conv2d`의 weight shape은 다음과 같음.

```python
[out_channels, in_channels, kernel_height, kernel_width]
```

하나의 output channel에 해당하는 filter 전체를 하나의 weight vector로 보려면 `out_channels` 축을 제외한 나머지 축 전체에 대해 norm을 계산해야 함.

따라서 `Conv2d`에서는 다음이 자연스러움.

```python
dim=(1, 2, 3)
```

즉, `dim=1`만 쓰면 filter 전체 norm이 아니라 일부 축에 대해서만 norm을 계산하게 되므로 일반적인 max-norm constraint로는 부정확함.

## 5. Layer별 norm 계산 기준

| Layer       | weight shape                              | 제한 대상                             | norm 계산 dim    |
| ----------- | ----------------------------------------- | --------------------------------- | -------------- |
| `nn.Linear` | `[out_features, in_features]`             | 각 output neuron의 incoming weights | `(1,)`         |
| `nn.Conv1d` | `[out_channels, in_channels, kW]`         | 각 output channel의 filter          | `(1, 2)`       |
| `nn.Conv2d` | `[out_channels, in_channels, kH, kW]`     | 각 output channel의 filter          | `(1, 2, 3)`    |
| `nn.Conv3d` | `[out_channels, in_channels, kD, kH, kW]` | 각 output channel의 filter          | `(1, 2, 3, 4)` |

핵심은 항상 같음.

> 첫 번째 축은 output unit 또는 output channel이고, 나머지 축 전체가 그 unit으로 들어오는 weight vector임.

## 6. 구현 예시

```python
import torch
import torch.nn as nn


def apply_max_norm(model, max_norm=2.0, epsilon=1e-8):
    with torch.no_grad():
        for module in model.modules():

            if isinstance(module, nn.Linear):
                weight = module.weight
                norm_dims = (1,)

            elif isinstance(module, (nn.Conv1d, nn.Conv2d, nn.Conv3d)):
                weight = module.weight
                norm_dims = tuple(range(1, weight.ndim))

            else:
                continue

            actual_norm = torch.linalg.vector_norm(
                weight,
                ord=2,
                dim=norm_dims,
                keepdim=True,
            )

            scale = torch.clamp(
                max_norm / (actual_norm + epsilon),
                max=1.0,
            )

            weight.mul_(scale)
```

## 7. Training Loop에서의 위치

Max-Norm Regularization은 `optimizer.step()` 이후에 적용함.

```python
loss.backward()
optimizer.step()

apply_max_norm(model, max_norm=2.0)

optimizer.zero_grad()
```

순서로 보면 다음과 같음.

1. loss 계산
2. gradient 계산
3. optimizer가 weight update
4. max-norm constraint 적용
5. gradient 초기화

즉, optimizer가 일단 weight를 바꾼 뒤, 그 결과가 $|\mathbf{w}|_2 \le r$ 조건을 넘으면 다시 projection하는 방식임.



