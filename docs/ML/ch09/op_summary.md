---
title: Optimizers 
tags: [Gradient, GD, Stochastic Gradient Descent, NAG, AdaGrad, RMSprop, Adam, Nadam, Momentum]
---

# Optimizers

parameters의 수가 적은 단순한 모델들의 경우 Hessian 계열 (Newton's Method)이 사용되기도 하나,  
***Deep Neural Network에선 Gradient 계열 만이 사용됨.***

* parameters의 수의 square에 비례하는 연산을 요구하는 Hessian 계열은 
* 메모리 문제와 함께 너무 느린 학습속도로 인해 DNN 에 적합하지 않음.

> Adaptive learning rate 를 위해,  
> 이차미분의 Hessian matrix 대신, Exponential Moving Average of gradient square 등이 사용됨.

---

## Gradient 계열 Optimizers

<figure markdown>
![](./img/optimizers.png){width="600" align="center"}
</figure>

대표적인 알고리즘의 요약.

Batch Gradient Decent (or Vanilla Gradient Decent) 
: Gradient계열의 원조.

Stochastic Gradient Decent 
: data 하나만으로 업데이트를 수행하여 Batch GD의 느린 문제 수정

Mini-batch GD 
: Batch GD와 SGD의 중간형.

[Momentum](op_momentum.md) 
: SGD의 local minimum에 빠지는 문제점을 momentum을 도입(이전 업데이트와 현재 gradient를 vector sum)하여 해결.

[NAG(Nesterov Accelerated Gradient)](./op_nesterov.md) 
: 우선 기존의 momentum 방향으로 미리 이동한 미래 위치에서 gradient를 계산하고,  
해당 gradient와 기존 momentum 을 결합(gradient에 weighting 처리하여 vector sum)한 후  
현재 위치에서 해당 결합 결과로 계산된 vector(velocity라고도 불림)로 이동.  
이 경우 Momentum에 비해 수렴위치인 minimum에서 요동치는 문제가 줄어들어 보다 안정화됨.

[Adagrad](./op_adagrad.md) 
: 학습이 진행되면서 parameter들의 업데이트되는 크기가 각기 다른 점을 반영하여,  
각 parameter 의 이전 gradient들의 제곱합(누적 업데이트된 정도)을 구하여  
이에 반비례하게 업데이트시키는 방식을 채택함: Adagrad는 `adaptive learning rate`를 도입한 대표적 알고리즘임.

[RMSprop](./op_rmsprop.md)과 Adadelta 
: Adagrad의 learning rate가 지나치게 이른 학습 단계에서 소실되는 문제를 해결하기 위해  
gradient의 square(2차 moment라고도 불림)의 exponential moving average를 도입한 알고리즘.  
RMSProp은 안정적인 `adaptive learning rate`를 제공하여 fine-tuning 등에서 많이 애용됨.  

Adadelta
: RMSProp과 함께, Adagrad의 지나치게 빠른 learning ratio 감소를 해결하기 위해 제안된 방법.  
가장 큰 특징은 learning rate($\eta$) 하이퍼파라미터를 명시적으로 사용하지 않는다는 점임.   
즉, 전통적인 의미의 global learning rate를 제거하고 gradient의 변화량과 parameter 업데이트의 변화량 모두에 EMA를 적용하고,  
이 두 값을 비율로 나누는 방식으로 step size를 자동으로 조절함.

[Adam](./op_adam.md) 
: RMSProp에 momentum을 도입하여 RMSProp과 Momentum을 효과적으로 결합함.  

AdaMax 
: **Adam에서 adaptive learning rate 를 감소시키는데 적용된 gradient의 square를 이용한 L2-norm**  
대신 **L$\infty$-norm (=Max값)으로 대체** 하여 보다 안정적인 학습을 가능하게 함.  
안정성 면에서는 우수하지만, 일반적으로 Adam이 보다 나은 것으로 알려져 있음.

[NAdam](./op_nadam.md)
: ADAM에 momentum 대신에 NAG(Nesterov Accelerated Gradient)를 적용.  
보다 빠른 수렴속도와 향상된 성능을 보이도록 개선됨.

---

다음 두 이미지는 Gradient Optimizers의 동작을 잘 보여줌.

* Images credit: [Alec Radford](https://twitter.com/alecrad).
* [참고 사이트: cs231n](https://cs231n.github.io/neural-networks-3)

<figure markdown>
![](./img/opt2.gif){width="400" align="center"}
</figure>

* Contours of a loss surface and time evolution of different optimization algorithms. (별모양이 최적값임)
    * Momentum 기반의 알고리즘들(`Momentum`와 `NAG`)에서 ***overshooting*** 이 보임. (hill에서 공을 아래로 굴릴 때 보이는 왔다갔다하와 동작.)

<figure markdown>
![](./img/opt1.gif){width="400" align="center"}
</figure>

* A visualization of a saddle point in the optimization landscape, where the curvature along different dimension has different signs (one dimension curves up and another down). 
    * `SGD`는 제대로 최소값으로 나가지 못하는 것을 확인할 수 있음.
        * ***고정된 learning rate를 사용하는 경우, local minima에 매우 취약함*** 을 알 수 있음.
    * ***Adaptive learning ratio계열*** 의 (`Adagrad`, `Adadelta`, `RMSprop`) 알고리즘들은 효과적으로 학습이 이루어짐을 확인 가능함.

---

---

## References

* Sebastian Ruder's [An overview of gradient descent optimization algorithms](https://arxiv.org/abs/1609.04747)
* [Unit Tests for Stochastic Optimization](https://arxiv.org/abs/1312.6055)
* [CS231n Convolutional Neural Networks for Visual Recognition](https://cs231n.github.io/neural-networks-3)
* HiddenBeginner's [딥러닝 최적화 알고리즘 알고 쓰자. 딥러닝 옵티마이저(optimizer) 총정리](https://hiddenbeginner.github.io/deeplearning/2019/09/22/optimization_algorithms_in_deep_learning.html)