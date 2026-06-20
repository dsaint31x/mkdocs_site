---
title: Batch Size
tags: [Batch Size, SGD, Mini-batch SGD, Large Batch, Learning Rate Scaling, Warmup, Critical Batch Size]
---

# Batch Size

> Batch size는  
> **한 번의 parameter update에 사용되는 sample의 수** 를 의미함.

Deep Learning에서는

* training dataset 전체를 한 번에 사용하는 것이 아니라,
* 일반적으로 여러 개의 작은 묶음으로 나누어 학습함.

이때

* 하나의 묶음을 **batch** 라고 하고,
* 하나의 batch에 포함된 sample 수를 **batch size** 라고 함.

즉,

$$
\text{batch size} = \text{number of samples in one batch}
$$

임.

예를 들어 training dataset에 $50{,}000$개의 sample이 있고,  
batch size가 $32$라면,

한 번의 parameter update에는 $32$개의 sample이 사용됨.

---

## Batch, Iteration, Epoch

Batch size를 이해하려면 다음 용어들을 같이 구분해야 함.

* **sample**: data 1개.
* **batch**: 여러 sample을 묶은 단위.
* **batch size**: batch 하나에 들어가는 sample 수.
* **iteration 또는 step**: batch 하나를 이용해 parameter를 한 번 update하는 과정.
* **epoch**: training dataset 전체를 한 번 모두 사용하는 과정.

training dataset의 크기가 $N$, batch size가 $B$라면,  
한 epoch에서 필요한 update 횟수는 대략 다음과 같음.

$$
\left\lceil \frac{N}{B} \right\rceil
$$

예를 들어 $N = 50{,}000$, $B = 32$이면,

$$
\left\lceil \frac{50{,}000}{32} \right\rceil \approx 1563
$$

즉, 한 epoch 동안 약 $1563$번의 parameter update가 발생함.

반면 batch size가 $1024$라면,

$$
\left\lceil \frac{50{,}000}{1024} \right\rceil \approx 49
$$

즉, 한 epoch 동안 약 $49$번만 parameter update가 발생함.

따라서,

$$
B \uparrow \Rightarrow \frac{N}{B} \downarrow
$$

즉, 다음이 성립함.

$$
\text{batch size 증가} \Rightarrow \text{epoch당 update 횟수 감소}
$$

---

## Batch Size가 중요한 이유

초기 neural network 학습에서는 전체 dataset을 사용하여 gradient를 계산하는 방식보다,  
일부 sample만 사용하여 gradient를 추정하는 **Stochastic Gradient Descent (SGD)** 방식이 널리 사용되었음.

이 방식은 gradient가 다소 noisy하더라도,

* 계산량이 적고,
* memory 사용량이 작으며,
* 큰 dataset에서도 반복적인 parameter update가 가능하다는 장점이 있었음.

이후 실제 Deep Learning에서는 sample 1개만 사용하는 순수 SGD와  
전체 dataset을 사용하는 full-batch gradient descent 사이의 절충안으로  
**mini-batch SGD** 가 표준적인 학습 방식으로 자리 잡음.

즉, batch size는

* gradient를 얼마나 정확하게 추정할 것인지,
* parameter를 얼마나 자주 update할 것인지,
* hardware를 얼마나 효율적으로 사용할 것인지

를 동시에 결정하는 hyperparameter임.

> Hyperparameter tuning의 주요 대상이긴 하나,  
> 실무에서는 GPU의 사용 가능한 memory 크기에 맞추어 정해지는 경우도 많음.
>
> 아래에서는 batch size의 의미와 trade-off를 자세히 다루지만,  
> 실제 학습 환경에서는 GPU memory가 중요한 제약 조건이 되는 경우가 많음.

---

## Small Batch와 Large Batch

* Batch size가 작은 경우를 **small batch training** 이라고 하고,
* batch size가 큰 경우를 **large batch training** 이라고 함.

다만 large batch의 절대적인 기준이 항상 정해져 있는 것은 아님.

대략적으로는 다음과 같이 볼 수 있음.

* $32$, $64$, $128$: 일반적인 small 또는 moderate batch.
* $1024$, $4096$, $8192$: large batch training에서 자주 등장하는 크기.

핵심 차이는 다음과 같음.

* **small batch**

    * 한 번의 update에 적은 sample 사용.
    * update 횟수가 많음.
    * gradient noise가 큼.
    * memory 사용량이 적음.
    * generalization에 유리할 수 있음.

* **large batch**

    * 한 번의 update에 많은 sample 사용.
    * update 횟수가 적음.
    * gradient가 상대적으로 안정적임.
    * GPU나 분산 학습 환경에서 병렬 처리 효율이 좋음.
    * memory 사용량이 큼.

즉, large batch는 다음의 특징을 가짐.

* 한 번에 더 많은 data를 보고 update함.
* 대신 parameter를 update하는 횟수는 줄어듦.

---

## Large Batch와 Generalization Gap

Large batch training에서는 small batch training보다  
validation 또는 test 성능이 낮아지는 경우가 보고되었음.

이를 **generalization gap** 이라고 부를 수 있음.

초기 large batch 연구에서는 이 현상을 다음과 같이 설명함.

* large batch가
* **sharp minimum** 으로 수렴하기 쉽기 때문이라고 설명함.

> **Sharp minimum** 은 주변으로 조금만 이동해도 loss가 빠르게 증가하는 해를 의미함.
>
> * 이런 해는 training data에는 잘 맞을 수 있지만,
> * unseen data에 대한 generalization이 나쁠 수 있음.

초기 연구들에는 batch size가 크면 generalization이 나빠진다는 설명이 많았으나,  
오늘날에는 이같이 단순한 설명은 부정확하다고 봄.

2017년 Hoffer et al.은 large batch의 generalization gap이

* batch size 자체의 문제라기보다는,
* **같은 epoch 수에서 update 횟수가 줄어드는 문제** 와
* 관련이 크다고 설명함.

예를 들어 $N = 50{,}000$인 dataset에서 다음과 같음.

| Batch size | 1 epoch당 update 수 | 10 epoch 총 update 수 |
|---:|---:|---:|
| $32$ | 약 $1563$회 | 약 $15630$회 |
| $1024$ | 약 $49$회 | 약 $490$회 |

같은 10 epoch을 학습해도,  
실제 parameter update 횟수는 크게 다름.

따라서 large batch를 사용할 경우,

* 같은 epoch 수로 단순 비교하면 안 됨.
* 줄어든 update 횟수를 고려해야 함.
* 필요하면 더 많은 epoch을 학습해야 함.

여기서 **더 오래 train한다** 는 것은

* 단순히 wall-clock time을 늘린다는 뜻이 아니라,
* 줄어든 update 횟수를 보상할 만큼 학습량을 늘린다는 의미임.

즉, large batch에서 generalization gap을 줄이려면  
전체 step 수, epoch 수, learning rate 설정을 함께 고려해야 함.

---

## Large Batch와 Learning Rate Scaling

Large batch에서는 update 횟수가 줄어듦.

그러면 다음과 같은 생각을 할 수 있음.

> 여러 번 update하는 대신,  
> 한 번 update할 때 더 크게 움직이면 되지 않을까?

이 아이디어가 **learning rate scaling** 임.

parameter update는 일반적으로 다음과 같이 표현할 수 있음.

$$
\theta_{t+1} = \theta_t - \eta g_t
$$

여기서

* $\eta$: learning rate.
* $g_t$: 현재 batch에서 계산된 gradient.

batch size가 커지면 $g_t$는 더 많은 sample을 평균낸 gradient가 됨.  
따라서 작은 batch에서 계산한 gradient보다 noise가 줄어드는 경향이 있음.

이 때문에 large batch에서는 learning rate를 더 크게 설정하는 전략을 사용할 수 있음.

대표적인 방법이 **Linear Scaling Rule** 임.

기준 batch size가 $B$, 기준 learning rate가 $\eta$일 때,  
batch size를 $k$배 키우면 learning rate도 $k$배 키움.

$$
B_{\text{new}} = kB
$$

이면,

$$
\eta_{\text{new}} = k\eta
$$

로 설정함.

예를 들어 기준 batch size가 $256$, learning rate가 $0.1$일 때,  
batch size를 $8192$로 키우면,

$$
k = \frac{8192}{256} = 32
$$

이므로,

$$
\eta_{\text{new}} = 32 \times 0.1 = 3.2
$$

가 됨.

즉, large batch에서는 줄어든 update 횟수를  
더 큰 learning rate로 어느 정도 보상할 수 있음.

단, 이것이 small batch 여러 번 update와 완전히 같은 것은 아님.

* small batch 여러 번 update:

    * update마다 parameter가 조금씩 바뀜.
    * 각 gradient는 서로 다른 parameter 위치에서 계산됨.

* large batch 한 번 update:

    * 모든 gradient가 같은 parameter 위치에서 계산됨.
    * 한 번에 크게 이동함.

따라서, 다음임을 명심할 것.

$$
\text{small batch several updates}
\neq
\text{large batch one update with larger learning rate}
$$

> **Linear Scaling Rule** 은
>
> * update 횟수 감소를 완전히 대체하는 방법이 아니라,
> * 이를 어느 정도 보상하기 위한 근사적 전략에 해당함.

---

## Warmup

앞서 살펴본 대로,  
large batch에서 learning rate를 크게 키우는 것은 유용할 수 있음.

하지만 처음부터 큰 learning rate를 사용하면  
학습 초기에 loss가 튀거나 발산할 수 있는 **optimization instability** 가 발생할 수 있음.

이를 줄이기 위한 방법으로 **warmup** 이 제안됨.

> **Warmup** 은
>
> * 학습 초기에 learning rate를 작은 값에서 시작하여,
> * 몇 epoch 동안 목표 learning rate까지 점진적으로 증가시키는 방법임.

즉, large batch training에서는 보통 다음 조합을 고려함.

* large batch 사용.
* learning rate scaling 적용.
* warmup 적용.

---

## 최신 연구 흐름: Critical Batch Size

최근 large-scale training, 특히 LLM pretraining에서는  
batch size를 단순히 “클수록 좋은 값”으로 보지 않음.

중요한 개념 중 하나가 **Critical Batch Size (CBS)** 임.

Critical batch size는 대략 다음과 같이 이해할 수 있음.

* batch size를 키웠을 때 training speed는 좋아지지만,
* 어느 지점을 넘으면 추가적인 batch size 증가의 이득이 급격히 줄어드는 경계.

즉, batch size를 키우면 **병렬 처리는 좋아질 수 있음**.  
이는 GPU 활용도 증가와 관련됨.

하지만 너무 큰 batch size를 사용하면,

* 한 번 update에 너무 많은 sample을 사용하게 되고,
* update 횟수는 크게 줄어들며,
* token efficiency 또는 data efficiency가 나빠질 수 있음.

> 최신 연구에서는
>
> * critical batch size가 고정된 값이 아니라,
> * training이 진행되면서 변할 수 있다고 봄.

특히 학습 초기에는 작은 batch size로도 충분한 경우가 많고,  
학습이 진행되면서 더 큰 batch size가 유용해질 수 있음.

이 관점에서는 learning rate warmup뿐 아니라  
**batch size warmup** 도 자연스러운 전략이 됨.

즉,

* 학습 초반에는 작은 batch size 사용.
* 학습이 진행되면서 batch size 증가.
* critical batch size를 넘지 않는 범위에서 data parallelism 활용.

이라는 방향임.

따라서 최신 large-scale training에서는 batch size를 하나의 고정값으로만 정하기보다,

* model size,
* training data size,
* learning rate schedule,
* optimizer,
* hardware parallelism,
* training stage

와 함께 조정하는 값으로 보는 경향이 강함.

---

## 정리

Batch size는  
**한 번의 parameter update에 사용되는 sample 수** 임.

Batch size가 작으면

* update가 자주 발생함.
* gradient noise가 큼.
* memory 사용량이 적음.
* generalization에 유리할 수 있음.

Batch size가 크면

* 한 번의 update에 많은 sample을 사용함.
* gradient가 안정적임.
* 병렬 연산 효율이 좋아질 수 있음.
* 같은 epoch 수에서는 update 횟수가 줄어듦.
* learning rate와 warmup 조정이 중요해짐.

따라서 large batch를 사용할 때는  
batch size만 키우면 안 됨.

다음 요소를 같이 고려해야 함.

* 전체 update 횟수.
* epoch 수.
* learning rate scaling.
* warmup.
* critical batch size.
* batch size schedule.
* memory 사용량.
* GPU 또는 분산 학습 환경.
* validation 성능.

결론적으로 batch size는  
단순히 “한 번에 몇 개의 sample을 넣을 것인가”의 문제가 아님.

Batch size는

* optimization,
* generalization,
* training speed,
* hardware efficiency,
* data efficiency

를 모두 바꾸는 중요한 hyperparameter임.

---

## References

* LeCun, Y., Bottou, L., Bengio, Y., and Haffner, P.  
  **Gradient-Based Learning Applied to Document Recognition**.  
  Proceedings of the IEEE, 1998.  
  초기 neural network 학습과 gradient-based learning의 대표적인 고전 논문임.

* Bottou, L.  
  **Large-Scale Machine Learning with Stochastic Gradient Descent**.  
  Proceedings of COMPSTAT, 2010.  
  large-scale learning에서 SGD가 왜 중요한지 설명한 대표적인 논문임.

* Bottou, L., Curtis, F. E., and Nocedal, J.  
  **Optimization Methods for Large-Scale Machine Learning**.  
  SIAM Review, 2018.  
  large-scale machine learning에서 stochastic gradient 계열 방법의 역할을 정리한 review 논문임.

* Keskar, N. S., Mudigere, D., Nocedal, J., Smelyanskiy, M., and Tang, P. T. P.  
  **On Large-Batch Training for Deep Learning: Generalization Gap and Sharp Minima**.  
  ICLR, 2017.  
  large batch training의 generalization gap을 sharp minima 관점에서 설명한 대표적인 논문임.

* Hoffer, E., Hubara, I., and Soudry, D.  
  **Train Longer, Generalize Better: Closing the Generalization Gap in Large Batch Training of Neural Networks**.  
  NeurIPS, 2017.  
  large batch의 generalization gap을 update 횟수 부족 관점에서 설명한 논문임.

* Goyal, P., Dollár, P., Girshick, R., Noordhuis, P., Wesolowski, L., Kyrola, A., Tulloch, A., Jia, Y., and He, K.  
  **Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour**.  
  arXiv, 2017.  
  large batch training에서 linear scaling rule과 warmup을 사용한 대표적인 논문임.

* McCandlish, S., Kaplan, J., Amodei, D., and OpenAI Dota Team.  
  **An Empirical Model of Large-Batch Training**.  
  arXiv, 2018.  
  gradient noise scale과 critical batch size 개념을 통해 large batch training의 한계를 설명한 논문임.

* Merrill, W., Arora, S., Groeneveld, D., and Hajishirzi, H.  
  **Critical Batch Size Revisited: A Simple Empirical Approach to Large-Batch Language Model Training**.  
  arXiv, 2025.  
  language model training에서 critical batch size가 학습 진행에 따라 변하며, batch size warmup이 유용할 수 있음을 보인 최신 연구임.

* Géron, A.  
  **Hands-On Machine Learning with Scikit-Learn and PyTorch: Concepts, Tools, and Techniques to Build Intelligent Systems**.  
  O’Reilly Media, 2025.  
  관련 chapter: Chapter 4. Training Models, Chapter 9. Introduction to Artificial Neural Networks, Chapter 10. Building Neural Networks with PyTorch.  
  Chapter 4는 batch gradient descent, stochastic gradient descent, mini-batch gradient descent를 다루며, Chapter 9와 Chapter 10은 neural network 학습 과정에서 learning rate, batch size, PyTorch 기반 training loop를 이해하는 데 관련됨.