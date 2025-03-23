# Back propagation (역전파, 오차 역전파)

***딥러닝 모델을 학습시키기 위한 핵심 알고리즘.***

Back propagation은 다음 2가지를 조합하여 ANN을 학습시킴.

- "Reverse-mode AutoDiff" (Reverse-mode automatic differentiation)
- ***"Gradient Descent"***

## Reverse-mode AutoDiff
 
* 컴퓨터로 정확하고 빠르게 Differentiation(미분)을 수행(=gradient 구하기)하기 위해  
^^여러 다른 분야에서 사용^^ 되는 알고리즘.  
* 1970년 Seppo Linnainmaa가 석사 논문 [The representation of the cumulative rounding error of an algorithm as a Taylor expansion of the local rounding errors](https://people.idsia.ch/~juergen/linnainmaa1970thesis.pdf)에서 제안.  
 
> 정말 천재적이라고 생각이 든다.  
> 복잡한 문제를 작은 단위로 나누어 처리하는 기본에 충실.
> 한 연산의 입/출력을 이용하여 local gradient를 구하고,  
> 이를 chain rule로 결합하여 전체 도함수의 값을 구해냄.

---

---

## Gradient Descent

* <u>loss function을 "model의 parameters"로 편미분</u>하여 구한 ***gradient를 이용*** 하여  
* 주어진 training dataset에 대해 loss function을 최소화하는 
* 최적의 parameters를 구하는 기법.

**참고:** [Gradient Descent Method](https://dsaint31.tistory.com/633)

## Back-propagation 의 역사. 

> 참고로, Back-propagation은 주로 딥러닝 분야에서 사용되는 용어이며  
> 다른 분야들에서는 Reverse-mode auto differentiation이라고 불림. 

* Back-propagation을 ANN의 학습에 적용시킨 이는 1974년 Paul J. Werbos임.  
* J. Werbos는 자신의 박사학위 논문 [Beyond regression: New tools for prediction and analysis in the behavioral sciences, 1974 (Paul J. Werbos, Ph.D. dissertation)](https://www.researchgate.net/publication/35055330_Beyond_regression_new_tools_for_prediction_and_analysis_in_the_behavior_sciences_microform)에서 이를 제안함.  
* 이후, Back-propagation은 현재의 Deep Learning의 전성기의 시작을 연 기념비적인 논문 중 하나인 1986년 Rumelhart와 Hinton의 [Learning internal representations by error propagation (Rumelhart, Hinton)](https://www.semanticscholar.org/paper/Learning-internal-representations-by-error-Rumelhart-Hinton/111fd833a4ae576cfdbb27d87d2f8fc0640af355)를 기점으로 **ANN의 학습기법** 으로 널리 사용되게 된다.

---

---

## **컴퓨터를 이용한 Differentiation** 

> Gradient Decent는 기본적으로 Differentiation의 수행을 요구함.

컴퓨터를 사용하여 Differentiation(미분)을 수행하는 방법은 크게 다음의 3가지로 나뉨.

1. Symbolic Differentiation
2. Numerical Differentiation
3. Forward-Mode or [Reverse-Mode Auto Differentiation](./reverse_mode_autodiff.md)

위의 1번과 3번의 경우는 ***Computation Graph 기법*** 에 의존하고 있음.

* [Tree와 Graph](https://dsaint31.tistory.com/463)
* [Graph란](./datastructure_graph.md)

특히 3번에서 Reverse-mode Auto Diff.는 Deep ANN을 학습시키기 위해 사용되는 대표적 기법임.

> Back-propagation은 Computation Graph를 사용하여 
> 
> * 수많은 연산을 node로 표현하고 
> * ***국소(local)적 계산*** 인 각 node에서의 ***input과 output*** 만을 사용하여 ***"partial derivative를 구하는 문제"를 단순화*** 할 수 있기 때문에
> * 복잡한 Deep ANN의 gradient를 효율적으로 계산할 수 있음.

---

---

## 참고: Computational Graph

계산 과정을 그래프로 나타낸 것(구조).  

- `node` : 주로, 연산 (operation) 및 변수 (variable)
    - 엄밀히는 계산의 기본 단위를 나타낸다.
    - `z = x + y`에서 `x`,`y`,`+`,`z`가 모두 node로 표시됨. 
- `edge` : node 간의 데이터의 흐름 방향을 나타냄. 
    - edge를 통해 연산의 입출력값이 결정됨.
    - 즉, 계산의 순서와 의존성을 정의함.

> ANN (특히 perceptron) 을 그래프로 그릴 때는 조금 다른 점을 주의하자.  
>
> * `node` : 주로, 변수 (variable)로 vector의 component. 또는 operation.
>     * 입력 벡터의 각 component나 출력 벡터의 각 component가 하나의 node차지.
>     * 경우에 따라  aggregation 이나 activation function 등의 연산도 node로 표현됨.  
> * `edge` : **edge에 지정된 weight과의 곱**. 계산그래프와의 차이.
>     * edge 시작점에 input variable이, 끝점에 output variable(=input과 weight의 곱)이 위치.    
>     * 단순히 데이터의 흐름 표시 외에 weight와의 곱과 activation  function을 거친 경우까지 표시하기도 함.
    
**참고** : [Reverse-Mode Autodiff (Auto-Differentiation) 관련자료](./reverse_mode_autodiff.md) 

---

---


## **Back-propagation** 의 동작 요약

Computational Graph 에 기반하며, 다음의 두 단계로 gradient를 구함.

- ***Forward pass*** 
    * “현재의 모델” 에서 주어진 training dataset에 대해 loss function 값을 구하면서 
    * 동시에 해당 forward pass에서 사용된 각 inputs와 모든 parameters와 intermediate results 를 저장 
        * 이는 predict나 inference 과정과의 차이점
    * Forward pass computes each result of all the operations and save any intermediates required to calculate gradient into memory.
- ***Backward pass*** 
    * `Reverse-mode Auto Diff`를 통해, 모델의 모든 inputs, parameters, 중간 결과들을 사용하여 ***loss function값을 편미분*** 하고,
    * 이들을 chain-rule에 기반하여 조합하여 
    * loss function을 최소화할 수 있는 최적의 parameters의 값으로 update하기 위해 
    * 필요한 ***gradients를 계산.*** 
        * loss function의 값을 오차로 볼 수 있으며, 
        * 이 오차를 반대방향으로 전파하면서 gradient가 구해진다고 볼 수 있음.
    * Partial differentiation with respect to all the inputs, parameters, and intermediate results.
    * Backward pass applies the chain rule to compute the gradient of the loss function with respect to the inputs, parameters, and intermediate results.
    
이처럼 구해진 gradient를 이용하여 ***Gradient Decent 기법*** 으로 Model의 parameters를 update함. 

- gradient를 구성하는 partial derivatives들과 learning ratio를 통해,
- 현재 loss function의 값을 만들어낸 모델의 parameter들( 오차에 관여하는 노드 값들의 weights와 bias)을 업데이트.

위의 과정을 통해 model의 parameters는 오차가 작아지는 방향(~ `loss function이 줄어드는 방향` = `-1 * gradient`)으로 반복해서 update가 이루어짐.

- 전체 training dataset의 samples에 대해 gradient를 계산하고 parameter update가 이루어지면 1번의 반복 (하나의 반복을 `epoch`라고 부름)이 끝남.
- 이를 여러 번 반복하고 반복한 횟수가 n인 경우 n `epoch` 수행했다 라고 기술함.

---

---

## **간단한 예**

1. input에 weight를 곱하고 bias를 합친 값 (affine transformation)이 threshold를 넘을 경우 1을 출력하고 아니면 0을 출력 (nonlinear activation) : 
    * `dense` layer (or fully connected layer) 와
    * `heavy side` function(or unit step function) 의 결합
2. 대상 `dense` layer에 대해 입력을 넣어 출력을 구하는 forward pass 수행.
3. ***2를 수행한 출력*** 과 **정답** 간의 ***오차*** 를 구하고, 해당 오차를 backward pass하여 오차를 줄이는 방향인 gradient를 구함.
4. Gradient Decent로 해당 gradient와 learning ratio를 통해 Model의 parameters를 업데이트. 