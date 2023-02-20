# Manifold and Manifold Learning

ML에서 manifold란, 고차원 공간에 내재된 저차원 공간(subspace)로 실제 dataset의 분포를 거의 다 포함(아닌 경우도 해당 subspace근처에 data들이 존재)하고 있는 것을 가르킴. 

> 수학적으로는 보다 엄격한 정의가 있으나... DL이나 ML을 하는 입장에서는 이 정도면 충분할 듯.


**Manifold 의 특징.**

- 일반적으로 nonlinear structure를 가짐.
- 하지만, 특정 data sample 근처의 좁은 영역 만으로 볼 경우엔 linearity를 가짐 (또는 linear하다고 approixmation할 수 있음.)

**ML 또는 DL 관점에서의 이해**

- Manifold는 feature extraction의 결과물이라고 볼 수 있음. 
- Manifold는 일반적으로 raw data space상에서 entangled 상태이므로 이를 disentangled로 바꾸는 transformer를 구하는 것이 바로 classifier 또는 data visualization이 하는 일임.

> A $d$-dimensional manifold is a part of an n-dimensional space (where $d \le n$) that locally resembles a $d$-dimensional hyperplane. 

## Manifold Learning

> Modeling the manifold on which the training instances lie; this is called Manifold Learning. 

Unsupervised learning의 일부분으로 다루어지는 경우가 많으며, Dimensional Reduction등에 많이 사용됨.

Manifold Learning은 다음의 두 가설에 의존한다. 

* 사실 다음의 2가설은 모든 machine learning에서의 prior로 사용되는 가설이다.
* supervised learning에서는 loss function의 특징을 규정하는데 사용됨.
* Unsupervised learning에서는 보다 명시적으로 아래 두 가설에 의존함.

## Mainfold Hypothesis

High Dimensional (Raw) Dataset은 ***하나 이상의 Manifold로 구성*** 되며, *모든 data sample들은 mainfold상 또는 manifold에 가깝게 위치* 하고 있다.

> Real-world data presented in high-dimensional spaces are expected to concentrate in the vicinity of a manifold $M$ of much lower dimensionality $d_M$, embedded in high-dimensional input space $R^d$. 
- Bengio et al. 2013

Data point 대부분이 Manifold 근처에 있다는 애기는 다음을 의미함.

> Probability density of data decreases very rapidly when getting away from the supporting maniflod.

Manifold hypothesis 가 성립한다고 가정하면, High diemsional dataset을 compressed (=lower dimensional) meaningful representation (=latent vector, code) 로 바꾸어 표현할 수 있다.

* compressed : lower dimensional
* meaningful : 모든 데이터가 maninfold 근처에 존재.
* representation : latent feature vector

### Smoothness Hypothesis

Dataset 에서의 data sample은 어떤 요인에 의해서 변화하는데, 해당 sample의 feature를 조금 변화가 이루어질 경우, 데이터의 feature space에서 매끄러운 곡면 (=mainfold)상에서 transition이 발생하게 된다. 

> Manifold follows naturally from continuous underlying factors (~ intrinsic manifold coordinate or features). Such continuous factors are part of a meaningful representation

![](../img/ch07/manifold_smoothness.png)

### Curse of High Dimensionality를 풀기위한 방법 : Manifold 찾기.

데이터의 space의 dimension 이 증가할 경우, 해당 space의 데이터 밀도를 유지하려면 훨씬 많은 datasample을 요구하는 것을 의미함.

Higher dimensional data 를 그대로 사용하면, 데이터 밀도가 낮아서 실제적인 data의 distribution을 찾는 probability distribution을 찾기 어려우나 meaningful manifold를 잘 찾아낸다면, 같은 데이터로도 충분히 probability distribution 을 찾아낼 수 있음.

대부분의 경우, lower dimensional representation이 ML등에서 task를 쉽게 풀 수 있도록 해준다 (이는 Mainfold hypothesis에 대한 implicit assumpation이라고 불림.). 하지만 아닌 경우도 있다. 

![](../img/ch07/manifold_learning.png)

* 왼쪽의 swiss roll의 경우, lower dimensional representation이 classification을 보다 쉽게 만든다.
* 하지만 오른쪽의 경우는 오히려 더 어렵게 만들 수도 있음을 보여준다 (이 경우 projection base method가 더 잘 동작). 

> Dimensional Reduction 방법은 크게 projection기반의 linear algorithm과 manifold learning기반의 non linear algorithm으로 나뉨.