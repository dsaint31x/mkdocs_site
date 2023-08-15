# Exponential Linear Unit (ELU)

the variants of ReLU 의 성공에도 불구하고, 이들의 discontinuity로 인한 slow converge나 gradient descent bounce 등의 단점이 해결되지 못함.

`ELU`는 ReLU의 장점에 smooth function의 장점을 조합시켜 이 문제를 해결함.

$$\text{ELU}(x)=\left\{ \begin{matrix} x & \text{ if } x \ge 0 \\ \alpha (e^x -1) & \text{ if } x < 0\end{matrix} \right.$$

* positive input에선 `ReLU`와 차이가 없으나 
* negative input에선 expontial을 이용하여 특정 한계치 $-\alpha$ 이상의 negative 출력을 하도록 제한하면서 smoothness를 유지하도록 함.
    * $\alpha=1$ 이 주로 사용되나 그 이상의 값을 사용할 수도 있음.
* ReLU 계열들과 마찬가지로 `He` weight initialization과 함께 쓰임.  

단점은 exponential function의 사용으로 연산량이 ReLU 계열보다 큰 편으로 훈련 시간이 더 걸린다는 점임 (수렴속도는 향상되지만… 연산량의 증가폭이 더 커서 훈련시간이 보다 긴 편임.) 

> `ELU` 까지는 monotonic하고 convex라는 공통점을 가졌으나, 최근의 activation은 보다 복잡한 shape를 가지기 시작함.  
> 기본적으로는 `ReLU` 정도면 속도나 성능에서 좋은 기본 선택이지만 좀더 복잡한 task에서의 성능 향상을 위해선 `Swish`와 같은 `SiLU` 계열도 좋은 선택임. 

Ref. : Djork-Arné Clevert et al., “Fast and Accurate Deep Network Learning by Exponential Linear Units (ELUs),” Proceedings of the International Conference on Learning Representations, arXiv preprint (2015).

---
  
## Scaled ELU

Scaled ELU는 몇가지 제한조건과 함께 사용되면, layer에서 self-normalized input/output 을 보장한다.

이는 layer의 input과 output이 mean=0, std=1인 normal distribution을 유지한다는 것임.

하지만 제한 조건이 꽤나 까다롭다 (skip-connection, batch-norm, drop-out 등의 기법을 사용할 수 없고 MLP architecutre만을 사용해야하는 등등).

때문에 SELU를 실제 사용하기가 쉽지않다.

관심이 있다면 다음 논문을 살펴보자.

Ref. :  Günter Klambauer et al., “Self-Normalizing Neural Networks”, Proceedings of the 31st International Conference on Neural Information Processing Systems (2017): 972–981.


