---
title: "[ML] Classic Classifier (Summary)"
description: >
  DeepLearning 계열을 제외한 Classic Classifier 모델들의 요약 정리.
  KNN, Logistic Regression, SGDClassifier, Naive Bayes, SVM,
  Decision Tree, Random Forest, AdaBoost, Gradient Boosting,
  XGBoost, LightGBM, CatBoost를 linear / non-linear,
  binary / multi-class / multi-label classification 관점에서 정리.
tags:
  - machine learning
  - classification
  - scikit-learn
  - logistic regression
  - support vector machine
  - decision tree
  - random forest
  - ensemble
  - boosting
  - bagging
  - multi-class classification
  - multi-label classification
---

# [ML] Classic Classifier (Summary)

> DeepLearning 계열을 제외한 Classic Classifier 모델들을 정리함.

Classification model은 다음 기준으로 구분할 수 있음.

* decision boundary 기준
    * linear classifier
    * non-linear classifier
* target 형태 기준
    * binary classification
    * multi-class classification
    * multi-label classification
* 학습 방식 기준
    * instance based model
    * probabilistic model
    * margin based model
    * tree based model
    * ensemble model

이 글에서는 먼저 target 형태를 기준으로 classification task를 구분하고,
binary classifier를 multi-class 또는 multi-label 문제로 확장하는 wrapper 전략을 정리한 뒤,
주요 classic classifier들을 모델별로 요약함.

---

## **1. Classification Task의 기본 구분**

Classification task는 target $y$의 형태에 따라 다음과 같이 구분됨.

| 구분 | target 형태 | sample당 정답 수 | 의미 | 예시 |
|---|---|---:|---|---|
| Binary Classification | $y \in \{0, 1\}$ | 1개 | 두 class 중 하나 선택 | 정상/비정상, 양성/음성 |
| Multi-class Classification | $y \in \{0, 1, \cdots, K-1\}$ | 1개 | 여러 class 중 정확히 하나 선택 | 숫자 0~9 분류, 품종 분류 |
| Multi-label Classification | $\mathbf{y} \in \{0,1\}^{L}$ | 여러 개 가능 | 여러 label을 동시에 선택 가능 | 이미지 태그 분류, 문서 태그 분류 |

* 여기서는 multi-output classification은 생략함.
* multi-class와 multi-label을 구분하는 핵심은 **하나의 sample이 여러 label을 동시에 가질 수 있는가**임.

---

### **1-1. Binary Classification**

Binary classification은 class가 두 개인 classification task임.

$$
y \in \{0, 1\}
$$

예:

* 암/정상
* 스팸/정상 메일
* 합격/불합격
* 고장/정상

확률 기반 classifier에서는 보통 class 1의 확률을 추정함.

$$
\hat{p} = P(y=1 \mid \mathbf{x})
$$

기본 threshold가 $0.5$인 경우, 예측 class는 다음과 같이 결정됨.

$$
\hat{y} =
\begin{cases}
1, & \hat{p} \ge 0.5 \\
0, & \hat{p} < 0.5
\end{cases}
$$

단, threshold $0.5$는 고정된 법칙이 아님.

* recall을 높이고 싶으면 threshold를 낮출 수 있음.
* precision을 높이고 싶으면 threshold를 높일 수 있음.
* imbalanced data에서는 threshold tuning이 중요함.

---

### **1-2. Multi-class Classification**

Multi-class classification은

* class가 3개 이상이고,
* 하나의 sample이 정확히 하나의 class에 속하는 문제임.

$$
y \in \{0, 1, 2, \cdots, K-1\}
$$

예:

* 숫자 이미지가 0~9 중 하나로 분류됨.
* 꽃이 setosa, versicolor, virginica 중 하나로 분류됨.
* 뉴스 기사가 정치, 경제, 사회, 문화 중 하나로 분류됨.

Multi-class classification에서는 class들이 mutually exclusive함.
즉, 하나의 sample은 여러 class에 동시에 속할 수 없음.

---

### **1-3. Multi-label Classification**

Multi-label classification은 하나의 sample이 여러 label을 동시에 가질 수 있는 문제임.

$$
\mathbf{y}_i = [y_{i1}, y_{i2}, \cdots, y_{iL}]
$$

각 label 값은 다음과 같음.

$$
y_{ij} \in \{0, 1\}
$$

예를 들어 target이 다음과 같은 vector로 주어질 수 있음.

$$
\mathbf{y}_i = [1, 0, 1, 0]
$$

이는 $i$번째 sample이 0번 label과 2번 label을 가진다는 의미임.

예:

* 이미지 태그:
    * `person`
    * `car`
    * `night`
    * `outdoor`
* 문서 태그:
    * `science`
    * `medicine`
    * `AI`
    * `policy`

Multi-label classification에서는 label들이 mutually exclusive하지 않음.
즉, 하나의 sample이 여러 label을 동시에 가질 수 있음.

---

### **1-4. Multi-class와 Multi-label의 차이**

| 구분 | Multi-class Classification | Multi-label Classification |
|---|---|---|
| target 형태 | 1D class label | 2D binary indicator |
| 예시 target | $y = 2$ | $\mathbf{y} = [1, 0, 1, 0]$ |
| sample당 정답 수 | 하나 | 여러 개 가능 |
| class/label 관계 | mutually exclusive | mutually non-exclusive |
| 출력 방식 | 하나의 class 선택 | label별 yes/no 판단 |
| 대표 예시 | 숫자 0~9 분류 | 이미지 태그 분류 |

---

## **2. Wrapper / Meta-estimator 기반 확장**

일부 classifier는 기본적으로 binary classification 문제만 직접 처리할 수 있음.

예를 들어 어떤 classifier가 다음 형태의 binary classifier라고 하자.

$$
h(\mathbf{x}) \in \{0, 1\}
$$

이 binary classifier를 multi-class 또는 multi-label classification에 사용하려면 문제를 여러 개의 binary classification task로 분해하고, 각 결과를 다시 조합해야 함.

$$
\text{complex classification problem}
\rightarrow
\text{several binary classification problems}
\rightarrow
\text{combine predictions}
$$

이 역할을 하는 것이 wrapper 또는 meta-estimator임.

wrapper는 base binary classifier의 내부 알고리즘을 바꾸지 않음.
대신 다음을 수행함.

* target $y$를 여러 binary target으로 변환함.
* base classifier를 여러 개 복제하여 각각 학습함.
* 여러 classifier의 score, probability, vote, binary output을 모아 최종 예측을 생성함.

---

### **2-1. Wrapper 전략 요약**

| 전략 | 주 사용 문제 | target 형태 | 내부 처리 | 최종 출력 |
|---|---|---|---|---|
| One-vs-Rest, OvR | Multi-class | 1D class label | class $k$ vs rest classifier를 class 수만큼 학습 | class 하나 |
| One-vs-One, OvO | Multi-class | 1D class label | class 쌍마다 classifier 학습 | class 하나 |
| Binary Relevance | Multi-label | 2D binary indicator | label마다 독립 classifier 학습 | label별 yes/no |
| Classifier Chain | Multi-label | 2D binary indicator | 앞 label 예측값을 뒤 label classifier의 feature로 사용 | label별 yes/no |

핵심 구분은 다음과 같음.

* One-vs-Rest와 One-vs-One은 multi-class classification 전략임.
* Binary Relevance와 Classifier Chain은 multi-label classification 전략임.
* scikit-learn의 `OneVsRestClassifier`는 이름은 OvR이지만, 2D binary indicator target을 넣으면 Binary Relevance 구현 도구로도 사용할 수 있음.

---

### **2-2. One-vs-Rest, OvR**

One-vs-Rest는 multi-class classification 문제를 여러 개의 binary classification 문제로 바꾸는 전략임.

class가 $K$개라면, $K$개의 binary classifier를 학습함.

$$
h_1(\mathbf{x}), h_2(\mathbf{x}), \cdots, h_K(\mathbf{x})
$$

각 classifier는 다음 문제를 학습함.

| classifier | 학습하는 문제 |
|---|---|
| $h_1(\mathbf{x})$ | class 1 vs not class 1 |
| $h_2(\mathbf{x})$ | class 2 vs not class 2 |
| $\cdots$ | $\cdots$ |
| $h_K(\mathbf{x})$ | class $K$ vs not class $K$ |

예를 들어 class가 다음과 같다고 하자.

* `cat`
* `dog`
* `horse`

One-vs-Rest는 다음 binary classifier들을 학습함.

* `cat` vs `not cat`
* `dog` vs `not dog`
* `horse` vs `not horse`

prediction 단계에서는 각 classifier의 score를 비교하여 가장 높은 score를 가진 class를 최종 class로 선택함.

$$
\hat{y} = \underset{k}{\arg\max}\ s_k(\mathbf{x})
$$

즉, One-vs-Rest는 여러 개의 binary classifier를 학습하지만, 최종 출력은 class 하나임.

```python
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression

# Multi-class classification에서 One-vs-Rest 전략 사용.
# y_train은 shape이 (n_samples,)인 1D class label vector임.
ovr_clf = OneVsRestClassifier(
    LogisticRegression(max_iter=1000)
)

ovr_clf = ovr_clf.fit(X_train_scaled, y_train)
```

```python
y_train = [0, 2, 1, 0, 2, 1]
```

* 각 sample은 class 하나에만 속함.

---

### **2-3. One-vs-One, OvO**

One-vs-One은 class 쌍마다 binary classifier를 학습하는 multi-class classification 전략임.

class가 $K$개라면 필요한 classifier 수는 다음과 같음.

$$
\frac{K(K-1)}{2}
$$

예를 들어 class가 다음과 같은 경우를 생각해보자.

* `cat`
* `dog`
* `horse`

One-vs-One은 다음 binary classifier들을 학습함.

* `cat` vs `dog`
* `cat` vs `horse`
* `dog` vs `horse`

prediction 단계에서는 각 classifier의 결과를 모아 voting 방식으로 최종 class를 결정함.

```python
from sklearn.multiclass import OneVsOneClassifier
from sklearn.svm import SVC

# Multi-class classification에서 One-vs-One 전략 사용.
# class 쌍마다 binary classifier를 학습함.
ovo_clf = OneVsOneClassifier(
    SVC(kernel="linear")
)

ovo_clf = ovo_clf.fit(X_train_scaled, y_train)
```

---

### **2-4. Binary Relevance**

Binary Relevance는 multi-label classification 문제를 label 수만큼의 independent binary classification 문제로 나누는 방법임.

label이 $L$개라면, Binary Relevance는 $L$개의 binary classifier를 학습함.

$$
h_1(\mathbf{x}), h_2(\mathbf{x}), \cdots, h_L(\mathbf{x})
$$

$j$번째 classifier는 다음 binary classification 문제를 학습함.

$$
h_j(\mathbf{x}_i) \approx y_{ij}
$$

여기서 $y_{ij}$는 $i$번째 sample이 $j$번째 label에 속하는지 여부를 나타냄.

$$
y_{ij} =
\begin{cases}
1, & i\text{번째 sample이 }j\text{번째 label을 가짐} \\
0, & i\text{번째 sample이 }j\text{번째 label을 가지지 않음}
\end{cases}
$$

예를 들어 label이 다음과 같다고 하자.

* `person`
* `car`
* `night`
* `outdoor`

Binary Relevance는 다음 classifier들을 학습함.

| classifier | 의미 |
|---|---|
| $h_{\text{person}}(\mathbf{x})$ | person label이 있는가? |
| $h_{\text{car}}(\mathbf{x})$ | car label이 있는가? |
| $h_{\text{night}}(\mathbf{x})$ | night label이 있는가? |
| $h_{\text{outdoor}}(\mathbf{x})$ | outdoor label이 있는가? |

각 classifier는 독립적으로 yes/no를 판단함.

만약 예측 결과가 다음과 같다면,

$$
[1, 1, 0, 1]
$$

이는 해당 sample이 다음 label들을 가진다는 의미임.

* `person`
* `car`
* `outdoor`

scikit-learn에서는 `OneVsRestClassifier`를 이용하여 Binary Relevance 방식의 multi-label classification을 구현할 수 있음.

```python
# 예시
# sample 0: label 0, label 2
# sample 1: label 1
# sample 2: label 0, label 1, label 3

y_train_multilabel = [
    [1, 0, 1, 0],
    [0, 1, 0, 0],
    [1, 1, 0, 1],
]
```

```python
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression

# Multi-label classification에서 Binary Relevance 방식으로 사용.
# 주의: 개념적으로 One-vs-Rest가 아니라 Binary Relevance임.
# scikit-learn의 OneVsRestClassifier를 구현 도구로 사용하는 것임.
# y_train_multilabel은 shape이 (n_samples, n_labels)인 2D binary indicator matrix여야 함.
br_clf = OneVsRestClassifier(
    LogisticRegression(max_iter=1000)
)

br_clf = br_clf.fit(X_train_scaled, y_train_multilabel)
```

예측 결과는 각 label에 대한 yes/no 판단임.

```python
y_pred_multilabel = br_clf.predict(X_test_scaled)
```

예측 확률을 얻은 뒤 label별 threshold를 따로 적용할 수도 있음.

```python
y_score = br_clf.predict_proba(X_test_scaled)

thresholds = [0.5, 0.4, 0.7, 0.3]

y_pred_custom = (y_score >= thresholds).astype(int)
```

Multi-label 문제에서는 모든 label에 동일한 threshold $0.5$를 쓰는 것이 항상 좋은 선택은 아님.
label별 prevalence, precision-recall trade-off, cost를 고려하여 threshold를 따로 조정할 수 있음.

Binary Relevance의 장점은 다음과 같음.

* 구현이 단순함.
* 기존 binary classifier를 그대로 사용할 수 있음.
* label마다 다른 threshold를 적용할 수 있음.
* label별 precision/recall 조정이 쉬움.

단점은 다음과 같음.

* label 간 dependency를 직접 modeling하지 않음.
* label 사이의 상관관계가 중요한 문제에서는 성능이 제한될 수 있음.
* 예를 들어 `beach`와 `sea`, `car`와 `road`처럼 label 간 관계가 강한 경우 이를 직접 반영하지 못함.

---

### **2-5. One-vs-Rest와 Binary Relevance의 차이**

`One-vs-Rest`와 `Binary Relevance`는 모두 여러 개의 binary classifier를 사용한다는 점에서 구조가 비슷함.
하지만 개념적으로는 다름.

| 구분 | One-vs-Rest | Binary Relevance |
|---|---|---|
| 주 사용 문제 | Multi-class classification | Multi-label classification |
| target 형태 | 1D class label vector | 2D binary indicator matrix |
| sample당 정답 | class 하나 | label 여러 개 가능 |
| classifier 의미 | class $k$ vs 나머지 class | label $j$ 존재 여부 |
| 최종 출력 | class 하나 선택 | label별 yes/no 출력 |
| 대표 구현 | `OneVsRestClassifier` | `OneVsRestClassifier`로 구현 가능 |

정리하면 다음과 같음.

* 개념:
    * multi-class에는 One-vs-Rest.
    * multi-label에는 Binary Relevance.
* scikit-learn 구현:
    * 둘 다 `OneVsRestClassifier`로 구현 가능.
    * 단, target $y$의 shape과 의미가 다름.

---

### **2-6. Classifier Chain**

Classifier Chain은 Binary Relevance의 한계를 보완하기 위한 multi-label classification 방법임.

Binary Relevance는 label 간 dependency를 고려하지 않음.
반면 Classifier Chain은 앞에서 예측한 label을 뒤 label classifier의 추가 입력 feature로 사용함.

label 순서가 다음과 같다고 하자.

$$
[0, 1, 2, 3]
$$

그러면 classifiers는 다음과 같이 연결됨.

$$
h_0(\mathbf{x}) \approx y_0
$$

$$
h_1(\mathbf{x}, \hat{y}_0) \approx y_1
$$

$$
h_2(\mathbf{x}, \hat{y}_0, \hat{y}_1) \approx y_2
$$

$$
h_3(\mathbf{x}, \hat{y}_0, \hat{y}_1, \hat{y}_2) \approx y_3
$$

Classifier Chain에서 `order`는 label을 예측하는 순서임.
뒤쪽 classifier는 앞쪽 label 예측값을 feature로 사용하므로, order에 따라 학습되는 모델과 성능이 달라질 수 있음.

```python
from sklearn.multioutput import ClassifierChain
from sklearn.linear_model import LogisticRegression

chain_clf = ClassifierChain(
    LogisticRegression(max_iter=1000),
    order=[0, 1, 2, 3],
    # order="random", # 무작위 label 순서를 사용.
    random_state=7
)

chain_clf = chain_clf.fit(X_train_scaled, y_train_multilabel)
```

Classifier Chain의 특징은 다음과 같음.

* label dependency를 일부 반영할 수 있음.
* 특정 order에 민감할 수 있음.
* 앞쪽 label 예측 오류가 뒤쪽 classifier에 전달되는 error propagation이 발생할 수 있음.
* label 순서에 대한 domain knowledge가 없으면 여러 random chain을 ensemble하는 방법을 고려할 수 있음.

---

## **3. Decision Boundary 기준 분류**

Decision boundary 기준으로 보면 classic classifier는 대략 다음처럼 구분할 수 있음.

| 구분 | 대표 모델 | 비고 |
|---|---|---|
| Linear Model | Logistic Regression, Linear SVM, SGDClassifier | feature space에서 선형 decision boundary 학습 |
| Probabilistic Model | Naive Bayes | 분포 가정에 따라 boundary 형태가 달라짐 |
| Non-linear Model | KNN, Kernel SVM, Decision Tree, Ensemble Model | 비선형 decision boundary 가능 |

Naive Bayes Classifier는 probabilistic classifier로 보는 편이 더 정확함.
다만 많은 설정에서 linear에 가까운 decision boundary를 가질 수 있음.

Ensemble Model에는 다음이 포함됨.

* Random Forest Classifier
* AdaBoost Classifier
* Gradient Boosting Classifier
* XGBoost Classifier
* LightGBM Classifier
* CatBoost Classifier

---

## **4. 주요 Classification 모델**

---

### **4-1. K-Nearest Neighbors Classifier, KNN 분류**

* **설명**:
    * 가장 가까운 $K$개의 training samples를 찾고,
    * 이들의 class label을 기반으로 test sample의 class를 결정하는 instance based model.
* **사용 함수**:
    * `sklearn.neighbors.KNeighborsClassifier`
* **Decision Boundary**:
    * Non-linear
* **적용 가능한 task**:
    * Binary classification
    * Multi-class classification
    * Multi-label classification 가능
* **특징**:
    * 명시적인 parameter learning 과정이 거의 없음.
    * training data 자체를 기준으로 prediction을 수행함.
    * 거리 기반 모델이므로 feature scaling이 중요함.
    * $K$ 값이 작으면 over-fitting 경향이 커짐.
    * $K$ 값이 크면 decision boundary가 부드러워지지만 under-fitting 가능성이 커짐.
    * sample 수가 많으면 prediction cost가 커질 수 있음.

```python
from sklearn.neighbors import KNeighborsClassifier

knn_clf = KNeighborsClassifier(
    n_neighbors=5,          # 사용할 이웃 수
    weights="distance",     # 'uniform' 또는 'distance'
    algorithm="auto",       # 'auto', 'ball_tree', 'kd_tree', 'brute'
    leaf_size=30,           # tree 기반 탐색에서 leaf size
    p=2,                    # 1: Manhattan distance, 2: Euclidean distance
    metric="minkowski",     # 거리 metric
    n_jobs=-1               # 병렬 처리
)

knn_clf = knn_clf.fit(X_train_scaled, y_train)
```

---

### **4-2. Logistic Regression, 로지스틱 회귀**

* **설명**:
    * 이름은 regression이지만 classification model임.
    * 입력 feature들의 linear combination을 logit으로 사용하고,
    * sigmoid 또는 softmax를 통해 class probability를 추정함.
* **사용 함수**:
    * `sklearn.linear_model.LogisticRegression`
* **Decision Boundary**:
    * Linear
* **적용 가능한 task**:
    * Binary classification
    * Multi-class classification
    * Multi-label classification은 wrapper 필요
* **특징**:
    * 선형 decision boundary를 학습함.
    * probability를 출력할 수 있어 해석이 비교적 쉬움.
    * regularization을 통해 over-fitting을 제어함.
    * gradient 기반 solver를 사용할 경우 feature scaling이 중요함.
    * baseline classifier로 자주 사용됨.

Binary classification에서 Logistic Regression은 다음 형태로 class 1의 확률을 추정함.

$$
\hat{p} = P(y=1 \mid \mathbf{x}) = \sigma(\mathbf{w}^{\top}\mathbf{x} + b)
$$

여기서 $\sigma(z)$는 sigmoid function임.

$$
\sigma(z) = \frac{1}{1 + e^{-z}}
$$

기본 threshold가 $0.5$이면 다음처럼 class를 결정함.

$$
\hat{y} =
\begin{cases}
1, & \hat{p} \ge 0.5 \\
0, & \hat{p} < 0.5
\end{cases}
$$

```python
from sklearn.linear_model import LogisticRegression

logistic_clf = LogisticRegression(
    penalty="l2",            # regularization 종류: 'l1', 'l2', 'elasticnet', None
    C=1.0,                   # regularization inverse strength. 작을수록 강한 regularization
    fit_intercept=True,      # bias term 사용 여부
    solver="lbfgs",          # 최적화 solver
    max_iter=1000,           # 최대 반복 횟수
    class_weight=None,       # class imbalance 처리: None 또는 'balanced'
    random_state=7,
    n_jobs=None
)

logistic_clf = logistic_clf.fit(X_train_scaled, y_train)
```

Multi-class classification에서는 class별 score를 softmax로 확률화할 수 있음.

$$
P(y=k \mid \mathbf{x}) =
\frac{\exp(z_k)}
{\sum_{j=1}^{K} \exp(z_j)}
$$

---

### **4-3. SGDClassifier**

* **설명**:
    * Stochastic Gradient Descent, SGD를 이용해 linear classifier를 학습하는 모델.
    * `loss` 설정에 따라 linear SVM, logistic regression 등과 유사한 모델을 만들 수 있음.
* **사용 함수**:
    * `sklearn.linear_model.SGDClassifier`
* **Decision Boundary**:
    * Linear
* **적용 가능한 task**:
    * Binary classification
    * Multi-class classification
    * Multi-label classification은 wrapper 필요
* **특징**:
    * sample 수가 매우 큰 경우 유리함.
    * sparse data에 적합함.
    * `partial_fit()`을 통해 online learning 또는 incremental learning에 사용할 수 있음.
    * gradient 기반 최적화이므로 feature scaling이 중요함.

```python
from sklearn.linear_model import SGDClassifier

sgd_clf = SGDClassifier(
    loss="log_loss",          # 'hinge': linear SVM, 'log_loss': logistic regression
    penalty="l2",             # 'l2', 'l1', 'elasticnet', None
    alpha=0.0001,             # regularization strength
    l1_ratio=0.15,            # elasticnet에서 L1 비율
    fit_intercept=True,
    max_iter=1000,            # 최대 epoch 수
    tol=1e-3,
    shuffle=True,
    class_weight=None,
    random_state=7,
    learning_rate="optimal",
    eta0=0.0,
    early_stopping=False,
    n_iter_no_change=5
)

sgd_clf = sgd_clf.fit(X_train_scaled, y_train)
```

* `loss="hinge"`:
    * Linear SVM과 유사한 classifier로 동작.
* `loss="log_loss"`:
    * Logistic Regression과 유사한 probabilistic classifier.
* `max_iter`:
    * parameter update 횟수라기보다 training set 전체를 반복하는 epoch 수에 가까움.

---

### **4-4. Naive Bayes Classifier**

* **설명**:
    * Bayes theorem을 기반으로 class posterior probability를 계산하는 probabilistic classifier.
    * features가 class 조건부로 서로 독립이라는 naive assumption을 사용함.
* **사용 함수**:
    * `sklearn.naive_bayes.GaussianNB`
    * `sklearn.naive_bayes.MultinomialNB`
    * `sklearn.naive_bayes.BernoulliNB`
* **Decision Boundary**:
    * 분포 가정에 따라 달라짐.
    * GaussianNB는 class별 Gaussian distribution을 가정함.
    * MultinomialNB는 count 기반 feature에 적합함.
* **적용 가능한 task**:
    * Binary classification
    * Multi-class classification
    * Multi-label classification은 wrapper 필요
* **특징**:
    * 학습이 매우 빠름.
    * 작은 dataset에서도 비교적 안정적으로 동작하는 경우가 많음.
    * text classification에서 많이 사용됨.
    * feature independence assumption이 강하므로 복잡한 feature interaction은 잘 반영하지 못함.

```python
from sklearn.naive_bayes import GaussianNB

nb_clf = GaussianNB(
    priors=None,        # class prior를 직접 지정할지 여부
    var_smoothing=1e-9  # 분산 안정화를 위한 smoothing 값
)

nb_clf = nb_clf.fit(X_train, y_train)
```

Text classification에서는 count vector 또는 TF-IDF feature와 함께 `MultinomialNB`가 자주 사용됨.

```python
from sklearn.naive_bayes import MultinomialNB

mnb_clf = MultinomialNB(
    alpha=1.0,          # smoothing strength
    fit_prior=True      # class prior 학습 여부
)

mnb_clf = mnb_clf.fit(X_train_count, y_train)
```

---

### **4-5. Support Vector Classifier, SVC**

* **설명**:
    * class 사이의 margin을 최대화하는 decision boundary를 찾는 classifier.
    * kernel trick을 사용하면 non-linear decision boundary를 만들 수 있음.
* **사용 함수**:
    * `sklearn.svm.SVC`
    * `sklearn.svm.LinearSVC`
* **Decision Boundary**:
    * `kernel="linear"` 또는 `LinearSVC`: Linear
    * `kernel="rbf"`, `kernel="poly"`: Non-linear
* **적용 가능한 task**:
    * Binary classification
    * Multi-class classification
    * Multi-label classification은 wrapper 필요
* **특징**:
    * margin maximization 기반으로 generalization 성능이 좋은 경우가 많음.
    * feature scaling이 매우 중요함.
    * sample 수가 매우 많으면 학습 비용이 커질 수 있음.
    * `probability=True`를 설정하면 probability 추정이 가능하지만 추가 비용이 발생함.

```python
from sklearn.svm import SVC

svc_clf = SVC(
    C=1.0,                  # regularization parameter
    kernel="rbf",           # 'linear', 'poly', 'rbf', 'sigmoid'
    degree=3,               # poly kernel에서 degree
    gamma="scale",          # kernel coefficient
    coef0=0.0,              # poly, sigmoid kernel에서 사용
    shrinking=True,
    probability=False,      # probability estimate 사용 여부
    tol=1e-3,
    class_weight=None,
    random_state=7
)

svc_clf = svc_clf.fit(X_train_scaled, y_train)
```

Linear SVM만 필요하다면 `LinearSVC` 또는 `SGDClassifier(loss="hinge")`를 사용할 수 있음.

```python
from sklearn.svm import LinearSVC

linear_svc_clf = LinearSVC(
    penalty="l2",
    loss="squared_hinge",
    C=1.0,
    class_weight=None,
    max_iter=5000,
    random_state=7
)

linear_svc_clf = linear_svc_clf.fit(X_train_scaled, y_train)
```

---

### **4-6. Decision Tree Classifier, 결정 트리 분류**

* **설명**:
    * feature space를 tree 구조로 분할하여 class를 예측하는 classifier.
* **사용 함수**:
    * `sklearn.tree.DecisionTreeClassifier`
* **Decision Boundary**:
    * Non-linear
* **적용 가능한 task**:
    * Binary classification
    * Multi-class classification
    * Multi-output classification 가능
* **특징**:
    * feature scaling이 거의 필요 없음.
    * decision rule을 시각화하거나 해석하기 쉬움.
    * over-fitting 가능성이 매우 높음.
    * Random Forest, Gradient Boosting 등의 base learner로 자주 사용됨.

```python
from sklearn.tree import DecisionTreeClassifier

tree_clf = DecisionTreeClassifier(
    criterion="gini",          # 'gini', 'entropy', 'log_loss'
    splitter="best",          # 'best' 또는 'random'
    max_depth=None,            # tree 최대 깊이
    min_samples_split=2,       # 내부 node split에 필요한 최소 sample 수
    min_samples_leaf=1,        # leaf node에 필요한 최소 sample 수
    max_features=None,         # split에 사용할 최대 feature 수
    class_weight=None,         # class imbalance 처리
    random_state=7,
    ccp_alpha=0.0              # cost-complexity pruning parameter
)

tree_clf = tree_clf.fit(X_train, y_train)
```

---

### **4-7. Random Forest Classifier, 랜덤 포레스트 분류**

* **설명**:
    * 여러 개의 Decision Tree를 bootstrap sample로 학습하고,
    * 각 tree의 예측을 voting 또는 probability averaging으로 결합하는 bagging 기반 ensemble model.
* **사용 함수**:
    * `sklearn.ensemble.RandomForestClassifier`
* **Decision Boundary**:
    * Non-linear
* **적용 가능한 task**:
    * Binary classification
    * Multi-class classification
    * Multi-label classification 가능
* **특징**:
    * 단일 Decision Tree보다 over-fitting에 강함.
    * feature scaling이 거의 필요 없음.
    * feature importance를 확인할 수 있음.
    * `oob_score=True`를 사용하면 out-of-bag sample 기반 평가가 가능함.

```python
from sklearn.ensemble import RandomForestClassifier

forest_clf = RandomForestClassifier(
    n_estimators=100,          # tree 개수
    criterion="gini",          # 'gini', 'entropy', 'log_loss'
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    max_features="sqrt",       # classification에서 자주 사용
    bootstrap=True,
    oob_score=False,
    class_weight=None,
    n_jobs=-1,
    random_state=7,
    ccp_alpha=0.0,
    max_samples=None
)

forest_clf = forest_clf.fit(X_train, y_train)
```

* Classification에서는 `max_features="sqrt"`가 자주 사용됨.
* 각 tree가 서로 다른 feature subset을 보게 하여 tree들 사이의 correlation을 줄이는 것이 목적임.
* class imbalance가 있으면 `class_weight="balanced"` 또는 `class_weight="balanced_subsample"`을 고려할 수 있음.

---

### **4-8. AdaBoost Classifier**

* **설명**:
    * weak learner를 순차적으로 학습시키며,
    * 이전 단계에서 잘못 분류한 sample에 더 큰 weight를 부여하는 boosting model.
* **사용 함수**:
    * `sklearn.ensemble.AdaBoostClassifier`
* **Decision Boundary**:
    * base estimator에 따라 달라짐.
    * 보통 Decision Tree stump를 사용하므로 non-linear ensemble model로 볼 수 있음.
* **적용 가능한 task**:
    * Binary classification
    * Multi-class classification
    * Multi-label classification은 wrapper 필요
* **특징**:
    * 단순한 weak learner를 결합하여 강한 classifier를 만듦.
    * noisy data와 outlier에 민감할 수 있음.
    * base estimator로 얕은 Decision Tree가 자주 사용됨.

```python
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

adaboost_clf = AdaBoostClassifier(
    estimator=DecisionTreeClassifier(max_depth=1),
    n_estimators=50,          # weak learner 개수
    learning_rate=1.0,        # 각 learner의 기여도
    random_state=7
)

adaboost_clf = adaboost_clf.fit(X_train, y_train)
```

---

### **4-9. Gradient Boosting Classifier**

* **설명**:
    * 이전 model의 error를 줄이는 방향으로 weak learner를 순차적으로 추가하는 boosting model.
    * classification에서는 log loss 등을 최소화하는 방향으로 학습함.
* **사용 함수**:
    * `sklearn.ensemble.GradientBoostingClassifier`
* **Decision Boundary**:
    * Non-linear
* **적용 가능한 task**:
    * Binary classification
    * Multi-class classification
    * Multi-label classification은 wrapper 필요
* **특징**:
    * 강력한 성능을 보이는 경우가 많으나 hyper-parameter에 민감함.
    * 학습이 Random Forest보다 느릴 수 있음.
    * over-fitting 방지를 위해 `learning_rate`, `n_estimators`, `max_depth` 조절이 중요함.

```python
from sklearn.ensemble import GradientBoostingClassifier

gb_clf = GradientBoostingClassifier(
    loss="log_loss",          # classification loss
    learning_rate=0.1,
    n_estimators=100,
    subsample=1.0,
    criterion="friedman_mse",
    min_samples_split=2,
    min_samples_leaf=1,
    max_depth=3,
    max_features=None,
    random_state=7,
    validation_fraction=0.1,
    n_iter_no_change=None,
    tol=1e-4
)

gb_clf = gb_clf.fit(X_train, y_train)
```

---

### **4-10. XGBoost / LightGBM / CatBoost Classifier**

* **설명**:
    * Gradient Boosting을 최적화한 고성능 third-party library 기반 classifier.
* **사용 함수**:
    * `xgboost.XGBClassifier`
    * `lightgbm.LGBMClassifier`
    * `catboost.CatBoostClassifier`
* **Decision Boundary**:
    * Non-linear
* **적용 가능한 task**:
    * Binary classification
    * Multi-class classification
    * wrapper 또는 별도 구성으로 multi-label classification에도 사용 가능
* **특징**:
    * tabular data에서 매우 강력한 성능을 보이는 경우가 많음.
    * missing value, categorical feature 처리 방식은 library마다 차이가 있음.
    * hyper-parameter tuning의 영향이 큼.
    * scikit-learn 외부 library 설치가 필요함.

---

#### **XGBClassifier**

```python
from xgboost import XGBClassifier

xgb_clf = XGBClassifier(
    objective="binary:logistic",  # binary classification
    n_estimators=100,
    learning_rate=0.1,
    max_depth=3,
    min_child_weight=1,
    gamma=0,
    subsample=1.0,
    colsample_bytree=1.0,
    reg_alpha=0.0,
    reg_lambda=1.0,
    random_state=7,
    n_jobs=-1,
    eval_metric="logloss"
)

xgb_clf = xgb_clf.fit(X_train, y_train)
```

Multi-class classification에서는 objective를 다음처럼 바꿀 수 있음.

```python
from xgboost import XGBClassifier

xgb_multi_clf = XGBClassifier(
    objective="multi:softprob",
    num_class=3,
    eval_metric="mlogloss",
    random_state=7
)

xgb_multi_clf = xgb_multi_clf.fit(X_train, y_train)
```

---

#### **LGBMClassifier**

```python
from lightgbm import LGBMClassifier

lgbm_clf = LGBMClassifier(
    boosting_type="gbdt",
    objective="binary",
    n_estimators=100,
    learning_rate=0.1,
    num_leaves=31,
    max_depth=-1,
    min_child_samples=20,
    subsample=1.0,
    colsample_bytree=1.0,
    reg_alpha=0.0,
    reg_lambda=0.0,
    class_weight=None,
    random_state=7,
    n_jobs=-1,
    verbose=-1
)

lgbm_clf = lgbm_clf.fit(X_train, y_train)
```

Multi-class classification에서는 objective를 다음처럼 설정할 수 있음.

```python
from lightgbm import LGBMClassifier

lgbm_multi_clf = LGBMClassifier(
    objective="multiclass",
    num_class=3,
    random_state=7,
    verbose=-1
)

lgbm_multi_clf = lgbm_multi_clf.fit(X_train, y_train)
```

---

#### **CatBoostClassifier**

```python
from catboost import CatBoostClassifier

cat_clf = CatBoostClassifier(
    iterations=1000,
    learning_rate=0.1,
    depth=6,
    loss_function="Logloss",      # binary classification
    eval_metric="Accuracy",
    random_seed=7,
    l2_leaf_reg=3.0,
    task_type="CPU",
    verbose=100
)

cat_clf = cat_clf.fit(X_train, y_train)
```

Multi-class classification에서는 다음처럼 설정할 수 있음.

```python
from catboost import CatBoostClassifier

cat_multi_clf = CatBoostClassifier(
    loss_function="MultiClass",
    eval_metric="Accuracy",
    random_seed=7,
    verbose=100
)

cat_multi_clf = cat_multi_clf.fit(X_train, y_train)
```

---

## **5. Linear vs Non-linear Classifier 정리**

| Model | Linear / Non-linear | Scaling 필요성 | Probability 출력 | 주요 특징 |
|---|---|---:|---:|---|
| Logistic Regression | Linear | 높음 | 가능 | 해석 쉬움, baseline으로 좋음 |
| LinearSVC | Linear | 높음 | 기본적으로 불가 | margin 기반 linear classifier |
| SGDClassifier | Linear | 높음 | loss에 따라 가능 | large-scale data에 적합 |
| Naive Bayes | 단순 probabilistic | 낮음~중간 | 가능 | 빠르고 text data에 강함 |
| KNN | Non-linear | 높음 | 가능 | instance based, prediction cost 큼 |
| SVC with RBF | Non-linear | 높음 | 옵션 필요 | 강력하지만 large data에 부담 |
| Decision Tree | Non-linear | 낮음 | 가능 | 해석 쉬우나 over-fitting 위험 |
| Random Forest | Non-linear | 낮음 | 가능 | 안정적, tabular baseline으로 강함 |
| AdaBoost | Non-linear | 낮음~중간 | 가능 | outlier에 민감할 수 있음 |
| Gradient Boosting | Non-linear | 낮음 | 가능 | 성능 좋지만 tuning 중요 |
| XGBoost / LightGBM / CatBoost | Non-linear | 낮음 | 가능 | tabular data에서 강력함 |

---

## **6. Binary / Multi-class / Multi-label 지원 정리**

| Model | Binary 직접 지원 | Multi-class 직접 지원 | Multi-label 직접 지원 | Wrapper / 별도 구성 | 비고 |
|---|---:|---:|---:|---:|---|
| Logistic Regression | 가능 | 가능 | 불가 | 필요 | `OneVsRestClassifier`로 Binary Relevance 구현 가능 |
| SGDClassifier | 가능 | 가능 | 불가 | 필요 | large-scale sparse data에 적합 |
| Naive Bayes | 가능 | 가능 | 불가 | 필요 | text classification에 자주 사용 |
| KNN Classifier | 가능 | 가능 | 가능 | 선택적 | multi-label target 직접 지원 가능 |
| SVC | 가능 | 가능 | 불가 | 필요 | multi-class는 내부적으로 OvO 기반 처리<br/>multi-label은 wrapper 필요 |
| LinearSVC | 가능 | 가능 | 불가 | 필요 | multi-class는 OvR 방식<br/>probability 출력은 기본적으로 불가 |
| Decision Tree Classifier | 가능 | 가능 | 가능 | 선택적 | multi-output / multi-label<br/>target 직접 처리 가능 |
| Random Forest Classifier | 가능 | 가능 | 가능 | 선택적 | multi-output / multi-label<br/>target 직접 처리 가능 |
| AdaBoost Classifier | 가능 | 가능 | 불가 | 필요 | multi-class는 SAMME 계열<br/>multi-label은 wrapper 필요 |
| Gradient Boosting Classifier | 가능 | 가능 | 불가 | 필요 | multi-label은 label별 모델 또는 wrapper 필요 |
| XGBoost / LightGBM / CatBoost | 가능 | 가능 | 일반적으로 불가 | 별도 구성 필요 | multi-label은 <br/>보통 label별 모델 또는 wrapper 사용 |

---

## **7. 주의사항**

* **Logistic Regression 은 baseline** 으로 주로 사용됨.
    * linear separability가 어느 정도 있는지 확인.
    * feature scaling 이 필요함.
    * coefficient 해석 가능.
* **feature interaction이나 non-linear relation이 강하면 tree 계열 사용**.
    * Decision Tree는 해석용 또는 개념 설명용.
    * Random Forest는 안정적인 baseline.
    * Gradient Boosting 계열은 성능 최적화용.
* sample 수가 매우 많고 sparse feature가 많으면 `SGDClassifier` 고려.
    * text classification, high-dimensional sparse data에 적합.
* dataset이 작거나 중간 규모이고 margin 기반 classifier가 적합해 보이면 `SVC` 고려.
    * scaling 필수.
    * RBF kernel은 non-linear boundary를 만들 수 있음.
* multi-class classification에서는 다음을 구분.
    * 모델이 multi-class를 직접 지원하는지 확인.
    * 필요하면 One-vs-Rest 또는 One-vs-One 사용.
* **multi-label classification** 에서는 다음을 구분.
    * 가장 기본적인 방법은 **Binary Relevance**.
    * scikit-learn에서는 `OneVsRestClassifier`를 Binary Relevance 구현 도구로 사용할 수 있음.
    * label dependency가 중요하면 Classifier Chain 고려.
    * label별 threshold tuning 필요.
