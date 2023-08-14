# Weight Initialization (가중치 초기화)

ANN이 1990년대 부활의 싹을 틔우고 있을 때에 가장 큰 문제점은 바로 Gradient Vanishing (and Exploding) Problem이었다.

Weight Initialization은 이 문제를 개선하기 위한 방법으로 제안되었고 2010년에 상당한 성과를 보여 가장 먼저 위 문제에 대한 해법으로 널리 사용되게 된다 (현재도 기본적으로 사용된다.)

## Gradient Vanishing and Exploding Problems

Back-propagation의 경우, forward-flow와 backward-flow 두 단계로 수행되고, backward-flow에서는 loss function의 partial derivatives (=error gradient)가 output에서 input으로 전달되게 되는데,  
ANN이 깊을 경우 해당 gradient가 output에서 작은 값으로 시작되면 중간에 너무 작은 값이 되어 input에 가까울 layers의 weights를 제대로 update하지 못하고 소실되는 문제가 발생한다.

이를 Gradient Vanishing Problem이라고 부르며, 반대로 Gradient가 지나치게 증폭되어 model이 diverge하는 경우가 Gradient Exploding Problem임.

ANN의 경우 깊어져야 task에 대한 representative feature를 얻어낼 수 있는데, Gradient vanishing은 이를 막는 가장 큰 문제점이었다.

## Weight Initialization 등장 배경.

2000년대까지도 왜 이런 문제가 발생하는지를 정확히 파악하지 못했는데, 2010년 Xavier Glorot et al.에 의해 이를 획기적으로 개선(해결이 아니고 개선임)하는 방법으로 적절한 weight initialization과 activation function의 조합이 제안된다.

Xavier Glorot et al.이 찾은 원인은 다음과 같음

당시 ANN의 경우, 

* logistic activation function과 normal distirbution으로 초기화된 weights를 사용했는데, 
* 이 조합은 각 layer에서 input nodes와 output nodes의 수가 다른 점과 함께 작용하여
* layer에서 input에서의 variance와 output의 variance가 매우 달라지게 함을 확인함.

output의 variance가 커질 경우, forward-pass에서 점점 variance는 증가하게 되고 최종 output layer에 가까운 layer에서는 대부분 logistic activation function이 0 또는 1로 saturate되는 결과를 일으키게 된다.

이후 이루어지는 backward-pass에서는 derivatives가 전달되어야 하는데, logistic의 saturated region에서의 derivatives는 거의 0으로 너무나 작고, 이같이 작은 값으로 시작되는 backward-pass의 전달은 중도에서 정말 0이 되어버려 lower layer들로 제대로된 gradient를 전달되지 않게 된다.

더욱이 logistic activation의 출력은 mean이 0.5이다보니 (normal distribution 의 variance는 0임을 기억), forward pass에서 variance가 커지는 문제가 더 심해졌다. 이는 `tanh` 이 logistic보다 좀더 학습을 잘 시키는 이유의 근거가 된다. (`tanh`은 mean이 0임.)

ANN에서 gradient vanishing을 막으려면 다음이 성립해야 한다.

* 각 layer를 거쳐도 variance는 변화가 없어야 한다.
* 이는 forward-flow 와 backward-flow 모두에서 성립해야 한다.

이는 이론적으로는 불가능하지만, Xavier Glorot et al.은 일종의 좋은 타협안으로 activation과 weight initialization을 제시했고 성공을 거뒀다. 