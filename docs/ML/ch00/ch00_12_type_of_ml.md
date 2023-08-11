# Categories of ML

ML은 다음과 같은 구분 기준을 가지고 subcategory들로 나눌 수 있다. 

* 단, 다음의 기준들이 ^^서로 exclusive한 것은 아니라는 점^^ 을 명심해야 한다. 각 특성을 동시에 가질 수 있다.
* 즉, `unsupervised 이면서 transductive 한 learning` 이 있을 수 있다. 

---

## human supervision의 정도 및 방식 에 따른 구분.

Whether or not they are trained with human supervision.

* Supervised Learning **
* Semi-supervised Learning
* Unsupervised Learning *
* Reinforcement Learning

---

## Model 여부에 따른 구분.

Whether the method relies on ^^comparing new data points to known ones in the training set^^ , or instead ^^detects patterns in the training data and creates a `predictive model`^^, much like scientists do.

* Instance based Learning
* Model based Learning

---

### Prediction의 가능 여부에 따른 구분.

`새로운 데이터에 대한 prediction이 가능` 한지 여부로 구분.

* Inductive Learning
* [Transductive Learning](http://ds31x.blogspot.com/search?q=transductive)

---

## 학습 시기에 따른 구분.

Whether they are capable of ***incremental on-the-fly learning***

* Batch Learning
* Online Learning (or Incremental Learning)

