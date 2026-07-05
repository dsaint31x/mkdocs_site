---
title: Gradient Clipping
author: HangKeun Kim
date: 2026-07-05
categories:
  - Deep Learning
  - PyTorch
tags:
  - deep learning
  - gradient clipping
  - gradient vanishing
  - gradient exploding
  - gradient norm
  - gradient value
  - rnn
  - optimization
  - training stability
  - pytorch
  - clip_grad_norm_
  - clip_grad_value_
---

# Gradient Clipping

## 정의

***Vanishing Gradient / Exploding Gradient Problem 을 방지하는 기법*** 중 하나로 BN 을 사용하기 어려운 경우 (RNN 등)에서 자주 사용됨.

* Gradient를 계산하고 나서,
* 해당 Gradient의 norm 이 일정 범위를 넘어가지 않도록 thresholding 처리:`torch.nn.utils.clip_grad_norm_()`
    * 1st arg.: `model.parameters()`
    * `max_norm`: default 1.0
* 또는 Gradient의 각 component가 일정 범위를 넘어가지 않도록 thresholding 처리:`torch.nn.utils.clip_grad_value_()`
    * 1st arg.: `model.parameters()`
    * `clip_value`: default 1.0, `[-1.0, +1.0]`

## code 활용

training 과정 중에 다음의 형태로 사용됨:

```python
...
loss = criterion(pred, label)
loss.backward()
nn.utils.clip_grad_norm_(model.parameters(), max_norm = 1.0)
optimizer.step()
optimizer.zero_grad()
...
```

> Regularization 의 한 기법인 [weight constraint](https://dsaint31.tistory.com/848#6.%20Weight%20Constraint-1-7) 과 비슷하지만,  
> 대상이 다름!! (parameters의 grad 인지 아니면 그 parameters 값 자체를 제한하는지)

## References

* [Razvan Pascanu et al., “On the Difficulty of Training Recurrent Neural Networks”, Proceed-
ings of the 30th International Conference on Machine Learning (2013): 1310–1318.](https://arxiv.org/abs/1211.5063)
