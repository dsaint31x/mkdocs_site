---
title: MLPRegressor
tags:
  - MLPRegressor
  - multilayer-perceptron
  - mlp
  - ann
  - regression
  - scikit-learn
  - neural network
  - hidden layer
  - activation-function
  - solver
  - early-stopping
  - loss-curve
  - regularization
  - hyperparameter
---

# MLPRegressor

`MLPRegressor`는 scikit-learn에서 제공하는
Multi-Layer Perceptron 기반의 regression model임.

즉, ANN(Artificial Neural Network)을 이용하여
연속값 target을 예측하는 regressor임.

입력 data는 다음 형태를 가짐.

```text
X.shape = (n_samples, n_features)
```

즉, 각 sample이
고정 길이의 feature vector로 표현되어야 함.

`MLPRegressor`는 다음과 같은 data에 사용함.

* 수치 feature 기반 data
* encoding이 끝난 categorical feature 포함 data
* feature extraction이 끝난 vector data
* 일반적인 tabular data

대표적인 regression 문제는 다음과 같음.

* 의료 비용 예측
* 주택 가격 예측
* 체지방률 예측
* 온도 예측
* 수요량 예측
* 점수 예측

주의할 점:

* raw image를 직접 처리하는 model은 아님.
* raw text를 직접 처리하는 model은 아님.
* raw audio를 직접 처리하는 model은 아님.
* 각 sample이 feature vector로 정리되어 있어야 함.

즉, `MLPRegressor`는
feature vector를 입력으로 받는 ANN 기반 regression model임.

---

---

## 기본 사용법

`MLPRegressor`는 scikit-learn의 estimator임.

따라서 기본 사용 흐름은 다른 regression model과 같음.

```text
model 생성
→ fit()
→ predict()
```

가장 기본적인 사용법은 다음과 같음.

```python
from sklearn.neural_network import MLPRegressor

model = MLPRegressor(
    hidden_layer_sizes=(100,),
    activation="relu",
    solver="adam",
    max_iter=200,
    random_state=42,
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
```

`fit()`은 model을 학습시킴.

```python
model.fit(X_train, y_train)
```

`predict()`는 학습된 model로 예측값을 계산함.

```python
y_pred = model.predict(X_test)
```

---

---

## Scaling과 함께 사용하는 경우

`MLPRegressor`는 gradient 기반으로 weight를 학습함.

이런 구조 때문에 feature 간 scale 차이가 크면
학습이 비효율적으로 진행되기 쉬움.

그래서 scikit-learn의 `MLPRegressor`를 사용할 때는
feature scaling을 같이 사용하는 경우가 많음.

대표적으로 `StandardScaler`를 함께 사용함.

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor

model = Pipeline(
    steps=[
        ("scaler", StandardScaler()),
        (
            "mlp",
            MLPRegressor(
                hidden_layer_sizes=(100,),
                activation="relu",
                solver="adam",
                max_iter=200,
                random_state=42,
            ),
        ),
    ]
)
```

다만 주의할 점이 있음.

feature scaling이
모든 ANN에서 항상 절대적으로 요구되는 것은 아님.

다음 조건이 갖추어진 deep learning 환경에서는
scale 문제의 영향이 줄어들 수 있음.

* 충분한 data
* 적절한 network 구조
* normalization 기법
* 적절한 optimizer 설정

하지만 scikit-learn의 `MLPRegressor`는
이런 보정 장치가 따로 내장되어 있지 않은,
비교적 단순한 MLP estimator임.

따라서 일반적으로는
`StandardScaler`와 함께 사용하는 편이 안정적임.

---

---

## Signature

최신 scikit-learn 기준
`MLPRegressor`의 주요 signature는 다음과 같음.

```python
MLPRegressor(
    loss="squared_error",
    hidden_layer_sizes=(100,),
    activation="relu",
    *,
    solver="adam",
    alpha=0.0001,
    batch_size="auto",
    learning_rate="constant",
    learning_rate_init=0.001,
    power_t=0.5,
    max_iter=200,
    shuffle=True,
    random_state=None,
    tol=0.0001,
    verbose=False,
    warm_start=False,
    momentum=0.9,
    nesterovs_momentum=True,
    early_stopping=False,
    validation_fraction=0.1,
    beta_1=0.9,
    beta_2=0.999,
    epsilon=1e-08,
    n_iter_no_change=10,
    max_fun=15000,
)
```

이 중 `loss` parameter는 scikit-learn 1.7에서 새로 추가됨.

선택 가능한 값:

* `"squared_error"`
* `"poisson"`

scikit-learn 1.7 미만 버전에는 `loss` parameter 자체가 존재하지 않으므로,
구버전 환경에서 이 parameter를 지정하면 `TypeError`가 발생함.

따라서 코드를 실행하기 전에
현재 사용 중인 버전을 먼저 확인해두는 것이 안전함.

```python
import sklearn
print(sklearn.__version__)
```

---

## 주요 parameter 정리

| parameter             | 기본값               | 선택 가능한 값 또는 형태                                 | 의미                                                                |
| --------------------- | ----------------- | ---------------------------------------------- | ----------------------------------------------------------------- |
| `loss`                | `"squared_error"` | `"squared_error"`, `"poisson"`                 | 학습에 사용할 loss function (scikit-learn 1.7 이상에서만 지정 가능)             |
| `hidden_layer_sizes`  | `(100,)`          | tuple 또는 list                                  | hidden layer의 개수와 각 layer의 neuron 수                               |
| `activation`          | `"relu"`          | `"identity"`, `"logistic"`, `"tanh"`, `"relu"` | hidden layer의 activation function                                 |
| `solver`              | `"adam"`          | `"lbfgs"`, `"sgd"`, `"adam"`                   | weight 최적화 방법                                                     |
| `alpha`               | `0.0001`          | float                                          | L2 regularization 강도                                              |
| `batch_size`          | `"auto"`          | `"auto"` 또는 int                                | mini-batch 크기 (`"auto"`이면 `min(200, n_samples)`)                  |
| `learning_rate`       | `"constant"`      | `"constant"`, `"invscaling"`, `"adaptive"`     | learning rate 변화 방식                                               |
| `learning_rate_init`  | `0.001`           | float                                          | 초기 learning rate                                                  |
| `power_t`             | `0.5`             | float                                          | `invscaling`에서 사용하는 지수                                            |
| `max_iter`            | `200`             | int                                            | 최대 반복 횟수                                                          |
| `shuffle`             | `True`            | bool                                           | 각 epoch마다 training sample 순서를 섞을지 여부 (validation set은 다시 분리되지 않음) |
| `random_state`        | `None`            | int 또는 None                                    | 난수 고정 (설정하면 early stopping 시 분리되는 validation set도 동일하게 유지됨)       |
| `tol`                 | `0.0001`          | float                                          | 학습 종료 판단 기준                                                       |
| `verbose`             | `False`           | bool                                           | 학습 과정 출력 여부                                                       |
| `warm_start`          | `False`           | bool                                           | 이전 학습 결과를 이어서 사용할지 여부                                             |
| `momentum`            | `0.9`             | float                                          | SGD에서 사용하는 momentum                                               |
| `nesterovs_momentum`  | `True`            | bool                                           | SGD에서 Nesterov momentum 사용 여부                                     |
| `early_stopping`      | `False`           | bool                                           | validation score가 개선되지 않으면 조기 종료할지 여부                             |
| `validation_fraction` | `0.1`             | float                                          | validation set 비율                                                 |
| `beta_1`              | `0.9`             | float                                          | Adam의 1차 moment decay rate                                        |
| `beta_2`              | `0.999`           | float                                          | Adam의 2차 moment decay rate                                        |
| `epsilon`             | `1e-08`           | float                                          | Adam의 수치 안정성용 값                                                   |
| `n_iter_no_change`    | `10`              | int                                            | 개선이 없다고 판단하기 전까지 기다리는 epoch 수                                     |
| `max_fun`             | `15000`           | int                                            | `lbfgs`에서 사용할 최대 function call 수                                  |

표에 있는 parameter가 많지만,
실제로 자주 손대는 항목은 일부로 한정됨.

이어지는 절에서는

* 구조를 결정하는 `hidden_layer_sizes`,
* 비선형성을 부여하는 `activation`,
* 그리고 학습 자체를 좌우하는 `loss`, `solver`, `alpha`, `learning_rate_init`,
`max_iter`, `early_stopping` 순서로 살펴봄.

---

---

## hidden_layer_sizes

`hidden_layer_sizes`는 hidden layer의 구조를 지정하는 parameter임.

```python
hidden_layer_sizes=(100,)
```

위 설정의 의미:

```text
hidden layer 1개
neuron 수 100개
```

구조는 다음과 같음.

```text
input
→ hidden layer: 100 neurons
→ output
```

다음 설정은 hidden layer 2개를 의미함.

```python
hidden_layer_sizes=(128, 64)
```

구조는 다음과 같음.

```text
input
→ hidden layer: 128 neurons
→ hidden layer: 64 neurons
→ output
```

즉, `hidden_layer_sizes=(128, 64)`는 다음을 의미함.

* 첫 번째 hidden layer: 128 neurons
* 두 번째 hidden layer: 64 neurons

주의할 점:

* input layer는 직접 지정하지 않음.
* input layer의 크기는 feature 개수로 자동 결정됨.
* output layer도 target 형태에 따라 자동 결정됨.
* layer 수를 말할 때 input layer 포함 여부는 문맥에 따라 다름.

가장 명확한 표현:

```text
hidden layer가 2개인 MLP
```

hidden layer 구조를 정했다면,
다음으로 결정해야 하는 것은 각 hidden layer에 적용할 activation function임.

---

## activation

`activation`은 ***hidden layer에서 사용할 activation function을 지정*** 함.

```python
activation="relu"
```

선택 가능한 값은 다음과 같음.

| 값            | 의미                    |
| ------------ | --------------------- |
| `"identity"` | (f(x) = x)            |
| `"logistic"` | sigmoid function      |
| `"tanh"`     | hyperbolic tangent    |
| `"relu"`     | rectified linear unit |

기본값은 `"relu"`임.

주의할 점:

* `activation`은 hidden layer에 적용됨.
* ***output layer의 activation function을 지정하는 parameter가 아님.***
* 일반적인 regression에서 output layer는 identity function으로 볼 수 있음.
* 따라서 출력값이 특정 범위로 제한되지 않음.

예를 들어 다음 설정을 사용해도,

```python
activation="relu"
```

최종 예측값이 반드시 0 이상으로 제한되는 것은 아님.

출력값 범위를 제한해야 하는 경우에는
다른 처리가 필요함.

예:

* target transformation
* 예측값 후처리
* PyTorch/TensorFlow에서 output layer 직접 설계

이처럼 output layer의 형태는 `activation`이 아니라
다음에 다룰 `loss` 선택에 따라 달라짐.

---

---

## loss

`loss`는 학습에 사용할 loss function을 지정함.

```python
loss="squared_error"
```

선택 가능한 값은 다음과 같음.

| 값                 | 의미                                                   |
| ----------------- | ---------------------------------------------------- |
| `"squared_error"` | 일반적인 regression에서 사용하는 squared error 계열 loss         |
| `"poisson"`       | (y \ge 0)인 target에 사용할 수 있는 Poisson deviance 계열 loss |

앞서 signature에서 언급했듯
`loss` parameter 자체는 scikit-learn 1.7부터 사용 가능함.

일반적인 연속값 regression에서는 다음을 사용함.

```python
loss="squared_error"
```

이 경우 output layer는 identity function으로 볼 수 있음.

target이 count data이거나
음수가 될 수 없는 양수 target이라면
다음 설정을 고려할 수 있음.

```python
loss="poisson"
```

`loss="poisson"` 을 사용할 때 target $y$ 가 0 이상이어야 함.

* `loss="poisson"`에서는 내부적으로 log-link를 사용함.
* 즉, output activation 관점에서는 exponential function이 사용되는 것으로 볼 수 있음.
* 단, 사용자가 output activation을 직접 선택하는 것을 의미하진 않음.
* `loss` 선택에 따라 정해진 출력 처리 방식이 함께 사용되는 것으로 이해할 것.

loss function을 정했다면,  
그 다음 결정할 것은 이 loss를 어떤 방식으로 최적화할지,  
즉 `solver`임.

---

## solver

`solver`는 weight를 최적화하는 방법을 지정함.

| 값         | 의미                          |
| --------- | --------------------------- |
| `"adam"`  | Adam optimizer              |
| `"sgd"`   | stochastic gradient descent |
| `"lbfgs"` | quasi-Newton 계열 optimizer   |

일반적인 경우에는 기본값인 `"adam"`을 많이 사용함.

```python
solver="adam"
```

`solver="adam"`의 특징:

* mini-batch 기반 학습
* adaptive learning rate 계열 optimizer
* 일반적인 설정에서 무난함

`solver="sgd"`의 특징:

* mini-batch 기반 학습
* learning rate 설정의 영향이 큼
* momentum 사용 가능

`solver="lbfgs"`의 특징:

* quasi-Newton 계열 최적화
* mini-batch를 사용하지 않음
* 작은 dataset에서 좋은 결과를 보일 수 있음
* `batch_size`, `learning_rate`, `momentum`과 직접 관련이 약함

세 solver 모두 결과적으로 weight를 갱신하지만,  
갱신 폭을 결정하는 방식은 서로 다름.

이 폭을 직접 제어하는 parameter가  
다음에 다룰 `learning_rate_init`임.

---

## learning_rate_init

`learning_rate_init`은 초기 learning rate를 의미함.

```python
learning_rate_init=0.001
```

사용되는 solver:

* `solver="sgd"`
* `solver="adam"`

의미:

* weight update의 초기 step size
* 너무 작으면 학습이 느려질 수 있음.
* 너무 크면 loss가 불안정하거나 발산할 수 있음.

`solver="lbfgs"`에서는 사용되지 않음.

이유:

* `lbfgs`는 quasi-Newton 계열 최적화 방법임.
* gradient와 Hessian 근사를 이용하여 step size가 결정됨.
* 이동 방향과 step size를 내부적으로 결정함.

---

---

## learning_rate

`learning_rate`는 learning rate 변화 방식을 지정함.

단, `solver="sgd"`에서만 사용됨.

| 값              | 의미                                |
| -------------- | --------------------------------- |
| `"constant"`   | learning rate를 일정하게 유지            |
| `"invscaling"` | iteration이 진행될수록 learning rate 감소 |
| `"adaptive"`   | 개선이 없으면 learning rate를 줄임         |

기본값:

```python
learning_rate="constant"
```

주의할 점:

* `solver="adam"`에서는 직접 신경 쓰지 않아도 됨 (적응형임).
* `solver="lbfgs"`에서는 아예 사용되지 않음.

learning rate를 정했다면,
이제 학습을 언제 멈출지, 그리고 model이 지나치게 복잡해지지 않도록
어떻게 제어할지를 정해야 함.
차례로 `max_iter`, `alpha`, `early_stopping`을 다룸.

---

## max_iter

`max_iter`는 최대 반복 횟수를 의미함.

```python
max_iter=200
```

`solver="sgd"` 또는 `solver="adam"`에서는  
전체 training data를 반복해서 보는 최대 횟수에 가까운 의미임.

학습이 충분히 수렴하지 않으면  
`ConvergenceWarning`이 발생할 수 있음.

이 경우 다음처럼 값을 늘릴 수 있음.

```python
max_iter=1000
```

주의할 점:

* 무조건 크게 잡는 것이 좋은 것은 아님.
* 학습 시간이 증가함.
* overfitting 가능성도 증가할 수 있음.

`max_iter`는 학습을 멈추는 가장 단순한 기준,  
즉 ***정해진 횟수에 도달하면 멈춘다*** 는 기준임.

---

---

## alpha

`alpha`는 L2 regularization 강도를 의미함.

```python
alpha=0.0001
```

역할:

* weight가 지나치게 커지는 것을 억제함.
* overfitting을 줄이는 데 사용할 수 있음.
* 값이 커질수록 model이 더 단순해지는 방향으로 학습됨.

예:

```python
alpha=0.001
```

주의할 점:

* 너무 작으면 regularization 효과가 약함.
* 너무 크면 underfitting이 발생할 수 있음.

`alpha`는 weight 크기를 직접 제약해서  
model이 단순한 방향으로 학습되도록 만드는 장치임.

반면 `early_stopping`은 weight 자체를 제약하는 대신  
학습을 멈추는 시점을 조절해서 비슷한 효과,  
즉 overfitting 억제를 얻는 방법임.

---

## early_stopping

`early_stopping`은 조기 종료 기능임.

```python
early_stopping=True
```

의미:

* training data 일부를 validation set으로 분리함.  
* validation score가 더 이상 좋아지지 않으면 학습을 멈춤.  

validation set 비율은 `validation_fraction`으로 지정함.

```python
validation_fraction=0.1
```

* 위 설정의 의미는 
* training data의 10%를 validation set으로 사용


조기 종료 판단에 관여하는 parameter는 다음임.

```python
tol=0.0001
n_iter_no_change=10
```

의미:

* validation score가 `tol` 이상 개선되지 않음.
* 이 상태가 `n_iter_no_change`번 지속됨.
* 그러면 학습 종료.

참고로, 학습 후에는 `loss_curve_`를 확인할 수 있음.

```python
model.loss_curve_
```

`loss_curve_`는 각 iteration에서의 training loss 값을 저장한 list임.

주의할 점:

* `early_stopping=False`인 경우에는 training loss를 기준으로 수렴 여부를 판단함.
* `early_stopping=True`인 경우에는 training loss는 계속 계산되지만, 조기 종료 여부는 validation score를 기준으로 판단함.
* scikit-learn의 `MLPRegressor`는 early stopping에 사용할 평가 지표를 사용자가 별도로 지정할 수 없음.
* regression에서는 내부적으로 validation set에 대한 $R^2$ score를 사용하여 개선 여부를 판단함.
* 즉, `loss_curve_`에 저장되는 training loss와 early stopping에 사용되는 validation score는 서로 다른 값임.
* 따라서 training loss가 계속 감소하더라도 validation score가 개선되지 않으면 학습이 종료될 수 있음.
* 반대로 training loss가 일시적으로 증가하더라도 validation score가 개선되면 학습이 계속될 수 있음.

여기까지가 학습을 직접 제어하는 parameter들이고,
이제부터는 `MLPRegressor` 구조 자체가 가지는 근본적인 한계를 살펴봄.

---

## 적은 dataset에서의 한계

`MLPRegressor`의 한계는
tabular data 자체 때문이 아님.

핵심은 다음임.

```text
sample 수 대비 parameter 수
```

`MLPRegressor`는 dense layer 기반 model임.

Dense layer의 특징:

* 이전 layer의 모든 neuron이 다음 layer의 모든 neuron과 연결됨.
* hidden layer가 커질수록 parameter 수가 빠르게 증가함.
* feature interaction과 non-linear relationship을 표현할 수 있음.
* 다만 그 관계를 안정적으로 학습하려면 충분한 sample이 필요함.

이로 인한 한계는 다음과 같음:

* 다른 단순 regression model보다 parameter 수가 많아지기 쉬움.
* 따라서 sample 수가 적으면 일반화 성능이 불안정할 수 있음.


이를 숫자로 확인해보면 다음과 같음.

예를 들어 input feature가 20개이고
hidden layer를 다음과 같이 지정했다고 하자.

```python
hidden_layer_sizes=(128, 64)
```

주요 weight 수는 다음과 같음.

```text
input → hidden1 : 20 × 128 = 2560
hidden1 → hidden2 : 128 × 64 = 8192
hidden2 → output : 64 × 1 = 64
```

bias까지 포함하면 parameter 수는 더 늘어남.

> 즉, 비교적 단순해 보이는 MLP도  
> 학습해야 할 parameter가 쉽게 수천 개 이상이 됨.

sample 수가 충분하면 문제되지 않을 수 있음.

하지만 sample 수가 적으면 다음 문제가 생기기 쉬움.

* parameter를 안정적으로 추정하기 어려움.
* training data에 과하게 맞을 수 있음.
* overfitting 가능성이 증가함.
* hidden layer 구조에 따라 성능이 크게 달라질 수 있음.
* learning rate 설정에 민감해질 수 있음.
* regularization 설정에 민감해질 수 있음.
* validation split에 따른 평가 변동이 커질 수 있음.

정리하면 다음과 같음.


> MLPRegressor는 tabular regression에서 특별히 불리한 model은 아님.
>
> 다만 sample 수가 적은 dataset에서는  
> 다른 단순 regression model보다 불리할 수 있음.
>
> 이유는 dense layer 구조상  
> sample 수에 비해 학습해야 할 parameter가 많아지기 쉽기 때문임.


따라서 작은 dataset에서는  
다른 regression model과 성능을 비교하는 것이 좋음.

비교 대상 예:

* `LinearRegression`
* `Ridge`
* `RandomForestRegressor`
* `GradientBoostingRegressor`
* `HistGradientBoostingRegressor`

위 model들은 

* 작은 dataset에서는
* 학습해야 할 자유도와 sample 수의 균형이
* MLP보다 더 잘 맞는 경우가 많음.

---

---

## fit 후 확인 가능한 attribute

지금까지는 `fit()` 이전에 지정하는 parameter들을 다뤘음.

`fit()`이 끝난 뒤에는 학습 결과를 직접 들여다볼 수 있는
attribute들이 model object에 채워짐.

* `fit()`이 끝나면 `model`에는 학습 과정과 결과를 담은 여러 attribute가 추가됨.
* 이름 끝에 `_`가 붙어 있는 것이 특징
* 이는 scikit-learn에서 "학습을 마쳐야 채워지는 값"이라는 관례적 표시임.

### 학습된 weight 자체

| attribute     | 의미                                                       |
| ------------- | -------------------------------------------------------- |
| `coefs_`      | layer 사이 weight matrix 목록. `coefs_[i]`는 layer i와 i+1 사이 weight |
| `intercepts_` | layer별 bias vector 목록. `intercepts_[i]`는 layer i+1의 bias  |

즉 `coefs_`와 `intercepts_`를 합치면 학습된 network 전체를 그대로 복원할 수 있음.

### network 구조 정보

| attribute          | 의미                                              |
| ------------------ | ----------------------------------------------- |
| `n_layers_`         | input, hidden, output을 모두 포함한 layer 개수          |
| `n_outputs_`        | output 개수 (일반적인 single-target regression이면 1)   |
| `out_activation_`   | output layer의 activation function 이름 (`MLPRegressor`는 `"identity"`) |
| `n_features_in_`    | `fit()` 시점에 입력으로 사용된 feature 개수                  |

* `out_activation_`이 `"identity"`라는 점은 앞서 `activation` 절에서 설명한 내용임.
* output layer에는 별도의 activation function이 적용되지 않는다는 사실을 모델 객체의 attribute 값으로도 직접 확인할 수 있다는 의미임.

### 학습 진행 상황

| attribute     | 의미                                                  |
| ------------- | --------------------------------------------------- |
| `n_iter_`     | solver가 실제로 수행한 iteration(epoch) 수                  |
| `loss_`       | 학습 종료 시점의 loss 값                                    |
| `loss_curve_` | 각 iteration에서의 training loss를 모아 둔 list             |

* `loss_curve_`는 앞서 `early_stopping` 절에서 다룬 것과 동일한 attribute임.
* `solver="lbfgs"`에서는 `loss_curve_`가 생성되지 않음.
* `solver="sgd"` 또는 `"adam"`에서만 제대로 생성됨.

### early stopping 관련 attribute

`early_stopping=True`로 학습한 경우에는  
다음 attribute도 함께 확인할 수 있음.

| attribute                  | 의미                                                  |
| --------------------------- | --------------------------------------------------- |
| `validation_scores_`        | 각 iteration에서의 validation set (R^2) score를 모아 둔 list |
| `best_validation_score_`    | early stopping을 발생시킨, 가장 좋았던 validation score      |

* 이 두 attribute는 `early_stopping=True`일 때만 값이 채워짐.
* `early_stopping=False`인 경우에는 `None`이며,
* 대신 `best_loss_`(training loss 기준 최솟값)를 확인하게 됨.


`loss_curve_`와 `best_loss_`는 training loss 쪽 지표이고,  
`validation_scores_`와 `best_validation_score_`는 validation score 쪽 지표라는 점을 주의할 것.

---

---

## 실제 예제

아래는 `MLPRegressor`를 사용하는 기본 예제임.

```python
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


dataset = fetch_california_housing(as_frame=True)

X = dataset.data
y = dataset.target


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)


model = Pipeline(
    steps=[
        ("scaler", StandardScaler()),
        (
            "mlp",
            MLPRegressor(
                hidden_layer_sizes=(128, 64),
                activation="relu",
                solver="adam",
                alpha=0.001,
                learning_rate_init=0.001,
                max_iter=1000,
                early_stopping=True,
                validation_fraction=0.1,
                n_iter_no_change=20,
                random_state=42,
            ),
        ),
    ]
)


model.fit(X_train, y_train)

y_pred = model.predict(X_test)


mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MSE : {mse:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"MAE : {mae:.4f}")
print(f"R^2 : {r2:.4f}")
```

이 예제에서 `hidden_layer_sizes=(128, 64)`는 hidden layer 구조를,
`alpha`와 `early_stopping` 조합은 overfitting 억제를,
`StandardScaler`는 학습 안정성을 각각 담당함.

---

---

## 정리

`MLPRegressor`는
scikit-learn에서 ANN 기반 regression을 수행하기 위한 model임.

입력은 다음 형태를 가짐.

```text
X.shape = (n_samples, n_features)
```

즉, 각 sample이 fixed-length feature vector로 표현되어야 함.

핵심 사용 흐름은 다음과 같음:

1. feature 준비
2. 필요하면 scaling
3. `MLPRegressor` 생성
4. fit()
5. predict()
6. regression metric 평가

중요한 parameter:

* `hidden_layer_sizes`
* `activation`
* `solver`
* `alpha`
* `learning_rate_init`
* `max_iter`
* `early_stopping`
* `loss` (scikit-learn 1.7 이상)

`MLPRegressor`는 다음 목적에 적절함.

* ANN 기반 regression 구조 이해
* hidden layer 구조 실험
* activation function 비교
* learning rate 영향 확인
* regularization 영향 확인
* scikit-learn pipeline 실습

**주의할 점**

MLPRegressor의 한계는 parameter의 수가 많기 때문에 많은 sample이 필요하다는 점임.

* sample 수가 충분하면 사용할 수 있지만,
* sample 수가 적으면 parameter 수 때문에 일반화 성능이 불안정할 수 있음.

---

---

## 참고: MLPClassifier

`MLPClassifier`는 

* `MLPRegressor`와 같은 Multi-Layer Perceptron 구조를 사용하지만,
* 연속값이 아니라 class label을 예측하는 classification model임.

> 즉, regression 문제에는 `MLPRegressor`를 사용하고,  
> classification 문제에는 `MLPClassifier`를 사용함.

참고로, 

* `MLPClassifier`에서도 `activation` parameter는 hidden layer의 activation function을 지정함.
* output layer의 activation function을 직접 지정하는 parameter는 아니며, classification 문제 유형에 따라 내부적으로 결정됨.

`MLPClassifier`에서 task에 따른 output activation과 loss는 다음처럼 정리할 수 있음.

| task                       | output activation | loss               | 출력 의미                          |
| -------------------------- | ----------------- | ------------------ | ------------------------------ |
| binary classification      | logistic func.  | binary cross-entropy loss<br/>negative log-likelihood<br/>`log_loss`라고도 불림. | positive class에 속할 probability |
| multi-class classification | softmax           | categorical cross-entropy loss<br/>negative log-likelihood<br/>`log_loss`라고도 불림. | 각 class에 속할 probability        |
| multi-label classification | logistic func.  | label-wise binary cross-entropy loss | 각 label이 1일 probability        |

