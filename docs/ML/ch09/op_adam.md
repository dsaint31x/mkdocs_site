# Adamptive Moment Estimation (Adam)

`RMSProp` (adaiptive learning rate)과 Momentum기법(update방향 변경)을 합친 optimizer.

많은 variants를 가지고 있으며, 가장 많이 사용되는 gradient 기반의 optimizer임.

## Adam 알고리즘.

1. $\textbf{m}\leftarrow \beta_1 \textbf{m} - (1-\beta_1) \nabla_\theta J(\theta)$
2. $\textbf{s} \leftarrow \beta_2 \textbf{s}+(1-\beta_2)\nabla_\theta J(\theta) \otimes \nabla_\theta J(\theta)$
3. $\hat{\textbf{m}}\leftarrow \frac{\textbf{m}}{1-{\beta_1}^t}$
4. $\hat{\textbf{s}}\leftarrow \frac{\textbf{s}}{1-{\beta_2}^t}$
5. $\theta \leftarrow \theta + \eta \hat{\textbf{m}} \oslash \sqrt {\textbf{s}+\epsilon}$

* 위에서 $t$는 iteration number이며 1부터 시작함.
* 1,2,5번은 사실 `momentum`과 `RMSProp`를 조합한 알고리즘임을 보여줌.
* 1번의 $\beta_1$은 `momentum`의 $\gamma$ 에 대응 (단, 여기선 exponentially decaying average를 이용함. $\beta, (1-\beta)$를 계수로 사용.)
    * $\gamma=\frac{\beta_1}{1-\beta_1}$에 해당함.
    * 즉, exponentially decaying sum 에 $(1-\beta_1)$을 곱하면 exponentially decaying average가 나오기 때문에 사실상 같다고 볼 수 있음 (상수배 차이).
* 2번의 $\beta_2$는 `RMSProp`의 $\rho$ 에 해당.
* 3번과 4번은 $\textbf{m}$와  $\textbf{s}$가 $\textbf{0}$로 시작할 경우, 초기 iteration에서 $\beta_1\textbf{m}$이나 $\beta_2\textbf{s}$의 기여도가 없게되는 문제를 해결하기 위해 제안됨.
    * 3번과 4번은 학습 초기 ($t$가 작은 수)에는 $\textbf{m}$과 $\textbf{s}$를 크게 증폭을 시켜주어 거의 $\textbf{0}$로 bias된 효과를 상쇄시켜줌.
    * 학습 후반부 ($t$가 큰 수)에서는 증폭 효과가 없어짐(분모가 1에 가까워짐)에 따라 원래의 $\textbf{m}$와  $\textbf{s}$에 의해 업데이트가 이루어짐.

## Keras에서의 구현.

아래와 같이 `Adam` optimizer 객체를 생성하여 `fit`에 넘겨주면 됨.

```Python
optimizer = tf.keras.optimizers.Adam(learning_rate=0.001, 
                                     beta_1=0.9,
                                     beta_2=0.999)
```

* momentum decay hyperparameter $\beta_1$ : `0.9`
* scaling decay hyperparameter $\beta_2$ : `0.999`
* the smoothing term $\epsilon$ : `1e-7`