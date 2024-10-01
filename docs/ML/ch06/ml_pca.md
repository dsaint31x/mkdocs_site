# Principal Component Analysis

Dataset에서 

1. variance를 최대로 보존하는 hyperplane을 찾고 
3. 해당 hyperplane에 data points를 projection하여 

feature vector의 dimensionality를 줄임.

> 아래에서도 나오지만, Linear Algebra의 Eigen Decomposition과 Singular Value Decomposition에 대한 이해를 하고 있다면 보다 쉽게 PCA를 이해할 수 있음.

---

## Cons. and Pros.

### Cons.

* PCA는 dataset에 linearity를 가정하고 있기 때문에 non-linear relation의 dataset에서는 좋은 성능을 기대하기 어려움.
    * Swiss roll등에서 PCA는 그리 좋은 성능을 보이지 못함.
* PCA는 target value (ex. class등)를 고려하지 않기 때문 (`unsupervised learning`)에 variance가 최대인 axis가 반드시 task를 수행하는데 필요한 data를 가장 잘 나타낸다는 보장이 없음.
* Principal component에 대한 해석이 쉽지 않음 (domain knowledge가 필요함).
* PCA를 수행하기 전에 반드시 standardization이 dataset에 이루어져야 함 (PCA는 dataset이 origin을 중심으로 분포한다고 가정하기 때문임).

### Pros.

* `Unsupervised Learning` : label (or target)에 상관없이 각각의 explanatory variable (feature vector의 한 element)들 간의 correlation을 이용하여 data loss가 가장 적은 dimensionality reduction이 가능함. 
* 가장 넓은 분야에서 기본적으로 사용되고 있는 dimensionality reduction 기법임. 

---

## PCA에서 찾아야하는 hyper-plane

* Dataset의 Variance를 최대로 보존.
* Data points를 해당 hyper-plane에 projection한 경우, raw data point와의 difference (ex. mean squared distance)가 최소임.
    * 달리 말하면, raw dataset에 가장 가까이 존재하는 hyper-plane을 찾는 것임.

PCA가 목표로하는 hyper-plane을 정의하고 있는 axis들이 바로 principal components임.

> 가장 variance가 큰 axis를 찾아 1st principal component로 삼고,  
> 해당 axis에 orthogonal한 axis 중에서 variance가 큰 axis를 찾아 2nd principal component로 삼는다.  
> 이를 원하는 수의 principal component를 찾거나, axis가 추가되면서 증가하는 cumulative explained variance가 원하는 수준(예를 들어 95%)에 도달하기까지 반복하는 것이  
> PCA라고 할 수 있다.

PCA를 linear transform으로 애기한다면, 

* 원래의 dataset $X$ (num of samples = num of rows, num of columns = num of features)를
* Principal axis들의 unit vectors 가 순서대로 column을 이루는 matrix $W$와 matrix multiplication을 수행 (=linear transform)하여
* reduced dataset $X_{\text{reduced}}$를 얻는 것임.

이는 Principal axis를 basis로 가지는 hyper-plane (or vector-space)에서 raw dataset $X$를 projection 하는 것이며, 얻어진 $X_{\text{reduced}}$는 principal axes의 coefficients로, principal axes를 basis로 하는 일종의 좌표로 projection의 결과 vector space의 data sample의 좌표임.

---

## PCA 수행 단계

1. Standardization (사실 zero-centered로만 전처리해도 됨.)
2. Covariance Matrix 계산
3. 이를 Eigen Decomposition 수행.
4. Eigen value가 큰 순으로 sorting한 eigen vectors를 구함.
5. 구해야하는 principal components의 수 만큼 상위 eigen vectors를 principal axes로 선정.

이를 다르게 표현하면,  
raw dataset인 matrix $X$를 SVD (singular value decomposition)을 수행 ($X=U\Sigma V^T$) 하여 얻은 $V$ matrix의 column vectors로 principal axes를 구할 수도 있음.

* $V$는 $X$의 row space의 orthonormal basis 임.
* 이를 PCA관점에서 Principal Matrix라고 부르기도 함.

---

## **참고자료** 

* [ipynb 예제](https://gist.github.com/dsaint31x/43049448ec3142fd8b6b156afd68dac5)
* [covariance와 centering에 대한 참고자료](https://dsaint31.tistory.com/278)

---

## 더 읽어보면 좋은 자료들

* ratgo's blog : [PCA](https://ratsgo.github.io/machine%20learning/2017/04/24/PCA/)
* ratgo's blog : [SVD와 PCA, 그리고 LSA](https://ratsgo.github.io/from%20frequency%20to%20semantics/2017/04/06/pcasvdlsa/)
