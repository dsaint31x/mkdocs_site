# Back propagation (역전파, 오차 역전파)

***딥러닝 모델을 학습시키기 위한 핵심 알고리즘.***

다음을 2가지를 조합하여 ANN을 학습시킴.

- "Reverse-mode AutoDiff" (Reverse-mode automatic differentiation)
- "Gradient Descent"

`Reverse-mod AutoDiff` 
: 컴퓨터로 정확하고 빠르게 Differentiation(미분)을 수행(=gradient)하기 위해 ^^여러 다른 분야에서 사용^^ 되는 알고리즘.  
1970년 Seppo Linnainmaa가 석사 논문 [The representation of the cumulative rounding error of an algorithm as a Taylor expansion of the local rounding errors](https://people.idsia.ch/~juergen/linnainmaa1970thesis.pdf)에서 제안.  
(정말 천재적이라고 생각이 든다. 복잡한 문제를 작은 단위로 나누어 처리하는 기본에 충실)

`Gradient Descent`
: loss function을 model의 parameters로 편미분하여 구한 gradient를 이용하여  
주어진 training dataset에 대해 loss function을 최소화하는 최적의 parameters를 구하는 기법.

> Back-propagation은 주로 딥러닝 분야에서 사용되는 용어이며 다른 분야들에서 Reverse-mode auto differentiation으로 불림. 

Back-propagation을 ANN의 학습에 적용시킨 이는 1974년 Paul J. Werbos로 이를 박사학위 논문 [Beyond regression: New tools for prediction and analysis in the behavioral sciences, 1974 (Paul J. Werbos, Ph.D. dissertation)](https://www.researchgate.net/publication/35055330_Beyond_regression_new_tools_for_prediction_and_analysis_in_the_behavior_sciences_microform)에서 제안했으며,  
현재의 Deep Learning의 전성기의 시작을 연 기념비적인 논문 중 하나인 1986년 Rumelhart와 Hinton의 [Learning internal representations by error propagation (Rumelhart, Hinton)](https://www.semanticscholar.org/paper/Learning-internal-representations-by-error-Rumelhart-Hinton/111fd833a4ae576cfdbb27d87d2f8fc0640af355)를 통해 ANN의 학습기법으로 널리 사용되게 된다.

---

## 컴퓨터를 이용한 Differentiation. 

Gradient Decent는 기본적으로 Differentiation의 수행을 기반함.

컴퓨터를 사용하여 Differentiation(미분)을 수행하는 방법은 크게 다음의 3가지로 나뉨.

1. Symbolic Differentiation
2. Numerical Differentiation
3. Forward-Mode or [Reverse-Mode Auto Differentiation](./reverse_mode_autodiff.md)

위의 1번과 3번의 경우는는 Computation Graph 기법에 의존하고 있음.

특히 3번에서 Reverse-mode Auto Diff.는 Deep ANN을 학습시키기 위해 사용되는 대표적 기법임.

> Back-propagation은 Computation Graph를 사용하여 
> 
> * 수많은 연산을 node로 표현하고 
> * 국소적 계산인 각 node에서의 input과 output만을 사용하여 문제를 단순화할 수 있기 때문에
> * 복잡한 Deep ANN의 gradient를 효율적으로 계산할 수 있음.

`Computational Graph` 
: 계산 과정을 그래프로 나타낸 것.  
: - `node` : 연산 (operation)
: - `edge` : 데이터가 흘러들어가는 방향을 나타냄.
    
    
참고 : [Reverse-Mode Autodiff (Auto-Differentiation) 관련자료](./reverse_mode_autodiff.md) 

---

## Back-propagation

Computational Graph 에 기반하며, 다음의 두 단계로 gradient를 구함.

- ***Forward pass*** 
    * “현재의 모델” 에서 주어진 training dataset에 대해 loss function 값을 구하면서 
    * 동시에 해당 forward pass에서 사용된 각 inputs와 모든 parameters와 intermediate results 를 저장 (predict나 inference과정과의 차이점)
    * Forward pass computes each result of all the operations and save any intermediates required to calculate gradient into memory.
- ***Backward pass*** 
    * `Reverse-mode Auto Diff`를 통해 모델의 모든 inputs, parameters, 중간 결과들로 loss function값을 편미분하고,
    * 이들을 chain-rule에 기반하여 조합하여 loss function을 최소화할 수 있는 최적의 parameters의 값으로 update하기 위해 필요한
    * gradients를 계산. (loss function의 값을 오차로 볼 수 있으며, 이 오차를 반대방향으로 전파하면서 gradient가 구해진다고 볼 수 있음.)
    * Partial differentiation with respect to all the inputs, parameters, and intermediate results.
    * Backward pass applies the chain rule to compute the gradient of the loss function with respect to the inputs, parameters, and intermediate results.
    
이처럼 구해진 gradient를 이용하여 ***Gradient Decent 기법*** 으로 Model의 parameters를 update함. 

- gradient를 구성하는 partial derivatives들과 learning ratio를 통해,
- 현재 loss function의 값을 만들어낸 모델의 parameter들( 오차에 관여하는 노드 값들의 weights와 bias)을 업데이트.

위의 과정을 통해 model의 parameters는 오차가 작아지는 방향(~ `loss function이 줄어드는 방향` = `-1 * gradient`)으로 반복해서 update가 이루어짐.

- 전체 training dataset의 samples에 대해 gradient를 계산하고 parameter update가 이루어지면 1번의 반복횟수로 count함.
- 이 반복횟수를 `1 epoch`라고 부름.

---

## 간단한 예

1. input에 weight를 곱하고 bias를 합친 값 (linear)이 threshold를 넘을 경우, 1을 출력하고 아니면 0을 출력 (nonlinear) : `dense` layer (or fully connected layer)
2. 1의 과정을 입력층 → 은닉층 → 출력층 순으로 적용하는 forward propagation 수행.
3. ***2를 수행한 출력*** 과 **정답** 간의 ***오차*** 를 구하고, 해당 오차를 back-propagation하여 오차를 줄이는 방향인 gradient를 구함.
4. Gradient Decent로 해당 gradient와 learning ratio를 통해 Model의 parameters를 업데이트. 