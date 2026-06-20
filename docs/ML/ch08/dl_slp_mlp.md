---
title: Perceptron and MLPClassifier
tags: [Perceptron, SLP, MLPClassifier, Classification, scikit-learn]
---

# Perceptron and MLPClassifier

`Perceptron`과 `MLPClassifier`는

* 둘 다 neural network 계열의 
* classification model로 볼 수 있음.

하지만 두 model은 구조와 표현력이 다름.

* `Perceptron`은 Single-Layer Perceptron, 즉 SLP의 대표적인 구현물임.
* `MLPClassifier`는 Multi-Layer Perceptron, 즉 MLP의 classification 구현물임.

여기서 중요한 점은

* `Perceptron`은 classification만 수행하는 단순한 linear classifier이고,
* `MLPClassifier`는 hidden layer를 통해 non-linear classification boundary를 학습할 수 있는 classifier라는 점임.

---

---

## Perceptron

> `Perceptron`은  
> 
> * 입력 feature들을 weighted sum으로 결합한 뒤,
> * 그 결과를 기준으로 class를 결정(step function 이용)하는
> * 가장 기본적인 neural network 기반 classifier임.

Perceptron의 기본 구조는 다음과 같음.

$$
\begin{aligned}z &= \mathbf{w}^\top \mathbf{x} + b \\
\hat{y} &= f(z)\end{aligned}
$$

여기서

* $\mathbf{x}$ : input feature vector
* $\mathbf{w}$ : weight vector
* $b$ : bias
* $z$ : linear combination 결과
* $f(z)$ : class를 결정하는 activation 또는 decision function

Perceptron은 hidden layer가 없음.

* input layer에서 output으로 바로 연결되는 구조임.
* 이 때문에 Perceptron은 Single-Layer Perceptron, 즉 SLP의 구현물로 볼 수 있음.

---

---

## Perceptron의 특징

Perceptron은 매우 단순한 classification model임.

주요 특징은 다음과 같음.

* classification 전용 model임.
* linear decision boundary를 학습함.
* hidden layer가 없음.
* non-linear pattern을 직접 학습하기 어려움.
* 학습 속도가 빠르고 구조가 단순함.
* `predict_proba()`를 제공하지 않음.

참고로, 

* scikit-learn의 `Perceptron`은
* `SGDClassifier`와 같은 내부 구현을 공유함.

실제로 다음 두 코드는 거의 같은 모델 객체를 반환함:

`Perceptron` 클래스 이용:

```python
Perceptron()
```

`SGDClassifier` 클래스 이용:

```python
SGDClassifier(
    loss="perceptron",
    eta0=1,
    learning_rate="constant",
    penalty=None,
)
```

scikit-learn에서  

* `Perceptron`은
* `'perceptron'` loss를 사용하는 
* linear classifier로 이해하면 됨.

---

---

## Perceptron의 한계

Perceptron은 linear decision boundary만 학습할 수 있음.

즉, 다음과 같은 형태의 결정 경계를 가짐.

$$
\mathbf{w}^\top \mathbf{x} + b = 0
$$

* 이 경계는 2차원에서는 직선이고,
* 고차원에서는 hyperplane임.

> Perceptron은 
> 
> * data가 선형적으로 구분 가능한 경우에는 사용할 수 있지만,
> * 복잡한 non-linear pattern을 가진 data에는 한계가 있음.
> 
> 대표적인 예가 **XOR 문제** 임.

XOR 문제는 하나의 직선 또는 hyperplane으로 class를 구분할 수 없기 때문에
단일 Perceptron만으로는 해결할 수 없음.

---

---

## Perceptron 사용 예

아래 예제는 scikit-learn의 `Perceptron`을 이용하여
Iris dataset을 classification하는 간단한 코드임:

```python
from sklearn.datasets import load_iris
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# 1. dataset load
X, y = load_iris(return_X_y=True)

# 2. train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

# 3. model 생성
model = make_pipeline(
    StandardScaler(),
    Perceptron(
        max_iter=1000,
        eta0=1.0,
        random_state=42,
    ),
)

# 4. training
model.fit(X_train, y_train)

# 5. prediction
y_pred = model.predict(X_test)

# 6. evaluation
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
```

`Perceptron`은 

* feature scale의 영향이 크기 때문에
* 일반적으로 `StandardScaler`와 같은 Feature Scaling이 함께 사용되어야 함.

---

---

## MLPClassifier

> `MLPClassifier`는  
> 
> * hidden layer를 포함하는
> * Multi-Layer Perceptron 기반 classification model임.

MLPClassifier는 

* Perceptron과 달리
* input layer와 output layer 사이에 
* 하나 이상의 hidden layer를 둘 수 있음.

기본 구조는 다음과 같음.

$$
\begin{aligned}
\mathbf{h} &= f(\mathbf{W}_{1}\mathbf{x} + \mathbf{b}_{1}) \\
\hat{y} &= g(\mathbf{W}_{2}\mathbf{h} + \mathbf{b}_{2})
\end{aligned}
$$

여기서

* $\mathbf{x}$ : input
* $\mathbf{h}$ : hidden layer의 출력
* $f$ : hidden layer activation function
* $g$ : output layer activation function
* $\hat{y}$ : predicted class 또는 class probability

MLPClassifier는 

* hidden layer와 
* step function 외의 (non-linaer) activation function을 사용하기 때문에
* linear model보다 복잡한 decision boundary를 학습할 수 있음.

---

---

## MLPClassifier의 특징

MLPClassifier의 주요 특징은 다음과 같음:

* classification 전용 MLP model임.
* hidden layer를 가질 수 있음.
* non-linear classification problem을 다룰 수 있음.
* backpropagation을 통해 weight를 학습함.
* `predict()`로 class label을 예측함.
* `predict_proba()`로 class probability를 얻을 수 있음.
* Perceptron보다 더 많은 hyperparameter를 조정해야 함.

> 참고로,  
> scikit-learn의 `MLPClassifier`는  
> 내부적으로 `log_loss`를 최적화함.

여기서 `log_loss`는 classification 문맥에서
negative log-likelihood, NLL을 가리킴.

* model이 true class에 높은 probability를 부여하면 loss가 작아지고,
* true class에 낮은 probability를 부여하면 loss가 커짐.

---

---

## MLPClassifier의 output activation과 loss

`MLPClassifier`는 

* classification task를 위한 model이므로
* output layer에서는 class probability를 출력하도록 동작함.

주의할 점은

* `activation="relu"`와 같은 parameter는
* hidden layer의 activation function을 지정하는 parameter라는 점임.

다음 코드에서 `activation="relu"`라고 하더라도  
output layer가 ReLU를 사용하는 것은 아님.

```python
MLPClassifier(
    hidden_layer_sizes=(100,),
    activation="relu",
)
```

`MLPClassifier`의 output activation은 task의 형태에 따라 내부적으로 다음과 같이 결정됨.

| task                       | output activation | loss                                                            | 출력 의미                          |
| -------------------------- | ----------------- | --------------------------------------------------------------- | ------------------------------ |
| binary classification      | logistic func.  | log loss<br/>binary cross-entropy / negative log-likelihood      | positive class에 속할 probability |
| multi-class classification | softmax           | log lossb<br/>categorical cross-entropy / negative log-likelihood | 각 class에 속할 probability        |
| multi-label classification | logistic func.  | label-wise binary cross-entropy / negative log-likelihood       | 각 label이 1일 probability        |

---

---

## binary classification에서의 log loss

binary classification에서 true label이
$y \in \{ 0, 1 \}$이고, model이 positive class probability를 $\hat{p}$로 예측한다고 하자.

이때 likelihood는 다음과 같음.

$$
P(y \mid \mathbf{x}) = \hat{p}^{y}(1-\hat{p})^{1-y}
$$

where

* $P(y \mid \mathbf{x})$: 입력 $\mathbf{x}$ 가 주어졌을 때 true label $y$가 관측될 likelihood.

이 likelihood에 negative log를 취하면 다음과 같음.

$$
\mathcal{L}_{\mathrm{NLL}}(y, \hat{p}) = -\log (P(y \mid \mathbf{x})) =
-\left[
y \log (\hat{p}) + (1-y)\log(1-\hat{p})
\right]
$$

where

* $y$ : true label. $0$ 또는 $1$의 값을 가짐.
* $\hat{p}$ : model이 예측한 positive class probability. 즉, $\hat{p}=P(y=1 \mid \mathbf{x})$.
* $1-\hat{p}$ : negative class probability. 즉, $P(y=0 \mid \mathbf{x})$.

이 식이 binary cross-entropy이고, classification 문맥에서는 `log loss`라고도 부름.

즉, binary classification에서는 다음 관계로 이해할 수 있음.

$$
\text{log loss} 
= \text{binary cross-entropy}
= \text{negative log-likelihood} \\
\mathcal{L}_{\text{log loss}}(y, \hat{p})
=
\mathcal{L}_{\mathrm{BCE}}(y, \hat{p})
=
\mathcal{L}_{\mathrm{NLL}}(y, \hat{p})
$$

where

* $\mathcal{L}_{\mathrm{NLL}}$ : negative log-likelihood.
* $\mathcal{L}_{\mathrm{BCE}}$ : binary cross-entropy.
* $\mathcal{L}_{\mathrm{log\ loss}}$ : binary classification에서의 log loss.

---

---

## multi-class classification에서의 log loss

multi-class classification에서는 여러 class 중 하나만 정답이 됨.

이때 output layer에서는 softmax를 통해 각 class에 속할 probability를 계산함.

수식을 살펴보면

* class가 $C$개이고,  
* 각 class probability를 $p_1, p_2, \dots, p_C$ 인 경우,  
* true class가 $k$라면 likelihood는 다음과 같음:

$$
P(y=k \mid x) = p_k
$$

따라서 negative log-likelihood는 다음과 같음.

$$
\mathcal{L}_{\mathrm{NLL}} = -\log (p_k)
$$

one-hot label $y_c$ 를 사용하면 다음처럼 쓸 수 있음.

$$
\mathcal{L}_{\mathrm{CCE}}(\mathbf{y}, \mathbf{p}) = -\sum_{c=1}^{C} y_c \log (p_c)
$$

이 식이 categorical cross-entropy이고,
multi-class classification에서의 log loss임.

즉, multi-class classification에서는 다음 관계로 이해할 수 있음.

$$
\text{log loss} = \text{categorical cross-entropy} = \text{negative log-likelihood} \\
\mathcal{L}_{\mathrm{log\ loss}} = \mathcal{L}_{\mathrm{categorical\ cross\ entropy}} = \mathcal{L}_{\mathrm{negative\ log\ likelihood}}
$$

여러 sample에 대한 평균 loss는 다음과 같음:

$$\mathcal{L}_{\text{log loss}} =
-\frac{1}{N}
\sum_{i=1}^{N}
\sum_{c=1}^{C}
y_{i,c}\log (p_{i,c})$$

---

---

## multi-label classification에서의 log loss

multi-label classification에서는 하나의 sample이 여러 label에 동시에 속할 수 있음.

* 예를 들어 하나의 image가 `cat`, `indoor`, `pet` label을 동시에 가질 수 있음.
* 이 경우 class들 중 하나만 고르는 softmax 구조가 적절하지 않음.

> multi-label classification에서는  
> 각 label을 독립적인 binary classification 문제처럼 다룸.

따라서 각 label마다 logistic sigmoid를 적용하여 해당 label이 1일 probability를 계산함.

수식으로 보면

* label이 $C$개이고,
* 각 label의 true value가 $y_c \in \{0, 1\}$,
* 예측 probability가 $\hat{p}_c$라고 하면 loss는 다음과 같음:

$$\mathcal{L}(\mathbf{y}, \hat{\mathbf{p}}) = -\frac{1}{C} \sum_{c=1}^{C}
\left[ y_c \log (\hat{p}_c) + (1-y_c)\log(1-\hat{p}_c) \right]$$

where

* $C$ : label의 개수
* $y_c$ : $c$번째 label의 실제값, 0 또는 1
* $\hat{p}_c$ : $c$번째 label이 1일 예측 확률
* $\mathcal{L}$ : multi-label classification에서의 loss.

즉, multi-label classification에서는
label별 binary cross-entropy를 합산하거나 평균낸 형태가 사용됨.

> 이것도 일종의 negative log-likelihood 임.

---

---

## MLPClassifier 사용 예

아래 예제는 scikit-learn의 `MLPClassifier`를 이용하여
Iris dataset을 classification하는 간단한 코드임.

```python
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# 1. dataset load
X, y = load_iris(return_X_y=True)

# 2. train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

# 3. model 생성
model = make_pipeline(
    StandardScaler(),
    MLPClassifier(
        hidden_layer_sizes=(100,),
        activation="relu",
        solver="adam",
        max_iter=1000,
        random_state=42,
    ),
)

# 4. training
model.fit(X_train, y_train)

# 5. prediction
y_pred = model.predict(X_test)

# 6. evaluation
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
```

`MLPClassifier`도 feature scale의 영향을 크게 받기 때문에
`StandardScaler`와 함께 사용하는 것이 일반적임.

---

## Perceptron과 MLPClassifier 비교

|                 | Perceptron                  | MLPClassifier                        |
| ----------------- | --------------------------- | ------------------------------------ |
| 기본 구조             | Single-Layer Perceptron     | Multi-Layer Perceptron               |
| hidden layer      | 없음                          | 있음                                   |
| 주요 용도             | classification              | classification                       |
| decision boundary | linear                      | non-linear 가능                        |
| 학습 방식             | perceptron learning rule 계열 | backpropagation                      |
| loss              | perceptron loss             | log loss                             |
| output activation | threshold 기반 decision       | task에 따라 logistic sigmoid 또는 softmax |
| 표현력               | 낮음                          | 높음                                   |
| 복잡도               | 낮음                          | 높음                                   |
| 확률 출력             | 일반적으로 제공하지 않음               | `predict_proba()` 제공                 |
| 주요 장점             | 단순함, 빠름                     | 복잡한 pattern 학습 가능                    |
| 주요 단점             | non-linear 문제에 약함           | hyperparameter 조정 필요                 |


## 언제 Perceptron/MLPClassifier 를 쓰는가?

Perceptron은 다음과 같은 경우에 적합함.

* 단순한 linear classification 문제
* baseline model이 필요한 경우
* neural network의 가장 기본 구조를 설명하는 경우
* SLP의 동작 원리를 보여주는 교육용 예제

Perceptron은 실무에서 복잡한 문제를 해결하기 위한 최종 model로 쓰기보다는
linear classifier와 neural network의 기본 개념을 설명할 때 유용함.


MLPClassifier는 다음과 같은 경우에 사용할 수 있음.

* linear classifier로 잘 분류되지 않는 문제
* feature 간의 non-linear 관계가 중요한 문제
* 간단한 neural network classifier를 scikit-learn API로 빠르게 실험하고 싶은 경우
* deep learning framework를 쓰기 전, MLP 구조를 간단히 실습하고 싶은 경우

주의할 점은,  

* MLPClassifier는 `hidden_layer_sizes`, `activation`, `solver`, `learning_rate_init`, `alpha`, `max_iter` 등의 hyperparameter에 영향을 많이 받음.
* 따라서 단순히 model만 바꾸는 것이 아니라
scaling, train/test split, validation, hyperparameter tuning을 함께 고려해야 함.
