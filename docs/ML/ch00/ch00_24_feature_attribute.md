# 관련 용어들

## Feature

ML에서 feature는 data sample이 가지고 있는 한가지 특징이라고 할 수 있다.  

보통 

* training dataset은 여러 data sample (혹은 data point)들로 구성되며, 
* 각각의 data sample은 여러 features(특징들)로 구성된다.

ML에서는 ***하나의 data sample을 vector로 표현*** 하게 된다 (참고로 vector란 숫자들의 ordered list이다.) 

* 이 경우, vector를 이루는 각 숫자 하나 하나가 해당 data sample이 가지고 있는 feature라고 생각할 수 있다. 
* 예를 들어, 한 학생을 나타내는 data sample은 나이, 학번, 몸무게, 성적을 나타내는 4개의 숫자로 구성된 vector로 표시될 수 있다. 
* 이 경우 feature가 4개이다.

Dataset은 흔히 matrix로 표현된다. 

* 일반적으로 row는 data sample에 해당하며, 
* column은 data sample이 가지고 있는 각각의 feature에 해당한다.

---

## Feature 와 Attribute의 차이

`Attribute`는 dataset에서 나타내는 column의 종류(or `type`)를 가리킬 때 많이 사용된다. 

* 앞서 예에서 나이, 학번, 몸무게, 성적 과 같은 column의 title이 
* 바로 attribute라고 불린다.

반면, `feature`는 

* 해당 `type`을 가리키는데 사용되기도 하지만, 
* 특정 data sample의 `해당 type에 할당된 value`를 가리키는데에도 사용된다. 

요약하면 attribute는 type만을 가리킬 때 사용되며, feature는 type과 value를 둘 다 가리킬 수 있다. 하지만 많은 경우 혼재되어 사용되므로 context에 맞춰 해석해야한다.

---

## Feature vector와 representation

### Representation:

* 데이터가 모델 내부에서 표현되는 방식 전반을 의미: **데이터 표현 전반** 을 가리킴!!
    * raw feature, engineered feature, hidden embedding, latent feature, embedding 등을 모두 가리킬 수 있음. 
* 특히, Task에 유용한 특징을 담고 있는 벡터 (latent feature, embedding 등)를 가리킴.
* 딥러닝, classical ML 모두에서 사용되는 포괄적 개념

### Feature Vector:

* 특정 시점에서 모델 입력으로 사용되는 수치 벡터
* Classical ML에서는 feature engineering, feature extraction 후 얻어진 벡터를 가리키는 경우가 많음
* Deep Learning에서는 학습 과정에서 자동으로 얻어지는 hidden representation을 feature vector라 부르기도 함

> **참고**
>
> Deep Learning
> 
> * Raw data(이미지, 음성, 텍스트 등)를 직접 입력으로 사용 가능
> * 네트워크 내부 layer가 representation learning을 수행하여 적절한 feature vector를 자동 추출
> * 예: CNN의 중간 계층 출력(feature map), Transformer의 hidden state
> 
> Classical ML
> 
> * Raw data를 직접 모델에 넣지 않음 : 차원의 저주 등의 이유로 인해서임.
> * feature extractor 또는 dimensionality reduction 기법을 통해 feature vector 생성
> * 이 feature vector를 학습 알고리즘(SVM, kNN, Random Forest 등)의 입력으로 사용

---

## Data sample과 Data point.

ML의 **Dataset은 여러 개의 data sample(or data instance)들의 집합**. 

* 하나의 data sample은 보통 feature vector로 표현됨.
* vector에서 ***해당 vector가 가지고 있는 숫자의 갯수 (number of elements)*** 를 `dimension` (차원)이라고 부르며, 
* 해당 vector는 ^^해당 차원수의 `vector space`에서의 한 point라고 정의^^ 할 수 있다.
* ML의 경우, real number로만 구성된 vector를 사용: $\mathbb{R}^n$ vector space사용.

쉬운 예로 3개의 숫자를 가진 vector는 3차원 공간에서의 특정 위치를 나타내는 position vector라고 생각할 수 있다 (물리시간에 배운 위치벡터를 생각해보자). 이는 3차원 이상의 다차원 벡터공간(=$\mathbb{R}^n$)으로 확장이 가능하다. 

* `vector space` $\mathbb{R}^n$ 는 일종의 vector들의 set이라고 봐도 된다 (vector addition과 scalar multiple과 같이 해당 set에 닫힌 연산들이 정의되고, 몇가지 axiom들을 만족해야하는 수학적 정의가 있긴 하지만, 일단 set이라고 해도 틀린 건 아님). 
* **참고 : [Vector Space의 정의](https://dsaint31.tistory.com/entry/Math-Definition-of-Vector-Space)

> 때문에, 하나의 data sample을 가리켜서 data point라고도 많이 애기하게 된다.

sample 이라는 용어가 경우에 따라서 dataset을 가리키기도 하므로,  
개별 데이터를 지칭할 때는 data point, data instance, sample point, sample instance 등의 용어도 자주사용된다.

---

## Target and Label

Supervised Learning에서 'target'과 'label'이라는 용어는 일반적으로 동의어로 취급됨.

* 두 용어 모두 모델이 예측하려는 목표 변수를 지칭하며, 
* 실제 값과 예측값을 비교하는 데 사용된다.

약간의 차이를 굳이 말한다면: 

* 'Target'은 주로 regression task에서 더 선호되는 용어로, 주로 연속적인 수치로 주어짐.
* 'Label'은 classification task에서 더 자주 사용되며, 많은 경우 categorical data임.

> 하지만 이러한 차이는 관행적인 것이며, 두 용어를 엄격히 구분하지 않고 사용하는 경우가 보다 많음.​​​​​​​​​​​​​​​​