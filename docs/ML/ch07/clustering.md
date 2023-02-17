# Clustering

feature space에서 가까운 sample들을 모아 하나의 cluster로 묶는 task.

* input : label이 되어있지 않은 training data
* output : 유사한 sample들이 묶여있는 cluster
* hyper-parameter : cluster 를 몇개 지정할지 (명시적으로 cluster의 수를 입력받는 경우도 있으나 간접적으로 이를 결정하는 값( self simialrity등)을 요구하기도 함)를 보통 hyper-parameter로 요구.

Unspervised Learning의 대표적인 Task임.

> 일부 문헌에서는 unsupervised learning의 task중에서 특정 application에 상관없이 unsupervised learning algorithm이 해결해야하는 ***general task*** 로서 clustering과  density estimation, dimension transformation을 언급한다.

## k-Means

https://scikit-learn-extra.readthedocs.io/en/stable/modules/cluster.html#k-medoids

k-means는 클러스터에 속한 멤버의 평균값을 cluster center로 합니다.


## Affinity Propagation Clustering

Ref.: [Brendan J. Frey et al., “Clustering by Passing Messages Between Data Points”, Science Feb. 2007](https://utstat.toronto.edu/reid/sta414/frey-affinity.pdf)

각 데이터 샘플들이 서로에게 메시지를 보내면서 일종의 투표를 수행하여 자신의 대표가 될 수 있는 데이터 샘플을 선택하여, 선택된 데이터 샘플을 중심으로 하여 다양한 크기의 cluster 가 생성되는 기법.

단점은 계산 복잡도로 $O(N^2T)$
를 가짐. 여기서 $N$은 샘플 수, $T$는 알고리즘 반복 횟수이다. 공간복잡도는 O(N^2)
​​​​이다. 매우 복잡도가 높기 때문에 작은 데이터에 적합하다.

모든 데이터 샘플 간에 similarity를 계산하고 이를 기반으로 각 샘플  pair 에서 responsibility $r_{ik}$와 availability $a_{ik}$를 계산 (이들을 메시지를 보내는 것으로 표현)하고 이들로 구성된 2개의 matrix를 반복적으로 업데이트하여 clustering을 수행함.

> k-Means와 마찬가지로 클러스터 형태가 둥글어야 하는(globular) 가정에 기반하고,  k-medoids와 동일하게 cluster center를 data point 자체(exemplar)를 사용한다. 

> k-Means는 Not-flat geometry ( 데이터가 존재하는 부분 공간이 선형이 아닌 굽어져 있는 경우) 공간처럼 euclidean distance를 쓰기 어려운 경우에는 성능이 그리 좋지 않음 반면, AP는 nearest-neighbor graph여서 보다 나은 것처럼 scikit-learning에선 언급되고 있으나, 역시 높은 성능은 아닌 듯 하다.

## similarity 계산

sample $i$와 $j$의 similarity는 다음과 같은 Euclidean distance의 제곱에 음수를 취한 것임.

$$
s_{ik}= \|\textbf{x}_{i}-\textbf{x}_{j}\|^2_2
$$

여기서 $s_{kk}$는 위의 식으로는 0이지만, hyper-parameter로 주어진다. 0보다 작은 음수값으로 주어지면 이 값이 작을수록 결과로 나오는 cluster의 수가 적어지게 된다.

> # of cluster를 명시적으로 설정하지 않고, $s_{kk}$를 통해 결과에서 나오는 cluster 수를 제어한다.  

보통 similarity matrix의 최소값으로 설정되지만, median, 또는 maximum으로 설정될 수 있음 (커질수로 cluster수가 증가)



## responsibility 계산

>  sample $\textbf{x}_k$
​​​​​가 sample $\textbf{x}_i$
​​​​​에 대해 얼마나 exemplar로 적합한지를 나타냄.

responsibility $r_{ik}$는 sample $\textbf{x}_i$를 기준으로 하여 sample $\textbf{x}_k$ 가 sample $\textbf{x}_i$의 대표가 되어야 하는 ^^정량적 근거(sklearn 에선 the accumulated evidence라고 기술)^^ 를 구한 것으로 sample $\textbf{x}_i$를 기준으로 target sample $\textbf{x}_k$ 와의 simialarity와  target sample $\textbf{x}_k$를 제외한 나머지 sample들간의 affinity를 고려한다.

식은 다음과 같다.

$$
r_{ik}=s_{ik}-\underset{k^\prime \ne k}{\max}(a_{ik^\prime}+s_{ik^\prime})
$$

responsibility $r_{ik}$는 

* sample $\textbf{x}_i$와 sample $\textbf{x}_k$간의 similarity가 높을수록 커지고,
* sample $\textbf{x}_i$가 다른 sample $\textbf{x}_{k^\prime}$과 affinitiy, $(a_{ik^\prime}+s_{ik^\prime})$가 클수록 작아진다.
* 즉 sample $\textbf{x}_i$ 주변에 exemplar로 적합한 sample $\textbf{x}_k^\prime$ 이 있다면, sample $\textbf{x}_k$ 는 $\textbf{x}_i$에 대해 낮은 responsibility를 가진다. 
* responsibility $r_{ik}$가 양수이면서 커지면, sample $\textbf{x}_k$ 가 대표가 될 가능성이 커짐.

responsibility $r_{ik}$는 responsibility matrix를 생성한다.

## availability 계산

availability $a_{ik}$는 sample $\textbf{x}_k$를 기준으로 하여 sample $\textbf{x}_i$ 에게 본인이 대표가 되어야 하는 정량적 근거를 구한 것이다. 이는 sample $\textbf{x}_k$과 자신을 제외한 다른 sample들로부터 responsibility를 다 더한 값과 0중에서 작은 값에 해당한다 (대부분 음수).

$$
a_{ik}=\min \left(0, r_{kk}+\sum_{i^\prime \notin \{i,k\}}\max(0,r_{i^\prime k}) \right) 
$$

 $r_{kk}$ 는 자기자신의 대표성에 해당한다.

 $$
 a_{ㅏk}=\sum_{i^\prime = i,k}\max(0,r_{i^\prime k})
 $$

## 순서

0. responsibility matrix 와 availability matrix 를 모두 0으로 초기화
1. similarity matrix계산
2. responsibility matrix 계산
3. availability matrix 계산
4. responsitibility matrix 와 availability matrix가 수렴할 때까지 2,3번 반복.
5. responsitibility matrix 와 availability matrix를 더해 criterion matrix를 계산하고 주대각성분 $r_{kk}+a_{kk}$ 가 0 이상이 sample $\textbf{x}_k$가 cluster의 대표가 된다.

## sklearn.cluster.AffinityPropagation

* Gist's [ipnb파일](https://colab.research.google.com/gist/dsaint31x/9aba90db977631aa1d2776623b16a1ec/ml_affinity-propagation-clustering-algorithm.ipynb)

### Hyper-parameters

`Preference`
: 각 data point들이 얼마다 exemplar로 선택될 가능성이 높은지를 지정하는 것으로, 높은 값을 부여할수록 더 많은 data point들이 exemplar가 되어서 그 결과 작은 클러스터가 더 많이 생기게 됩니다. 반대로 preference가 작을수록, 적은 수의 사이즈가 큰 클러스터가 만들어지는 경향이 있습니다.

> Preference는 위의 수식에서 Similarity Matrix의 main diagonal $s_{kk}$을 가르키고 있음.

**Damping factor** $\lambda$
: 반복되는 Responsiblity Matrix와 Availability Matrix를 업데이트에서 Damping factor는 Exponential weighted average를 적용할 때 필요한 hyper parameter임. Exponential weighted average를 적용하여 noise에 좀 더 robust하게 해주며, 동시에 값들이 numerical oscillations (진자현상)을 보이지 않도록 막아줄 수 있다. 적절한 damping factor를 지정할 경우 보다 빨리 그리고 안정적으로 수렴하게 됨.

$$
r_{t+1}(i, k) = \lambda\cdot r_{t}(i, k) + (1-\lambda)\cdot r_{t+1}(i, k) \\
a_{t+1}(i, k) = \lambda\cdot a_{t}(i, k) + (1-\lambda)\cdot a_{t+1}(i, k)
$$

## Summary

정리
이상으로 Affinity Propagation 클러스터링 알고리즘에 대해서 살펴봤습니다. Scikit-learn 문서에서 k-Means 다음에 소개될 정도로 비중이 있어 보이지만, 자주 쓰일 것 같지는 않습니다. 그 이유로는,

k-Means와는 다르게 k를 지정하지 않아도 된다는 장점이 있지만, 반대급부로 preference를 잘 조정해야 합니다. 그리고 k-Means에서 k를 결정하는 문제는 효과적인 heuristic 한 방법이 있기 때문에 큰 문제가 되지는 않습니다.

이어서, 클러스터의 경계를 나눌 때는 k-Means처럼 centroid 사이의 가운데 지점을 기준으로 나누는 것이 아닌, 각 클러스터의 크기와 주변 점들과의 affinity를 고려해서 클러스터 경계를 나누기 때문에 때에 따라서 더 좋은 결과를 가져올 때가 있지만, 그로 인해 사용하기에 좀 더 어려워집니다.

마지막으로 사실 클러스터링 문제는 data point 간의 distance를, 즉 metric을 어떻게 정의하느냐가 성능을 가장 크게 좌우하기 때문에 좀 더 간단하고 직관적인 알고리즘이 때로는 문제를 풀 때 더 효과적인 것 같습니다.

## References

* scikit-learn [2.3. Clustering](https://scikit-learn.org/stable/modules/clustering.html)
* Cory Maklin's [Affinity Propagation Algorithm Explained](https://towardsdatascience.com/unsupervised-machine-learning-affinity-propagation-algorithm-explained-d1fef85f22c8)
* 아이리스's [7.55 R에서 Affinity Propagation 군집분석 실시하기
(https://blog.naver.com/PostView.naver?blogId=pmw9440&logNo=222297976432&parentCategoryNo=&categoryNo=7&viewDate=&isShowPopularPosts=true&from=search)
* [Affinity Propagation 살펴보기](https://jaehc.github.io/ml/affinity-propagation/)