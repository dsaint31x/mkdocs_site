# Logistic Regression

Logistic Regression은 이름과 달리, binary classification task를 위한 모델로서 특정 class에 속할 확률을 출력해준다 (output이 하나의 확률값임).

다음의 순서를 따름.

1. Regression으로 어떤 score $t$ (=*logit score* or *log odds score* )를 구함 
2. 해당 score를 logistic function의 입력값으로 넣으면 0~1사이의 확률값 $\hat{p}$이 나옴.
3. 해당 확률로 classification (binary classification)

참고 : [Logit을 통한 Logistic Regression 유도](https://dsaint31.tistory.com/320)

> 이 문서는 Logistic Regression을  
> Bernoulli Distribution에 기반한 Maximum Likelihood Estimation의 관점으로 해석하여  
> DL에서의 binary classification model에 대한 이해로 확장해나가는 것을 목표로 함.

![](./img/logistic_regression_ann.png)

$$
\hat{p}(\hat{y}=1) = \sigma(t) = \sigma \left( b+\omega_1x_1+\omega_2x_2 +\dots+\omega_n x_n\right)
$$

* [ori](https://docs.google.com/presentation/d/1EG6nPMYbYjS4CcCVHSpMDOg7iwlzZLxahb0E9S2LkQg/edit#slide=id.g23bf78dd669_0_0)

---

## Binary Classification

input $\textbf{x}$가 주어질 경우, 출력이 binary class를 나타내는 task를 binary classification임.

ANN등으로 만들 경우, output이 숫자 하나로 나오며 특정 class에 속할 확률 $\hat{p}$로 나오게 된다. 이는 다른 class에 속할 확률이 $\hat{q}=1-\hat{p}$임을 의미하기도 한다.

해당 task에 대해 label은 $y \in \{0,1\}$로 주어져서 $i$번째 input $\textbf{x}^{(i)}$에 대응하는 label $y^{(i)}$는 0 또는 1 중의 하나가 된다.

---

## Posterior probability로 살펴본 Binary classification.

binary classification model의 output이   
**$\hat{y}$가 1일 확률 $\hat{p}$** 는  
logistic regression의 경우 다음과 같이 주어진다.

$$\hat{p}=h_{\boldsymbol{\theta}}(\textbf{x})=\sigma(\textbf{x}^T\boldsymbol{theta})$$

* $h_{\boldsymbol{\theta}}( \cdot )$ : hypothesis. model을 나타내는 function으로 model의 parameters가 $\boldsymbol{\theta}$임을 의미.
* $\hat{p}$ : 1에 속할 확률. model이 예측한 결과이므로 hat이 씌어짐.
    * logistic regression의 output임.
* $\sigma( \cdot )$ : logistic function.

이 $\hat{p}$는 $\textbf{x}$와 $\boldsymbol{\theta}$가 주어졌을 때, $\hat{y}=1$일 일종의 사후확률(posterior probability)이며 해당 확률이 0.5 이상이며 $\hat{y}=1$이라고 판정하고 아니면 $\hat{y}=0$이라고 판정한다고 볼 수 있음.

이를 다음과 같이 표기할 수 있다.

$$p(y=1 | \textbf{x}) \approx \hat{p}(y=1 | \textbf{x}; \boldsymbol{\theta}) = h_{\boldsymbol{\theta}}(\textbf{x})$$

이는 model의 (trainable) parameters $\boldsymbol{\theta}$는 

* training dataset $\left\{(x^{(i)},y^{(i)})| i=1, \dots, M \right\}$ ($M$은 training dataset에서 sample의 갯수임)에서 model로부터 얻는 posterior probability distribution $\hat{p}(\hat{y}=1| \textbf{x}; \boldsymbol{\theta})$가 
* 실제 training dataset의 확률분포 $p(y=1 | \textbf{x})$에 가장 비슷하도록 조정됨을 의미한다.

---

## Logistic regression model이 정답을 맞출 확률 : Bernoulli Distribution

모델이 $i$번째 sample의 input $\textbf{x}^{(i)}$에 대해 정답 $y^{(i)}$을 맞출 확률 $p$는 다음과 같이 정의할 수 있다.

$$p(y^{(i)}|\textbf{x}^{(i)};\boldsymbol{\theta})=(\hat{p}^{(i)})^{y^{(i)}}(1-\hat{p}^{(i)})^{1-y^{(i)}}$$

* $p(y^{(i)}|\textbf{x}^{(i)};\boldsymbol{\theta})$는 주어진 $i$번째 input $\textbf{x}$와 현재 model parameters $\boldsymbol{\theta}$ 하에서 모델이 정답(label) $y^{(i)}$를 출력할 likelihood를 의미함.
* $\hat{p}^{(i)}=\sigma(\textbf{x^{(i)}}^T\boldsymbol{\theta})$ 는 input $\textbf{x}^{(i)}$에 대한 logistic regression의 출력으로 예측치 $\hat{y}=1$이 될 확률임.

위의 식은 Logistic regression model이 정답을 맞출 확률 $p$가 ***Bernoulli random variable의 distribution*** 을 따름을 보여줌 (위의 식은 Bernoulli distribution의 PMF임).

* ref. : [Bernoulli distribution에 대해서](https://dsaint31.tistory.com/582)

**label $y^{(i)}=0$인 경우**
: Logistic regression model의 output $\hat{p}$가 0에 가까울수록 정답에 가까운 것이므로 위의 $p$는 1에 가까워지고, 반대인 경우엔 $p$는 0에 가까워지므로 model의 결과가 얼마나 정확한지를 의미함.

**label $y^{(i)}=1$인 경우**
: Logistic regression model의 output $\hat{p}$가 1에 가까울수록 정답에 가까운 것이므로 $p$가 1에 가까워지고, 반대인 경우엔 $p$가 0에 가까워지므로 model의 결과가 얼마나 정확한지를 의미함.

> 참고로 Bernoulli random variable은 0 또는 1을 값으로 가지는 discrete random variable 임.  
> Binary classification가 Bernoulli trial로 볼 수 있음을 의미함.  
> 달리 말하면 model의 output (=종속변수)가 Bernoulli probability distribution을 따른다고 볼 수 있음.

위의 $p(\hat{y}|\textbf{x};\boldsymbol{\theta})$를 likelihood로 삼아 

(ref. : [likelihood (우도)](https://dsaint31.tistory.com/317))

이를 최대화하는 maximum likelihood expectation (`MLE`)는 다음과 같으며, 이 `MLE`를 통해 구해진  
likelihood를 최대화 하는 parameters $\boldsymbol{\theta}$가 바로 학습이 끝난 model을 구성한다.

> 각 likelihood들의 joint probability를 통해 training dataset의 모든 $M$개의 sample들에 기반한 최적의 parameters $\boldsymbol{\theta}$를 구한다.  
(모델에서 각 sample들이 서로의 class를 결정할 때 각각에 대해 독립이라는 가정에 기반.)  

$$\begin{aligned}\boldsymbol{\theta}&=\underset{\boldsymbol{\theta}}{\text{argmax }} \prod _{i=1}^M p(y^{(i)}|\textbf{x}^{(i)};\boldsymbol{\theta})\\&=\underset{\boldsymbol{\theta}}{\text{argmax }} \prod _{i=1}^M \mathcal{L}(\boldsymbol{\theta}|\textbf{x}^{(i)},y^{(i)})\\&=\underset{\boldsymbol{\theta}}{\text{argmax }} \prod _{i=1}^M (\hat{p}^{(i)})^{y^{(i)}}(1-\hat{p}^{(i)})^{1-y^{(i)}}\end{aligned}$$

* $\displaystyle \prod _{i=1}^M p(y^{(i)}|\textbf{x}^{(i)};\boldsymbol{\theta})$가 최대화된다는 것은 Logistic regression model이 정답을 맞출 확률이 커진다는 것을 의미함.
* $\boldsymbol{\theta}$를 조절하면 해당 확률은 변하며, 각각의 $\boldsymbol{\theta}$에 따른 해당 확률값들을 모두 더할 경우 1이 되진 않음 (물론 값이 클수록 가능성은 커짐) : 때문에 likelihood라고 부르며 이 부분을 강조하여 $\mathcal{L}$로 표기하기도 함.
* 이는 $\hat{p}=\sigma(\textbf{x}^T\boldsymbol{\theta})$ 는 logistic regression의 출력으로 $\hat{y}=1$이 될 확률임에 기반.


---

## Negative Log-Likelihood

`MLE`는 ^^utility function을 사용하므로 최대화가 목표^^ 이므로, loss function으로 사용하기 위해서는 다음과 같이 최소화의 문제로 바꾸면 됨.

* 위의 likelihood를 loss function으로 바꾸면 
* `-` 기호를 붙여주면(negation) 된다. 
* `-1`을 곱하면 utility function을 loss function으로 변경하게 됨.

그리고 likelihood를 training dataset의 모든 샘플에 대해 구하기 위해선 

* 각 likelihood를 곱해야 하는데, 
* 이처럼 곱해주는 것($\prod$)보다는 
* 더해나가는게($\sum$) 편하므로 
* $\log$를 취해주는 경우가 일반적임.

이같은 방식을 가르켜 ***Negative Log Likelihood*** 라고 부름.

* Negative : loss function으로 삼아 최소화 문제로 변경.
* Log : $\prod$ 대신 $\sum$을 사용하기 위해.

이를 통해 얻은 Objective function (=loss function) $J$는 다음과 같음.

$$J(\boldsymbol{\theta}) = -\frac{1}{m} \sum_{i=1}^m \left[ y^{(i)}\log \left(\hat{p}^{(i)}\right)+ (1-y^{(i)})\log\left(1-\hat{p}^{(i)}\right)\right]$$

* $J(\boldsymbol{\theta})$는 loss function이 parameters $\boldsymbol{\theta}$를 독립변수로 삼는 함수임을 강조한 표기.
* 이 loss function을 ***Logistic Loss*** 또는 ***Negative Log Loss***, ***Log Loss*** 라고 부름.

<br/>

지금까지 살펴본 내용은 다음을 의미함.

* binary classification인 logistic regression은 일종의 `MLE`라고 볼 수 있다.
* 해당 `MLE`는 확률분포가 Bernoulli Distribution이라는 것을 기반으로 한다.
* Likelihood objective function을 Negative Log Likelihood로 바꾸어서 사용한다.

> DL에서 binary classification에서 이용하는 cross-entropy 와 위의 Negative Log Likelihood 를 살펴보면 매우 유사함을 알 수 있음. 
>  
> [Cross Entropy란?](https://dsaint31.tistory.com/entry/Math-Cross-Entropy)

참고로 위의 loss function은 linear regression (=logistic activation이 없는 경우)과 달리 closed form solution이 알려져 있지 않음. 

* Normal equation과 같은 analytic method로 최적의 parameter를 단번에 직접 구할 수 없음.
* sigmoid activation의 도입으로 non-linear이며, non-linear의 경우 거의 대부분 쉽게 풀리지 않는다(closed form solution 없음). ==;;

하지만, 다행스럽게도 위의 loss function은 ***convex function*** 임.

* Gradient Decent를 사용할 경우 global minimum에 해당하는 parameters를 항상 구할 수 있음을 의미함. 

---

## Logistic cost function partial derivatives

loss function $J(\boldsymbol{\theta})$를 $j$번째 parameter $\theta_j$에 대한 partial derivatives는 다음과 같음.

$$\dfrac{\partial}{\partial \theta_j}J(\boldsymbol{\theta})=\frac{1}{M}\sum_{i=1}^M \left( \color{red}{\sigma \left( \boldsymbol{\theta}^\text{T}\textbf{x}^{(i)}\right) - y^{(i)}}\color{black}\right)\color{blue}{x_j^{(i)}}$$

* $M$ : training set에서의 instance 수.
* 각 instance에 대해,
    * prediction error (red)를 구하고
    * 여기에 해당하는 input vector의 $j$ feature (blue) $x_j^{(i)}$를 곱하고
* 이를 training set의 모든 instances에 대해 averaging.

위와 같은 partial derivatives를 통해 gradient $\nabla_{\boldsymbol{\theta}}J(\boldsymbol{\theta})$를 구하고,  
이를 이용한 Gradient Decent method로 parameters를 구해나가면  
Logistic regression의 training이 이루어짐. 

* [참고: Gradient Decent Method (GD)](https://dsaint31.tistory.com/633)

---

## Logistic Regression 과 ANN : negative log loss vs. MSE for binary classification

Logistic Regression은 ANN (or `DL`)의 관점에서 보면  

***logistic activation의 single fully connected layer*** (single layer `FCN`) 임.  
(loss function은 `cross-entropy`). 

* 앞서 살펴본 negative log likelihood object function은 ***convex*** 하기 때문에  global minimum을 구하는게 보장된다. (주의할 건 이는 single layer인 경우에 한정됨.)
* 단, 여러 layer를 쌓는 경우 convexity는 유지되지 않는다.
    * `DL`에서 convexity가 유지되는 경우는 거의 없다고 봐도 된다. ㅠㅠ
    * 하지만 `DL`로 구해진 solution들은 global minimum이라는 보장은 없으나 실제로 task를 수행하는데 충분한 성능을 보임.

> 달리 말하면, 이 `single layer FCN`도  
> negative log likelihood를 object function으로 삼은 (Bernoulli Distribution에 기반한) ***`MLE`의 일종***  
> 으로 해석가능함을 의미함.  

***$\boldsymbol{\theta}$는 실제로 여러 개의 parameters로 구성된 `vector`*** 이나 이를 scalar로 단순화하고 logistic regression의 objective function을 parameter에 대해 그리면 convex임을 확인 가능함 (input 도 scalar로 단순화하고 이는 고정시킴).


single fully connected layer 로 구현할 경우  
ANN의 loss function을  
앞서 말한 cross entropy가 아닌,  
regression의 경우처럼 다음과 같은 ***Mean squared loss*** `MSE`로 삼을 수도 있긴 함(가능하지만 권장하진 않음).

$$\text{MSE}=\left(\frac{1}{1+e^{-\sum_{i=1}^{N}\theta_i x_i}}-1\right)^2$$

하지만 `MSE`를 loss로 사용하는 경우,  
아래 그림(red line)에서 보이듯이 
`MSE`는 convexity도 성립하지 못하며,  
loss function의 최대값 (기껏해야 1)도 제한되는 단점이 있음을  
확인할 수 있다.  
(반면에 negative log의 경우 loss function은 최대값이 무한대까지의 범위를 보임)

* 매우 틀린 오답을 현재 parameters의 모델이 보일 경우, negative log loss는 매우 큰 값을 보이지만, 
* `MSE` loss는 그리 큰 값을 보이지 못함.
* 큰 오차에서는 가급적 큰 loss를 가져야 함.
* 때문에 `MSE`의 경우, 오차가 큰 초반 epoch 초반에 weight들이 최적의 값으로 빠르게 변화하지 못하는 단점을 추가적으로 가짐.

<figure markdown>
![](./img/nll_vs_mse.png){width="400" align="center"}
</figure>

때문에 binary classification task를 수행하는 ANN에서 `MSE`보다는 `cross-entropy`를 선호한다.

수학적으로 비교할 경우, weight와 bias에 대한 loss function의 partial derivative를 확인해보면 왜 MSE가 적절치 않은지를 확인할 수 있음.

아래는 `MSE`의 partial derivative임.  
앞서 보였던 logistic regression의 loss (=Cross entropy cost)와 달리  
$\color{red}{\sigma^\prime \left(\boldsymbol{\theta}^\text{T}\textbf{x}^{(i)}\right)}$ term이 중간에 추가되어 있는데,  
이 sigmoid의 미분 term으로 인해  
partial derivative가 작은 값으로 감소하게 되고  이로인해 back-propagation에서 효과적인 training을 하기 어렵게 된다.

$$\begin{aligned}\dfrac{\partial}{\partial \theta_j}J(\boldsymbol{\theta})&=\frac{1}{M}\sum_{i=1}^M \left( {\sigma \left( \boldsymbol{\theta}^\text{T}\textbf{x}^{(i)}\right) - y^{(i)}}\right)\color{red}{\sigma^\prime \left(\boldsymbol{\theta}^\text{T}\textbf{x}^{(i)}\right)}\color{black}{x_j^{(i)}}\\&=\frac{1}{M}\sum_{i=1}^M \left( {\sigma \left( \boldsymbol{\theta}^\text{T}\textbf{x}^{(i)}\right) - y^{(i)}}\right)\color{red}{\sigma \left(\boldsymbol{\theta}^\text{T}\textbf{x}^{(i)}\right)(1-\sigma \left(\boldsymbol{\theta}^\text{T}\textbf{x}^{(i)}\right))}\color{black}{x_j^{(i)}}\end{aligned}$$

* logistic의 derivative는 0.25를 max로 가지는 normal distribution의 모양임.
* tanh의 경우, logistic보다 큰 derivative를 가지고 있어서 학습에 보다 유리한 것으로 알려짐.

결론적으로 Binary Classification의 경우,  
MSE 보다는 cross entropy가 보다 적합한 loss function임.

참고1: [derivative of logistic function](https://dsaint31.tistory.com/613)

참고2: [hyperbolic tangent function](https://dsaint31.tistory.com/577)

---

## Multi-class Classification으로 확장.

Logistic regression의 logistic function을 multi-class로 확장하면 softmax function이 된다.

* 증명 : [https://dsaint31.tistory.com/319](From softmax to logistic function)

> 이는 binary classification이 logistic function을 activation으로 하던 것을 일반화하여  
> multiclass classification의 경우  
> softmax function을 activation으로 삼게 됨을 의미함.

* [참고 : softmax function](https://dsaint31.tistory.com/294)

Logistic Regression이 Beroulli Distribution에 기반한 `MLE` 였던 것을 multi-class classification으로 일반화하면, Gaussian Distribution에 기반한 `MLE`가 된다.

즉, `Softmax` function을 이용한 ***multi-nomial logistic regression*** (or softmax regression) 모델은  

***각 class에서 sample들의 분포가 각각의 class의 중심으로부터 Gaussian Distribution을 따른다.***

라고 가정하고 classification이 이루어지는 것이다.

때문에 해당 가정에 맞지 않는 classification task에서는 잘 동작하지 않는다.

> 비슷하게 `MSE`를 기반으로 하는 linear regression의 경우,  
>
> data가 linear하고 residual error 가 Normal Equation을 따른다.
>  
> 라는 가정을 기반으로 regression이 수행되기 때문에  
> 해당 가정에 맞지 않는 task에서는 bias가 발생한다.

NFLT (No Free Lunch Theorme)에 의해
* Model이 기반하고 있는 가정이 성립하는 경우 해당 model은 좋은 성능을 보이지만, 
* 아닐 경우 더 나쁜 성능을 보일 수 밖에 없다.

[No Free Lunch Theorem](https://dsaint31.tistory.com/605)

---

## References

[Minimizing the Negative Log-Likelihood, in English](https://willwolf.io/2017/05/18/minimizing_the_negative_log_likelihood_in_english/?fbclid=IwAR0nSqtezeZqG0kc2OqQZBSzxB-UXiNKILD44oPGlFcPxGdTbPyOokDyIVE)