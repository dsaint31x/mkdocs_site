---
title: "[ML] Classic Classifier (Summary)"
description: >
  DeepLearning 계열을 제외한 Classic Classifier 모델들의 요약 정리.
  KNN, Logistic Regression, Ridge Classifier, SGDClassifier, Naive Bayes,
  SVC, Decision Tree, Random Forest, Extra Trees, AdaBoost, Gradient Boosting,
  HistGradientBoosting, XGBoost, LightGBM, CatBoost를
  linear / non-linear, binary / multi-class / multi-label classification
  관점에서 정리. Wrapper 전략(OvR, OvO, Binary Relevance, Classifier Chain) 포함.
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

* [관련 ipynb 파일](https://gist.github.com/ds31x/)

---

## **분류 기준 (Classification Criteria)**

Classification model은 다음 기준으로 구분할 수 있음.

* **Target 형태 기준**
    * Binary classification
    * Multi-class classification
    * Multi-label classification
    * Multi-output classification
* **Decision boundary 기준**
    * Linear classifier
    * Non-linear classifier
* **학습 방식 기준**
    * Instance based model
    * Probabilistic model
    * Margin based model
    * Tree based model
    * Ensemble model

---

## **1. Classification Task의 기본 구분**

Target $y$의 형태에 따라 classification task를 구분함.

| 구분 | Target 형태 | Sample당 output 수 | 의미 | 예시 |
|---|---|---:|---|---|
| Binary Classification | $y \in \{0, 1\}$ | 1개 | 두 class 중 하나 선택 | 정상/비정상,<br/>양성/음성 |
| Multi-class Classification | $y \in \{0, 1, \cdots, K-1\}$ | 1개 | 여러 class 중 <br/>정확히 하나 선택 | 숫자 0~9 분류,<br/>품종 분류 |
| Multi-label Classification | $\mathbf{y} \in \{0,1\}^{L}$ | 여러 개 가능 | 여러 label을 <br/>동시에 선택 가능 | 이미지 태그 분류,<br/>문서 태그 분류 |
| Multi-output Classification | $\mathbf{y} \in \{0,\cdots,K_j{-}1\}^{Q}$ | $Q$개 <br/>(각 output 독립) | 여러 개의 독립된 <br/>classification target을 동시에 예측 | 날씨 종류<br/>+ 강풍 여부<br/> 동시 예측 |

---

### **1-1. Binary Classification**

$$
y \in \{0, 1\}
$$

확률 기반 classifier에서는 class 1의 확률을 추정함.

$$
\hat{p} = P(y=1 \mid \mathbf{x})
$$

기본 threshold가 $0.5$인 경우 예측 class는 다음과 같이 결정됨.

$$
\hat{y} =
\begin{cases}
1, & \hat{p} \ge 0.5 \\
0, & \hat{p} < 0.5
\end{cases}
$$

threshold $0.5$는 고정된 법칙이 아님.

* recall을 높이고 싶으면 threshold를 낮출 수 있음.
* precision을 높이고 싶으면 threshold를 높일 수 있음.
* imbalanced data에서는 threshold tuning이 중요함
  (ROC curve보다 PR curve를 이용하는게 권장됨).

---

### **1-2. Multi-class Classification**

* Class가 3개 이상이고, 하나의 sample이 **정확히 하나의 class** 에 속하는 문제임.
* Class들이 mutually exclusive함.

$$
y \in \{0, 1, 2, \cdots, K-1\}
$$

---

### **1-3. Multi-label Classification**

* 하나의 sample이 **여러 label을 동시에** 가질 수 있는 문제임.
* Label들이 mutually exclusive하지 않음.

$$
\mathbf{y}_i = [y_{i1}, y_{i2}, \cdots, y_{iL}], \quad y_{ij} \in \{0, 1\}
$$

예를 들어 $\mathbf{y}_i = [1, 0, 1, 0]$이면 $i$번째 sample이 0번, 2번 label을 가진다는 의미임.

---


### **1-3b. Multi-output Classification**

Multi-output classification은 하나의 sample에 대해 **여러 개의 독립적인 output** 을 동시에 예측하는 문제임.

각 output $j$는 그 자체로 독립된 classification target임.

$$
\mathbf{y}_i = [y_{i1}, y_{i2}, \cdots, y_{iQ}], \quad y_{ij} \in \{0, 1, \cdots, K_j - 1\}
$$

여기서 $K_j$는 $j$번째 output의 class 수이며, output마다 class 수가 달라도 됨.

예:

* 날씨 예측: output 1 = 맑음/흐림/비, output 2 = 강풍/약풍
* 의료 진단: output 1 = 질환 종류, output 2 = 중증도

Multi-label classification과의 차이는 다음과 같음.

| 구분 | Multi-label Classification | Multi-output Classification |
|---|---|---|
| Target 형태 | 2D binary indicator | 2D class label (각 열이 독립 class) |
| 각 output의 값 | $\{0, 1\}$ | $\{0, 1, \cdots, K_j - 1\}$ |
| 의미 | 하나의 target에 여러 label | 여러 개의 독립된 target |

scikit-learn에서 Decision Tree, Random Forest, Extra Trees는 multi-output target을 직접 처리할 수 있음.
그 외 모델에서는 `MultiOutputClassifier`를 사용함.

```python
from sklearn.multioutput import MultiOutputClassifier
from sklearn.linear_model import LogisticRegression

# 각 output에 대해 독립적인 classifier를 학습함
mo_clf = MultiOutputClassifier(LogisticRegression(max_iter=1000))
# y_train_multioutput: shape (n_samples, n_outputs)
mo_clf = mo_clf.fit(X_train_scaled, y_train_multioutput)
```

### **1-4. Multi-class와 Multi-label의 차이**

| 구분 | Multi-class Classification | Multi-label Classification |
|---|---|---|
| Target 형태 | 1D class label | 2D binary indicator |
| 예시 target | $y = 2$ | $\mathbf{y} = [1, 0, 1, 0]$ |
| Sample당 정답 수 | 하나 | 여러 개 가능 |
| Class/label 관계 | Mutually exclusive | Mutually non-exclusive |
| 대표 예시 | 숫자 0~9 분류 | 이미지 태그 분류 |

> Multi-output classification은 위 두 가지와 구분되는 별도 task임. 각 output이 독립된 classification 문제로 구성됨.

---

## **2. Wrapper / Meta-estimator 기반 확장**

일부 classifier는 기본적으로 binary classification만 직접 처리할 수 있음.

* 대표적인 예는 SVM 계열임.
* SVM은 두 class 사이의 margin을 최대화하는 binary classification 임.
* 따라서 class가 3개 이상인 multiclass classification에서는
One-vs-One 또는 One-vs-Rest 방식으로 여러 개의 binary SVM을 학습한 뒤
그 결과를 조합해야 함.

scikit-learn에서도 SVC는 내부적으로 OvO 방식을 사용하고,
LinearSVC는 OvR 방식을 사용하여 multiclass classification을 처리한다.

> 참고로 Logistic Regression은 multi-nomial logistic regression으로 일반화가 가능하여, multi-class classification으로 직접 확장이 가능함.

이처럼 binary classifier를 multi-class 또는 multi-label classification에 사용하려면
문제를 여러 개의 binary classification task로 분해한 뒤 결과를 조합해야 함.

$$
\text{complex classification}
\rightarrow
\text{several binary classifications}
\rightarrow
\text{combine predictions}
$$

이 역할을 하는 것이 **wrapper** 또는 **meta-estimator** 임.

Wrapper는 base classifier의 내부 알고리즘을 바꾸지 않고, 다음을 수행함.

* Target $y$를 여러 binary target으로 변환함.
* Base classifier를 여러 개 복제하여 각각 학습함.
* 여러 classifier의 score, probability, vote, binary output을 모아 최종 예측을 생성함.

---

### **2-1. Wrapper 전략 요약**

| 전략 | 주 사용 문제 | Target 형태 | 내부 처리 | 최종 출력 |
|---|---|---|---|---|
| One-vs-Rest (OvR) | Multi-class | 1D class label | class $k$ vs rest classifier를 class 수만큼 학습 | class 하나 |
| One-vs-One (OvO) | Multi-class | 1D class label | class 쌍마다 classifier 학습 | class 하나 |
| Binary Relevance | Multi-label | 2D binary indicator | label마다 독립 classifier 학습 | label별 yes/no |
| Classifier Chain | Multi-label | 2D binary indicator | 앞 label 예측값을 뒤 label classifier의 feature로 사용 | label별 yes/no |

* OvR, OvO는 multi-class classification 전략임.
* Binary Relevance, Classifier Chain은 multi-label classification 전략임.
* 참고로, scikit-learn의 `OneVsRestClassifier`는 2D binary indicator target을 넣으면 Binary Relevance 구현 도구로도 사용 가능함.

---

### **2-2. One-vs-Rest (OvR)**

Class $K$개에 대해 $K$개의 binary classifier를 학습함.

| Classifier | 학습하는 문제 |
|---|---|
| $h_k(\mathbf{x})$ | class $k$ vs not class $k$ |

Prediction 시 각 classifier의 score를 비교하여 가장 높은 score의 class를 선택함.

$$
\hat{y} = \underset{k}{\arg\max}\ s_k(\mathbf{x})
$$

```python
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression

# y_train: shape (n_samples,)인 1D class label vector
# LogisticRegression은 멀티클래스를 자동으로 지원가능하나,
# 예를 들기 위해 사용함.
ovr_clf = OneVsRestClassifier(LogisticRegression(max_iter=1000))
ovr_clf = ovr_clf.fit(X_train_scaled, y_train)
```

---

### **2-3. One-vs-One (OvO)**

Class $K$개에 대해 class 쌍마다 binary classifier를 학습함.

$$
\text{classifier 수} = \frac{K(K-1)}{2}
$$

Prediction 시 각 classifier의 결과를 모아 voting으로 최종 class를 결정함.

* Prediction 시 각 binary classifier는 두 class 중 하나에 vote를 부여함.
* 기본적으로 가장 많은 vote를 얻은 class가 최종 class로 선택됨.
* 단, 구현에 따라 vote가 동률인 경우 pair-wise classifier의 confidence score를 tie-breaking에 사용할 수 있음. 
* 참고로 scikit-learn의 `OneVsOneClassifier`는 `decision_function()`에서 vote에 정규화된 pair-wise confidence score를 더해 class별 decision score를 계산함.

```python
from sklearn.multiclass import OneVsOneClassifier
from sklearn.svm import SVC

ovo_clf = OneVsOneClassifier(SVC(kernel="linear"))
ovo_clf = ovo_clf.fit(X_train_scaled, y_train)
```

---

### **2-4. Binary Relevance**

Label $L$개에 대해 $L$개의 독립적인 binary classifier를 학습함.

> Relevance 는 해당 label과 샘플의 관련성을 의미!

$$
h_j(\mathbf{x}_i) \approx y_{ij}
$$

각 classifier는 label $j$의 존재 여부를 독립적으로 판단함.

```python
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression

# y_train_multilabel: shape (n_samples, n_labels)인 2D binary indicator matrix
# 개념적으로는 Binary Relevance이며, OneVsRestClassifier를 구현 도구로 사용하는 것임.
br_clf = OneVsRestClassifier(LogisticRegression(max_iter=1000))
br_clf = br_clf.fit(X_train_scaled, y_train_multilabel)
```

예측 결과는 각 label에 대한 yes/no 판단임.

```python
# y_train_multilabel 구조 예시
y_train_multilabel = [
    [1, 0, 1, 0],  # sample 0: label 0, label 2
    [0, 1, 0, 0],  # sample 1: label 1
    [1, 1, 0, 1],  # sample 2: label 0, label 1, label 3
]
```

```python
y_pred_multilabel = br_clf.predict(X_test_scaled)
```

Label별 threshold를 따로 적용할 수 있음.

```python
y_score = br_clf.predict_proba(X_test_scaled)
thresholds = [0.5, 0.4, 0.7, 0.3]
y_pred_custom = (y_score >= thresholds).astype(int)
```

| Classifier | 의미 |
|---|---|
| $h_{\text{person}}(\mathbf{x})$ | person label이 있는가? |
| $h_{\text{car}}(\mathbf{x})$ | car label이 있는가? |
| $h_{\text{night}}(\mathbf{x})$ | night label이 있는가? |
| $h_{\text{outdoor}}(\mathbf{x})$ | outdoor label이 있는가? |

Multi-label 문제에서는 모든 label에 동일한 threshold $0.5$를 쓰는 것이 항상 좋은 선택은 아님.
label별 prevalence, precision-recall trade-off, cost를 고려하여 threshold를 따로 조정할 수 있음.

* **장점**: 구현 단순. 기존 binary classifier 그대로 사용. label별 threshold 조정 용이.
* **단점**: label 간 dependency를 직접 modeling하지 않음.

---

### **2-5. OvR과 Binary Relevance의 차이**

| 구분 | One-vs-Rest | Binary Relevance |
|---|---|---|
| 주 사용 문제 | Multi-class classification | Multi-label classification |
| Target 형태 | 1D class label vector | 2D binary indicator matrix |
| Sample당 정답 | class 하나 | label 여러 개 가능 |
| Classifier 의미 | class $k$ vs 나머지 class | label $j$ 존재 여부 |
| 최종 출력 | class 하나 선택 | label별 yes/no 출력 |
| scikit-learn 구현 | `OneVsRestClassifier` | `OneVsRestClassifier` |

---

### **2-6. Classifier Chain**

Binary Relevance의 한계를 보완하기 위한 multi-label classification 방법임.

앞에서 예측한 label을 뒤 label classifier의 추가 입력 feature로 사용함.

$$
h_0(\mathbf{x}) \approx y_0
$$
$$
h_1(\mathbf{x}, \hat{y}_0) \approx y_1
$$
$$
h_2(\mathbf{x}, \hat{y}_0, \hat{y}_1) \approx y_2
$$

```python
from sklearn.multioutput import ClassifierChain
from sklearn.linear_model import LogisticRegression

chain_clf = ClassifierChain(
    LogisticRegression(max_iter=1000),
    order=[0, 1, 2, 3],   # label 예측 순서
    # order="random",      # 무작위 label 순서 사용
    random_state=7
)
chain_clf = chain_clf.fit(X_train_scaled, y_train_multilabel)
```

* Label dependency를 일부 반영할 수 있음.
* `order`에 따라 학습되는 모델과 성능이 달라질 수 있음.
* 앞쪽 label 예측 오류가 뒤쪽 classifier에 전달되는 **error propagation** 이 발생할 수 있음.
* Label 순서에 대한 domain knowledge가 없으면 여러 random chain을 ensemble하는 방법을 고려할 수 있음.

---

## **3. Decision Boundary 기준 분류**

| 구분 | 대표 모델 | 비고 |
|---|---|---|
| Linear Model | Logistic Regression, Ridge Classifier, Linear SVM, SGDClassifier | Feature space에서 선형 decision boundary |
| Probabilistic Model | Naive Bayes | 분포 가정에 따라 boundary 형태가 달라짐 |
| Non-linear Model | KNN, Kernel SVM, Decision Tree, Ensemble | 비선형 decision boundary 가능 |

---

## **4. 주요 Classifier 모델**

### **학습 방식 기준 분류**

* **Instance Based Algorithm**
    * K-Nearest Neighbors Classifier
* **Model Based Algorithm**
    * **Linear Model**
        * Logistic Regression
        * Ridge Classifier
        * SGDClassifier
    * **Probabilistic Model**
        * Naive Bayes
    * **Non-linear Model**
        * Support Vector Classification
        * Decision Tree Classification
        * **Ensemble Model**
            * Random Forest Classification
            * Extra Trees Classification
            * AdaBoost Classification
            * Gradient Boosting Classification
            * HistGradientBoosting Classification
            * XGBoost, LightGBM, CatBoost

---

### **4-0. K-Nearest Neighbors Classifier (KNN)**

참고: [k-Nearest Neighbors](https://dsaint31.tistory.com/832)

* **설명**:
    * 가장 가까운 $K$개의 training sample을 찾고, 이들의 class label을 voting하여 class를 결정하는 instance based model.
    * Fix & Hodges의 1951년 **미발표 보고서(unpublished technical report)** 에서 유래하였으며, Cover & Hart(1967)에 의해 공식화됨.
* **사용 Class**: `sklearn.neighbors.KNeighborsClassifier`
* **Decision Boundary**: Non-linear
* **적용 가능한 Task**: Binary / Multi-class / Multi-label classification 가능. Multi-output classification은 wrapper 필요.
* **특징**:
    * 명시적인 parameter learning 과정이 거의 없음 (lazy learner).
    * 거리 기반 모델이므로 **feature scaling 필수**.
    * $K$ 값이 작으면 over-fitting, $K$ 값이 크면 under-fitting 경향이 있음.
    * Sample 수가 많으면 prediction 비용이 커질 수 있음.

```python
from sklearn.neighbors import KNeighborsClassifier

knn_classifier = KNeighborsClassifier(
    n_neighbors=5,      # 이웃 수 (k 값)
    weights='distance', # 거리 가중치 ('uniform' 또는 'distance')
    algorithm='auto',   # 이웃 탐색 알고리즘 ('auto', 'ball_tree', 'kd_tree', 'brute')
    leaf_size=30,       # tree 기반 탐색에서 leaf size
    p=2,                # 거리 측정 방법 (1: Manhattan, 2: Euclidean)
    metric='minkowski', # 거리 계산 metric
    n_jobs=-1           # 병렬 처리 CPU 코어 수 (-1: 모든 코어 사용)
)
knn_classifier = knn_classifier.fit(X_train_scaled, y_train)
```

참고: [Minkowski Distance](https://dsaint31.tistory.com/827)

---

### **4-1. Logistic Regression (로지스틱 회귀)**

* **설명**:
    * 이름에 regression이 들어가지만 **classification을 위한 대표적인 linear classifier** 임.
    * Feature들의 linear combination을 logit으로 사용하고, sigmoid 또는 softmax를 통해 class probability를 추정함.
    * Binary classification에서 class 1의 확률 추정 형태는 다음과 같음.

$$
\hat{p} = P(y=1 \mid \mathbf{x}) = \sigma(\mathbf{w}^{\top}\mathbf{x} + b)
$$

$$
\sigma(z) = \frac{1}{1 + e^{-z}}
$$

* **사용 Class**: `sklearn.linear_model.LogisticRegression`
* **Decision Boundary**: Linear
* **적용 가능한 Task**:
    * Binary / Multi-class classification 직접 지원.
    * Multi-label / Multi-output classification은 wrapper 필요.
* **특징**:
    * Probability output을 제공하여 해석이 비교적 쉬움.
    * L1, L2, ElasticNet regularization 사용 가능.
    * Gradient 기반 solver 사용 시 **feature scaling 중요**.
    * Baseline classifier로 자주 사용됨.

```python
from sklearn.linear_model import LogisticRegression

logistic_classifier = LogisticRegression(
    # sklearn 1.8: penalty 파라미터 deprecated → 1.10에서 제거 예정.
    # 대체 방식 (l1_ratio 기본값은 0.0):
    #   penalty='l2'         → l1_ratio=0.0  (기본값, 생략 가능)
    #   penalty='l1'         → l1_ratio=1.0, solver='saga' 또는 'liblinear'
    #   penalty='elasticnet' → 0 < l1_ratio < 1, solver='saga'
    #   penalty=None         → C=np.inf
    penalty='l2',       # 정칙화 방식 ('l1', 'l2', 'elasticnet', None) — deprecated in 1.8
    C=1.0,              # 정칙화 강도의 역수 (작을수록 강한 정칙화)
    fit_intercept=True, # bias term 사용 여부
    solver='lbfgs',     # 최적화 solver
    max_iter=1000,      # 최대 반복 횟수
    tol=1e-4,           # 수렴 기준 허용 오차
    class_weight=None,  # class imbalance 보정 가중치 ('balanced' 또는 dict)
    random_state=7,
    n_jobs=-1
)
logistic_classifier = logistic_classifier.fit(X_train_scaled, y_train)
```

`penalty`와 `solver`의 대표적인 관계는 다음과 같음.

| `solver` | 사용 가능한 `penalty` | 특징 |
|---|---|---|
| `lbfgs` | `l2`, `None` | 일반적으로 많이 사용 |
| `liblinear` | `l1`, `l2` | 작은 dataset, binary classification에 적합 |
| `sag` | `l2`, `None` | sample 수가 많을 때 유리, scaling 필요 |
| `saga` | `l1`, `l2`, `elasticnet`, `None` | large-scale data, sparse data에 적합 |
| `newton-cg` | `l2`, `None` | 안정적이나 상대적으로 무거울 수 있음 |

> **sklearn 1.8 변경사항**: `penalty` 파라미터가 deprecated 처리됨 (1.10에서 제거 예정).  
> `l1_ratio` 기본값이 `None` → **`0.0`** 으로 변경됨.  
> 향후 권장 방식: `l1_ratio=0.0` (L2), `l1_ratio=1.0` (L1), `0 < l1_ratio < 1` (ElasticNet), `C=np.inf` (penalty 없음).

Multi-class classification에서는 class별 score를 softmax로 확률화함.

$$
P(y=k \mid \mathbf{x}) = \frac{\exp(z_k)}{\sum_{j=1}^{K} \exp(z_j)}
$$

---

### **4-2. Ridge Classifier (릿지 분류기)**

참고: [Ridge](https://dsaint31.tistory.com/947)

* **설명**:
    * Ridge Regression과 유사하게 **L2 Regularization을 사용** 하는 linear classifier.
    * Classification 문제의 label을 내부적으로 변환하여 linear model을 학습하고, decision score가 가장 큰 class를 선택함.
* **사용 Class**: `sklearn.linear_model.RidgeClassifier`
* **Decision Boundary**: Linear
* **적용 가능한 Task**:
    * Binary / Multi-class classification 직접 지원.
    * Multi-label / Multi-output classification은 wrapper 필요.
* **특징**:
    * L2 Regularization을 통해 큰 parameter를 억제함.
    * **`predict_proba()`를 제공하지 않음.**
    * High-dimensional data에서 비교적 안정적으로 동작함.
    * Feature scaling 권장.
    * Probability가 필요하면 `LogisticRegression`, `SVC(probability=True)`, 또는 calibration을 고려해야 함.

```python
from sklearn.linear_model import RidgeClassifier

ridge_classifier = RidgeClassifier(
    alpha=1.0,          # 정칙화 강도 (클수록 강한 정칙화)
    fit_intercept=True, # bias term 사용 여부
    copy_X=True,        # 원본 데이터 복사 여부
    max_iter=None,      # 최대 반복 횟수
    tol=1e-4,           # 수렴 기준 허용 오차
    class_weight=None,  # class imbalance 보정 가중치
    solver='auto',      # 계산 방법 ('auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg' 등)
    positive=False,     # 계수를 양수로 제한할지 여부 (sklearn 1.1 이후 추가)
    random_state=7      # solver가 stochastic한 경우 사용할 난수 seed
)
ridge_classifier = ridge_classifier.fit(X_train_scaled, y_train)
```

---

### **4-3. SGDClassifier**

참고: [linear_model.SGDClassifier](https://ds31x.tistory.com/669)

* **설명**:
    * Stochastic Gradient Descent(SGD)를 사용하여 linear classification 계열 objective function을 iterative하게 최적화하는 classifier.
    * Closed-form solution을 구하지 않고, sample을 하나씩 보면서 gradient를 추정하고 parameter를 update함.
    * `loss` 설정에 따라 Linear SVM, Logistic Regression, Perceptron 등과 유사한 모델을 구성할 수 있음.
* **사용 Class**: `sklearn.linear_model.SGDClassifier`
* **Decision Boundary**: Linear
* **적용 가능한 Task**:
    * Binary / Multi-class classification 직접 지원.
    * Multi-label / Multi-output classification은 wrapper 필요.
* **특징**:
    * Sample 수가 매우 많거나 sparse data에 유리함.
    * **Gradient 기반 최적화이므로 feature scaling 중요.**
    * `partial_fit()`을 통해 **online learning / incremental learning** 에 사용할 수 있음.

`loss` 파라미터별 특성은 다음과 같음.

| `loss` 설정 | 의미 | `predict_proba()` |
|---|---|---:|
| `"hinge"` | Linear SVM | 없음 |
| `"log_loss"` | SGD 기반 Logistic Regression | 있음 |
| `"modified_huber"` | Robust한 margin 기반 classifier | 있음 |
| `"perceptron"` | Perceptron | 없음 |

```python
from sklearn.linear_model import SGDClassifier

sgd_classifier = SGDClassifier(
    loss='log_loss',          # 손실 함수
    penalty='l2',             # 정칙화 방식 ('l2', 'l1', 'elasticnet', None)
    alpha=0.0001,             # 정칙화 강도
    l1_ratio=0.15,            # ElasticNet에서 L1 penalty 비율
    fit_intercept=True,
    max_iter=1000,            # 최대 epoch 수 (parameter update 횟수가 아닌 전체 dataset 반복 횟수)
    tol=0.001,
    shuffle=True,             # 각 epoch마다 sample 순서 섞을지 여부
    random_state=7,
    learning_rate='optimal',  # learning rate schedule ('constant', 'optimal', 'invscaling', 'adaptive')
    eta0=0.01,                # 초기 learning rate. sklearn 1.8부터 반드시 양수여야 함 (기본값 0.01)
                              # learning_rate='optimal' 사용 시 eta0은 실제로 사용되지 않음
    early_stopping=False,
    validation_fraction=0.1,  # early_stopping=True일 때 validation set 비율
    n_iter_no_change=5,       # 개선 없을 때 종료까지 기다릴 epoch 수
    class_weight=None,
    warm_start=False,         # 이전 fit 결과를 다음 fit의 초기값으로 재사용할지 여부
    average=False             # update 과정의 평균 weight 사용 여부
)
sgd_classifier = sgd_classifier.fit(X_train_scaled, y_train)
```

* `fit()`을 다시 호출하면 learning rate 관련 counter가 reset됨.
* `partial_fit()`은 주어진 data subset에 대해 한 epoch의 SGD를 수행하며, 기존 counter를 유지함.
* `warm_start=True`는 재학습 시 초기값을 재사용하는 것이고, `partial_fit()`은 incremental learning에 가까움.

---

### **4-4. Naive Bayes Classifier**

* **설명**:
    * **Bayes theorem** 을 기반으로 class posterior probability를 계산하는 probabilistic classifier.
    * 각 feature가 class 조건부로 서로 독립이라는 **naive assumption** 을 사용함.
    * 이 가정이 현실적으로는 강하지만, text classification 등에서 좋은 baseline으로 사용됨.
* **사용 Class**:
    * `sklearn.naive_bayes.GaussianNB`: continuous feature에 적합
    * `sklearn.naive_bayes.MultinomialNB`: count 기반 feature에 적합
    * `sklearn.naive_bayes.BernoulliNB`: binary feature에 적합
* **Decision Boundary**: 분포 가정에 따라 달라짐. GaussianNB는 class별 Gaussian distribution을 가정하며 quadratic boundary를 가짐. MultinomialNB는 count 기반 feature에 적합함.
* **적용 가능한 Task**:
    * Binary / Multi-class classification 직접 지원.
    * Multi-label / Multi-output classification은 wrapper 필요.
* **특징**:
    * 학습과 예측이 빠름.
    * 복잡한 feature interaction은 잘 반영하지 못함.
    * Text classification에서 `MultinomialNB`가 자주 사용됨.

```python
from sklearn.naive_bayes import GaussianNB

gnb_classifier = GaussianNB(
    priors=None,       # class prior probability (None이면 data에서 추정)
    var_smoothing=1e-9 # 분산 안정화를 위한 smoothing 값
)
gnb_classifier = gnb_classifier.fit(X_train_scaled, y_train)
```

Text count feature 또는 TF-IDF feature를 사용하는 경우 `MultinomialNB`를 사용함.

```python
from sklearn.naive_bayes import MultinomialNB

mnb_classifier = MultinomialNB(
    alpha=1.0,       # Laplace smoothing 강도
    force_alpha=True,
    fit_prior=True,  # class prior 학습 여부
    class_prior=None # 직접 지정할 class prior
)
mnb_classifier = mnb_classifier.fit(X_train_count, y_train)
```

---

### **4-5. Support Vector Classification (SVC)**

* **설명**:
    * Class 사이의 **margin을 최대화** 하는 decision boundary를 찾는 classifier.
    * 이론적 기반은 Vapnik & Chervonenkis(1963)에서 유래하며, kernel trick은 Boser et al.(1992)에 의해 도입되었고, 현재의 soft-margin SVM은 Cortes & Vapnik(1995)에 의해 정립됨.
    * **kernel trick** 을 통해 non-linear decision boundary를 구성할 수 있음.
* **사용 Class**: `sklearn.svm.SVC`, `sklearn.svm.LinearSVC`
* **Decision Boundary**:
    * `kernel='linear'` 또는 `LinearSVC`: Linear
    * `kernel='rbf'`, `kernel='poly'`: Non-linear
* **적용 가능한 Task**:
    * Binary / Multi-class classification 직접 지원.
    * Multi-label / Multi-output classification은 wrapper 필요.
* **특징**:
    * **Feature scaling 필수**.
    * Small to medium size dataset에서 강력한 성능을 보일 수 있음.
    * Kernel 기반 SVC는 sample 수가 많을수록 학습 비용이 커짐.
    * `probability=True`를 설정하면 probability 추정이 가능하지만 추가 비용 발생.
    * Multi-class classification에서 `sklearn.svm.SVC`는 **내부적으로 OvO(One-vs-One) 전략** 으로 학습함.
      `decision_function_shape='ovr'`는 학습 전략을 바꾸는 것이 아니라, decision function의 **출력 형태만** OvR 형태(n_samples, n_classes)로 변환하는 옵션임.

```python
from sklearn.svm import SVC

svc_classifier = SVC(
    C=1.0,                         # regularization parameter (클수록 training error를 줄이려 함)
    kernel='rbf',                  # 커널 유형 ('linear', 'poly', 'rbf', 'sigmoid')
    degree=3,                      # poly 커널의 차수
    gamma='scale',                 # 커널 계수 ('scale', 'auto' 또는 float)
    coef0=0.0,                     # poly/sigmoid 커널의 상수 항
    shrinking=True,                # shrinking heuristic 사용 여부
    probability=False,             # probability estimate 사용 여부 (True이면 내부 CV로 인해 느려짐)
    tol=1e-3,
    cache_size=200,                # 커널 계산 캐시 크기 (MB)
    class_weight=None,
    verbose=False,
    max_iter=-1,                   # 최대 반복 횟수 (-1: 무제한)
    decision_function_shape='ovr', # 출력 형태만 변환 (학습 전략은 항상 OvO)
    random_state=7
)
svc_classifier = svc_classifier.fit(X_train_scaled, y_train)
```

Linear SVM만 필요하다면 `LinearSVC` 또는 `SGDClassifier(loss='hinge')`를 사용할 수 있음.
`LinearSVC`는 multi-class를 **OvR 방식** 으로 학습하며, 대규모 dataset에서 `SVC(kernel='linear')`보다 빠른 경우가 많음.

```python
from sklearn.svm import LinearSVC

linear_svc_clf = LinearSVC(
    penalty='l2',
    loss='squared_hinge',
    C=1.0,
    class_weight=None,
    max_iter=5000,
    random_state=7
)
linear_svc_clf = linear_svc_clf.fit(X_train_scaled, y_train)
```

`SVC`의 kernel별 decision boundary는 다음과 같이 이해할 수 있음.

* `kernel='linear'`: 원래 feature space에서 linear decision boundary를 사용함.
* `kernel='rbf'`: 고차원 feature space로 mapping한 것과 유사한 효과를 통해 non-linear decision boundary를 구성함.

---

### **4-6. Decision Tree Classifier (결정 트리 분류)**

* **설명**:
    * Feature space를 tree 형태로 분할하여 class를 예측하는 classifier. (CART 1984, ID3 1986)
    * 각 node에서 feature와 threshold를 선택하여 impurity를 줄이는 방향으로 분기함.
* **사용 Class**: `sklearn.tree.DecisionTreeClassifier`
* **Decision Boundary**: Non-linear
* **적용 가능한 Task**: Binary / Multi-class / Multi-label / **Multi-output classification 직접 지원** (`MultiOutputClassifier` wrapper 없이 2D target 직접 입력 가능).
* **특징**:
    * **Feature scaling 불필요** (값의 크기가 아닌 threshold 기반 분할이기 때문).
    * Decision rule을 시각화하고 해석하기 쉬움.
    * **Over-fitting 가능성이 매우 높음.**
    * Random Forest, Gradient Boosting 등의 base learner로 자주 사용됨.

```python
from sklearn.tree import DecisionTreeClassifier

tree_classifier = DecisionTreeClassifier(
    criterion='gini',             # 분할 기준 ('gini', 'entropy', 'log_loss')
    splitter='best',              # 분할 방법 ('best': 최적 분할, 'random': 랜덤 분할)
    max_depth=None,               # 트리 최대 깊이 (None이면 제한 없음)
    min_samples_split=2,          # 내부 노드 분할 최소 샘플 수
    min_samples_leaf=1,           # leaf 노드 최소 샘플 수
    min_weight_fraction_leaf=0.0, # leaf 노드 최소 가중치 비율
    max_features=None,            # 분할에 사용할 최대 feature 수
    random_state=7,
    max_leaf_nodes=None,          # 최대 leaf 노드 수
    min_impurity_decrease=0.0,    # 분할에 필요한 최소 불순도 감소
    class_weight=None,
    ccp_alpha=0.0                 # cost-complexity pruning parameter
)
tree_classifier = tree_classifier.fit(X_train, y_train)
```

* `criterion='gini'`: Gini impurity를 줄이는 방향으로 split.
* `criterion='entropy'`: Information gain을 기준으로 split.
* `criterion='log_loss'`: Probabilistic classification 관점의 log loss 기준으로 split. (sklearn 1.2 이후 추가)

---

### **4-7. Random Forest Classifier (랜덤 포레스트 분류)**

* **설명**:
    * 여러 개의 Decision Tree를 **bootstrap sample로 학습** 하고, 각 tree의 예측을 voting으로 결합하는 **bagging 기반 ensemble model**. (Breiman, 2001)
    * [Ho(1995)](https://ieeexplore.ieee.org/document/598994)의 Random Subspace Method와 [Breiman(1996) bagging](https://link.springer.com/article/10.1007/BF00058655)을 결합한 방법임.
    * 각 split에서 전체 feature가 아닌 랜덤 subset만 고려하여 tree 간 다양성(diversity)을 높임.
* **사용 Class**: `sklearn.ensemble.RandomForestClassifier`
* **Decision Boundary**: Non-linear
* **적용 가능한 Task**: Binary / Multi-class / Multi-label / **Multi-output classification 직접 지원**.
* **특징**:
    * 단일 Decision Tree보다 **over-fitting에 강함**.
    * **Feature scaling 불필요**.
    * `feature_importances_`로 impurity 기반 feature importance 확인 가능.
    * `oob_score=True` 사용 시 out-of-bag sample 기반 평가 가능.
    * Class imbalance 시 `class_weight='balanced'` 또는 `'balanced_subsample'` 고려 가능.

```python
from sklearn.ensemble import RandomForestClassifier

forest_classifier = RandomForestClassifier(
    n_estimators=100,             # 생성할 트리의 개수
    criterion='gini',             # 분할 기준 ('gini', 'entropy', 'log_loss')
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    min_weight_fraction_leaf=0.0,
    max_features='sqrt',          # classification에서 권장 설정
    max_leaf_nodes=None,
    min_impurity_decrease=0.0,
    bootstrap=True,               # bootstrap sampling 사용 여부
    oob_score=False,              # OOB 샘플로 성능 평가 여부
    n_jobs=-1,
    random_state=7,
    verbose=0,
    warm_start=False,
    class_weight=None,
    ccp_alpha=0.0,
    max_samples=None              # bootstrap sampling 시 최대 샘플 수/비율
)
forest_classifier = forest_classifier.fit(X_train, y_train)
```

---

### **4-8. Extra Trees Classifier (Extremely Randomized Trees)**

* **설명**:
    * Random Forest와 유사하지만, **split threshold까지 random하게 선택** 하는 ensemble tree classifier.
    * Random Forest보다 더 많은 randomness를 도입하여 tree 간 correlation을 더욱 줄임.
* **사용 Class**: `sklearn.ensemble.ExtraTreesClassifier`
* **Decision Boundary**: Non-linear
* **적용 가능한 Task**: Binary / Multi-class / Multi-label / **Multi-output classification 직접 지원**.
* **특징**:
    * Random Forest보다 bias는 다소 증가할 수 있으나 variance를 더 줄일 수 있음.
    * **Feature scaling 불필요**.
    * Noise가 있는 data에서도 강한 baseline으로 사용 가능.
    * Random Forest와 달리 기본적으로 `bootstrap=False` 임.

```python
from sklearn.ensemble import ExtraTreesClassifier

extra_trees_classifier = ExtraTreesClassifier(
    n_estimators=100,
    criterion='gini',
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    min_weight_fraction_leaf=0.0,
    max_features='sqrt',
    max_leaf_nodes=None,
    min_impurity_decrease=0.0,
    bootstrap=False,              # ET 기본값: False (Random Forest와 다름)
    oob_score=False,              # bootstrap=True일 때만 유효
    n_jobs=-1,
    random_state=7,
    verbose=0,
    warm_start=False,
    class_weight=None,
    ccp_alpha=0.0,
    max_samples=None
)
extra_trees_classifier = extra_trees_classifier.fit(X_train, y_train)
```

---

### **4-9. AdaBoost Classifier**

* **설명**:
    * Weak learner를 순차적으로 학습시키며, **이전 단계에서 잘못 분류한 sample에 더 큰 weight** 를 부여하는 boosting model. (Freund & Schapire, 1995)
* **사용 Class**: `sklearn.ensemble.AdaBoostClassifier`
* **Decision Boundary**: Base estimator에 따라 달라짐 (stump 사용 시 non-linear ensemble)
* **적용 가능한 Task**:
    * Binary / Multi-class classification 직접 지원.
    * Multi-label / Multi-output classification은 wrapper 필요.
* **특징**:
    * Simple weak learner들을 순차적으로 결합함.
    * Noisy data나 outlier에 민감할 수 있음.
    * Base estimator로 depth가 얕은 Decision Tree(stump)가 자주 사용됨.

> scikit-learn 1.4부터 `algorithm='SAMME.R'`이 deprecated 처리되었으며, 1.8부터 `algorithm` 파라미터가 완전히 제거됨. 현재는 `SAMME` 알고리즘만 남아 있음.

```python
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

adaboost_classifier = AdaBoostClassifier(
    estimator=DecisionTreeClassifier(max_depth=1), # weak learner (stump)
    n_estimators=50,   # weak learner 개수 (클수록 모델 복잡도 증가)
    learning_rate=1.0, # 각 learner의 기여도 (낮추면 더 많은 estimator 필요)
    random_state=7
)
adaboost_classifier = adaboost_classifier.fit(X_train, y_train)
```

---

### **4-10. Gradient Boosting Classifier**

* **설명**:
    * 이전 model이 남긴 error를 줄이는 방향으로 weak learner를 순차적으로 추가하는 boosting model.
    * Classification에서는 log loss 등을 최소화하는 방향으로 학습함.
* **사용 Class**: `sklearn.ensemble.GradientBoostingClassifier`
* **Decision Boundary**: Non-linear
* **적용 가능한 Task**:
    * Binary / Multi-class classification 직접 지원.
    * Multi-label / Multi-output classification은 wrapper 필요.
* **특징**:
    * 강력한 성능을 보이는 경우가 많으나 **hyper-parameter에 민감함**.
    * Random Forest보다 학습이 느릴 수 있음.
    * `learning_rate`, `n_estimators`, `max_depth` 조절이 over-fitting 방지에 중요함.

```python
from sklearn.ensemble import GradientBoostingClassifier

gb_classifier = GradientBoostingClassifier(
    loss='log_loss',              # 손실 함수 ('log_loss', 'exponential')
    learning_rate=0.1,
    n_estimators=100,
    subsample=1.0,                # 각 트리 학습에 사용할 sample 비율
    criterion='friedman_mse',     # 트리 분할 기준
    min_samples_split=2,
    min_samples_leaf=1,
    min_weight_fraction_leaf=0.0,
    max_depth=3,
    min_impurity_decrease=0.0,
    init=None,                    # 초기 추정기 (None이면 평균값으로 시작)
    random_state=7,
    max_features=None,
    verbose=0,
    max_leaf_nodes=None,
    warm_start=False,
    validation_fraction=0.1,      # 조기 종료용 validation set 비율
    n_iter_no_change=None,        # 조기 종료 조건 (None이면 비활성)
    tol=1e-4,
    ccp_alpha=0.0
)
gb_classifier = gb_classifier.fit(X_train, y_train)
```

---

### **4-11. HistGradientBoosting Classifier**

* **설명**:
    * **Histogram 기반** Gradient Boosting Classifier.
    * Continuous feature를 binning하여 histogram 형태로 처리함으로써 학습 속도를 높인 boosting model.
* **사용 Class**: `sklearn.ensemble.HistGradientBoostingClassifier`
* **Decision Boundary**: Non-linear
* **적용 가능한 Task**:
    * Binary / Multi-class classification 직접 지원.
    * Multi-label / Multi-output classification은 wrapper 필요.
* **특징**:
    * Large dataset에서 `GradientBoostingClassifier`보다 빠른 경우가 많음.
    * **Missing value를 내부적으로 처리** 할 수 있음.
    * scikit-learn 내부에서 제공하는 고성능 boosting classifier임.
    * Tree 기반 모델이므로 feature scaling 필수는 아님.
    * `categorical_features='from_dtype'`은 sklearn 1.4 이후 추가된 기능임.

```python
from sklearn.ensemble import HistGradientBoostingClassifier

hist_gb_classifier = HistGradientBoostingClassifier(
    loss='log_loss',
    learning_rate=0.1,
    max_iter=100,                       # boosting iteration 수
    max_leaf_nodes=31,                  # 각 트리의 최대 leaf node 수
    max_depth=None,
    min_samples_leaf=20,                # leaf node 최소 sample 수
    l2_regularization=0.0,
    max_features=1.0,                   # 각 트리에서 사용할 feature 비율
    max_bins=255,                       # histogram bin 최대 개수
    categorical_features='from_dtype',  # categorical feature 처리 방식 (sklearn >= 1.4)
    monotonic_cst=None,
    interaction_cst=None,
    warm_start=False,
    early_stopping='auto',
    scoring='loss',
    validation_fraction=0.1,
    n_iter_no_change=10,
    tol=1e-7,
    verbose=0,
    random_state=7,
    class_weight=None
)
hist_gb_classifier = hist_gb_classifier.fit(X_train_scaled, y_train)
```

* Tree 기반 모델이므로 feature scaling 필수는 아님.
* 다만 다른 model과 pipeline으로 같이 비교할 때는 **preprocessing 방식을 통일** 하는 편이 실험 관리에 유리함.

---

### **4-12. XGBoost / LightGBM / CatBoost**

* **설명**:
    * Gradient Boosting을 더 최적화한 고성능 third-party library 기반 classifier.
    * scikit-learn API와 유사한 interface를 제공하므로 scikit-learn workflow와 함께 사용하기 쉬움.
* **사용 Class**:
    * `xgboost.XGBClassifier`: GB 최적화 (2014년 개발, 2016년 KDD 논문 발표)
    * `lightgbm.LGBMClassifier`: 빠른 학습과 낮은 메모리 사용을 목표로 개발 (NeurIPS 2017)
    * `catboost.CatBoostClassifier`: Categorical data를 효율적으로 처리하는 GB (Yandex, 2017)
* **Decision Boundary**: Non-linear
* **적용 가능한 Task**:
    * Binary / Multi-class classification 직접 지원.
    * Multi-label / Multi-output classification은 별도 구성 필요 (label별 모델 또는 wrapper 사용).
* **특징**:
    * Tabular data에서 매우 강력한 성능을 보이는 경우가 많음.
    * Missing value, categorical feature 처리 방식은 library마다 차이가 있음.
    * **Hyper-parameter tuning의 영향이 큼.**
    * Third-party library 설치가 필요함.

---

#### **XGBClassifier**

```python
import xgboost as xgb

xgb_classifier = xgb.XGBClassifier(
    objective='binary:logistic',  # binary: 'binary:logistic', multi-class: 'multi:softprob'
    n_estimators=100,
    learning_rate=0.1,
    max_depth=3,
    min_child_weight=1,           # leaf node 최소 가중치 합
    gamma=0,                      # 분할에 필요한 최소 loss 감소
    subsample=1.0,
    colsample_bytree=1.0,         # 각 트리 학습에 사용할 feature 비율
    reg_alpha=0.0,                # L1 regularization
    reg_lambda=1.0,               # L2 regularization
    booster='gbtree',             # ('gbtree', 'gblinear', 'dart')
    n_jobs=-1,
    random_state=7,
    eval_metric='logloss',    # 평가 metric (binary: 'logloss', multi-class: 'mlogloss')
    verbosity=0               # 출력 수준 (0: silent, 1: warning, 2: info, 3: debug)
)
xgb_classifier = xgb_classifier.fit(X_train, y_train)
```

Multi-class classification에서는 objective를 다음처럼 설정함.

```python
xgb_multi_clf = xgb.XGBClassifier(
    objective='multi:softprob',
    num_class=3,
    eval_metric='mlogloss',
    random_state=7
)
xgb_multi_clf = xgb_multi_clf.fit(X_train, y_train)
```

---

#### **LGBMClassifier**

```python
import lightgbm as lgb

lgb_classifier = lgb.LGBMClassifier(
    boosting_type='gbdt',     # ('gbdt', 'rf', 'dart', 'goss')
    objective='binary',       # binary: 'binary', multi-class: 'multiclass'
    num_leaves=31,            # 트리의 최대 leaf node 수
    max_depth=-1,             # 트리 최대 깊이 (-1: 제한 없음)
    learning_rate=0.1,
    n_estimators=100,
    subsample_for_bin=200000, # feature bin 구성에 사용할 sample 수
    class_weight=None,
    min_split_gain=0.0,
    min_child_weight=1e-3,
    min_child_samples=20,
    subsample=1.0,
    subsample_freq=0,
    colsample_bytree=1.0,
    reg_alpha=0.0,
    reg_lambda=0.0,
    random_state=7,
    n_jobs=-1,
    verbose=-1                # -1: 로그 비활성화, 0: 경고만, 1: 전체 출력
)
lgb_classifier = lgb_classifier.fit(X_train, y_train)
```

Multi-class classification에서는 objective를 다음처럼 설정함.

```python
lgb_multi_clf = lgb.LGBMClassifier(
    objective='multiclass',
    num_class=3,
    random_state=7,
    verbose=-1
)
lgb_multi_clf = lgb_multi_clf.fit(X_train, y_train)
```

---

#### **CatBoostClassifier**

```python
# !pip install -q catboost
from catboost import CatBoostClassifier

catboost_classifier = CatBoostClassifier(
    iterations=1000,           # 부스팅 반복 횟수
    learning_rate=0.1,
    depth=6,
    loss_function='Logloss',   # binary: 'Logloss', multi-class: 'MultiClass'
    eval_metric='Accuracy',
    random_seed=7,             # CatBoost는 random_state가 아닌 random_seed를 사용함
    l2_leaf_reg=3.0,
    bootstrap_type='Bayesian',
    task_type='CPU',           # GPU 사용 시 'GPU'
    verbose=100
)
catboost_classifier = catboost_classifier.fit(X_train, y_train)
```

Multi-class classification에서는 다음처럼 설정함.

```python
cat_multi_clf = CatBoostClassifier(
    loss_function='MultiClass',
    eval_metric='Accuracy',
    random_seed=7,
    verbose=100
)
cat_multi_clf = cat_multi_clf.fit(X_train, y_train)
```

* CatBoost는 **categorical feature를 직접 처리** 할 수 있다는 점이 큰 장점임.
* Categorical feature 지정 방식은 scikit-learn 기본 estimator와 다름.

---

## **5. Linear vs Non-linear Classifier 정리**

| Model | Linear / Non-linear | Feature Scaling | Probability 출력 | 주요 특징 |
|---|---|---:|---:|---|
| Logistic Regression | Linear | 높음 | 가능 | 해석 쉬움, baseline으로 좋음 |
| Ridge Classifier | Linear | 권장 | 불가 | probability 출력 없음, 빠른 학습 |
| LinearSVC | Linear | 높음 | 불가 (기본) | margin 기반, OvR 방식 multi-class |
| SGDClassifier | Linear | 높음 | loss에 따라 가능 | large-scale, sparse data에 적합 |
| Naive Bayes | Probabilistic | 낮음~중간 | 가능 | 빠르고 text data에 강함 |
| KNN | Non-linear | 높음 | 가능 | instance based, prediction cost 큼 |
| SVC (RBF) | Non-linear | 높음 | 옵션 필요 | 강력하지만 large data에 부담 |
| Decision Tree | Non-linear | 불필요 | 가능 | 해석 쉬우나 over-fitting 위험 |
| Random Forest | Non-linear | 불필요 | 가능 | 안정적, tabular baseline으로 강함 |
| Extra Trees | Non-linear | 불필요 | 가능 | RF보다 randomness 높음 |
| AdaBoost | Non-linear | 낮음~중간 | 가능 | outlier에 민감할 수 있음 |
| Gradient Boosting | Non-linear | 불필요 | 가능 | 성능 좋지만 tuning 중요 |
| HistGradientBoosting | Non-linear | 불필요 | 가능 | 대규모 data에 빠름, missing value 처리 |
| XGBoost / LightGBM / CatBoost | Non-linear | 불필요 | 가능 | tabular data에서 강력함 |

---

## **6. Binary / Multi-class / Multi-label 지원 정리**

| Model | Binary | Multi-class | Multi-label | Multi-output | 비고 |
|---|---:|---:|---:|---:|---|
| Logistic Regression | 직접 | 직접 | Wrapper 필요 | Wrapper 필요 | `OneVsRestClassifier`로 Binary Relevance 구현 가능 |
| Ridge Classifier | 직접 | 직접 | Wrapper 필요 | Wrapper 필요 | probability 출력 불가 |
| SGDClassifier | 직접 | 직접 | Wrapper 필요 | Wrapper 필요 | large-scale sparse data에 적합 |
| Naive Bayes | 직접 | 직접 | Wrapper 필요 | Wrapper 필요 | text classification에 자주 사용 |
| KNN | 직접 | 직접 | 직접 | Wrapper 필요 | multi-label target 직접 지원 가능 |
| SVC | 직접 | 직접 (OvO) | Wrapper 필요 | Wrapper 필요 | multi-class는 내부적으로 OvO 기반 |
| LinearSVC | 직접 | 직접 (OvR) | Wrapper 필요 | Wrapper 필요 | probability 출력 기본 불가 |
| Decision Tree | 직접 | 직접 | **직접** | **직접** | multi-output / multi-label 직접 처리 가능 |
| Random Forest | 직접 | 직접 | **직접** | **직접** | multi-output / multi-label 직접 처리 가능 |
| Extra Trees | 직접 | 직접 | **직접** | **직접** | multi-output / multi-label 직접 처리 가능 |
| AdaBoost | 직접 | 직접 (SAMME) | Wrapper 필요 | Wrapper 필요 | sklearn 1.8 이후 SAMME만 남음 |
| Gradient Boosting | 직접 | 직접 | Wrapper 필요 | Wrapper 필요 | multi-label은 label별 모델 또는 wrapper 사용 |
| HistGradientBoosting | 직접 | 직접 | Wrapper 필요 | Wrapper 필요 | missing value 내부 처리 가능 |
| XGBoost / LightGBM / CatBoost | 직접 | 직접 | 별도 구성 필요 | 별도 구성 필요 | multi-label은 보통 label별 모델 또는 wrapper 사용 |

---

## **7. 주의사항 및 모델 선택 가이드**

* **Logistic Regression을 baseline** 으로 먼저 사용함.
    * Linear separability 여부를 확인할 수 있음.
    * Feature scaling 필요.
    * Coefficient 해석 가능.
* **Feature interaction이나 non-linear relation이 강하면 tree 계열** 을 사용함.
    * Decision Tree: 해석 / 개념 설명용.
    * Random Forest: 안정적인 tabular baseline.
    * Gradient Boosting 계열 (GBM / XGBoost / LightGBM / CatBoost): 성능 최적화용.
* **Sample 수가 매우 많고 sparse feature가 많으면 `SGDClassifier`** 를 고려함.
    * Text classification, high-dimensional sparse data에 적합.
* **Dataset이 작거나 중간 규모이고 margin 기반 classifier가 적합하다면 `SVC`** 를 고려함.
    * Feature scaling 필수.
    * RBF kernel은 non-linear boundary를 만들 수 있음.
* **Multi-class classification** 에서는 다음을 확인함.
    * 모델이 multi-class를 직접 지원하는지 확인.
    * 필요하면 One-vs-Rest 또는 One-vs-One 사용.
    * `SVC`의 경우 학습은 항상 OvO, `LinearSVC`는 OvR 방식임.
* **Multi-label classification** 에서는 다음을 확인함.
    * 가장 기본적인 방법은 **Binary Relevance** (`OneVsRestClassifier` 활용).
    * Label dependency가 중요하면 **Classifier Chain** 고려.
    * Label별 threshold tuning 필요.
