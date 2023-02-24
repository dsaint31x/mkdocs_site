# Supervised Learning

가장 전형적인 ML을 가르킨다. 

^^inpute data^^ 와 ^^`label` (or target)이라고 불리는 원하는 output^^에 해당하는 데이터로 구성된 pair들로 training set과 test set을 가지고 있고 이를 통해 학습이 이루어진다. 

input-output의 pair들을 가지고 있기 때문에 input과 output의 relation을 ML이 파악하여 이를 mapping해주는 function을 approximation하는 것이라고 생각하면 된다.

![](../img/ch00/supervised.png)

## 주요 Task

Supervised Learning 으로 해결하고자 하는 주요 task는 다음과 같다.

`Classfication`
: Discerete한 category를 label로 가지면서, 특정 data sample에 대해 해당 category를 할당하는 task. exclusive하게 category가 할당될 수도 있지만, 여러 label이 하나의 data sample에 할당될 수도 있음.

![](../img/ch00/classification.png)

`Regression`
: Continuous한 숫자값을 label로 가지는 경우로, 특정 data sample에 대해 해당 숫자값을 할당하는 task임. Statistics에서 regression model 등에서 유래된 이름으로, input을 dependent variable (or predictor)로, 그리고 output을 independent variable (or target)으로 생각하면 된다.

![](../img/ch00/regression.png)

| | Classification | Regression |
|:---:|:---|:---|
|차이점 | output이 될 수 있는 값이 discrete하고 갯수가 고정됨. | output이 주로 continuous하며, 갯수가 무한대임. (range가 고정되는 경우가 일반적이나 반드시 그렇지는 않음) |
|대표적 model| kNN, SVM, Decision Tree | Regression Model, SVM |
|Example| Class명(=label) : 01(개), 10(고양이) / 결과값 : 개 또는 고양이(label 중 하나) | 성적 예측: range $[0,100]$ 내에서 어떤 값도 성적이 될 수 있음 |

참고로, novelty detection, dimensional reduction 등의 Unsupervised Learning의 대표적 task들도 supervised learning으로 수행가능하다.

## 대표적인 알고리즘들.

* k-Nearest Neighbors
* Linear Regression
* Logistic Regression (← classification)
* Support Vector Machine
* Decision Tree
* Random Forest
* Artficial Neural Network
    * Autoencoder, RBM 등은 unsupervised임.
    * DBN 등은 semi-supervised로 분류됨.
