---
title: Unsupervised Pretraining
tags:
  - unsupervised learning
  - unsupervised pretraining
  - self-supervised learning
  - transfer learning
  - representation learning
  - deep learning
  - autoencoder
  - rbm
  - dbn
  - gan
  - diffusion model
  - semi-supervised learning
---

# Unsupervised Pretraining

## 1. 정의

`Unsupervised pretraining`은

* **human-labeled data 없이 먼저 model 또는 representation을 학습한 뒤,**
* **그 결과를 downstream task에 재사용하는 training strategy** 를 의미함.

좁은 의미에서는 *2000년대 후반의 고전적 딥러닝 문맥에서 사용된 용어* 로,

* RBM
* DBN
* Autoencoder
* Denoising Autoencoder
* Contractive Autoencoder

같은 unsupervised learning model을 이용해 network의 각 layer를 미리 학습하고,
이후 labeled data로 supervised fine-tuning하는 절차를 가리킴.

넓은 의미에서는

* human label 없이 대규모 unlabeled data로 먼저 representation을 학습한 뒤,
* 이를 target task에 transfer하는 모든 pretraining 방식을 포함함.

> 따라서 현대적 관점에서는 self-supervised pretraining도  
> 넓은 의미의 unsupervised pretraining에 포함될 수 있음.

```text
Unsupervised pretraining
= human label 없이 먼저 representation 또는 parameter를 학습한 뒤,
  downstream task에 재사용하는 절차
```

다만 용어를 정확히 구분하면 다음과 같음.

| 개념 | 핵심 의미 |
| :---: | :---: |
| `Unsupervised Learning`           | human label 없이 데이터의 구조, 분포, 잠재표현을 학습하는 학습 방식                                                             |
| `Unsupervised Pretraining`        | unsupervised learning 또는 self-supervised learning을 pretraining 목적으로 사용한 뒤 downstream task에 transfer하는 절차 |
| `Self-supervised Learning`        | 데이터 자체에서 target을 자동 생성하여 supervised-like objective로 representation을 학습하는 방식                              |
| `Transfer Learning`               | source task/domain에서 학습한 지식을 target task/domain에 재사용하는 상위 전략                                             |
| `Pretraining with Auxiliary Task` | 최종 target task가 아닌 보조 task로 먼저 학습한 뒤 target task에 transfer하는 방식                                          |

즉 `unsupervised learning`과 `unsupervised pretraining`은 같은 말이 아님.

예를 들어 GAN을 학습하여 image generation만 수행하고 끝낸다면 이는 unsupervised learning이지만, downstream task로 transfer하지 않았으므로 unsupervised pretraining은 아님.

반면 GAN의 discriminator 일부 layer를 feature extractor로 재사용하여 classification task에 사용한다면, 이는 넓은 의미의 unsupervised pretraining으로 볼 수 있음.

---

---

## 2. Transfer Learning 안에서의 위치

`Transfer Learning`은 가장 상위 개념임.

핵심은 다음과 같음.

* Source task/domain에서 얻은 지식을
* Target task/domain에 재사용하는 것

예를 들어 ImageNet으로 학습한 CNN의 feature extractor를 의료 영상 분류에 재사용하는 경우가 transfer learning임.

```text
ImageNet classification
        ↓
pretrained CNN
        ↓
medical image classification
```

이 경우 source task에서 human label을 사용했으므로 supervised pretraining 기반 transfer learning임.

반면 unlabeled corpus로 BERT를 masked language modeling 방식으로 pretraining한 뒤 감성 분석에 fine-tuning하면 self-supervised pretraining 기반 transfer learning임.

```text
Large unlabeled corpus
        ↓
Masked Language Modeling
        ↓
pretrained BERT
        ↓
sentiment classification
```

따라서 pretraining은 transfer learning의 대표적인 구현 방식이지만, transfer learning 전체가 pretraining은 아님.

Transfer learning에는 다음도 포함됨.

* feature extraction
* fine-tuning
* domain adaptation
* multi-task learning 기반 transfer
* pretraining 후 downstream adaptation

이 문서의 주제인 unsupervised pretraining은 그중 다음 위치에 놓임.

```text
Transfer Learning
│
└─ Pretraining-based Transfer Learning
   │
   └─ Pretraining with Auxiliary Task
      │
      ├─ Supervised Pretraining
      │  └─ ImageNet classification → medical image classification
      │
      └─ Unsupervised Pretraining
         │
         ├─ Classical Unsupervised Pretraining
         │  ├─ RBM / DBN
         │  ├─ Autoencoder
         │  ├─ Denoising Autoencoder
         │  └─ Contractive Autoencoder
         │
         └─ Self-Supervised Pretraining
            ├─ BERT masked language modeling
            ├─ GPT next-token prediction
            ├─ SimCLR contrastive learning
            └─ MAE masked image reconstruction
```

* 비록 self-supervised learning이 human label을 사용하지 않아 넓은 의미의 Unsupervised Pretraining에 속하나
* self-supervised learning은 데이터 자체에서 target을 만들어 $x \rightarrow y$ 형태의 supervised-like objective로 학습하므로,
* 전통적인 unsupervised learning과 구분해서 부르는 것이 일반적임.

---

---

## 3. 등장 배경

2006년 이전까지 여러 hidden layer를 가진 deep network는
random initialization 후 backpropagation만으로 학습시키기 어려운 경우가 많았음.

대표적인 문제는 다음과 같음.

* gradient가 layer를 거치며 소실되거나 발산함
* 당시에는 적절한 initialization 기법이 부족하여 optimization이 제대로 진행되지 않는 경우가 많았음
* layer 수가 늘어날수록 shallow network보다 성능이 나빠지는 경우가 있었음
* labeled data가 부족한 상황에서 deep network가 쉽게 overfitting됨

이 문제를 완화하기 위해 2006년경 등장한 전략이 unsupervised pretraining임.

핵심 아이디어는 다음과 같음.

```text
Unlabeled data로 먼저 feature 또는 representation을 학습
        ↓
그 parameter를 초기값으로 사용
        ↓
Labeled data로 target task에 fine-tuning
```

즉 처음부터 random initialization으로 supervised learning을 수행하지 않고,
먼저 unlabeled data의 구조를 반영한 parameter에서 학습을 시작하게 만드는 방식임.

* Hinton, Osindero, Teh (2006)는 RBM을 layer-wise로 쌓아
  Deep Belief Network를 학습하는 방법을 제안했음.
* Bengio, Lamblin, Popovici, Larochelle (2007)은 이를 일반화하여
  `greedy layer-wise pretraining`이라는 형태로 정리했음.

이 시기의 unsupervised pretraining (=고전적)은 다음을 의미함:

```text
Unsupervised learning model을 이용한 layer-wise pretraining
```

따라서 초기 문맥에서는

```text
Unsupervised pretraining
≈ RBM / DBN / Autoencoder 기반 layer-wise pretraining
```

으로 이해해도 큰 문제가 없음.

---

---

## 4. 고전적 Unsupervised Pretraining

### 4.1 Greedy Layer-wise Pretraining

고전적 unsupervised pretraining의 대표 절차는 greedy layer-wise pretraining임.

절차는 다음과 같음.

1. 첫 번째 layer를 input $x$에 대해 unsupervised objective로 학습함.
2. 학습된 첫 번째 layer의 출력 $h_1$을 다음 layer의 입력으로 사용함.
3. 두 번째 layer를 $h_1$에 대해 다시 unsupervised objective로 학습함.
4. 이 과정을 layer마다 반복함.
5. 모든 layer를 쌓은 뒤, task-specific head를 붙이고 labeled data로 supervised fine-tuning함.

$$
x \rightarrow h_1 \rightarrow h_2 \rightarrow h_3 \rightarrow \cdots
$$

이 방식이 `greedy`라고 불리는 이유는

* 전체 network를 한 번에 최적화하지 않고, 각 layer를 순차적으로 하나씩 학습하기 때문임.
* 이때 각 layer는 이전 layer의 출력을 더 잘 설명하거나 복원하는 representation을 학습함.
* RBM 기반이면 이전 layer 출력의 확률분포를 모델링하고,
  autoencoder 기반이면 이전 layer 출력을 reconstruction하도록 학습함.

---

### 4.2 왜 도움이 되었는가

Erhan et al. (2010)은 unsupervised pretraining이 deep learning에 도움이 되는 이유를
크게 다음의 두 가지로 설명함.

* 첫째, optimization 효과임.

  * pretraining은 parameter를 완전히 random한 위치에서 시작하지 않게 함.
  * 즉 supervised fine-tuning이 더 좋은 basin of attraction에서 시작되도록 도와줌.

```text
Random initialization
        ↓
불리한 parameter region에서 학습 시작 가능

Unsupervised pretraining
        ↓
데이터 분포를 어느 정도 반영한 parameter region에서 학습 시작
```

* 둘째로 regularization 효과임.

  * Unlabeled data의 구조를 반영한 representation에서 출발하므로,
  * labeled data가 적을 때 overfitting을 줄이고 generalization을 높이는 효과가 있음.
  * 즉 unsupervised pretraining은 단순히 optimization만 돕는 것이 아니라,
    data distribution을 반영한 inductive bias를 제공한다고 볼 수 있음.

---

---

## 5. 대표적인 고전적 기법

### 5.1 RBM / DBN

`Restricted Boltzmann Machine`은 visible layer와 hidden layer로 구성된 확률적 에너지 기반 생성 모델(probabilistic energy-based generative model)이며, 여러 RBM을 층별로 쌓아 Deep Belief Network(DBN)를 구성할 수 있음.

* RBM은 visible unit과 hidden unit 사이에는 연결이 있지만,  
  같은 layer 내부의 unit들 사이에는 연결이 없는 bipartite 구조를 가짐.
* RBM은 energy function을 기반으로 데이터의 분포를 학습함.

앞서 말한대로 여러 RBM을 layer-wise로 쌓으면 Deep Belief Network가 됨.

이후 마지막에 classifier를 붙이고 labeled data로 fine-tuning함.

```text
pretrained DBN → classifier head → supervised fine-tuning
```

DBN은 2006년 전후 deep network를 실제로 학습 가능하게 만든 대표적인 초기 사례로 평가됨.

다만 오늘날에는 거의 사용되지 않음. 

* RBM 기반 학습은 계산 비용이 크고 구현이 복잡하며, contrastive divergence 같은 근사 추론 과정이 필요해 학습이 불안정할 수 있음. 
* 또한 Xavier/He initialization, ReLU 계열 activation, Batch Normalization, Residual Network 등의 발전으로 deep network를 random initialization에서 end-to-end로 직접 학습하는 것이 가능해졌기 때문임. 
* 그 결과 DBN의 핵심 장점이었던 layer-wise unsupervised pretraining의 필요성이 크게 감소하여 현재는 주로 역사적 의미를 갖는 기법으로 남아 있음.

---

### 5.2 Autoencoder

`Autoencoder`는 input을 압축한 뒤 다시 복원하도록 학습하는 neural network임.

구조는 다음과 같음.

$$
x \rightarrow \text{Encoder} \rightarrow z \rightarrow \text{Decoder} \rightarrow \hat{x}
$$

대표적인 reconstruction loss는 다음과 같음.

$$
\mathcal{L}_{\text{rec}} = \lVert x - \hat{x} \rVert^2
$$

Unsupervised pretraining에서 중요한 점은 decoder가 아니라 encoder임.

* Pretraining 후에는 decoder를 제거하고, 
* encoder를 feature extractor 또는 supervised model의 초기값으로 재사용함.

```text
Pretraining:
x → Encoder → z → Decoder → x_hat

Transfer:
x → Encoder → z → Task Head → y_hat
```

즉 autoencoder 기반 unsupervised pretraining의 핵심은

* reconstruction 자체가 아니라 
* reconstruction을 통해 학습한 representation을  
  downstream task에 재사용하는 것임.

---

---

### 5.3 Denoising Autoencoder

`Denoising Autoencoder`는 input에 noise를 추가한 뒤,
원래 input을 복원하도록 학습함.

$$
\tilde{x} = x + \epsilon \\
\tilde{x} \rightarrow \text{Encoder} \rightarrow z \rightarrow \text{Decoder} \rightarrow \hat{x} \\
\mathcal{L}_{\text{rec}} = \lVert x - \hat{x} \rVert^2
$$

일반 autoencoder는 input을 그대로 복사하는 identity mapping을 배울 위험이 있음.

Denoising autoencoder는 

* 2008년 Vincent et al.에 의해 제안된 기법으로, 
* noise가 섞인 input에서 원래 input을 복원해야 하므로,
* 더 robust한 representation을 학습하도록 유도함.

이 점에서 현대 self-supervised learning의 pretext task와 유사한 부분이 있음.

다만 역사적으로는 self-supervised learning이라는 용어가 널리 정착되기 전의
고전적 unsupervised pretraining 기법으로 분류하는 것이 자연스러움.

---

---

### 5.4 Contractive Autoencoder

`Contractive Autoencoder`는 2011년 Rifai, Vincent, Muller, Glorot, Bengio가 제안한 모델로, 기본적인 autoencoder를 기반으로 하며 reconstruction loss에 encoder의 Jacobian penalty를 추가함.

$$
\lVert x - \hat{x} \rVert^2
+
\lambda \lVert J_f(x) \rVert_F^2
$$

여기서 

* $J_f(x)$는 encoder $f$의 Jacobian임.
* 이 penalty는 input이 조금 변해도 representation $z$가 크게 변하지 않도록 유도함.

즉 input의 작은 perturbation에 둔감한 representation을 학습하도록 만드는 방식임.

* Denoising autoencoder가 noise를 직접 넣어서 robust representation을 유도한다면,
* contractive autoencoder는 Jacobian penalty를 통해 이를 명시적으로 제약함.

---

---

## 6. GAN과 Diffusion Model은 어디에 위치하는가

GAN과 Diffusion Model은 각각 2014년(GAN, Goodfellow et al.)과 2015년(Diffusion Probabilistic Model의 초기 형태, Sohl-Dickstein et al.)에 처음 제안된 생성 모델 계열로, 일반적으로 unsupervised learning 또는 generative modeling에 속함.

이들의 학습 과정에서 얻은 discriminator feature, encoder representation, 또는 backbone을 downstream task에 재사용하는 경우에는 unsupervised pretraining으로 활용될 수 있음.

주의할 점은 이들이 항상 unsupervised pretraining인 것은 아님.

### 6.1 GAN

GAN은 generator와 discriminator를 adversarial objective로 학습함.

```text
Generator:
z → fake sample

Discriminator:
x → real / fake
```

* GAN 학습 자체는 human label을 사용하지 않으므로 unsupervised learning으로 분류할 수 있음.
* 하지만 GAN을 학습해 image generation만 수행한다면, 이는 transfer learning도 아니고 unsupervised pretraining도 아님.

반면 DCGAN (Radford et al., 2015)처럼 discriminator의 중간 layer를 feature extractor로 재사용하면, 이는 넓은 의미의 unsupervised pretraining으로 볼 수 있음.

```text
Unlabeled images
        ↓
GAN training
        ↓
Discriminator feature
        ↓
Downstream classification
```

즉 GAN은 다음처럼 구분해야 함.

| 경우 | 분류 |
| :---: | :---: |
| GAN으로 image generation만 수행                      | unsupervised learning    |
| GAN discriminator feature를 downstream task에 재사용 | unsupervised pretraining |

---

### 6.2 Diffusion Model

Diffusion model은 Sohl-Dickstein et al. (2015) 이후 발전한 생성 모델 계열로, 

* noise를 점진적으로 추가하고 
* model이 noise 또는 denoised sample을 예측하도록 학습하는 
* generative model임.

간단히 쓰면 다음 구조임.

$$
x_0 \rightarrow x_t \\
x_t \rightarrow \epsilon
$$

여기서 

* $x_t$는 noise가 추가된 sample이고,
* $\epsilon$은 추가된 noise임.

Diffusion model도 human label을 사용하지 않고 학습할 수 있으므로  
unsupervised learning 또는 generative modeling으로 볼 수 있음.

주의할 점:

* diffusion model을 학습한 뒤 
* 그 encoder, representation, backbone을 
* 다른 downstream task에 재사용할 때에만 
* unsupervised pretraining이라고 부르는 것이 적절함.

즉 diffusion model도 GAN과 마찬가지로 다음처럼 구분해야 함.

| 경우                                                    | 분류                                          |
| :---: | :---: |
| Diffusion model로 sample generation만 수행                | unsupervised learning / generative modeling |
| Diffusion model의 representation을 downstream task에 재사용 | unsupervised pretraining                    |

---

## 7. 오늘날 고전적 Layer-wise Pretraining이 줄어든 이유

2006년 전후에는 deep network를 random initialization에서 아무런 사전학습 없이 곧바로 end-to-end supervised learning으로 학습시키기 어려웠음. 

* hidden layer가 깊어질수록 
* gradient vanishing/exploding 문제가 심해졌고, 
* optimization이 불안정하여 
* 깊은 hidden layers 에서 기대되는 충분한 성능을 얻기 어려운 경우가 많았음.

하지만 이후 다음 기법들이 등장하면서 상황이 달라졌음.

| 문제  | 대표적 해결책  |
| :---: | :---: |
| vanishing/exploding gradient        | Xavier initialization (2010), He initialization (2015),<br/>ReLU (2010) 및 ReLU 계열 activation |
| internal covariate shift 및 학습 불안정   | Batch Normalization (2015) |
| layer가 깊어질수록 optimization이 어려워지는 문제 | Residual connection (2015) |
| overfitting                         | dropout (2014), data augmentation, regularization                                        |
| 계산 자원 부족                            | GPU, distributed training  |

위의 기법들이 발전하면서
deep network를 random initialization에서 end-to-end로 학습하는 것이 가능해짐.

그 결과 고전적인 greedy layer-wise unsupervised pretraining은
현재 실무에서는 거의 쓰이지 않음.

즉 다음 방식은 더 이상 주류가 아님.

```text
Layer 1 pretraining
        ↓
Layer 2 pretraining
        ↓
Layer 3 pretraining
        ↓
Supervised fine-tuning
```

대신 현재는 다음 방식이 주류임.

```text
Large unlabeled data
        ↓
End-to-end self-supervised pretraining
        ↓
Downstream fine-tuning
```

> 여기서 `end-to-end`란  
> 
> * 각 layer를 따로 순차적으로 pretraining하는 것이 아니라,  
> * 전체 network의 parameter를 하나의 objective로 동시에 최적화한다는 의미임.

오늘날에는 

* 고전적인 layer-wise pretraining처럼 각 layer를 순차적으로 하나씩 학습하기보다는, 
* 입력부터 마지막 layer까지 순전파한 뒤 loss를 계산하고, 
* 그 loss의 gradient를 backpropagation으로 모든 layer에 전달하여 
* 전체 network를 end-to-end로 동시에 학습하는 것이 일반적임.

---

---

## 8. Self-supervised Learning과의 관계

`Self-supervised learning`은 2010년대 중반 이후 representation learning 연구가 발전하면서 본격적으로 주목받기 시작한 학습 패러다임임.

* 특히 2018년 BERT, 2020년 SimCLR 등의 성공 이후 NLP와 Computer Vision 분야의 핵심 pretraining 방법으로 자리 잡았음.
* 개념적으로는 data 자체에서 target을 자동으로 만들어 representation을 학습하는 방식임.

즉 human label은 없지만, 학습 형식은 supervised learning과 비슷함.

예를 들어 2018년에 발표된 BERT의 masked language modeling은 다음과 같음.

```text
Original sentence:
The cat sat on the mat.

Input:
The cat sat on the [MASK].

Target:
mat
```

여기서 `mat`은 사람이 붙인 label이 아니라 원래 문장에서 자동으로 얻은 target임.

GPT의 next-token prediction은 

* 2018년 GPT-1 발표 이후 대표적인 self-supervised learning 방식으로 자리잡았으며, 
* 원리는 BERT와 마찬가지로 데이터 자체에서 학습 목표를 생성한다는 점에서 동일함.

```text
Input:
I love machine [      ]

Target:
learning
```

SimCLR은 2020년에 제안된 self-supervised learning 기법으로, 

* 같은 image에서 만든 두 augmented view는 가깝게, 
* 다른 image에서 만든 view는 멀게 학습함.

```text
same image → similar representation
different image → different representation
```

이처럼 self-supervised learning은 다음 성격을 동시에 가짐.

| 관점 | 설명 |
| --- | --- |
| label 관점     | human label을 사용하지 않으며, target은 데이터 자체로부터 자동 생성됨 |
| objective 관점 | input-target 구조가 있으므로 supervised-like 학습임 |
| transfer 관점  | downstream task에 fine-tuning되는 경우 transfer learning의 한 사례가 됨 |

> 따라서  
> self-supervised pretraining은
> 넓은 의미의 unsupervised pretraining에 포함될 수 있음.

하지만 둘을 완전히 같은 말로 쓰면 안 됨.

* self-supervised pretraining은 고전적 unsupervised pretraining에는 RBM처럼 $p(x)$ 자체를 modeling하는 방식도 포함됨. 
* 이런 방식은 명시적인 pretext task나 self-generated target을 갖지 않으므로 self-supervised learning이라고 부르기 어렵기 때문임.

따라서 가장 정확한 관계는 다음과 같음.

```text
Self-supervised pretraining ⊂ 넓은 의미의 Unsupervised pretraining

하지만

Self-supervised learning ≠ Unsupervised pretraining 전체
```

즉 self-supervised pretraining은

* 오늘날 unsupervised pretraining을 구현하는 주류 방식이지만,
* unsupervised pretraining 전체와 동일한 개념은 아님.

---

---

## 9. Semi-supervised Learning과의 관계

`Semi-supervised learning`은 algorithm이 아니라 data 구성상의 problem setting임.

즉 labeled data와 unlabeled data가 함께 주어지는 상황을 의미함.

$$
\mathcal{D} = \mathcal{D}_L \cup \mathcal{D}_U
$$

여기서 

* $\mathcal{D}_L$은 labeled dataset이고,
* $\mathcal{D}_U$는 unlabeled dataset임.

Unsupervised pretraining은 이 setting을 해결하는 한 방법이 될 수 있음.

```text
Unlabeled data
        ↓
Unsupervised pretraining
        ↓
Pretrained model

Labeled data
        ↓
Fine-tuning
        ↓
Target task model
```

즉 다음처럼 구분해야 함.

```text
Semi-supervised learning
= labeled data와 unlabeled data가 함께 주어지는 problem setting

Unsupervised pretraining
= 그 setting을 해결하기 위해 사용할 수 있는 procedure
```

둘은 같은 분류 축에 있는 개념이라고 보기 어려움.

**예제:**

* DBN을 unlabeled data로 pretraining하고, 소량의 labeled data로 fine-tuning하면 semi-supervised learning setting을 푸는 방법이 됨.
* 마찬가지로 BERT를 unlabeled corpus로 pretraining하고, labeled sentiment dataset으로 fine-tuning하면 self-supervised pretraining을 활용한 semi-supervised learning setting으로 볼 수 있음.

> 다만  
> zero-shot evaluation처럼 labeled data를 전혀 사용하지 않는 경우는  
> semi-supervised learning이라고 보기 어려움.

---

---

## 10. 전체 관계 정리

전체 관계는 다음과 같이 정리할 수 있음.

```text
Transfer Learning
│
├─ Supervised Pretraining
│  └─ ImageNet classification → medical image classification
│
└─ Unsupervised Pretraining
   │
   ├─ Classical Unsupervised Pretraining
   │  ├─ RBM / DBN
   │  ├─ Autoencoder
   │  ├─ Denoising Autoencoder
   │  └─ Contractive Autoencoder
   │
   ├─ Generative Model 기반 Feature Pretraining
   │  ├─ GAN discriminator feature reuse
   │  └─ Diffusion representation reuse
   │
   └─ Self-Supervised Pretraining
      ├─ BERT masked language modeling
      ├─ GPT next-token prediction
      ├─ SimCLR contrastive learning
      └─ MAE masked image reconstruction
```

각 개념의 차이점은 다음과 같음.

| 개념 | 차이점  |
| --- | --- |
| `Unsupervised Learning`    | human label 없이 데이터의 구조, 분포, representation을 학습하는 학습 방식이며,<br/>transfer를 반드시 포함하지는 않음                                                                                                       |
| `Unsupervised Pretraining` | human label 없이 먼저 representation 또는 parameter를 학습한 뒤,</br>이를 downstream task에 transfer하는 절차를 포함함                                                                                           |
| `Self-supervised Learning` | 데이터 자체에서 target을 생성하여<br/>supervised-like objective로 representation을 학습하는 방식임                                                                                                              |
| `Transfer Learning`        | source task/domain에서 얻은 지식을 target task/domain에 재사용하는 상위 전략이며,<br/>반드시 unlabeled data를 사용하는 것은 아님.<br/>예를 들어 ImageNet으로 supervised pretraining한 모델을<br/>다른 분류 문제에 재사용하는 경우도 transfer learning에 해당함 |
| `Semi-supervised Learning` | algorithm이 아니라<br/>labeled data와 unlabeled data가 함께 주어지는 problem setting임 |

---

---

## 11. 정리

* `Transfer Learning`은 source task/domain에서 얻은 지식을 target task/domain에 재사용하는 가장 상위의 전략임.
* `Pretraining`은 transfer learning의 대표적인 구현 방식이지만, transfer learning 전체와 같은 말은 아님.
* `Unsupervised Learning`은 human label 없이 데이터의 구조, 분포, representation을 학습하는 방식임.
* `Unsupervised Pretraining`은 human label 없이 먼저 representation 또는 parameter를 학습한 뒤, 이를 downstream task에 transfer하는 절차임.
* 고전적 unsupervised pretraining은 RBM, DBN, Autoencoder 등을 이용한 greedy layer-wise pretraining을 중심으로 발전했음.
* 이 방식은 deep network의 optimization과 regularization을 돕기 위해 등장했음.
* 오늘날에는 Xavier/He initialization, ReLU, batch normalization, residual connection 등의 발전으로 고전적 layer-wise pretraining은 거의 쓰이지 않음.
* 그러나 unlabeled data로 먼저 representation을 학습한 뒤 downstream task에 transfer한다는 아이디어는 사라지지 않았음.
* 현대에는 이 역할을 주로 self-supervised pretraining이 수행함.
* `Self-supervised Learning`은 데이터 자체에서 target을 자동 생성하여 supervised-like objective로 학습하는 방식임.
* Self-supervised pretraining은 넓은 의미의 unsupervised pretraining에 포함될 수 있지만, unsupervised pretraining 전체와 같은 말은 아님.
* `Semi-supervised Learning`은 labeled data와 unlabeled data가 함께 주어지는 problem setting이며, unsupervised pretraining은 그 setting을 해결하는 한 방법임.

---

## 참고문헌

* Hinton, G. E., Osindero, S., & Teh, Y. W. (2006). A fast learning algorithm for deep belief nets. *Neural Computation*, 18(7), 1527-1554.
* Bengio, Y., Lamblin, P., Popovici, D., & Larochelle, H. (2007). Greedy layer-wise training of deep networks. *NeurIPS 19*, 153-160.
* Erhan, D., Manzagol, P. A., Bengio, Y., Bengio, S., & Vincent, P. (2009). The difficulty of training deep architectures and the effect of unsupervised pre-training. *AISTATS*, 153-160.
* Erhan, D., Bengio, Y., Courville, A., Manzagol, P. A., Vincent, P., & Bengio, S. (2010). Why does unsupervised pre-training help deep learning? *JMLR*, 11, 625-660.
* Vincent, P., Larochelle, H., Bengio, Y., & Manzagol, P. A. (2008). Extracting and composing robust features with denoising autoencoders. *ICML*.
* Rifai, S., Vincent, P., Muller, X., Glorot, X., & Bengio, Y. (2011). Contractive auto-encoders: Explicit invariance during feature extraction. *ICML*.
* Radford, A., Metz, L., & Chintala, S. (2015). Unsupervised representation learning with deep convolutional generative adversarial networks. *arXiv:1511.06434*.
* He, K., Zhang, X., Ren, S., & Sun, J. (2015). Deep residual learning for image recognition. *arXiv:1512.03385*.
* Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of deep bidirectional transformers for language understanding. *NAACL-HLT*.
* Chen, T., Kornblith, S., Norouzi, M., & Hinton, G. (2020). A simple framework for contrastive learning of visual representations. *ICML*.
