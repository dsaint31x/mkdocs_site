---
title: "Perceptron Loss, Weight Update, SGD, and SVM"
description: "Perceptron의 0/1 및 -1/+1 label notation에서의 loss와 weight update를 정리하고, SGDClassifier, Hinge loss, 그리고 SVM과의 연결을 설명"
tags:
  - Machine Learning
  - Perceptron
  - SGD
  - SGDClassifier
  - Hinge Loss
  - SVM
  - Classification
categories:
  - Machine Learning
  - Linear Models
---

# Perceptron Loss, Weight Update, SGD, 그리고 SVM

Perceptron은 binary classification을 위한 linear classifier 임. 

* Input 자체는 binary일 필요가 없으며,
* class label은 0/1 또는 -1/+1로 표현할 수 있음.

주의할 점은, Label notation에 따라 loss와 weight update의 표현도 달라진다.

## 1. 0/1 notation

Target과 prediction은 다음과 같음:

$$
y,\hat y\in{0,1}
$$

Perceptron의 weighted sum은 다음과 같음:

$$
z=\mathbf{w}^{\top}\mathbf{x}+b
$$

Prediction은 step activation을 통해 결정됨:

$$
\hat y=
\begin{cases}
1, & z\geq0\
0, & z<0
\end{cases}
$$

Perceptron loss는 다음과 같이 표현할 수 있음:

$$
L_{\mathrm{Perceptron}} = \max\left(0,-(2y-1)z\right)
$$

Target별 표현은 다음과 같음:

$$
L_{\mathrm{Perceptron}} = \begin{cases}
\max(0,-z), & y=1\
\max(0,z), & y=0
\end{cases}
$$

* correct classification: loss가 0.
* misclassification: decision boundary의 잘못된 쪽으로 이동할수록 loss가 증가.
* misclassified sample에 대해서만 penalty가 발생.

Weight update는 다음과 같음:

$$
\boxed{
w_i^{(\mathrm{next})} = w_i+\eta(y-\hat y)x_i
}
$$

각 경우의 update는 다음과 같음.

* correct classification: no update.
* false negative: positive direction으로 update.
* false positive: negative direction으로 update.

False negative의 경우:

$$
y=1,\qquad \hat y=0
$$

Weight update는 다음과 같음:

$$
w_i^{(\mathrm{next})} = w_i+\eta x_i
$$

False positive의 경우:

$$
y=0,\qquad \hat y=1
$$

Weight update는 다음과 같음:

$$
w_i^{(\mathrm{next})} = w_i-\eta x_i
$$

Bias update는 다음과 같음:

$$
b^{(\mathrm{next})} = b+\eta(y-\hat y)
$$

즉, 0/1 notation에서는 prediction error를 직접 이용하는 형태로 update를 표현할 수 있음.

## 2. -1/+1 notation

Perceptron을 수학적으로 표현할 때는 -1/+1 notation이 더 간단함.

Target은 다음과 같음:

$$
t\in{-1,+1}
$$

Weighted sum은 동일함:

$$
z=\mathbf{w}^{\top}\mathbf{x}+b
$$

Prediction은 sign function으로 표현됨:

$$
\hat t=\operatorname{sign}(z)
$$

Classification의 correctness는 signed margin 형태로 표현할 수 있음:

$$
tz
$$

* positive: correct classification.
* negative: misclassification.
* magnitude: decision boundary로부터 떨어진 정도.

Perceptron loss는 다음과 같음:

$$
\boxed{
L_{\mathrm{Perceptron}} = \max(0,-tz)
}
$$

Correct classification에서는 loss가 0이고, misclassification에서만 loss가 발생함.

Misclassified sample에 대한 weight update는 다음과 같음:

$$
\boxed{
\mathbf{w}^{(\mathrm{next})} = \mathbf{w}+\eta t\mathbf{x}
}
$$

Bias update는 다음과 같음:

$$
b^{(\mathrm{next})} = b+\eta t
$$

Positive sample의 misclassification:

$$
t=+1
$$

Weight update는 다음과 같음:

$$
\mathbf{w}^{(\mathrm{next})} = \mathbf{w}+\eta\mathbf{x}
$$

Negative sample의 misclassification:

$$
t=-1
$$

Weight update는 다음과 같음:

$$
\mathbf{w}^{(\mathrm{next})} = \mathbf{w}-\eta\mathbf{x}
$$

따라서 0/1 notation과 -1/+1 notation은 표현 방식만 다를 뿐 동일한 Perceptron learning rule을 나타냄.

두 notation의 mapping은 다음과 같음:

$$
t=2y-1
$$

따라서 다음과 같이 대응됨:

$$
y=0 \rightarrow t=-1
$$

$$
y=1 \rightarrow t=+1
$$

## 3. Perceptron과 Stochastic Gradient Descent

Perceptron learning은 

* sample 단위로 parameter를 update한다는 점에서
* Stochastic Gradient Descent와 직접 연결할 수 있음.

일반적인 single-sample SGD update는 다음과 같음:

$$
\mathbf{w}^{(\mathrm{next})} = \mathbf{w} - \eta \nabla_{\mathbf w}L_i
$$

Perceptron loss를 signed label notation으로 표현하면 다음과 같음:

$$
L_i = \max(0,-t_i z_i)
$$

Misclassified sample에서 gradient는 다음과 같음:

$$
\nabla_{\mathbf w}L_i = -t_i\mathbf{x}_i
$$

SGD update는 다음과 같음:

$$
\mathbf{w}^{(\mathrm{next})} = \mathbf{w} + \eta t_i\mathbf{x}_i
$$

이는 classical Perceptron의 -1/+1 notation update와 동일함.

여기서 `SGDClassifier`에 실제로 입력하는 class label은 반드시 -1/+1일 필요가 없음. 

Binary classification에서는 0/1 label을 그대로 입력할 수 있음.

이 경우, 실제 input label은 다음과 같음:

$$
y\in{0,1}
$$

수식 전개에서는 signed label로 변환하여 표현할 수 있음:

$$
t=2y-1
$$

즉, `SGDClassifier`에는 0/1 label을 입력하면서도,  
Perceptron loss와 update를 수학적으로 설명할 때는 -1/+1 notation을 사용할 수 있음.

0/1 notation에서의 classical Perceptron update는 다음과 같음:

$$
\mathbf{w}^{(\mathrm{next})} = \mathbf{w} + \eta(y-\hat y)\mathbf{x}
$$

Signed label notation에서의 update는 다음과 같음:

$$
\mathbf{w}^{(\mathrm{next})} = \mathbf{w} + \eta t\mathbf{x}
$$

두 식은 label coding만 다를 뿐 같은 learning rule을 표현함.

참고로,  
scikit-learn의 `Perceptron`은  
다음 설정의 `SGDClassifier`와 equivalent하게 볼 수 있음:

```python
SGDClassifier(
    loss="perceptron",
    learning_rate="constant",
    eta0=1,
    penalty=None
)
```

각 설정의 의미는 다음과 같음.

* `loss="perceptron"`: Perceptron loss 사용.
* `learning_rate="constant"`: learning rate를 iteration에 따라 감소시키지 않음.
* `eta0=1`: constant learning rate를 1로 설정.
* `penalty=None`: regularization을 사용하지 않음.

Learning rate는 다음과 같음:

$$
\eta=1
$$

Misclassified sample에 대한 update는 다음과 같음:

$$
\mathbf{w}^{(\mathrm{next})} = \mathbf{w} + t_i\mathbf{x}_i
$$

즉, `SGDClassifier`에 Perceptron loss, constant learning rate, unit learning rate, no regularization을 적용하면 classical Perceptron update와 연결됨.

## 4. Perceptron Loss와 Hinge Loss

Perceptron loss와 Hinge loss의 관계는 **-1/+1 notation에서 가장 명확** 하게 나타남.

Perceptron loss는 다음과 같음:

$$
L_{\mathrm{Perceptron}} = \max(0,-tz)
$$

Hinge loss는 다음과 같음:

$$
\boxed{
L_{\mathrm{hinge}} = \max(0,1-tz)
}
$$

두 loss의 핵심적인 차이는 margin requirement에 있음.

Perceptron에서는 correct side에 위치하면 loss가 0:

$$
tz>0
$$

Hinge loss에서는 일정한 margin까지 확보해야 loss가 0:

$$
tz\geq1
$$

따라서 sample은 다음과 같이 구분할 수 있음.

* misclassification: Perceptron loss와 Hinge loss 모두 penalty 발생.
* correct classification with small margin: Perceptron loss는 0, Hinge loss는 penalty 발생.
* correct classification with sufficient margin: 두 loss 모두 0.

즉, 

* Perceptron은 mistake-driven learning에 가깝고,
* Hinge loss는 margin-driven learning에 가깝다고 볼 수 있음.

## 5. Hinge Loss와 SVM

Hinge loss를 사용하는 대표적인 linear classifier가 Support Vector Machine, SVM임.

Linear SVM의 objective는 다음과 같음:

$$
\boxed{
\min_{\mathbf w,b}
\frac{1}{2}|\mathbf w|^2 + C \sum_i \max\left( 0, 1-t_i(\mathbf w^\top\mathbf x_i+b) \right)
}
$$

첫 번째 term은 regularization term (Hard SVM에서 margin maximization. 단, margin constraint를 만족해야함):

$$
\frac{1}{2}|\mathbf w|^2
$$

두 번째 term은 Hinge loss (Soft SVM 의 slack variable 을 unconstrained objective로 도입한 결과):

$$
\max\left(
0,
1-t_i(\mathbf w^\top\mathbf x_i+b)
\right)
$$

SVM은 단순한 correct classification뿐 아니라 large margin을 추구함.

Perceptron과 SVM의 차이는 loss의 threshold에서 명확하게 나타남.

Perceptron:

$$
L_{\mathrm{Perceptron}} = \max(0,-tz)
$$

* correct side에 있으면 loss가 0.
* misclassified sample에 대해서만 penalty.
* margin의 크기는 직접적으로 요구하지 않음.

SVM:

$$
L_{\mathrm{hinge}} = \max(0,1-tz)
$$

* correct classification만으로는 충분하지 않음.
* margin 내부에 위치한 sample에도 penalty.
* regularization과 함께 large-margin decision boundary를 추구함.

## 6. Perceptron, SGD, SVM의 연결

전체 관계를 정리하면 다음과 같음.

Perceptron:

$$
L=
\max(0,-tz)
$$

* misclassification 중심.
* sample 단위 update.
* SGD 형태로 optimize 가능.
* classical Perceptron은 constant learning rate와 no regularization의 특수한 형태로 볼 수 있음.

Classical Perceptron과 equivalent한 `SGDClassifier` 설정:

```python
SGDClassifier(
    loss="perceptron",
    learning_rate="constant",
    eta0=1,
    penalty=None
)
```

Hinge loss:

$$
L= \max(0,1-tz)
$$

* misclassification뿐 아니라 insufficient margin에도 penalty.
* correct classification 이후에도 margin 확보를 계속 요구.

SVM:

$$
\text{Hinge loss} + \text{regularization}
$$

* Hinge loss를 기반으로 margin을 확보.
* regularization을 통해 large-margin decision boundary를 추구(margin maximization).
* SGD를 이용해서도 optimize 가능.

결국 `SGDClassifier`는 Perceptron과 linear SVM을 동일한 stochastic optimization framework 안에서 이해하는 데 유용함.

* `loss="perceptron"`: Perceptron으로 연결.
* `loss="hinge"`: linear SVM의 Hinge loss로 연결.
* learning rate와 regularization 설정에 따라 실제 optimization behavior가 달라짐.
