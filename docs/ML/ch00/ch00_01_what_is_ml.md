# Machine Learning (ML)이란?

간단하게 말하면, ^^data로부터 computer가 학습(learning)을 하도록 프로그래밍하는 과학분야 또는 기술^^ 을 가리키는 용어임.

좀 더 풀어서 애기하면, 

* computer에게 기존의 알고리즘 (with explicitly programming)과 같이 어떻게 task를 수행할지를 명시적으로 알려주지 않고, 
* 관련 data들을 제공해주면서, computer가 스스로 해당 data로부터 task를 수행하는데 필요한 logic과 rule을 학습할 수 있도록 해주는 프로그래밍 기법 
    * 또는 이를 연구하는 분야이다.

---

## General Definition

위의 정의는 ML이라는 용어를 최초로 제시(또는 대중화에 기여)한 Arthur Samuel (1901-1990)이 제안한 정의이다.

---

Machine Learning is the **field of study that**

- **gives computers the ability to *learn***
- ***without being explicitly programmed*.**

— Arthur Samuel, 1959, Studies in Machine Learning Using the Game of Checkers

* 위의 논문에서 ML이라는 용어가 최초로 등장함.

---

## Engineering-oriented Definition

좀 더 engineer에게 적합한 정의는 Tom Mitchell(1977)의 정의이다.

A computer program is said

- to learn from experience **E**
- with respect to some task **T** and some performance measure **P**,
- if its performance on **T**, as measured by **P**,
- improves with experience **E**.

ML이 실제로 유용하게 사용된 첫번째 사례는 1990년대의 spam filter라고 할 수 있다.  
spam filter의 경우를 위의 정의에 비추어 `E`, `T`, `P`를 잘 나누어보면 ML에 대한 정확한 개념이 자리잡을 것이다.

* `T`ask 는 ML로 풀고자 하는 문제이다.
* `E`xperience 는 Data를 의미한다.
* `P`erformance 는 사람을 위한 metric과 model 학습을 위한 loss function으로 나타내어진다. 

> 참고로 ML을 통해 얻어지는 model은 결국 일종의 function이며, ML을 통해 model의 parameter (=weight + bias)들이 task를 수행하는데 최적의 값 (loss값을 최소화 = loss를 parameter로 편미분한 gradient의 반대방향으로 update)을 가지도록 update해나가는 과정이 training임.

---

## ML의 구성요소

ML은 다음으로 구성된다고도 생각할 수 있다.

`ML = Representation + Evaluation + Optimization + Generalization`

각각의 정의는 다음과 같다.

**`Representation`**

- 수행하고자 하는 task(혹은 해결하고자 하는 문제)에 맞추어 
**입력값** 을 어떤 **결괏값** 으로 만들지를 결정하는 방법(=`model` or `algorithm`)
    - SVM, Decision Tree, k-means model

**Evaluation**

- Representation 의 결괏값이 수행하고자하는 task를 얼마나 잘 수행하는지 판정.
    - [Root Mean Squared Error (RMSE)](https://www.notion.so/Root-Mean-Squared-Error-RMSE-d2da420a632545f6bde38db4507abcb2)
    - [Mean Absolute Error (MAE)](https://www.notion.so/Mean-Absolute-Error-MAE-8ba37f490ddd4700af4a8a1cd60fa48d)


**Optimization**

- evaluation 에서 원하는(또는 요구되는) 기준(성능)을 
***최적으로 만족시키기 위한 조건(~ model의 *parameter, weight*)*** 을 **찾는 방법**.
- 좀 더 기술적으로 애기하면, model의 parameter(or weight)를 evaluation에서 원하는 수준의 좋은 metric 수치를 얻도록 update하는 방법.
    - Gradient Descent, Adam 등.

**Generalization**

- 학습된 model을 이용하여 ***새로운 데이터에 대한 예측*** 을 수행.
    - 학습에 사용되지 않은 데이터에 대해 학습된 model로 inference수행.

---

## ML vs. Data Mining

**classification, regression, clustering 등을 위한 기술, 모델, 알고리즘** 을 ***이용*** 하여 
***어떤 task를 수행*** 하거나 ***problem을 해결*** 하는 것을 

- **컴퓨터 과학 관점** 에서 **Machine Learning** 이라고 부름. *← 추론적*
- **통계학적 관점** 에서는 **Data Mining** 이라 부름. *← 기술적*

---

### Data Mining

`Data Mining`은 

1990년대 ^^통계학의 이슈들^^ 을  
***Machine Learning적 접근법(컴퓨터 공학적 접근법)을 사용하여 효율적으로 해결하려고 했던 움직임에 기원*** 하는데,  
이로 인해 두 분야가 상당 부분에서 유사점을 가짐.

요약하면 다음과 같음.

- ML : 학습한 모델을 통해 **새로운 데이터에 정확한 예측치** 를 얻어내는 것이 목표.
- Data Mining : 가지고 있는 데이터에서 **현상 및 특성 등을 발견** 하는 것( ***~보다 데이터를 잘 이해하고 묘사하는 방법을 찾는 것*** )이 목표.