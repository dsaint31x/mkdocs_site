# Root Mean Square Propagation (RMSProp)

이 알고리즘은 publish가 되지않고, Hinton 교수님의 Coursera 강의에서 소개된 알고리즘임.

`AdaGrad`와 거의 비슷하지만, 

* 지금까지의 모든 gradient를 accumulate하여 $\textbf{s}$를 구하는 것이 아닌, 
* ***Exponential Moving Average*** 를 통해 
* 과거의 gradient의 영향을 지수함수로 감소시키고 
* 최근의 gradient들을 중심으로 누적시켜 
* 지나치게 learning rate가 빠르게 감소하는 문제를 해결함. 

참고: [Exponential Moving Average](https://dsaint31.tistory.com/860)

즉, `RMSProp`은 `AdaGrad`의 문제점을 개선한 adaptive learning rate 기반의 optimizer임.

수식은 다음과 같음.

$$
\begin{aligned}
s_{t+1}
&= \beta\, s_t
  + (1-\beta)\,
    \bigl(\nabla_\theta J(\theta_t)
    \;\otimes\;
    \nabla_\theta J(\theta_t)\bigr), \\
\theta_{t+1}
&= \theta_t
  - \eta\;
    \nabla_\theta J(\theta_t)
    \;\oslash\;
    \bigl(\sqrt{s_{t+1}} + \varepsilon\bigr).
\end{aligned}
$$

* Exponential Decaying Factor인 $\beta$ (forgetting factor, decaying factor, smoothing factor)는 `0.9`를 기본값으로 가지며, 일종의 hyperparameter로 0.9~0.999의 값을 취함.
* $\frac{1}{1-\beta}$의 gradient들에 대한 평균으로 근사하기도 함. (즉 $\beta$가 클 수록 오래전의 gradient들을 고려하여 누적시켜 learning rate를 감소시킴)
* $\otimes$는 element-wise multiplication (Hadamard product) 임.
* $\oslash$는 element-wise division (Hadamard division)임.


## Pseudo code

```
cache = decay_rate * cache + (1 - decay_rate) * dx**2
x += - learning_rate * dx / (np.sqrt(cache) + eps)
```

* `decay_rate` is a hyperparameter and typical values are [0.9, 0.99, 0.999]
* `x+=` update is identical to `Adagrad`, but the cache variable is a “leaky”

## Keras에서의 구현.

아래와 같이 `RMSProp` optimizer 객체를 생성하여 `fit`에 넘겨주면 됨.

```Python
optimizer = tf.keras.optimizers.RMSprop(learning_rate=0.001,
                                        rho=0.9)
```

## References

* [slide 29 of Lecture 6 of Geoff Hinton’s Coursera class.](http://www.cs.toronto.edu/~tijmen/csc321/slides/lecture_slides_lec6.pdf)
* [CS231n Convolutional Neural Networks for Visual Recognition](https://cs231n.github.io/neural-networks-3/#RMSprop)