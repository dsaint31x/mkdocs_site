# Rectified Linear Unit (ReLU)

초기 perceptron의 Unit step에서 logistic 으로 activation function으로 바꾸어진 이후, 가장 효과적인 activation function으로 부상한 것이 `ReLU` 이다.

## 기존 Sigmoid function의 단점.

logistic과 같은 sigmoid function 계열의 activation function의 가장 큰 단점은 gradient vanishing 이 발생하기 쉽다는 점임.

* 양 끝단(=양과 음으로 매우 큰 input)에서의 gradient가 0에 가깝게 너무 작아지는 문제가 있음.
* 때문에 많은 layers 가 사용되는 deep ANN 에서 사용이 적절하지 않음.

—- 

## ReLU 의 장점.

* `ReLU`는 positive input에 대해 기울기가 1을 유지하기 때문에 deep ANN 에서도 gradient가 소실되는 단점이 sigmoid 계열에 비해 획기적으로 개선됨.
    * 양으로 큰 input에 대해서도 기울기가 1로 유지됨.
* `ReLU`는 negative input에 대해선 기울기가 0이 되는 non-linearity를 가지고 있기 때문에 identity function과 달리 ANN에 non-linearity를 부가해주는 activation function의 역할을 함.
    * ***Activation function은 반드시 non-linear function이어야 함.***
* 계산 효율성 측면에서도 연산량이 많은 exponential 을 사용하는 sigmoid에 비해서 `ReLU`는 max 함수 기반으로 훨씬 간단하기 때문에 유리하다.
* 기존의 Glorot weight init.과 함께 사용될 경우, forward-pass에서 layer의 output이 0의 값으로 쏠리는 분포를 보이는 단점이 있으나, 이를 개선한 He weight init.과 사용시 이같은 문제가 거의 없음.
* `ReLU`는 Sparse activation을 생성함으로서 over-fitting을 막아주는 효과를 가짐(L1 Norm기반의 Lasso loss를 사용할 경우 Model의 weights를 sparse하게 해주면서 over-fitting을 막아주던 것과 비슷)

—-

## ReLU 의 단점.

* Sparse activation이 지나치게 심해질 경우, 절반 이상의 node가 0이 되버리는 `dying ReLUs` 가 발생하게 됨. 
    * ANN이 깊어질수록 이같은 경향이 심해진다 (input이 0 이하가 되기만 하면 그 이후는 출력이 0으로 고정되버리기 때문) 
    * `leaky ReLU` 를 통해 개선됨.
* 미분이 가능한 smooth function이 아니기 때문에 Lasso loss를 Gradient Decent에서 사용할 때의 문제점을 그대로 `ReLU` 도 가짐.
    * 0에서의 discontinuity를 가지는 경우 최적의 값 근처에서 gradient decent bounce가 발생.
    * converge 속도가 느려지는 단점을 보임 
    * 이는 the variants of `ReLU`들이 가지는 문제점으로 smooth하게 변경한 Exponential Linear Unit (ELU)등을 통해 개선됨. 

—-

## The variants of ReLU

### Leaky ReLU

negative input에 대해서 0으로 처리하는 `ReLU`와 달리 `Leaky ReLU`는 leakage factor $\alpha$ 만큼의 gradient를 유지해줌.

$$\text{leaky ReLU}=\text{max}(x, \alpha x)$$

where

* $0. \ge \alpha < 1.$

단점은 $\alpha$로 인해 hyper-parameter가 하나 더 늘어났다는 점이며, 적절한 $\alpha$를 찾아야 한다는 점이다.

일반적으로 $0.2$ 정도의 large leakage factor가 $0.01$ 의 적은 경우보다 좋은 결과로 이어지는 것으로 알려짐.

Ref. : Bing Xu et al., “Empirical Evaluation of Rectified Activations in Convolutional Network,” arXiv preprint arXiv:1505.00853 (2015).

### Paramateric Leaky ReLu 

Leaky ReLU의 $\alpha$를 trainable parameter로 삼아서 dataset을 기반으로 최적의 값을 찾도록 한 변형이다.

* 단점은 적은 수의 training dataset에서 over-fit하기 싶다는 점임.
* 적은 수의 training dataset에서는 $\alpha$를 일정값의 범위에서 random하게 선택하여 training시키고, 이후 사용된 값의 평균으로 지정하여 inference를 수행하는 `Randomized Leaky ReLU`를 사용하는게 보다 나음.
 
    
 