# Supervised Learning

가장 전형적인 ML을 가르킨다. 

^^input data^^ 와 ^^`label` (or target)이라고 불리는 원하는 output^^ 에 해당하는 데이터로 구성된 pair들로   
training set과 test set을 가지고 있고 이를 통해 학습이 이루어진다. 

input-output의 pair들을 가지고 있기 때문에 input과 output의 relation을 ML이 파악하여 이를 mapping해주는 function을 approximation하는 것이라고 생각하면 된다.

![](../img/ch00/supervised.png){width="300" align="center"}

---

## 주요 Tasks **

Supervised Learning 으로 해결하고자 하는 ^^주요 task^^ 는 다음과 같다.

`Classification`
: Discrete한 category를 label로 가지면서, 특정 data sample에 대해 해당 category를 할당하는 task. exclusive하게 category가 할당될 수도 있지만, 여러 label이 하나의 data sample에 할당될 수도 있음.

![](../img/ch00/classification.png){width="400" align="center"}

`Regression`
: Continuous한 숫자값을 label로 가지는 경우로, 특정 data sample에 대해 해당 숫자값을 할당하는 task임. Statistics에서 regression model 등에서 유래된 이름으로, input을 dependent variable (or predictor)로, 그리고 output을 independent variable (or target)으로 생각하면 된다.

![](../img/ch00/regression.png){width="400" align="center}

> Regression에서 가장 단순한 형태는 `Linear Regression` (선형회귀)이며,  
> input과 output 간의 linear relationship을 찾아 modeling 함.  
> training dataset에서 가장 적합한 (= loss function이 가장 적은) parameters를 가지는  
> model을 만들고 training에 사용하지 않은 새로운 input에서도 가장 적합한 output을 구하는 것을  
> 목표로 한다. `linear`를 떼면 `Regression`이 되며, `linear`라는 제약조건이 없이 
> input과 output 간의 relation을 찾게 됨.

| | Classification | Regression |
|:---:|:---|:---|
|차이점 | output이 될 수 있는 값이 discrete하고 갯수가 고정됨. | output이 주로 continuous하며, 갯수가 무한대임. (range가 고정되는 경우가 일반적이나 반드시 그렇지는 않음) |
|대표적 model| kNN, SVM, Decision Tree | Regression Model, SVM |
|Example| Class명(=label) : 01(개), 10(고양이) / 결과값 : 개 또는 고양이(label 중 하나) | 성적 예측: range $[0,100]$ 내에서 어떤 값도 성적이 될 수 있음 |

참고로, novelty detection, dimensionality reduction 등의 Unsupervised Learning의 대표적 task들도 supervised learning으로 수행가능하다.

> classification과 regression이 supervised learning의 대표적인 task이나  supervised learning에 한정되진 않는다.

---

## 대표적인 알고리즘 (or Model)들.

* k-Nearest Neighbors
* Linear Regression
* Logistic Regression (← classification)
* Support Vector Machine
* Decision Tree
* Random Forest
* Artificial Neural Network
    * ^^Auto-encoder, Restricted Boltzmann Machine (RBM) 등은 `unsupervised`임^^ .
    * ^^Deep Belief Network (DBN) 등은 `semi-supervised`로 분류^^ 됨.
