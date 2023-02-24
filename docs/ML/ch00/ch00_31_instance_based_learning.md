# Instance based Learning

ML의 learning system에서 generalization을 training dataset 그 자체로 구현하는 경우를 instance based learning이라고 한다.

어떤 일반화된 model 이나 function을 구하는 대신에, similarity 혹은 distance를 측정하는 metric fuction을 이용하여, 기존의 data point와의 유사도를 이용하여 prediction을 수행한다.

즉, ML system이 각각의 instance를 기억하고, 새로운 sample과의 similarity를 이용하여 prediction을 수행한다.

> 물론 모든 data sample이 아닌 대표적인 일부만을 기억하는 경우도 많다.

대표적인 알고리즘으로 k-NN이 instance based learning에 해당한다.

![](../img/ch00/instance_based_learning.png)

* 삼각형과 네모로 label이 붙은 training dataset을 기억함.
* 이후 x 표시의 새로운 data point가 주어졌을 때, k=3으로 3개의 가까운 이웃을 구하고, 이들의 다수에 해당하는 label로 prediction을 수행.

## Similarity

distance의 경우 수학적으로 몇가지 조건을 만족해야 한다. 그 중 기억할 부분이 symmetry를 가져야 한다. 만일 $d(x,y)$ 라는 binary operation이 distance를 구하는 function이 되려면,  $$(x,y) = d(y,x)$ 가 성립해야 한다.

Euclidean distance나 difference vector의 l-p norm을 이용한 function들은 대부분 distance로 사용가능하지만, probability distribution 등을 비교하는 Kullbeck-Leibler Divergence, Cross entropy들과 같은 경우엔 symmetry를 만족하지 못하는 경우도 많다. 

때문에 similarity라는 용어로 distance를 대체하는 경우, 상당수가 해당 metric이 symmetric 하지 않은 경우가 많다.

## Measure of Similarity 의 중요성.

비슷하다거나 동일하다는 개념은 우리에게 어떤 차이를 측정하는 measure가 필요함을 의미!!
 
- ML에서 input과 output은 주로 vector임. (ordered list of numbers)
- 이는 vector간의 difference 혹은 similarity를 측정하는 metric이 바로 similarity를 정량화한다는 것을 의미함. ←선형대수 (subtraction b/w vectors)
- 동시에 대상을 vector로 만들 때, subtraction이 가능한 scale이 되도록 해야함 ← word embeding등. 
    - [nominal scale](https://www.notion.so/0-1-Basic-Terminology-01-Probability-Statistics-e42372dd447b4db78a5a4e87a6ff6821)을 적용한 입력 vector에선 similarity의 정도를 구하기 어려움. 
    - nominal scale에서는 L-p norm 기반의 distance를 사용하기 적절치 않다.
    
- vector가 아닌 일종의 probability distribution으로 보는 경우라면, distribution의 difference를 구하는 cross-entroy, Kullbeck-Leibler Divergence등이 사용될 수도 있다.

