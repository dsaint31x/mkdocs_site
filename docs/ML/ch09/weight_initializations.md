# Weight Initialization (가중치 초기화)

Weight Initialization은 Gradient Vanishing or Exploding Problem을 개선하기 위해 연구된 방법으로 2010년에 상당한 성과를 보이면서 deep neural network를 효과적으로 학습시키기 위해 널리 사용됨. (현재도 기본적으로 사용된다.)

## Weight Initialization 중요성.

2000년대까지도 왜 Gradient vanishing 및 exploding이 발생하는지를 정확히 파악하지 못했는데, 2010년 Xavier Glorot et al.에 의해 이에 대한 단서가 찾아졌고, 이를 통해 획기적으로 개선(해결이 아니고 개선임)하는 방법으로 적절한 weight initialization과 activation function의 조합이 제안된다.

Xavier Glorot et al.이 찾은 원인은 다음과 같음

당시 ANN의 경우, 

* ***"`logistic` activation function"***과 ***"normal distribution으로 초기화된 weights"*** 를 사용했는데, 
* 이 조합은 ^^각 layer에서 input nodes와 output nodes의 수가 다른 점^^ 과 함께 작용하여
* layer에서 ***input에서의 variance와 output의 variance가 매우 달라지게 함(output의 variance가 커짐)*** 을 확인함.
    * 좀 더 자세히 말하면, ^^input node의 갯수 ($\text{fan}_\text{in}$)에 비례하여 layer output의 variance가 커짐^^. (forward flow의 경우이며, backward flow의 경우엔 output node의 갯수 ($\text{fan}_\text{out}$)에 비례하여 커짐.)

output의 variance가 커질 경우, forward-pass에서 점점 variance는 증가하게 되고 최종 output layer에 가까운 layer에서는 대부분 logistic activation function이 0 또는 1로 saturate(수렴)되는 결과를 일으키게 된다.

이후 이루어지는 backward-pass에서는 derivatives가 전달되어야 하는데, logistic의 saturated region에서의 derivatives는 거의 0으로 너무나 작고, 이같이 작은 값으로 시작되는 backward-pass의 전달은 중도에서 정말 0이 되어버려(Vanishing Gradient), lower layer들로 제대로된 gradient를 전달되지 않게 된다.

> 더욱이 logistic activation의 출력은 mean이 0.5이고 항상 양수를 출력하다보니  
> (normal distribution 의 mean은 0임을 기억)  
> forward pass에서 output의 weighted sum이 input의 weighted sum보다 커지는 `bias shift`가 발생하기 쉬움 (이는 여러 layers를 통과할수록 variance가 커지는 문제로 이어짐).  
> 이는 `tanh` 이 logistic보다 좀더 학습을 잘 시키는 이유의 근거가 된다. (`tanh`은 mean이 0임.)

* 참고 : [sigmoid](https://dsaint31.tistory.com/430)
* 참고 : [hyperbolic tangent, `tanh`](https://dsaint31.tistory.com/577)
* 참고 : [Random variable의 곱과 variance](https://dsaint31.tistory.com/580) 

---

***중요***

ANN에서 gradient vanishing을 막으려면 다음이 성립해야 한다.

* 각 layer를 거쳐도 variance는 변화가 없어야 한다.
* 이는 forward-flow 와 backward-flow 모두에서 성립해야 한다.
* 이를 위해선 layer의 input과 output이 동일한 variance를 가져야 한다.

$\text{fan}_\text{in}$과 $\text{fan}_\text{out}$이 같지 않을 경우 variance를 완전히 동일하게 만들기는 불가능하지만, Xavier Glorot et al.은 일종의 좋은 타협안을 제시했고 성공을 거뒀다. 

이 타협안은 바로 문제가 되는 variance를 $\text{fan}_\text{in}$ 과 $\text{fan}_\text{out}$ 를 기반으로 조절하는 것이었음.

사실 Yann LeCun et al. (1998)도 비슷한 형태의 Weight Initialization을 제시했다.

이 외에 weight의 초기화에서 주의할 점들은 다음과 같음.

* weights는 0으로 초기화되어선 안됨 (모두 0을 곱하면 같은 출력이 나오게 된다.)
* weights를 constant로 초기화해선 안됨 (모든 같은 gradient를 가지게 되기 때문).
* 때문에 작은 수의 random number로 초기화되어야 함 (값이 너무 클 경우 logistic function의 출력을 saturation시킴.)
* random이어야 하는 이유는 weights의 분포가 asymmetric해야하기 때문임.

때문에 normal distribution으로 초기화할 경우 gradient vanishing이 발생하기 쉬움을 알 수 있다.
(normal distribution의 variance인 1은 gradient vanishing의 관점에서 보면 작지 않다. 때문에, 만약 0.01 정도로 줄인다면 좀더 나은 결과를 얻을 수 있음.)


## "Fan in" and "Fan out"

앞서 애기한 fan in과 fan out은 다음과 같다.

$\text{fan}_\text{in}$
: layer에 들어오는 input node 수에 해당함. 

$\text{fan}_\text{out}$
: layer에 들어오는 output node 수에 해당함. 

***Ex.***: `conv2d` layer 에서 receptive field의 크기가 $5 \times 5$이고, input의 channel이 $3$ 이고 output은 $10$ 인 경우는 다음과 같음.

* `kernel_shape` : $5 \times 5 \times 3 \times 10$
* $\text{fan}_\text{in}$ : $5 \times 5 \times 3 = 72$
* $\text{fan}_\text{out}$ : $5 \times 5 \times 10 = 250$

## Weight Initialization Methods

초기에 많이 애용된 

* constant로 고정된 경우나 
* Normal distribution을 사용한 경우는, 

오늘날 사용되지 않으며 다음의 방법들이 주로 이용된다.

주의할 것은 activation function에 따라 좀더 적절한 initialization이 결정된다는 점임. 때문에 아래 표도 궁합이 맞는 activation function이 같이 표기됨.

| Initialization | Activation functions | $\sigma^2$(Normal dist.) | [$-l$, $l$] (Uniform dist.) | Keras impl. |
|:----:|:----:|:----:|:----:|:----:|
| Yann LeCun	| SELU	| $\sigma^2 = 1/\text{fan}_\text{in}$	| $l=\sqrt{3\sigma^2}$ | `lecun_normal`, `lecun_uniform`|
| Xavier Glorot |	None, tanh, sigmoid, softmax |	$\sigma^2 = 1/\text{fan}_\text{avg}$ | $l = \sqrt{3\sigma^2}$ | `glorot_normal`, `glorot_uniform` | 
| Kaiming He	| ReLU, Leaky ReLU, ELU, GELU, Mish	| $\sigma^2 = 2/\text{fan}_\text{in}$ |	$l = \sqrt{3\sigma^2}$ | `he_normal`,`he_uniform`| 

* 위의 normal distribution들은 variance만 차이가 있을 뿐, 모두 mean=0임.
* Xavier Glorto et al.이 제안한 방식의 경우, `ReLU`가 유행하기 전까지 가장 많이 사용되었으나 아쉽게도 `ReLU`와는 잘 맞지 않는다 (layer가 깊어질수록 0에 치우치게 된다.)는 결과들로 인해 ***Kaiming He et al.*** 의 방식이 제안됨.
    * `ReLU`에서 0 이상의 값은 그대로 통과시키다보니 다시 $\text{fan}_\text{in}$만을 고려하면서 He의 방식에서는 coefficient를 조금 다르게 줌. `ReLU` 계열들을 사용시 기본으로 사용됨.
* 참고로 LeCun의 방법과 가장 궁합이 맞는 `SELU`는 한참 뒤인 2017년에 개발된 방식임.

## References
* [Efficient BackProp. Yann LeCun et al.1998](https://www.researchgate.net/publication/2811922_Efficient_BackProp)
* [Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification, Kaiming He et al., 2015](https://arxiv.org/abs/1502.01852)
* ExcelsiorCJH's [Chap11.1 - 심층 신경망 훈련](https://github.com/ExcelsiorCJH/Hands-On-ML/blob/master/Chap11-Training_DNN/Chap11_1-Training_DNN.ipynb) ****
* [갈아먹는 딥러닝 기초 [2] weight initialization](https://yeomko.tistory.com/40) ***
* Keras API Ref. : [Layer weight initializers](https://keras.io/api/layers/initializers/) **
* Github : [Keras Source Code: initializers.py](https://github.com/keras-team/keras/blob/7a39b6c62d43c25472b2c2476bd2a8983ae4f682/keras/initializers.py#L462) 
* [Hyper parameters in Action](https://towardsdatascience.com/hyper-parameters-in-action-part-ii-weight-initializers-35aee1a28404) **