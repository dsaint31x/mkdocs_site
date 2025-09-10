# Tree Growth

Decision Tree나 Boosting의 weak learner로 사용되는 Decision Stumps에서 Tree의 node들이 분할되는 방식을 Tree Growth라고 함.

크게 다음의 2가지로 나누어짐.

* Level-wise Growth
* Leaf-wise Growth

## Level-wise Growth

BFS (Breadth First Search) 처럼 Root에 인접한 node들부터 분할시키는 방식을 가리킴.

* Tree가 균형있는 모양으로 확장됨.

> Random Forest, XGBoost 등에서 사용됨.  

## Leaf-wise Growth

DFS (Depth First Search) 와 비슷한 순서로 node가 분할됨.

* cost function (or loss function)을 가장 급격하게 감소시키는 node부터 분할이 이루어지면서 확장.
* 불균일한 Tree 형태로 확장이 이루어진다.

> LightGBM 등에서 사용됨.

## 비교

Full Tree로 성장시키고 나면 Level-wise Growth나 Leaf-wise Growth나 같은 결과물에 도달하나, ML에선 일반적으로 Full Tree의 경우 과대적합이 되기 때문에 중간에 확장을 멈추게 됨.  

때문에 Tree Growth 의 차이에 따라 다른 모델이 된다.

Level-wise Growth가 좀 더 안정적이나 training에 resource (시간, memory 등)을 더 많이 요구하는 경향이 있음.
