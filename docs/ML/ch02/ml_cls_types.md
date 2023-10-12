# The Types of Classification

## Multiclass Classification

`Multinomial Classification`이라고도 불림.

`Binary Classification` 의 generalization으로 한 sample에 하나의 label값이 주어지지만, 해당 label값의 종류가 여러 class인 경우를 애기함.

sample의 `학점` 을 classification하는 것이 대표적인 예라고 할 수 있음.

* Gaussian Naive Baysian 이나 Logistic Regression, Random Forrest 등은 multiclass classification task로 확장이 가능하지만,
* 기본적으로 binary classification만이 가능한 Support Vector Machine Classifier나 Stochastic Gradient Classifier는 One-vs-One (`OvO`) 또는 One-vs-Rest (`OvR`) 등의 방식으로 여러 binary classification model을 통해 multiclass classification을 수행함.

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

또는 특정 사진에 2개의 인물 A와 B가 있는 경우, 해당 사진은 A 가 포함되었는지를 나타내는 binary classifcation과 B가 포함되었는지를 나타내는 binary classification이 동시에 이루어지게 구현될 수 있으며 이 경우 multilabel classification이라고 함.

---

## Multioutput-multiclass Classification

한 sample이 여러 개의 label을 가질 수 있으며, 각각의 label은 여러 class로 구성됨.

하나의 sample의 `학점`과 `학과`를 동시에 classifcation하는 task를 예로 들 수 있다.

하나의 sample은 2개의 label을 가짐 : `학점`, `학과`
각 label은 여러 class 중 하나의 값을 가짐 

`학점`
: A, B, C, D, F

`학과`
: 의공학과, 컴퓨터공학과, 기계학과, 전자과 등등

Multioutput-multiclass classification은 줄여서 multioutput classification 이라고도 불림.