---
title: "Perceptron과 Linear Regression의 차이"
description: "Perceptron과 Linear Regression의 linear output, loss, prediction, update 방식의 차이를 비교하고 scikit-learn Perceptron의 SGD 기반 구현과 연결"
tags:
  - Machine Learning
  - Perceptron
  - Linear Regression
  - Logistic Regression
  - SGD
  - SGDClassifier
  - Linear Models
categories:
  - Machine Learning
  - Linear Models
---

# Perceptron과 Linear Regression의 차이

Perceptron, Logistic Regression과 Linear Regression은 모두 linear combination을 사용함:

$$
z=\mathbf{w}^{\top}\mathbf{x}+b
$$

차이는 이 linear output을 어떻게 사용하고, 어떤 loss와 update rule로 학습하는지에 있음.

---

---

## 1. Linear Regression

Linear Regression의 목적은 continuous value prediction임.

Prediction은 linear output 자체를 사용:

$$
\hat y=z
$$

대표적인 loss는 Mean Squared Error, MSE:

$$
L_{\mathrm{MSE}} = \frac{1}{2}(y-\hat y)^2
$$

Linear Regression 자체가 sample-wise update를 반드시 요구하는 것은 아님.

* Batch Gradient Descent: 전체 training set으로 update.
* SGD: single sample 단위로 update.
* Mini-batch Gradient Descent: 일부 sample 단위로 update.
* closed-form solution을 사용하는 경우 iterative update 자체가 필요하지 않을 수도 있음.

Linear Regression을 SGD로 학습하는 경우의 weight update는 다음과 같음:

$$
w_i^{(\mathrm{next})} = w_i+\eta(y-\hat y)x_i
$$

여기서 prediction error는 continuous value이므로 ***error magnitude가 update 크기에 직접 반영됨.***

### 참고: SGD를 통한 Linear Regression

Linear Regression을 SGD로 학습하는 경우 gradient는 다음과 같음:

$$
\frac{\partial L}{\partial w_i} = (\hat y-y)x_i
$$

Gradient Descent는 gradient의 반대 방향으로 parameter를 update하므로 다음이 성립:

$$
\begin{aligned}
w_i^{(\mathrm{next})} &= w_i-\eta(\hat y-y)x_i \\
&= w_i+\eta(y-\hat y)x_i
\end{aligned}
$$

---

---

## 2. Logistic Regression

Logistic Regression은 

* binary classification을 위한 linear model임.
* Logistic function 자체는 19세기에 제안되었으며,
    * Joseph Berkson이 1944년 logit을 이용한 binary response model을 제안하면서
    * 현대적인 Logistic Regression의 기반이 마련됨.

Linear combination은 Linear Regression과 동일:

$$
z=\mathbf{w}^{\top}\mathbf{x}+b
$$

하지만 linear output을 그대로 prediction으로 사용하지 않고 sigmoid function을 적용:

$$
\hat{y} = \sigma(z) = \frac{1}{1+e^{-z}}
$$

따라서 

* output은 0과 1 사이의 continuous value이며,
* 일반적으로 positive class에 대한 estimated probability로 해석함:

$$
0<\hat{y}<1
$$

대표적인 loss는 Binary Cross-Entropy, BCE:

$$
L_{\mathrm{BCE}} = -\left[ y\log\hat{y} + (1-y)\log(1-\hat y) \right]
$$

sigmoid와 BCE를 함께 사용하는 경우 weight에 대한 gradient는 다음과 같이 정리됨:

$$
\frac{\partial L}{\partial w_i} = (\hat y-y)x_i
$$

따라서 SGD update는 다음과 같음:

$$
w_i^{(\mathrm{next})} = w_i+\eta(y-\hat y)x_i
$$

위의 식의 형태만 보면 Linear Regression을 SGD로 학습할 때의 update와 동일함.

차이는 prediction error의 의미에 있음.

**Linear Regression:**

$$
y-\hat y\in\mathbb{R}
$$

* continuous residual.
* error magnitude가 update 크기에 직접 반영됨.

**Logistic Regression:**

$$
-1<y-\hat y<1
$$

* target class와 predicted probability 사이의 차이.
* probability가 target에서 얼마나 떨어져 있는지가 update 크기에 반영됨.

---

---

## 3. Perceptron

Perceptron은 Frank Rosenblatt가 1957년 제안한 초기 artificial neural network model임 (이를 소개한 대표 논문은 1958년에 출판됨).

Perceptron의 목적은 binary classification임.

Weighted sum은 Linear Regression과 동일:

$$
z=\mathbf{w}^{\top}\mathbf{x}+b
$$

Prediction은 step activation을 통해 결정됨:

$$
\hat y=
\begin{cases}
1, & z\geq0 \\
0, & z<0
\end{cases}
$$

Output은 binary:

$$
\hat y\in \{0,1\}
$$

0/1 notation에서 Perceptron의 weight update는 다음과 같음:

$$
w_i^{(\mathrm{next})} = w_i+\eta(y-\hat y)x_i
$$

형태만 보면 Linear Regression을 SGD로 학습할 때의 update와 동일하게 보임.

차이는 prediction error의 의미에 있음.

**Linear Regression:**

$$
y-\hat y\in\mathbb{R}
$$

* continuous residual.
* error magnitude가 update 크기에 직접 반영됨.

**Perceptron:** 

$$
y-\hat y\in \{-1,0,+1\}
$$

* correct classification: no update.
* false negative: positive direction update.
* false positive: negative direction update.
* 기본 Perceptron에서는 decision boundary에서 얼마나 멀리 틀렸는지가 update 크기에 직접 반영되지 않음.

--- 

---

## 4. Update 방식의 차이

Perceptron은 classical algorithm 자체가 sample-wise update를 사용함.

Training sample을 하나씩 확인하고, misclassification이 발생하면 즉시 parameter를 update:

$$
\mathbf{w}^{(\mathrm{next})} = \mathbf{w}+\eta(y-\hat y)\mathbf{x}
$$

즉, Perceptron은 기본적으로 stochastic 또는 online 형태의 learning rule을 가짐.

scikit-learn의 `Perceptron`도 같은 방식으로 구현되어 있음. 

* `fit()`에 전체 training set을 전달하지만
* Batch Gradient Descent를 수행하는 것은 아님.
* Training data를 sample 단위로 순회하면서
* misclassified sample에서 parameter를 update하며,
* 전체 dataset의 한 번의 순회가 one epoch에 해당함.

scikit-learn의 `Perceptron`은 다음 `SGDClassifier` 설정과 equivalent함:

```python
SGDClassifier(
    loss="perceptron",
    learning_rate="constant",
    eta0=1,
    penalty=None
)
```

즉,

* loss="perceptron": Perceptron loss 사용.
* learning_rate="constant": constant learning rate.
* eta0=1: learning rate를 1로 설정.
* penalty=None: regularization 없음.
* sample-wise SGD update를 수행.

반면 Linear Regression과 Logistic Regression은 model 자체가 특정 update unit을 강제하지 않음.

* Batch GD,
* SGD,
* mini-batch GD 또는
* 다른 optimization algorithm

등으로 학습할 수 있음.

Linear Regression의 경우 closed-form solution도 사용할 수 있음.

---

---

## 5. 핵심 비교

|                    | Linear Regression    | Logistic Regression	 | Perceptron |
| --- | --- | --- | --- |
| Task               | Regression           | Binary classification | Binary classification |
| Linear output      | prediction 자체        | logit | decision score |
| Final output       | continuous           | probability | binary |
| Activation         | 없음                   | logistic func. | step function |
| 대표 loss            | MSE                  | Binary Cross-Entropy | Perceptron loss |
| Error              | continuous residual  | probability error | classification error |
| Update 크기          | error magnitude 반영   | error magnitude 반영 | misclassification 방향 중심     |
| Sample-wise update | 필수 아님                | 필수 아님 | classical rule에서 기본         |
| Decision boundary  | classification 목적 없음 | linear decision boundary 사용 | linear decision boundary 사용 |

세 모델의 SGD-style update는 형태적으로 매우 유사함.

**Linear Regression with SGD:**

$$
w_i^{(\mathrm{next})} = w_i+\eta(y-\hat y)x_i
$$

**Logistic Regression with SGD:**

$$
w_i^{(\mathrm{next})} = w_i+\eta(y-\hat y)x_i
$$

**Perceptron:**

$$
w_i^{(\mathrm{next})} = w_i+\eta(y-\hat y)x_i
$$

그러나 prediction의 의미가 다름.

* Linear Regression에서는 prediction이 실제 값 자체를 의미하는 continuous output이고, 
* Perceptron에서는 decision boundary를 기준으로 한 class label을 결정하기 위한 score라는 점에서 차이가 있음.

**Linear Regression:**

$$
\hat y=\mathbf{w}^{\top}\mathbf{x}+b
$$

**Logistic Regression:**

$$
\hat y=\sigma(\mathbf{w}^{\top}\mathbf{x}+b)
$$

**Perceptron:**

$$
\hat y=\operatorname{step}(\mathbf{w}^{\top}\mathbf{x}+b)
$$

따라서 

* Linear Regression은 continuous residual을 최소화하는 모델이고,
* Logistic Regression은 probability를 추정하여 linear decision boundary로 classification을 수행하는 모델이며,
* Perceptron은 linear decision boundary를 기준으로 misclassification을 교정하는 모델이라고 볼 수 있음.

세 모델은 동일한 linear combination에서 출발하고 update 식도 비슷한 형태를 가질 수 있지만, prediction의 의미와 loss function이 서로 다름.

---

---

## 궁시렁

* Logistic Regression과 Perceptron은 모두 linear combination을 기반으로 한 binary classifier이지만, 서로 다른 연구 전통에서 등장함. 
* Logistic Regression은 probability modeling을 목적으로 sigmoid를 사용한 반면, Perceptron은 생물학적 neuron의 firing을 모사하기 위해 hard threshold와 별도의 learning rule을 사용함. 
* 현대적 관점(back propagation을 알고 있는 이들의 관점)에서는 Logistic Regression의 differentiable sigmoid가 artificial neuron의 형태로 더 확장성이 높아 보이지만, 당시에는 이러한 연결이 중심적으로 발전하지 않았음.

