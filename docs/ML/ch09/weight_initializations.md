# Weight Initialization (가중치 초기화)

ANN이 1990년대 부활의 싹을 틔우고 있을 때에 가장 큰 문제점은 바로 Gradient Vanishing (and Exploding) Problem이었다.

Weight Initialization은 이 문제를 개선하기 위한 방법으로 제안되었고 2010년에 상당한 성과를 보여 가장 먼저 위 문제에 대한 해법으로 널리 사용되게 된다 (현재도 기본적으로 사용된다.)

## Gradient Vanishing and Exploding Problems

Back-propagation의 경우, forward-flow와 backward-flow 두 단계로 수행되고, backward-flow에서는 loss function의 partial derivatives (=error gradient)가 output에서 input으로 전달되게 되는데,  
ANN이 깊을 경우 해당 gradient가 output에서 작은 값으로 시작되면 중간에 너무 작은 값이 되어 input에 가까울 layers의 weights를 제대로 update하지 못하고 소실되는 문제가 발생한다.

이를 Gradient Vanishing Problem이라고 부르며, 반대로 Gradient가 지나치게 증폭되어 model이 diverge하는 경우가 Gradient Exploding Problem임.

ANN의 경우 깊어져야 task에 대한 representative feature를 얻어낼 수 있는데, Gradient vanishing은 이를 막는 가장 큰 문제점이었다.

## Weight Initialization 중요성.

2000년대까지도 왜 이런 문제가 발생하는지를 정확히 파악하지 못했는데, 2010년 Xavier Glorot et al.에 의해 이를 획기적으로 개선(해결이 아니고 개선임)하는 방법으로 적절한 weight initialization과 activation function의 조합이 제안된다.

Xavier Glorot et al.이 찾은 원인은 다음과 같음

당시 ANN의 경우, 

* logistic activation function과 normal distribution으로 초기화된 weights를 사용했는데, 
* 이 조합은 각 layer에서 input nodes와 output nodes의 수가 다른 점과 함께 작용하여
* layer에서 input에서의 variance와 output의 variance가 매우 달라지게 함을 확인함.

output의 variance가 커질 경우, forward-pass에서 점점 variance는 증가하게 되고 최종 output layer에 가까운 layer에서는 대부분 logistic activation function이 0 또는 1로 saturate되는 결과를 일으키게 된다.

이후 이루어지는 backward-pass에서는 derivatives가 전달되어야 하는데, logistic의 saturated region에서의 derivatives는 거의 0으로 너무나 작고, 이같이 작은 값으로 시작되는 backward-pass의 전달은 중도에서 정말 0이 되어버려 lower layer들로 제대로된 gradient를 전달되지 않게 된다.

더욱이 logistic activation의 출력은 mean이 0.5이다보니 (normal distribution 의 variance는 0임을 기억), forward pass에서 variance가 커지는 문제가 더 심해졌다. 이는 `tanh` 이 logistic보다 좀더 학습을 잘 시키는 이유의 근거가 된다. (`tanh`은 mean이 0임.)

> 참고 : [Random variable의 곱과 variance](https://dsaint31.tistory.com/580) 

ANN에서 gradient vanishing을 막으려면 다음이 성립해야 한다.

* 각 layer를 거쳐도 variance는 변화가 없어야 한다.
* 이는 forward-flow 와 backward-flow 모두에서 성립해야 한다.
* 이를 위해선 layer의 input과 output이 동일한 variance를 가져야 한다.

이는 이론적으로는 불가능하지만, Xavier Glorot et al.은 일종의 좋은 타협안으로 activation과 weight initialization을 제시했고 성공을 거뒀다. 

사실 Yann LeCun et al. (1998)도 비슷한 형태의 Weight Initialization을 제시했다.

## "Fan in" and "Fan out"

$\text{fan}_\text{in}$
: layer에 들어오는 input node 수에 해당함. 

$\text{fan}_\text{out}$
: layer에 들어오는 output node 수에 해당함. 

***Ex.***: `conv2d` layer 에서 receptive field의 크기가 $5 \times 5$이고, input의 channel이 $3$ 이고 output은 $10$ 인 경우는 다음과 같음.

* `kernel_shape` : $5 \times 5 \times 3 \times 10$
* $\text{fan}_\text{in}$ : $5 \times 5 \times 3 = 72$
* $\text{fan}_\text{out}$ : $5 \times 5 \times 10 = 250$

## Weight Initialization Methods

초기에 constant로 고정된 경우나, Normal distribution을 사용한 경우는 오늘날 사용되지 않으며 다음의 방법들이 주로 이용된다.

주의할 것은 activation function에 따라 좀더 적절한 initialization이 결정된다는 점임. 때문에 아래 표도 궁합이 맞는 activation function이 같이 표기됨.

| Initialization | Activation functions | $\sigma^2$(Normal dist.) | [$-l$, $l$] (Uniform dist.) | TF impl. |
|:----:|:----:|:----:|:----:|:----:|
| Yann LeCun	| SELU	| $\sigma^2 = 1/\text{fan}_\text{in}$	| $l=\sqrt{3\sigma^2}$ | `lecun_normal`, `lecun_uniform`|
| Xavier Glorot |	None, tanh, sigmoid, softmax |	$\sigma^2 = 1/\text{fan}_\text{avg}$ | $l = \sqrt{3\sigma^2}$ | `glorot_normal`, `glorot_uniform` |
| Kaiming He	| ReLU, Leaky ReLU, ELU, GELU, Mish	| $\sigma^2 = 2/\text{fan}_\text{in}$ |	$l = \sqrt{3\sigma^2}$ | `he_normal`,`he_uniform`|

* 위의 normal distribution들은 variance만 차이가 있을 뿐, 모두 mean=0임.
* Xavier Glorto et al.이 제안한 방식의 경우, ReLU가 유행하기 전까지 가장 많이 사용되었으나 아쉽게도 ReLU와는 잘 맞지 않는다는 결과들로 인해 Kaiming He et al.의 방식이 제안됨.
* ReLU에서 0이상의 값은 그대로 통과시키다보니 다시 $\text{fan}_\text{in}$만을 고려하면서 LeCun의 방식에서 coefficient를 조금 다르게 줌. ReLU 계열들을 사용시 기본으로 사용됨.

## References
* [Efficient BackProp. Yann LeCun et al.1998](https://www.researchgate.net/publication/2811922_Efficient_BackProp)
* [Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification, Kaiming He et al., 2015](https://arxiv.org/abs/1502.01852)
* [갈아먹는 딥러닝 기초 [2] weight initialization](https://yeomko.tistory.com/40) ***
* Keras API Ref. : [Layer weight initializers](https://keras.io/api/layers/initializers/) **
* Github : [Keras Source Code: initializers.py](https://github.com/keras-team/keras/blob/7a39b6c62d43c25472b2c2476bd2a8983ae4f682/keras/initializers.py#L462) 
* [Hyper parameters in Action](https://towardsdatascience.com/hyper-parameters-in-action-part-ii-weight-initializers-35aee1a28404) **