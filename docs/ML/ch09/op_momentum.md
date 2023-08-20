# Momentum 

momentum은 운동량이라는 뜻으로 기존의 gradient decent에서 이전의 gradient 정보를 이용하여 보다 빠르게 training이 converge하도록 도와주는 방법임.

> Gradient Decent의 역사가 워낙 오래된 터라, momentum optimizer도 1960년대부터 사용이 된 정말 오래된 알고리즘이다. 그래도 정말 효과적이며 많이 사용된다된

model의 parameter vector $\boldsymbol{\theta}$를 업데이트 하는 방향을 gradient $\nabla_{\boldsymbol{\theta}}J(\theta)$만을 사용하는 regular gradient와 달리 이전의 업데이트 방향의 gradient vector와의 vector sum을 통해 parameters의 업데이트 방향을 결정함.

inertia (관성)의 개념을 도입하여 parameters를 업데이트할 vector의 방향이 결정된다. (여기서 계속 방향이라고 애기하는 이유는 parameters를 vector라고 볼 경우, 해당 vector의 각 elements가 어떻게 변경될지를 나타내는 것도 일종의 vector로 표현되며, vector이므로 방향과 크기를 가짐. 크기의 조절은 learning ratio로 이루어지며 방향은 gradient로 결정됨).

parameter vector $\boldsymbol{\theta}$의 업데이트는 다음과 같이 이루어짐.

$$\boldsymbol{\theta}_{t+1}=\boldsymbol{\theta}_{t}+ \textbf{m}_{t+1}$$

여기서 momentum $\textbf{m}_{t+1}$은 inertia coef. (or momentum coef.)$\gamma$를 통해 inertia의 정도가 결정(inertia coef가 클수록 관성이 커서 기존의 update 방향이 잘 안 변함. 만약 inertia coef.가 0일 경우 regular gradient와 같음).

$$\begin{aligned} \textbf{m}_{t+1}&=\gamma \textbf{m}_t - \eta\nabla_{\boldsymbol{\theta}}J(\boldsymbol{\theta}_t)\\ \\ \textbf{m}_0 &= \textbf{0}\end{aligned}$$

관성계수(inertia coef.) $\gamma$은 일반적으로 0.9를 사용.

- SGD보다 일반적으로 빠른 수렴속도
    - $\nabla_{\boldsymbol{\eta}}J(\boldsymbol{\theta}_t)$가 constant $C$라면, $\eta$가 $\frac{1}{1-\gamma}\eta$로 수렴하게 됨.
    - 만약 $\gamma=0.9$일 경우, regular gradient보다 10배의 learning ratio가 적용되는 셈으로 매우 빠른 학습속도를 보임.    
- Gradient 가 0인 곳에서도 업데이트가 이루어지므로 local minima에 탈출할 확률이 SGD보다 높음.

단점으로는 inertia의 도입으로 인해 ***최적의 값*** 에서도 업데이트가 이루어져 지나칠 수 있음.

> tunning을 해야할 hyper-parameter $\gamma$가 하나 늘어나기는 하지만, 일반적으로 0.9정도면 거의 대부분 regular gradient decent보다 잘 동작하기 때문에 단점이라고 보기 어려움.


## Momentum의 빠른 학습속도의 이유.

gradient가 constant인 경우, momentum의 변화가 특정값으로 수렴하게 되는데 (마치 air resistance에서의 terminal speed가 수렴하는 것처럼) 이 경우 $\dfrac{d \textbf{m}}{d t}=0$이 됨.

이 경우 다음과 같은 식이 성립함.

$$\begin{aligned} \textbf{m}_{t+1}&=\gamma \textbf{m}_t -\eta\nabla_{\boldsymbol{\theta}}J(\boldsymbol{\theta}_t) \\ &= \gamma \textbf{m}_t - \eta C \\
\textbf{m} &= \gamma \textbf{m} - \eta C \\
(1-\gamma)\textbf{m} &= - \eta C\\
\textbf{m} &= \frac{1}{1-\gamma}(-\eta)C\\ \\
\therefore \boldsymbol{\theta}_{t+1} &= \boldsymbol{\theta}_{t}-\frac{1}{1-\gamma}(\eta)C \end{aligned}$$

위 식에 보이듯이 gradient가  $C$로 일정한 경우, learning ratio가 $\eta$에 $\frac{1}{1-\gamma}$가 곱해지며, $\gamma=0.9$인 경우, regular gradient보다 10배 큰 learning ratio가 가해진 것과 같아짐.

## Keras에서의 구현.

`tf.keras.optimizers.SGD` optimizer를 생성할 때, `momentum` parameter를 추가하면 $\gamma=0.9$인 momentum optimizer를 생성함. (이를 모델의 `fit`에 넘겨주면 됨.)

```Python
opt = tf.keras.optimizers.SGD(
    learning_rate = 0.001,
    momentum = 0.9
)
```


