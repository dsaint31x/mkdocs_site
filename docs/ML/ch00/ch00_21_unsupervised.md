# Unsupervised Learning

Labeling이 필요없는 ML로서 최근들어 중요성이 더욱 커지고 있는 분야임.

사람이 추가해주는 ^^`label` 데이터가 없으며, 
ML이 데이터에서 알아서 내재된 특징(feature vector, representation)들을 추출^^ 하여 Task를 수행한다.

![](../img/ch00/tSNE_MNIST.png){width="400"}

* MNIST 데이터에서 lable없이 unsupervised learning으로 clustering을 수행한 결과임 (t-SNE).

---

## 주요 Task

Unsupervised Learning 으로 해결하고자 하는 ^^주요 task^^ 는 다음과 같다.

`Clustering`
: input date의 sample들의 내재적인 특징(feature)를 추출하여, 비슷한 sample들끼리 하나의 cluster로 묶는 task.

`Dimensionality Reduction`
: ML에서 사용되는 data들은 일종의 vector로 표현되는데, 이때 해당 vector들이 놓여지는 vector space의 공간의 차원수를 dimesnion이라고 부른다(쉽게 말하면 숫자 4개로 구성된 vector는 4차원의 공간에서의 한점을 나타내므로 차원수가 4차원이라고 할 수 있다.).  
다차원의 데이터들은 `cusrse of dimension`과 같은 문제점이 있기 때문에 가지고 있는 ^^information의 소실을 최대한 막고 dimension을 축소^^ (=compression)해야하는 경우가 많으며 이를 수행하는 task를 `Dimensionality reduction`이라고 부른다.

* `(Data) Visualization` : `Dimensionality reduction`에서 ^^target dimension을 2 또는 3 차원으로 한 경우^^ 로, data들의 분포의 특징등을 시각적으로 잘 나타내는 task 또는 application을 지칭.  
ML 또는 Data Mining으로 찾아낸 데이터들의 특성 또는 분포를 2차원의 chart (보통 scattergram)로 표현하여 ^^데이터에 대한 insight를 제공^^ 하는데 사용됨.

`Anomaly detection` (or `novelty detection`, `odd detection`)
: Training data에 있는 sample과 다른 특성을 가지는 sample (outliar, odd)들을 탐지하는 task.  
일반적으로 ^^training data에는 outliar가 없다고 생각하고 학습^^ 하고, 새로 주어진 data sample이 기존의 training data와 같은지 아니면 outlier인지를 구분한다.

![](../img/ch00/anomaly_detection.png){width="400"}

`Manifold Learning`
: 학습 데이터들에 내재된 ^^manifold를 모델링(or extraction)^^ 하는 task를 가르킴.  
Deimensionality Reduction과 Representation Learning들과 매우 밀접하게 연관되어 있다. 관점에 따라서는 `Dimensionality Reduction` 에 속하는 세부 분야라고도 볼 수 있다. 

## 대표적인 알고리즘들

* k-Means, k-Medoids
* Affinity Propagation Clustering
* Density-Based Spatial Clustering of Applications with Noise (DBSCAN)
* Hierarchical Cluster Analysis (HCA)
* One-calss SVM
* Isolation Forest
* Principal Component Analysis (PCA)
* Kernel PCA
* Locally Linear Embeding (LLE)
* t-Distributed Stochastic Neighbor Embedding (t-SNE)
* Apriori (Association Rule Learning)
* Eclcat (Association Rule Learning)

## Self-supervised Learning과의 차이.

Unsupervised learning의 경우, dataset에 내재되어있는 feature를 추출하는 데 초점이 보다 쏠려있는 것과 비교하여 self-supervised learning은 자체적으로 labeling을 수행하고 난 다음에 일반적인 supervised learning으로 해결하는 task를 수행하는 차이가 있다.

대부분의 self-supervised learning의 경우, unsupervised learning을 수행하고 얻은 knowledge를 final goal을 위한 supervised learning에 transfer하는 방식을 취한다. 즉, label이 전혀 없는 데이터를 이용하는 부분은 unsupervised learning과 같으나, 최종 task는 사실상 supervised learning의 task인 경우가 대부분이다.