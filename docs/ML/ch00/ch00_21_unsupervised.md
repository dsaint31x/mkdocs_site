# Unsupervised Learning

Labeling이 필요없는 ML로서 최근들어 중요성이 더욱 커지고 있는 분야임.

사람이 추가해주는 ^^`label` 데이터가 없으며, 
ML이 데이터에서 알아서 내재된 특징(feature vector, representation)들을 추출^^ 하여 Task를 수행한다.

<figure markdown>
![](../img/ch00/tSNE_MNIST.png){width="400" align="center"}
</figure>

* MNIST 데이터에서 label없이 unsupervised learning으로 clustering을 수행한 결과임 (t-SNE).

---

## 주요 Tasks

Unsupervised Learning 으로 해결하고자 하는 ^^주요 task^^ 는 다음과 같다.

`Clustering`
: input date의 sample들의 내재적인 특징(feature)를 추출하여, 비슷한 sample들끼리 하나의 cluster로 묶는 task.  

: * [Clustering (군집)](../ch07/clustering.md)
    * [Applications of Clustering](https://ds31x.blogspot.com/2023/08/ml-clustering.html) 


`Dimensionality Reduction`
: ML에서 사용되는 data들은 일종의 vector로 표현되는데, 이때 해당 vector들이 놓여지는 vector space의 공간의 차원수를 dimension이라고 부른다(쉽게 말하면 숫자 4개로 구성된 vector는 4차원의 공간에서의 한점을 나타내므로 차원수가 4차원이라고 할 수 있다.).  
다차원의 데이터들은 `curse of dimension`과 같은 문제점이 있기 때문에 가지고 있는 ^^information의 소실을 최대한 막고 dimension을 축소^^ (=compression)해야하는 경우가 많으며 이를 수행하는 task를 `Dimensionality reduction`이라고 부른다.

: * `(Data) Visualization` : `Dimensionality reduction`에서 ^^target dimension을 2 또는 3 차원으로 한 경우^^ 로, data들의 분포의 특징등을 시각적으로 잘 나타내는 task 또는 application을 지칭.  
ML 또는 Data Mining으로 찾아낸 데이터들의 특성 또는 분포를 2차원의 chart (보통 scattergram, scatter plot)로 표현하여 ^^데이터에 대한 insight를 제공^^ 하는데 사용됨.

`Outlier Detection` (이상치 탐지)
: 전체 데이터셋 내에서 비정상적인 패턴이나 관측치를 식별하는 task. 주요 특징은 ***전체 데이터로 모델 훈련*** 시키기 때문에 "훈련데이터셋"에 outlier(이상치)가 포함되어 있음. outlier는 샘플 수가 적으므로 대다수 샘플과 크게 차이가 나는 outlier 데이터 포인트를 분류하도록 훈련됨.

`Novelty Detection` (특이치 탐지)
: outlier detection과 매우 비슷한 task이지만, novelty detection은 "정상 데이터" 만으로 모델을 훈련시켜 이후 추론 단계에서 주어지는 데이터들의 정상 여부를 판단하는 task임. 특징은 ***정상 데이터만으로 모델 훈련*** 한다는 점으로 훈련단계에서 보지 못한 패턴의 데이터 (Novelty)을 감지하도록 훈련된다는 점임.


<figure markdown>
![](../img/ch00/anomaly_detection.png){width="400" align="center"}
</figure>

`Manifold Learning`
: 학습 데이터들에 내재된 ^^manifold를 모델링(or extraction)^^ 하는 task를 가르킴: [t-SNE](../ch07/tSNE.md) 가 대표적인 [Manifold Learning](../ch07/manifold.md)임. 
Dimensionality Reduction과 [Representation Learning](./ch00_00_intro.md#representation-learning-)들과 매우 밀접하게 연관되어 있다. 관점에 따라서는 `Dimensionality Reduction` 에 속하는 세부 분야라고도 볼 수 있다. 

## 대표적인 알고리즘들

* [k-Means, k-Medoids](https://dsaint31.me/mkdocs_site/ML/ch07/clustering/#k-means)
* [Affinity Propagation Clustering](https://dsaint31.me/mkdocs_site/ML/ch07/clustering/#affinity-propagation-clustering)
* [Density-Based Spatial Clustering of Applications with Noise (DBSCAN)](https://dsaint31.me/mkdocs_site/ML/ch07/clustering/#density-based-spatial-clustering-of-applications-with-noise-dbscan)
* [Hierarchical Clustering](../ch07/clustering.md#hierarchical-clustering)
* One-class SVM
* Isolation Forest
* [Principal Component Analysis (PCA)](../ch06/ml_pca.md)
* Kernel PCA
* Locally Linear Embedding (LLE)
* [t-Distributed Stochastic Neighbor Embedding (t-SNE)](../ch07/tSNE.md)
* Apriori (A Priori, Association Rule Learning)
* ECLAT (Equivalence Class Clustering and Bottom-Up, Association Rule Learning)

> Generative Adversary Networks (GAN)은 unsupervised learning에 속할까?

---

## Self-supervised Learning (of DL).

`Unsupervised learning` 은 **dataset에 내재되어있는 feature를 추출하는 데 초점** 이 보다 쏠려있음. 

이와 달리  
`Self-supervised learning`은 **자체적으로 labeling을 수행하고 난 다음에 일반적인 supervised learning으로 해결하는 task (= downstream task)를 수행** 하는 차이가 있다.

* 참고: [Self-supervised Learning 에 대한 보다 자세한 자료](./ch00_24_selfsupervised_learning.md)

즉, label이 전혀 없거나 일부 있는 데이터를 이용하는 부분(=pre-training)은 unsupervised learning(or semi-supervised learning)과 같으나, 최종 task는 사실상 supervised learning의 task인 경우가 대부분이다.


