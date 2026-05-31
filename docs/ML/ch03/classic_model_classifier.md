---

title: "[ML] Classic Classifier (Summary)"
description: >
DeepLearning 계열을 제외한 Classic Classifier 모델들의 요약 정리.
KNN, Logistic Regression, Ridge Classifier, SGDClassifier, Naive Bayes,
SVC, Decision Tree, Random Forest, AdaBoost, Gradient Boosting,
HistGradientBoosting, XGBoost, LightGBM, CatBoost
tags:

* machine learning
* classification
* scikit-learn
* ensemble
* boosting
* bagging
* random forest
* support vector machine

---

# [ML] Classic Classifier (Summary)

DeepLearning 계열을 제외한 Classifier 모델들을 간단하게 정리함.

![](./imgs/classic_classifier.png){style="display:block; margin:0 auto; width:500px"}

* [관련 ipynb파일](https://gist.github.com/ds31x/)

---

## **분류**

* Instance Based Algorithm

  * [K Neighbors Classification](#0-k-nearest-neighbors-classifier-knn)
* Model Based Algorithm

  * Linear Model

    * Logistic Regression
    * Ridge Classifier
    * [Regularization](https://dsaint31.tistory.com/848#1.%20L1%20%EB%B0%8F%20L2%20Regularization-1-2)
    * [Stochastic Gradient Descent](https://ds31x.tistory.com/669)
  * Probabilistic Model

    * Naive Bayes
  * Non-Linear Model

    * Support Vector Classification
    * Decision Tree Classification
    * [Ensemble Model](https://dsaint31.tistory.com/798)

      * Random Forest Classification
      * AdaBoost Classification
      * Gradient Boosting Classification
      * HistGradientBoosting Classification
      * XGBoost, LightGBM, CatBoost

---

## **설명**

### **0. K-Nearest Neighbors Classifier (KNN 분류)**

참고: [k-Nearest Neighbors](https://dsaint31.tistory.com/832)

* **설명**:

  * 가장 가까운 K개의 데이터 포인트를 기반으로 class를 결정하는 instance based model (1951)
      * Fix & Hodges의 1951년 연구는 **미발표 보고서(unpublished technical report)**임. 
  * 주변 sample들의 label을 voting하여 classification을 수행함.
* **사용 함수**:

  * `sklearn.neighbors.KNeighborsClassifier`
* **특징**:

  * 비선형 decision boundary를 만들 수 있음.
  * Minkowski distance 등의 거리 기반이라 [feature scaling](https://dsaint31.tistory.com/720)이 필수임.
  * 학습 단계에서는 별도의 parameter fitting이 거의 없으나, prediction 시 주변 sample 탐색 비용이 큼.

```Python
# KNN Classifier 모델 (기본값으로 k=5 사용)
from sklearn.neighbors import KNeighborsClassifier

# KNeighborsClassifier 모델 생성
knn_classifier = KNeighborsClassifier(
    n_neighbors=5,      # 이웃 수 (k 값)
    weights='distance', # 거리 가중치 ('uniform' 또는 'distance')
    algorithm='auto',   # 가까운 이웃을 찾는 알고리즘 ('auto', 'ball_tree', 'kd_tree', 'brute')
    leaf_size=30,       # 트리 기반 알고리즘에서의 leaf 사이즈
    p=2,                # 거리 측정 방법 (1: 맨해튼 거리, 2: 유클리드 거리)
    metric='minkowski', # 거리 계산에 사용할 메트릭 ('minkowski', 'euclidean', 'manhattan' 등)
    n_jobs=-1           # 병렬처리할 CPU 코어 수 (-1은 모든 코어 사용)
)

knn_classifier = knn_classifier.fit(X_train_scaled, y_train)
```

* [Minkowski Distance](https://dsaint31.tistory.com/827)

---

### **1. Logistic Regression (로지스틱 회귀)**

* **설명**:
  * 이름에는 Regression이 들어가지만, **classification을 위한 대표적인 linear classifier** 임.
  * feature들의 linear combination을 구한 뒤, 
  * **sigmoid 또는 softmax를 통해 class probability를 추정&& 함.
  * binary classification에서는 다음과 같은 형태를 가짐.

$$
p(y=1|\mathbf{x}) = \sigma(\mathbf{x}^{\top}\mathbf{w} + b)
$$

* **사용 함수**:
  * `sklearn.linear_model.LogisticRegression`
* **특징**:
  * linear decision boundary를 가지는 기본적인 classifier.
  * probability output을 제공할 수 있음.
  * L1, L2, ElasticNet regularization을 사용할 수 있음.
  * gradient 기반 최적화이므로 feature scaling이 중요함.
  * `solver`에 따라 사용할 수 있는 `penalty`가 달라짐.

```Python
from sklearn.linear_model import LogisticRegression

# LogisticRegression 모델 생성
logistic_classifier = LogisticRegression(
    penalty='l2',       # 정칙화 방식 ('l1', 'l2', 'elasticnet', None)
    C=1.0,              # 정칙화 강도의 역수. 작을수록 정칙화가 강함.
    fit_intercept=True, # 절편을 계산할지 여부
    solver='lbfgs',     # 최적화 알고리즘 ('lbfgs', 'liblinear', 'sag', 'saga', 'newton-cg' 등)
    max_iter=1000,      # 최대 반복 횟수
    tol=1e-4,           # 수렴 기준 허용 오차
    class_weight=None,  # class imbalance 보정용 가중치 ('balanced' 또는 dict)
    random_state=7,     # 난수 seed
    n_jobs=-1           # 병렬 처리할 CPU 코어 수
)

logistic_classifier = logistic_classifier.fit(X_train_scaled, y_train)
```

`penalty`와 `solver`의 대표적인 관계는 다음과 같음.

| solver      | 사용 가능한 penalty                | 특징                                    |
| ----------- | -------------------------------- | ------------------------------------- |
| `lbfgs`     | `l2`, `None`                     | 일반적으로 많이 사용                           |
| `liblinear` | `l1`, `l2`                       | 작은 dataset, binary classification에 적합 |
| `sag`       | `l2`, `None`                     | sample 수가 많을 때 유리, scaling 필요         |
| `saga`      | `l1`, `l2`, `elasticnet`, `None` | large-scale data, sparse data에 적합     |
| `newton-cg` | `l2`, `None`                     | 안정적이나 상대적으로 무거울 수 있음                  |

* 참고:
  * Logistic Regression은 class probability를 modeling하지만, decision boundary는 기본적으로 linear임.
  * multi-class classification의 경우 softmax 기반 multinomial logistic regression으로 확장 가능함.

---

### **2. Ridge Classifier (릿지 분류기)**

참고: [Ridge](https://dsaint31.tistory.com/947)

* **설명**:
  * Ridge Regression과 유사하게 **L2 Regularization을 사용** 하는 linear classifier.
  * classification 문제의 label을 내부적으로 변환하여 linear model을 학습하고, 
  * decision score가 가장 큰 class를 선택함.
* **사용 함수**:
  * `sklearn.linear_model.RidgeClassifier`
* **특징**:
  * L2 Regularization을 통해 큰 parameter를 억제함.
  * **probability output을 직접 제공하지 않음.**
  * high-dimensional data에서 비교적 안정적으로 동작함.
  * feature scaling을 하는 것이 권장됨.

```Python
from sklearn.linear_model import RidgeClassifier

# RidgeClassifier 모델 생성
ridge_classifier = RidgeClassifier(
    alpha=1.0,          # 정칙화 강도 (alpha 값이 클수록 정칙화가 강해짐)
    fit_intercept=True, # 절편을 계산할지 여부
    copy_X=True,        # 원본 데이터를 복사할지 여부
    max_iter=None,      # 최대 반복 횟수
    tol=1e-4,           # 수렴 기준 허용 오차
    class_weight=None,  # class imbalance 보정용 가중치 ('balanced' 또는 dict)
    solver='auto',      # 계산 방법 선택 ('auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg' 등)
    random_state=7      # solver가 stochastic한 경우 사용할 난수 seed
)

ridge_classifier = ridge_classifier.fit(X_train_scaled, y_train)
```

* RidgeClassifier는 `predict_proba()`를 제공하지 않음.
* probability가 필요한 경우 `LogisticRegression`, `SVC(probability=True)`, 또는 calibration을 고려해야 함.

---

### **3. SGDClassifier**

참고: [linear_model.SGDClassifier](https://ds31x.tistory.com/669)

* **설명**:
  * Stochastic Gradient Descent(SGD)를 사용하여 
  * linear classification 계열 objective function을 iterative하게 최적화하는 classifier.
  * loss 설정에 따라 Linear SVM, Logistic Regression, Perceptron 등과 유사한 모델을 구성할 수 있음.
  * closed-form solution을 구하지 않고, sample을 하나씩 보면서 gradient를 추정하고 parameter를 update함.
* **사용 함수**:
  * `sklearn.linear_model.SGDClassifier`
* **특징**:
  * sample 수가 매우 많거나 sparse data를 사용할 때 유리함.
  * **gradient 기반 최적화이므로 feature scaling이 중요함.**
  * `partial_fit()`을 통해 online learning 또는 **incremental learning** 에 사용할 수 있음.
  * `loss='log_loss'`를 사용하면 Logistic Regression과 유사한 classifier가 됨.
  * `loss='hinge'`를 사용하면 Linear SVM과 유사한 classifier가 됨.

| 설정             | 의미           |    logistic function 사용 | `predict_proba()` |
| --------------- | ------------- | -----------------------: | ----------------: |
| `loss="hinge"`          | Linear SVM        |          아님 |               없음 |
| `loss="log_loss"`       | SGD 기반 Logistic Regression   |       사용 |      있음 |
| `loss="modified_huber"` | robust한 margin 기반 classifier | 직접적인 logistic regression은 아님 |   있음 |
| `loss="perceptron"`     | Perceptron                   |        아님 |              없음 |


```Python
from sklearn.linear_model import SGDClassifier

# SGDClassifier 모델 생성
sgd_classifier = SGDClassifier(
    loss='log_loss',          # 손실 함수 ('hinge', 'log_loss', 'modified_huber', 'perceptron' 등)
    penalty='l2',             # 정칙화 방식 ('l2', 'l1', 'elasticnet', None)
    alpha=0.0001,             # 정칙화 강도
    l1_ratio=0.15,            # ElasticNet에서 L1 penalty 비율
    fit_intercept=True,       # 절편을 계산할지 여부
    max_iter=1000,            # 최대 epoch 수
    tol=0.001,                # 수렴 기준 허용 오차
    shuffle=True,             # 각 epoch마다 sample 순서를 섞을지 여부
    random_state=7,           # 난수 seed
    learning_rate='optimal',  # learning rate schedule ('constant', 'optimal', 'invscaling', 'adaptive')
    eta0=0.0,                 # 초기 learning rate
    early_stopping=False,     # validation score 기반 조기 종료 여부
    validation_fraction=0.1,  # early_stopping=True일 때 validation set 비율
    n_iter_no_change=5,       # 개선이 없을 때 종료까지 기다릴 epoch 수
    class_weight=None,        # class imbalance 보정용 가중치
    warm_start=False,         # 이전 fit 결과를 다음 fit의 초기값으로 재사용할지 여부
    average=False             # update 과정의 평균 weight를 사용할지 여부
)

sgd_classifier = sgd_classifier.fit(X_train_scaled, y_train)
```

* `SGDClassifier`에서 SGD는 각 sample에 대한 loss gradient를 이용해 parameter를 update하는 방식임.
* `max_iter`는 parameter update 횟수가 아니라 training set 전체를 최대 몇 번 반복할지를 의미함.
* `fit()`을 다시 호출하면 learning rate 관련 counter가 reset됨.
* 반면 `partial_fit()`은 주어진 data subset에 대해 한 epoch의 SGD를 수행하며, 기존 counter를 계속 증가시킴.
* 따라서 `warm_start=True`와 `partial_fit()`은 모두 이전 학습 결과를 활용하지만, `warm_start`는 재학습 초기값 재사용이고 `partial_fit()`은 incremental learning에 가까움.

---

### **4. Naive Bayes Classifier (나이브 베이즈 분류기)**

* **설명**:
  * **Bayes theorem을 기반** 으로 하는 probabilistic classifier.
  * 각 feature들이 class 조건부로 서로 독립이라고 가정함.
  * 이 독립 가정이 현실적으로는 강한 가정이지만, **text classification 등에서는 좋은 baseline으로 사용됨.**
* **사용 함수**:
  * `sklearn.naive_bayes.GaussianNB`
  * `sklearn.naive_bayes.MultinomialNB`
  * `sklearn.naive_bayes.BernoulliNB`
* **특징**:
  * 학습과 예측이 빠름.
  * feature independence assumption 때문에 복잡한 feature interaction을 잘 반영하지 못함.
  * probability output을 제공함.
  * text classification에서 `MultinomialNB`가 자주 사용됨.

```Python
from sklearn.naive_bayes import GaussianNB

# GaussianNB 모델 생성
gnb_classifier = GaussianNB(
    priors=None,          # class prior probability. None이면 data에서 추정
    var_smoothing=1e-9    # 분산 안정화를 위해 더해지는 작은 값
)

gnb_classifier = gnb_classifier.fit(X_train_scaled, y_train)
```

text count feature 또는 TF-IDF 계열 feature를 사용할 경우 다음과 같이 `MultinomialNB`를 사용할 수 있음.

```Python
from sklearn.naive_bayes import MultinomialNB

# MultinomialNB 모델 생성
mnb_classifier = MultinomialNB(
    alpha=1.0,            # Laplace smoothing 강도
    force_alpha=True,     # alpha 값을 강제로 유지할지 여부
    fit_prior=True,       # class prior를 학습할지 여부
    class_prior=None      # 직접 지정할 class prior
)

mnb_classifier = mnb_classifier.fit(X_train_count, y_train)
```

* `GaussianNB`는 continuous feature에 적합함.
* `MultinomialNB`는 count 기반 feature에 적합함.
* `BernoulliNB`는 binary feature에 적합함.

---

### **5. Support Vector Classification (SVC)**

* **설명**:
  * class 사이의 margin을 최대화하는 decision boundary를 찾는 classifier. (1963 등장/1992 kernel trick 도입)
  * 현재 많이 이용되는 soft-margin SVM은 1995년 논문 출판.
  * kernel trick을 통해 non-linear decision boundary를 구성할 수 있음.
* **사용 함수**:
  * `sklearn.svm.SVC`
- **특징**:
  * small to medium size dataset에서 강력한 성능을 보일 수 있음.
  * kernel 기반 SVC는 sample 수가 매우 많을 경우 학습 비용이 커짐.
  * feature scaling이 중요함.
  * 기본적으로 binary classifier이며, multi-class classification은 OvO 전략을 사용:
    *  `decision_function_shape='ovr' 을 지정할 경우, OvR 전략도 사용가능.

```Python
from sklearn.svm import SVC

# SVC 모델 생성
svc_classifier = SVC(
    C=1.0,               # regularization parameter. 값이 클수록 training error를 줄이려 함.
    kernel='rbf',        # 커널 유형: 'linear', 'poly', 'rbf', 'sigmoid'
    degree=3,            # 다항식 커널을 사용할 때, 다항식의 차수
    gamma='scale',       # 커널 계수: 'scale', 'auto' 또는 float 값
    coef0=0.0,           # 다항식 및 시그모이드 커널에서 상수 항
    shrinking=True,      # shrinking heuristic 사용 여부
    probability=False,   # probability estimate 사용 여부. True이면 내부 CV로 인해 느려질 수 있음.
    tol=1e-3,            # 반복 과정에서 수렴 기준 허용 오차
    cache_size=200,      # SVM에서 커널 계산을 위한 캐시 크기 (MB 단위)
    class_weight=None,   # class imbalance 보정용 가중치 ('balanced' 또는 dict)
    verbose=False,       # 학습 과정에서 출력 여부
    max_iter=-1,         # 최대 반복 횟수 (-1이면 무제한)
    decision_function_shape='ovr',
    random_state=7       # probability=True일 때 사용될 수 있는 난수 seed
)

svc_classifier = svc_classifier.fit(X_train_scaled, y_train)
```

`SVC`의 decision boundary는 다음과 같이 이해할 수 있음.
* `kernel='linear'`:
  * 원래 feature space에서 linear decision boundary를 사용함.
* `kernel='rbf'`:
  * 고차원 feature space로 mapping한 것과 유사한 효과를 통해 non-linear decision boundary를 구성함.

---

### **6. Decision Tree Classifier (결정 트리 분류)**

* **설명**:
  * 데이터 공간을 Tree 형태로 분할하여 class를 예측. (1980s)
  * 각 node에서 feature와 threshold를 선택하여 impurity를 줄이는 방향으로 분기함.
* **사용 함수**:
  * `sklearn.tree.DecisionTreeClassifier`
* **특징**:
  * 비선형 관계를 잘 모델링하고 feature scaling이 필요없음.
  * Tree계열은 feature scaling이 필요없음. 값의 크기 자체보다 순서와 threshold 기반 분할이 중요함.
  * over-fitting 가능성이 매우 높아서 Random Forest Classifier가 사용됨.
  * Random Forest Classifier를 이해하기 위한 stepping stone.

```Python
from sklearn.tree import DecisionTreeClassifier

# DecisionTreeClassifier 모델 생성
tree_classifier = DecisionTreeClassifier(
    criterion='gini',            # 분할 품질 기준 ('gini', 'entropy', 'log_loss')
    splitter='best',             # 분할 방법 ('best': 가장 좋은 분할 선택, 'random': 랜덤 분할)
    max_depth=None,              # 트리의 최대 깊이 (None이면 깊이에 제한이 없음)
    min_samples_split=2,         # 내부 노드를 분할하기 위한 최소 샘플 수
    min_samples_leaf=1,          # 리프 노드에 있어야 할 최소 샘플 수
    min_weight_fraction_leaf=0.0,# 리프 노드에 필요한 가중치 합의 최소 비율
    max_features=None,           # 분할에 사용할 최대 특성 수 (None이면 모든 특성 사용)
    random_state=7,              # 트리의 무작위성을 제어하는 시드 값
    max_leaf_nodes=None,         # 리프 노드의 최대 개수 (None이면 제한 없음)
    min_impurity_decrease=0.0,   # 노드를 분할하는 데 필요한 최소 불순도 감소
    class_weight=None,           # class imbalance 보정용 가중치
    ccp_alpha=0.0                # 가지치기 비용-복잡도 매개변수 (0.0이면 가지치기 없음)
)

tree_classifier = tree_classifier.fit(X_train_scaled, y_train)
```

* `criterion='gini'`:
  * Gini impurity를 줄이는 방향으로 split.
* `criterion='entropy'`:
  * Information gain을 기준으로 split.
* `criterion='log_loss'`:
  * probabilistic classification 관점의 log loss를 기준으로 split.

---

### **7. Random Forest Classifier (랜덤 포레스트 분류)**

* **설명**:
  * 여러 개의 Decision Tree를 ensemble하여 예측하는 Bagging 기법. (2001)
  * 각 tree는 bootstrap sample과 feature randomness를 이용해 서로 다른 decision boundary를 형성함.
  * classification에서는 각 tree의 class prediction을 voting하여 최종 class를 결정함.
* **사용 함수**:
  * `sklearn.ensemble.RandomForestClassifier`
* **특징**:
  * over-fitting 방지 및 generalization 성능 향상.
  * feature scaling이 필요없음.
  * `feature_importances_`를 통해 impurity 기반 feature importance를 확인할 수 있음.
  * class imbalance가 있으면 `class_weight='balanced'` 등을 고려할 수 있음.

> [Leo Breiman(2001)](https://link.springer.com/article/10.1023/A:1010933404324) 은
>
> * [Ho(1995)](https://ieeexplore.ieee.org/document/598994)가 처음 소개한 Random Subspace Method의 아이디어(Tree별로 feature를 무작위로 사용하던 것을 Breiman은 노드 분기 시 feature를 무작위로 선택)를 확장.
> * Decision Tree 구성 시 추가적인 무작위성을 도입([1996년 자신이 제안](https://link.springer.com/article/10.1007/BF00058655)한 [bagging](https://dsaint31.tistory.com/798#Bagging%20%28%EB%B0%B0%EA%B9%85%29-1-1) 사용).
> * CART(Classification and Regression Trees) 기법을 사용.
> * Classification과 Regression 모두를 포괄하는 **Random Forest 를 정립**.

```Python
from sklearn.ensemble import RandomForestClassifier

# RandomForestClassifier 모델 생성
forest_classifier = RandomForestClassifier(
    n_estimators=100,            # 생성할 트리의 개수
    criterion='gini',            # 분할 기준 ('gini', 'entropy', 'log_loss')
    max_depth=None,              # 트리의 최대 깊이 (None이면 제한 없음)
    min_samples_split=2,         # 노드를 분할하기 위한 최소 샘플 수
    min_samples_leaf=1,          # 리프 노드에 있어야 하는 최소 샘플 수
    min_weight_fraction_leaf=0.0,# 리프 노드에서 최소 가중치 비율
    max_features='sqrt',         # 각 분할에 사용할 최대 특성 수 ('sqrt', 'log2', None 또는 정수)
    max_leaf_nodes=None,         # 최대 리프 노드 수 (None이면 제한 없음)
    min_impurity_decrease=0.0,   # 분할을 위한 최소 불순도 감소
    bootstrap=True,              # 부트스트랩 샘플링 사용 여부
    oob_score=False,             # OOB (Out of Bag) 샘플로 성능 평가 여부
    n_jobs=-1,                   # 병렬 처리에 사용할 CPU 코어 수 (-1이면 모든 코어 사용)
    random_state=7,              # 무작위성 제어
    verbose=0,                   # 학습 과정 중 출력 여부
    warm_start=False,            # 이전 학습 결과를 이용해 추가 학습을 할지 여부
    class_weight=None,           # class imbalance 보정용 가중치
    ccp_alpha=0.0,               # 비용-복잡도 가지치기의 매개변수
    max_samples=None             # 부트스트랩 샘플링 시 사용할 최대 샘플 비율
)

forest_classifier = forest_classifier.fit(X_train_scaled, y_train)
```

* `max_features='sqrt'`는 classification에서 널리 사용되는 설정임.
* 각 split에서 전체 feature가 아닌 일부 feature만 고려하면 tree 간 다양성이 증가함.
* ensemble에서 개별 tree의 다양성은 generalization 성능 향상에 중요함.

---

### **8. Extra Trees Classifier (Extremely Randomized Trees)**

* **설명**:
  * Random Forest와 유사하지만, 
  * ***split threshold를 더 random하게 선택*** 하는 ensemble tree classifier.
  * Random Forest보다 **더 많은 randomness를 도입** 함.
* **사용 Class**:
  * `sklearn.ensemble.ExtraTreesClassifier`
* **특징**:
  * Random Forest보다 bias는 증가할 수 있으나 variance를 더 줄일 수 있음.
  * feature scaling이 필요없음.
  * noise가 있는 data에서도 강한 baseline으로 사용할 수 있음.

```Python
from sklearn.ensemble import ExtraTreesClassifier

# ExtraTreesClassifier 모델 생성
extra_trees_classifier = ExtraTreesClassifier(
    n_estimators=100,            # 생성할 트리의 개수
    criterion='gini',            # 분할 기준 ('gini', 'entropy', 'log_loss')
    max_depth=None,              # 트리의 최대 깊이
    min_samples_split=2,         # 내부 노드를 분할하기 위한 최소 샘플 수
    min_samples_leaf=1,          # 리프 노드에 있어야 하는 최소 샘플 수
    min_weight_fraction_leaf=0.0,# 리프 노드에서 최소 가중치 비율
    max_features='sqrt',         # 각 분할에 사용할 최대 특성 수
    max_leaf_nodes=None,         # 최대 리프 노드 수
    min_impurity_decrease=0.0,   # 분할을 위한 최소 불순도 감소
    bootstrap=False,             # bootstrap sampling 사용 여부
    oob_score=False,             # OOB 평가 여부
    n_jobs=-1,                   # 병렬 처리에 사용할 CPU 코어 수
    random_state=7,              # 무작위성 제어
    verbose=0,                   # 학습 과정 출력 여부
    warm_start=False,            # 이전 학습 결과를 사용하여 추가 학습할지 여부
    class_weight=None,           # class imbalance 보정용 가중치
    ccp_alpha=0.0,               # 비용-복잡도 가지치기 계수
    max_samples=None             # bootstrap=True일 때 사용할 sample 수 또는 비율
)

extra_trees_classifier = extra_trees_classifier.fit(X_train_scaled, y_train)
```

---

### **9. AdaBoost Classifier (아다부스트 분류)**

* **설명**:
  * Weak Learner(보통 결정 트리)를 결합하여 성능을 향상시키는 Boosting 기법. (1995)
  * 이전 단계에서 잘못 분류한 sample에 더 큰 weight를 부여하면서 다음 weak learner를 학습함.
* **사용 Class**:
  * `sklearn.ensemble.AdaBoostClassifier`
* **특징**:
  * simple weak learner들을 순차적으로 결합함.
  * noisy data나 outlier에 민감할 수 있음.
  * 기본 weak learner로 depth가 얕은 Decision Tree가 자주 사용됨.

```Python
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

# AdaBoostClassifier 모델 생성
adaboost_classifier = AdaBoostClassifier(
    estimator=DecisionTreeClassifier(max_depth=1), # 약한 학습자로 결정 트리 분류 사용
    n_estimators=50,                               # 부스팅 과정에서 생성할 약한 학습자의 개수
    learning_rate=1.0,                             # 각 학습자가 기여하는 정도를 제어
    random_state=7                                 # 무작위성을 제어하는 시드 값
)

adaboost_classifier = adaboost_classifier.fit(X_train_scaled, y_train)
```

* `n_estimators`가 커질수록 모델 복잡도가 증가함.
* `learning_rate`를 낮추면 각 weak learner의 영향이 작아지므로 더 많은 estimator가 필요할 수 있음.

> scikit-learn 1.8 부터 `alogrithm`파라미터가 완전히 제거됨.  
> SAMME 만 남은 상태로 알려짐.

---

### **10. Gradient Boosting Classifier (그래디언트 부스팅 분류)**

* **설명**:
  * weak learner를 직렬로 결합하여 점진적으로 classification loss를 줄이는 ensemble 기법.
  * Boosting 계열에 속함.
  * 이전 모델이 남긴 error를 다음 모델이 보완하는 방식으로 학습함.
* **사용 Class**:
  * `sklearn.ensemble.GradientBoostingClassifier`
* **특징**:
  * 강력한 성능을 보일 수 있음.
  * 학습이 느릴 수 있으며 hyper-parameter에 의한 성능 차이가 큼.
  * over-fitting의 위험이 존재하므로 `learning_rate`, `n_estimators`, `max_depth` 조절이 중요함.

```Python
from sklearn.ensemble import GradientBoostingClassifier

# GradientBoostingClassifier 모델 생성
gb_classifier = GradientBoostingClassifier(
    loss='log_loss',            # 손실 함수 ('log_loss', 'exponential')
    learning_rate=0.1,          # 학습률, 각 tree가 기여하는 정도를 제어
    n_estimators=100,           # 생성할 tree의 개수
    subsample=1.0,              # 각 tree 학습에 사용할 sample 비율
    criterion='friedman_mse',   # tree 분할 기준
    min_samples_split=2,        # 내부 노드를 분할하기 위한 최소 샘플 수
    min_samples_leaf=1,         # 리프 노드에 있어야 하는 최소 샘플 수
    min_weight_fraction_leaf=0.0,# 리프 노드에서의 가중치 최소 비율
    max_depth=3,                # tree의 최대 깊이
    min_impurity_decrease=0.0,  # 노드를 분할하는 데 필요한 불순도 감소
    init=None,                  # 초기 추정기
    random_state=7,             # 난수 seed
    max_features=None,          # 각 분할에서 고려할 최대 특성 수
    verbose=0,                  # 학습 과정 중 출력 여부
    max_leaf_nodes=None,        # 리프 노드의 최대 개수
    warm_start=False,           # True로 설정하면 이전 학습 결과에서 추가 학습 가능
    validation_fraction=0.1,    # 조기 종료를 위해 검증용으로 사용할 훈련 데이터 비율
    n_iter_no_change=None,      # 조기 종료 조건
    tol=1e-4,                   # 성능 향상이 없을 때 종료하기 위한 허용 오차
    ccp_alpha=0.0               # 비용-복잡도 가지치기의 매개변수
)

gb_classifier = gb_classifier.fit(X_train_scaled, y_train)
```

---

### **11. HistGradientBoosting Classifier**

* **설명**:
  * Histogram 기반 Gradient Boosting Classifier.
  * continuous feature를 binning하여 histogram 형태로 처리함으로써 학습 속도를 높인 boosting 모델.
* **사용 함수**:
  * `sklearn.ensemble.HistGradientBoostingClassifier`
* **특징**:
  * large dataset에서 `GradientBoostingClassifier`보다 빠른 경우가 많음.
  * missing value를 내부적으로 처리할 수 있음.
  * scikit-learn 내부에서 제공하는 고성능 boosting classifier임.
  * XGBoost, LightGBM, CatBoost 같은 외부 라이브러리 없이 사용할 수 있음.

```Python
from sklearn.ensemble import HistGradientBoostingClassifier

# HistGradientBoostingClassifier 모델 생성
hist_gb_classifier = HistGradientBoostingClassifier(
    loss='log_loss',             # classification loss
    learning_rate=0.1,           # 학습률
    max_iter=100,                # boosting iteration 수
    max_leaf_nodes=31,           # 각 tree의 최대 leaf node 수
    max_depth=None,              # tree의 최대 깊이
    min_samples_leaf=20,         # leaf node에 필요한 최소 sample 수
    l2_regularization=0.0,       # L2 regularization 강도
    max_features=1.0,            # 각 tree에서 사용할 feature 비율
    max_bins=255,                # histogram bin의 최대 개수
    categorical_features='from_dtype', # categorical feature 처리 방식(1.4 이후 추가)
    monotonic_cst=None,          # monotonic constraint
    interaction_cst=None,        # interaction constraint
    warm_start=False,            # 이전 학습 결과를 사용하여 추가 학습할지 여부
    early_stopping='auto',       # 조기 종료 여부
    scoring='loss',              # early stopping 기준 score
    validation_fraction=0.1,     # validation set 비율
    n_iter_no_change=10,         # 개선이 없을 때 종료까지 기다릴 iteration 수
    tol=1e-7,                    # 조기 종료 허용 오차
    verbose=0,                   # 출력 여부
    random_state=7,              # 난수 seed
    class_weight=None            # class imbalance 보정용 가중치
)

hist_gb_classifier = hist_gb_classifier.fit(X_train_scaled, y_train)
```

* Tree 기반 모델이므로 feature scaling은 필수는 아님.
* 다만 다른 model과 pipeline으로 같이 비교할 때는 preprocessing 방식을 통일하는 편이 실험 관리에 유리함.

---

### **12. XGBoost / LightGBM / CatBoost (외부 라이브러리 사용)**

* **설명**:

  * Gradient Boosting을 더 최적화한 고성능 모델들.
  * scikit-learn API와 유사한 interface를 제공하므로, scikit-learn workflow와 함께 사용하기 쉬움.
* **사용 함수**:

  * `xgboost.XGBClassifier`: GB를 최적화 (2014 개발. 2016.8 논문 발표)
  * `lightgbm.LGBMClassifier`: 빠른 learning 과 낮은 메모리 사용을 목표로 개발 (2017)
  * `catboost.CatBoostClassifier`: Categorical data를 효율적으로 처리하는 GB (2017)
* **특징**:

  * 복잡한 데이터셋에서도 우수한 성능을 보이나 third-party library가 필요.
  * tabular data에서 strong baseline으로 자주 사용됨.
  * hyper-parameter tuning에 따른 성능 차이가 큼.

---

**XGBClassifier**

```Python
import xgboost as xgb

# XGBClassifier 모델 생성
xgb_classifier = xgb.XGBClassifier(
    objective='binary:logistic',   # 목적 함수. multi-class는 'multi:softprob' 등을 사용
    n_estimators=100,              # 부스팅 과정에서 생성할 tree의 개수
    learning_rate=0.1,             # 학습률
    max_depth=3,                   # 각 tree의 최대 깊이
    min_child_weight=1,            # leaf node가 가져야 할 최소 가중치 합
    gamma=0,                       # node를 분할하기 위한 최소 loss 감소
    subsample=1.0,                 # 각 tree 학습에 사용할 sample 비율
    colsample_bytree=1.0,          # 각 tree 학습에 사용할 feature 비율
    reg_alpha=0,                   # L1 regularization 항의 가중치
    reg_lambda=1,                  # L2 regularization 항의 가중치
    booster='gbtree',              # 부스팅 알고리즘 ('gbtree', 'gblinear', 'dart')
    n_jobs=-1,                     # 병렬 처리에 사용할 CPU 코어 수
    random_state=7,                # 무작위성을 제어하기 위한 seed
    verbosity=1                    # 출력 메시지 수준
)

xgb_classifier = xgb_classifier.fit(X_train_scaled, y_train)
```

---

**LGBMClassifier**

```Python
import lightgbm as lgb

# LGBMClassifier 모델 생성
lgb_classifier = lgb.LGBMClassifier(
    boosting_type='gbdt',        # 부스팅 유형 ('gbdt', 'rf', 'dart', 'goss')
    num_leaves=31,              # 하나의 tree가 가질 수 있는 최대 leaf node 수
    max_depth=-1,               # tree의 최대 깊이 (-1은 제한 없음)
    learning_rate=0.1,          # 학습률
    n_estimators=100,           # 부스팅 과정에서 생성할 tree의 개수
    subsample_for_bin=200000,   # feature bin 구성에 사용할 sample 수
    objective=None,             # 목적 함수. None이면 task에 따라 자동 설정
    class_weight=None,          # class imbalance 보정용 가중치
    min_split_gain=0.0,         # node를 분할할 때 필요한 최소 loss 감소
    min_child_weight=1e-3,      # leaf node가 가져야 할 최소 가중치 합
    min_child_samples=20,       # leaf node에 있어야 할 최소 sample 수
    subsample=1.0,              # 각 tree 학습에 사용할 sample 비율
    subsample_freq=0,           # subsample 수행 빈도
    colsample_bytree=1.0,       # 각 tree 학습에 사용할 feature 비율
    reg_alpha=0.0,              # L1 regularization 계수
    reg_lambda=0.0,             # L2 regularization 계수
    random_state=7,             # 무작위성 제어를 위한 seed
    n_jobs=-1,                  # 병렬 처리에 사용할 CPU 코어 수
    verbose=-1                  # -1: 로그 메시지 비활성화
)

lgb_classifier = lgb_classifier.fit(X_train_scaled, y_train)
```

---

**CatBoostClassifier**

```Python
# !pip install catboost
from catboost import CatBoostClassifier

# CatBoostClassifier 모델 생성
catboost_classifier = CatBoostClassifier(
    iterations=1000,          # 부스팅 반복 횟수
    learning_rate=0.1,        # 학습률
    depth=6,                  # tree의 최대 깊이
    loss_function='Logloss',  # binary classification 손실 함수
    eval_metric='Accuracy',   # 평가 metric
    random_seed=42,           # 무작위성 제어를 위한 seed
    l2_leaf_reg=3.0,          # L2 regularization 계수
    bootstrap_type='Bayesian',# 부트스트랩 샘플링 방식
    task_type='CPU',          # GPU 사용 시 'GPU'
    verbose=100               # 학습 과정에서 출력 메시지 빈도
)

catboost_classifier = catboost_classifier.fit(X_train_scaled, y_train)
```

* CatBoost는 categorical feature를 직접 처리할 수 있다는 점이 큰 장점임.
* scikit-learn wrapper 형태로 사용할 수 있으나, categorical feature 지정 방식은 scikit-learn 기본 estimator와 다름.
