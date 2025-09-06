# Categories of ML

ML은 다음과 같은 구분 기준을 가지고 subcategory들로 나눌 수 있다. 

* 단, 다음의 기준들이 ^^서로 exclusive한 것은 아니라는 점^^ 을 명심해야 한다. 
* 한 모델이 각 특성을 동시에 가질 수 있으며 여러 subcategory 에 동시에 속할 수 있음.
* 즉, `unsupervised 이면서 transductive 한 learning` 이 있을 수 있다. 

---

## human supervision의 정도 및 방식 에 따른 구분.

Whether or not they are trained with human supervision.

* [Supervised Learning](./ch00_20_supervised.md) **
* [Unsupervised Learning](./ch00_21_unsupervised.md) *
* [Semi-supervised Learning](./ch00_22_semisupervised.md)
* [Reinforcement Learning](./ch00_23_reinforcement_learning.md)
* [Self-supervised Learning](./ch00_24_selfsupervised_learning.md)

---

## Model 여부에 따른 구분.

단순히 훈련 때 주어진 데이터 샘플을 기억하고, 이들과의 similarity를 이용하여 새로운 샘플에 대한 판정을 하는 경우와 훈련 데이터를 통해 일반적인 패턴을 추출하여 이를 통해  predictive model을 만들고 해당 모델에 기반하여 새로운 샘플에 대한 판정을 하는 경우를 구분할 수 있음.

이 기준으로 나눈 분류는 다음과 같음.

> Whether the method relies on ^^comparing new data points to known ones in the training set^^ , or instead ^^detects patterns in the training data and creates a `predictive model`^^, much like scientists do.

* Instance based Learning
* Model based Learning

---

## Prediction의 가능 여부에 따른 구분.

`새로운 데이터에 대한 prediction이 가능` 한지 여부로 구분.

* Inductive Learning (귀납적 학습)
    * Training dataset 에서 일반화가 가능한 규칙, 함수, 모델을 도출.
    * Training dataset 에 없는 새로운 데이터에 대해 prediction 가능! 
* [Transductive Learning](http://ds31x.blogspot.com/2023/08/ml-transductive-learning-and-inductive.html?view=classic) *
    * 전달적/전이적 학습
    * 주어진 데이터만 잘 설명하는 함수, 모델을 도출. 
    * training dataset에 없는 새로운 데이터에 대한 prediction 불가.

---

## 학습 시기에 따른 구분.

Whether they are capable of ***incremental on-the-fly learning***

* [Batch Learning](./ch00_42_batch_learning.md) 
  * 모든 training data를 이용하여 학습.
  * 학습이 종료된 이후 inference 및 서비스 실행 (해당 과정에선 학습이 이루어지지 않음)
* [Online Learning (or Incremental Learning)](./ch00_41_online_learning.md)
  * 데이터가 순차적으로 들어올 때마다 점진적으로 모델의 parameter가 업데이트됨.

