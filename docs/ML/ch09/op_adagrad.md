# Adaptive Gradient (AdaGrad)

momentum과 nesterov accelerated gradient가 parameter vector의 변화되는 방향(direction)에 초점을 맞춘 것과 달리, AdaGrad는 adative learning rate optimizer로써 적절할 learning rate를 parameter vector의 각 component에 다르게 계산한다.

변화가 심하게 된 component에서는 learning rate를 더 많이 감소시키고, 변화가 많이 이루어지지 않은 component에 대해서는 learning rate를 덜 감소시키는 ***`adaptive learning rate`를 채택함***.

수식 (vectorized equation)은 다음과 같음.

$$
\textbf{s}_{t+1} = \textbf{s}_{t}+\nabla_\theta J(\boldsymbol{\theta}_{t}) \otimes \nabla_\theta J(\boldsymbol{\theta}_{t}) \\
\boldsymbol{\theta}_{t+1} = \boldsymbol{\theta}_{t} - \eta \nabla_\theta J(\boldsymbol{\theta}_{t}) \oslash \sqrt {\textbf{s}+\epsilon}
$$

* gradient의 square를 계속해서 누적한 $\textbf{s}$를 통해 parameter vector $\boldsymbol{\theta}$의 각 component가 얼마나 변화했는지를 체크.
    * $\otimes$는 element-wise multiplication임.
* 변화량을 square로 계산했으므로 여기에 square root를 취하고 이를 learning rate $\eta$에 나누어줌으로서 adaptive learning rate를 구함. 
    * $\oslash$는 element-wise disision임.
* $\epsilon=10^{-10}$으로 zero division을 막아줌.

gradient가 컸던 component (=경사가 가파른 축)에 대해선 learning rate의 감소가 보다 많이 이루어지고, graident가 작았던 component (=경사가 완만한 축)에 대해선 learning rate 감소가 크게 이루어지지 않도록 처리하여 각 component별로 적절한 learning rate를 적용하는 것이 AdaGrad의 핵심임.

> 단점은 deep neural network에선 AdaGrad의 경우 지나치게 learning rate가 작아져서 제대로 학습이 안되는 경우(중도에 더 이상 학습이 안됨)가 잦은 편이라, neural network 훈련에는 권장되지 않음.  
> 
> * linear regression등에 적용할 경우 잘 동작함.
>
> 이는 $\textbf{s}$가 처음부터 끝까지의 gradient를 누적하고 있어서 너무 큰 값으로 learning rate의 값을 나누어주기 때문이라, 이를 개선한 `RMSProp`가 보다 많이 사용됨.

## Keras에서의 구현.

아래와 같이 AdaGrad optimizer 객체를 생성하여 `fit`에 넘겨주면 됨.

```Python
optimizer = tf.keras.optimizers.Adagrad(learning_rate=0.001)
```

