---
tags: [binary-classification, multiclass, multilabel, multioutput, OvO, OvR]
---

# Types of Classification

![](./img/classification_type.png){style="display: block; margin: 0 auto; width:300px"}

## Binary Classification

`Binary Classification` (이진분류)는 각 sample에 2개의 label 중 하나를 할당하는 task임.

* 일반적으로 특정 class에 속하는지 아닌지를 구분하는 형태로 분류함.
* Multiclass classification (다중클래스분류)와 Multilabel classification (다중라벨분류)의 기본이 되는 task.

---

## Multiclass Classification

`Multinomial Classification`이라고도 불림.

`Binary Classification` 의 generalization으로 한 sample에 하나의 label값이 주어지지만, 해당 label값의 종류가 여러 class인 경우를 애기함.

sample의 `학점` 을 classification하는 것이 대표적인 예라고 할 수 있음.

* Gaussian Naive Bayesian 이나 Logistic Regression, Random Forrest 등은 Multiclass classification task로 구현상 자연스럽게 확장이 가능하지만,
* 기본적으로 binary classification 만이 가능한 Support Vector Machine Classifier나 Stochastic Gradient Classifier는 One-vs-One (`OvO`) 또는 One-vs-Rest (`OvR`) 등의 방식으로 여러 binary classification model을 통해 Multiclass classification을 수행함.

> 일반적으로 `OvR`이 선호됨.  
> 단, `SVC`와 같이 큰 training dataset에서 훈련이 어려운 경우엔 `OvO`를 취해 더 많은 수의 모델을 각각 적은 수의 학습데이터로 훈련시키는 전략이 사용되기도 함.  
>
> 참고로 `scikit-learn`의 경우, `LinearSVC` (liblinear 기반) 는 `OvR`을 채택하고 있으며, `SVC` (libsvm 기반)는 `OvO`를 채택하고 있음.

---

## Multilabel Classification

한 sample의 label값이 여러 개인 경우 (달리 말하면 한 sample이 여러 class가 동시에 될 수 있음).

* label은 vector로 주어지며 각 label vector의 element가 하나의 label을 의미함.

예를 들어 어떤 image의 대상의 성별과 합격 여부를 나타내는 2개의 label이 주어진 경우를 들 수 있음.

* 이 경우 2개의 elements로 구성된 label vector가 사용되고, 각 elements는 0,1 (or False, True)의 2가지 값 중 하나를 가지게 됨.

또는 특정 사진에 2개의 인물 A와 B가 있는 경우, 해당 사진은 A 가 포함되었는지를 나타내는 binary classification과 B가 포함되었는지를 나타내는 binary classification이 동시에 이루어지게 구현될 수 있으며 이 경우 Multilabel classification이라고 함.

---

## Multioutput-Multiclass Classification

> 한 sample이 여러 개의 label을 가질 수 있으며, 각각의 label은 여러 class로 구성됨.

하나의 sample의 `학점`과 `학과`를 동시에 classification하는 task를 예로 들 수 있다.

* 이 예제 task에서 하나의 sample은 2개의 label을 가짐 : 
    * `학점`, 
    * `학과`
* 각 label은 다음과 같이 여러 class 중 하나의 값을 가짐 
    * `학점` : A, B, C, D, F
    * `학과` : 의공학과, 컴퓨터공학과, 기계학과, 전자과 등등

Multioutput-Multiclass classification은 줄여서  

* Multioutput classification (가장 많이 사용됨) 
* 또는 Multitask Classification 이라고도 불림.

---

참고자료: [Classification 과 관련 metrics 에 대한 소개](https://ds31x.tistory.com/307)