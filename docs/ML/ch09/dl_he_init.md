# He Initialization 유도

`He Initialization`은 `ReLU` 계열의 activaton function를 사용하는 layer의 weight를 초기화하는 방법임.

* He Initialization 은 다른 weight initialization 방법과 마찬가지로
* 다음 layer의 pre-activation scale이 지나치게 작아지거나 커지지 않도록 
* weight의 초기 variance를 정하는 것임.

즉, layer의 입력이 $X \sim \mathcal{N}(0, \sigma)$ 인 경우,  
다음 layer의 pre-activation 도 같은 분포를 유지하도록 하는 것임

---

## 1. Layer 표기

$l$번째 layer의 $i$번째 neuron에 대한 pre-activation을 다음과 같이 둠:

$$
z_i^{(l)} = \sum_{j=1}^{n_{l-1}} w_{ij}^{(l)} a_j^{(l-1)}
$$

여기서 $n_{l-1}$은 layer $l$의 입력 개수임:

$$
n_{l-1} = \text{fan}_\text{in}^{(l)}
$$

ReLU activation 을 거친 activation (=ReLU출력)은 다음과 같음:

$$
a_i^{(l)} = ReLU(z_i^{(l)})
$$

## 2. 기본 가정

He Initialization 유도는 다음의 가정 위에서 이루어짐:

weight의 평균은 0임!

$$
\begin{aligned}
E[w_{ij}^{(l)}] &= 0 \\\\
\text{Var}(w_{ij}^{(l)}) &= \sigma^2_{w,l}
\end{aligned}
$$

$w_{ij}^{(l)}$와 $a_j^{(l-1)}$ 는 서로 independent(독립)이라고 가정함.

그리고 다음과 같이 서로 다른 항들 $w_{ij}^{(l)}a_j^{(l-1)}$ 은 서로 독립 또는 최소한 비상관이라고 가정함.

---

## 3. Pre-activation 의 variance $Var(z_i^{(l)})$ 계산

$l$번째 layer의 $i$번째 neuron의 pre-activation $z_i^{(l)}$은 다음과 같음:

$$
z_i^{(l)} = \sum_{j=1}^{n_{l-1}} w_{ij}^{(l)} a_j^{(l-1)}
$$

이 $l$번째 layer의 $i$번째 neuron의 pre-activation $z_i^{(l)}$의 variance는 다음과 같음:

$$
\text{Var}(z_i^{(l)}) = \text{Var}\left(
\sum_{j=1}^{n_{l-1}} w_{ij}^{(l)} a_j^{(l-1)}
\right)
$$

서로 다른 항들이 독립 또는 최소 **비상관** 이라고 가정했으므로  
covariance 항은 0이 되어 다음이 성립:

$$
\begin{aligned}
\text{Var}(z_i^{(l)}) &=\sum_{j=1}^{n_{l-1}} \text{Var}\left( w_{ij}^{(l)} a_j^{(l-1)} \right) + 2 \color{red}{\sum_{j < k} \text{Cov}(w_{ij}^{(l)} a_j^{(l-1)} , w_{ik}^{(l)} a_k^{(l-1)} )} \\\\
& = \sum_{j=1}^{n_{l-1}} \text{Var}\left( w_{ij}^{(l)} a_j^{(l-1)} \right) + 2\cdot \color{red}{0} \\\\
\text{Var}(z_i^{(l)}) &= \sum_{j=1}^{n_{l-1}} \text{Var}\left( w_{ij}^{(l)} a_j^{(l-1)} \right)
\end{aligned}
$$

summation이 되는 항 $\text{Var}\left(w_{ij}^{(l)} a_j^{(l-1)}\right)$ 는 다음과 같음:

$$
\text{Var}\left(
w_{ij}^{(l)} a_j^{(l-1)}
\right) = E\left[
\left(
w_{ij}^{(l)} a_j^{(l-1)}
\right)^2
\right] - E\left[
w_{ij}^{(l)} a_j^{(l-1)}
\right]^2
$$

$w_{ij}^{(l)}$ 와 $a_j^{(l-1)}$ 는 서로 independent(독립)이라고 가정했으므로  
우선 뒤의 평균 항은 다음이 성립:

$$
E\left[w_{ij}^{(l)} a_j^{(l-1)}\right] = E[w_{ij}^{(l)}]E[a_j^{(l-1)}]
$$

앞서 평균이 0이라고 가정했으므로 다음이 성립:

$$
E[w_{ij}^{(l)}] = 0
$$

즉,

$$
\begin{aligned}
E\left[ w_{ij}^{(l)} a_j^{(l-1)} \right] &= 0 E[a_j^{(l-1)}]  \\\\
&=0
\end{aligned}
$$

따라서, 다음이 성립:

$$
\text{Var} \left(w_{ij}^{(l)} a_j^{(l-1)} \right) = E\left[\left( w_{ij}^{(l)} a_j^{(l-1)} \right)^2 \right]
$$

제곱을 풀면 다음이 성립:

$$
E\left[\left(w_{ij}^{(l)} a_j^{(l-1)}\right)^2 \right] = E\left[ (w_{ij}^{(l)})^2 (a_j^{(l-1)})^2 \right]
$$

독립성에 의해,

$$
E\left[(w_{ij}^{(l)})^2(a_j^{(l-1)})^2\right] = E[(w_{ij}^{(l)})^2] E[(a_j^{(l-1)})^2]
$$

또한 weight들의 평균 $E[w_{ij}^{(l)}]=0$이므로 다음이 성립:

$$
E[(w_{ij}^{(l)})^2] = \text{Var}(w_{ij}^{(l)}) = \sigma_{w,l}^2
$$

따라서, 다음이 성립:

$$
\text{Var}\left(w_{ij}^{(l)} a_j^{(l-1)}\right) =\sigma_{w,l}^2 E[(a_j^{(l-1)})^2]
$$

이를 다시 $\text{Var}(z_i^{(l)})$에 대입하면,

$$
\text{Var}(z_i^{(l)}) = \sum_{j=1}^{n_{l-1}} \sigma_{w,l}^2 E[(a_j^{(l-1)})^2]
$$

각 입력 activation이 같은 scale을 가진다고 보면,
$E[(a_j^{(l-1)})^2]$ 는 $j$에 대해 동일하게 볼 수 있음.

따라서, 다음이 성립:

$$
\text{Var}(z_i^{(l)}) = n_{l-1} \sigma_{w,l}^2 E[(a_j^{(l-1)})^2]
$$

$n_{l-1} = \text{fan}_\text{in}^{l}$ 이므로 다음이 성립:

$$ \text{Var}(z_i^{(l)}) = \text{fan}_\text{in}^{(l)}
\cdot
\text{Var}(w_{ij}^{(l)})
\cdot
E[(a_j^{(l-1)})^2]
$$

임.

위의 식에서 주의할 점은 

* He initialization 의 대상인 pre-activation 의 variance 에 영향을 주는 건
* 이전 layer의 activation 의 variance $Var(a_j^{(l-1)})$가 아닌
* 바로 이전 layer의 activation 의 second raw moment $E[(a_j^{(l-1)})^2]$ 임.


---

## 4. Second Raw Moment 가 대상!

variance 의 정의는 다음과 같음:

$$
Var(a_j^{(l-1)}) =

E\left[
\left(
a_j^{(l-1)} - E[a_j^{(l-1)}]
\right)^2
\right]
$$

즉, variance는 평균을 기준으로 한 second central moment임.

반면 다음은 second raw moment 임:

$$
E[(a_j^{(l-1)})^2]
$$

앞의 계산에서 

* 다음 layer의 pre-activation variance에 들어간 activation 관련 항은
* second central moment인 variance가 아닌
* second raw moemnt 임.

그 이유는 현재 우리가 사용하는 weight들의 평균을 0이라고 가정하기 때문임:

$$
E[w_{ij}^{(l)}] = 0
$$

동시에 $w_{ij}^{(l)}$와 $a_j^{(l-1)}$은 독립이므로, 
다음과 같이 곱 $w_{ij}^{(l)}a_j^{(l-1)}$의 평균도 0이 됨:

$$
E[w_{ij}^{(l)}a_j^{(l-1)}] = E[w_{ij}^{(l)}]E[a_j^{(l-1)}] = 0 \cdot E[a_j^{(l-1)}]
$$

* 중요한 점은 $E(a_j^{(l-1)})=0$일 필요가 없다는 것임. 
* ReLU 이후 activation은 보통 0 이상이라 평균이 0이 아닐 수 있음. 
* $E(a_j^{(l-1)}) \ne 0$ 라도 weight의 평균이 0이면 $E[w_{ij}^{(l)}a_j^{(l-1)}]=0$이 성립


이를 반영하면, pre-activation variance 는 다음이 성립

$$
\begin{aligned}
Var(w_{ij}^{(l)}a_j^{(l-1)}) &= E [ (w_{ij}^{(l)}a_j^{(l-1)})^2 ] - ( E[(w_{ij}^{(l)}a_j^{(l-1)})])^2 \\\\
&= E [ (w_{ij}^{(l)}a_j^{(l-1)})^2 ] \\\\
&= E [ w_{ij}^{(l)}^2 a_j^{(l-1)}^2 ] \\\\
&= E[(w_{ij}^{(l)})^2] E[(a_j^{(l-1)})^2]
$$

* $w_{ij}^{(l)}$ 와 $a_j^{(l-1)}$ 이 서로 독립이라고 가정함.


따라서 He Initialization 유도에서는 activation의 variance가 아니라 activation의 second raw moment를 기준으로 삼음.

---

## 5. ReLU의 효과

이제 ReLU가 pre-activation $z_i^{(l)}$ 의 second raw moment 를 어떻게 바꾸는지 살펴보자.

$$
a_i^{(l)} = ReLU(z_i^{(l)})
$$

$z_i^{(l)}$가 평균 0이고 대칭적인 분포를 가진다고 가정하자.

$$
E[z_i^{(l)}] = 0
$$

ReLU는 이 pre-activation $z_i^{(l)$의 음수 영역을 0으로 만들고, 양수 영역만 통과시킴.

$$
ReLU(z_i^{(l)}) =
\begin{cases}
z_i^{(l)} & \text{if } z_i^{(l)} > 0 \\
0 & \text{if } z_i^{(l)} \leq 0
\end{cases}
$$

따라서, 다음이 성립:

$$
E[(a_i^{(l)})^2] = E[ReLU(z_i^{(l)})^2]
$$

ReLU의 특성상 다음이 성립:

$$
E[ReLU(z_i^{(l)})^2] =
E[(z_i^{(l)})^2 \mid z_i^{(l)} > 0]P(z_i^{(l)} > 0)
$$

또한 $(z_i^{(l)})^2$는 양수 영역과 음수 영역에서 대칭적으로 같은 크기를 가지고 대칭분포이므로 다음이 성립:

$$
P(z_i^{(l)} > 0) = \frac{1}{2}
$$

따라서, 다음이 성립:

$$
\begin{aligned}
E[ReLU(z_i^{(l)})^2] &= \frac{1}{2}E[(z_i^{(l)})^2] \\\\
E[(a_i^{(l)})^2] &= \frac{1}{2}E[(z_i^{(l)})^2]
\end{aligned}
$$



여기서 $E[z_i^{(l)}]=0$이므로 다음이 성립:

$$
[(z_i^{(l)})^2] = Var(z_i^{(l)})
$$

따라서, 다음이 성립:

$$
E[(a_i^{(l)})^2] =
\frac{1}{2}Var(z_i^{(l)})
$$

---

## 6. 앞의 결과 대입

앞에서 구한 식은 다음으로 변경됨

$$
\text{Var}(z_i^{(l)}) = n_{l-1} \sigma_{w,l}^2 E[(a_j^{(l-1)})^2]
$$

이를 ReLU 이후 second raw moment 식에 대입함.

$$
E[(a_i^{(l)})^2] = \frac{1}{2}Var(z_i^{(l)})
$$

따라서, 다음이 성립:

$$
\begin{aligned} 
E[(a_i^{(l)})^2] &= \frac{1}{2} \left( n_{l-1} \sigma_{w,l}^2 E[(a_j^{(l-1)})^2] \right) \\\\
&=\frac{1}{2} n_{l-1} \sigma_{w,l}^2 E[(a_j^{(l-1)})^2]
\end{aligned}
$$

---

## 7. He initialization 의 구하기

ReLU를 activation으로 사용하는 layer 에서 vanihsing gradient 나 exploding gradient 를 방지하려면
activation의 second raw moment가 유지되어야 함:

$$
E[(a_i^{(l)})^2] = E[(a_j^{(l-1)})^2]
$$

앞의 식을 대입하면,

$$
\frac{1}{2}
n_{l-1}
\sigma_{w,l}^2
E[(a_j^{(l-1)})^2] =
E[(a_j^{(l-1)})^2]
$$

양변을 $E[(a_j^{(l-1)})^2]$로 나눔.

$$
\frac{
\frac{1}{2}
n_{l-1}
\sigma_{w,l}^2
E[(a_j^{(l-1)})^2]
}{
E[(a_j^{(l-1)})^2]
} = \frac{
E[(a_j^{(l-1)})^2]
}{
E[(a_j^{(l-1)})^2]
}
$$

따라서, 다음이 성립해야 activation의 second raw moment가 유지됨:

$$
\frac{1}{2}
n_{l-1}
\sigma_{w,l}^2 = 1
$$

이를 $sigma^2_{w,l}$에 대해 정리하면 다음과 같음:

$$
\sigma_{w,l}^2 = \frac{2}{n_{l-1}}
$$

즉, 다음이 성립.

$$
\text{Var}(w_{ij}^{(l)}) = \frac{2}{n_{l-1}}
$$

$n_{l-1} = \text{fan}_\text{in}^{(l)}$ 이므로 다음으로 정리됨:

$$
Var(w_{ij}^{(l)}) = \frac{2}{\text{fan}_\text{in}^{(l)}}
$$

---

## 8. 결론

정규분포 기반 He Initialization은 다음과 같음.

$$
w_{ij}^{(l)} \sim \mathcal{N}
\left(
0,
\frac{2}{\text{fan}_\text{in}^{(l)}}
\right)
$$

즉, 표준편차를 다음과 같이 정하면 됨:

$$
\text{std}(w_{ij}^{(l)}) =

\sqrt{
\frac{2}{\text{fan}_\text{in}^{(l)}}
}
$$

