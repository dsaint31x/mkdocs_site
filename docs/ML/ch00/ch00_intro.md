# Introduction

## AI 란

Jack McCarthy 에 따르면  Artificial Intellience (AI)의 정의는 다음과 같음.

> ref. : [Basic Questions](http://www-formal.stanford.edu/jmc/whatisai/node1.html)

**Q. What is `artificial intelligence`?**
: A. It is the science and engineering of making intelligent machines, especially intelligent computer programs. It is related to the similar task of using computers to understand human intelligence, but AI does not have to confine itself to methods that are biologically observable.

AI라는 용어는 1956년 다트머스대학 컨퍼런스에서 최초로 등장했으며, `기계 혹은 시스템으로부터 만들어진 지능` 또는 
`이와 같은 지능을 만들 수 있는 방법론 등을 연구하는 분야` 를 가르킨다. 

> Machine Learning 이라는 용어를 1959년 만들어낸 Aurther Samuel도 여기 참석함.

AI는 매우 다양한 분야의 학문과 연계됨.

* 철학 : 지능이란? 인간의 인지, 학습, 기억, 추론이 어떻게 이루어지는지 
* 인지심리학 : 인간(혹은 동물)이 정보를 인지,저장,분석,처리 하는 메커니즘을 연구
* 수학 : 대수학, 논리학, 확률 …
* 컴퓨터 과학(공학 포함), 로봇공학 : 다른 분야의 연구 결과를 통해 실제 동작하는 구현물을 만들어냄.

## AI 에 대한 구분.

Stuart Russell 및 Peter Norvig가 기재한 AI 연구의 선도적인 교과서 [Artificial Intelligence: A Modern Approach, 4th US ed.](http://aima.cs.berkeley.edu/)에서 *합리성* 과 *사고 대 행동* 을 기반으로 기존의 컴퓨터 시스템과 구분되는 AI의 4가지 잠재적 목표 (or 정의)를 다음과 같이 제시함.

* 인간처럼 사고(생각)하는 시스템
* ***인간처럼 행동하는 시스템***
* 합리적으로 사고(생각)하는 시스템
* ***합리적으로 행동하는 시스템***

현재 어떤 AI기술도 General AI(인간처럼 사고/행동)는 구현치 못했음. 하지만, Deep Learning을 통해 Computer Vision분야 등에서는 인간 이상의 성과를 보이는 Narrow AI (특정 작업에서 인간처럼 혹은 이상으로 사고/행동)가 구현되기 시작했다. 대표적인 분야는 다음과 같음.

* 체스, 바둑
* 이미지 인식(일부)


## Turing Test

Alan Turing은 "인간처럼 행동하는 시스템"의 범주에 속하는 정의를 제시했다. 

> Turing Test는 기계가 인간과 얼마나 비슷하게 대화할 수 있는지를 기준으로 기계에 지능이 있는지를 판별하는 것으로 "행동"을 "대화"로 생각하면 된다. 하지만, 인간처럼 대화하는 것이 지능이 있다는 기준인지에 대해서 논란이 있다.

Turing Test에서는 사람인 조사관이 블라인드 상태에서 컴퓨터와 5분간 채팅하여 상대가 컴퓨터인지 사람인지 판단한다.  여러 조사관들 중 상대가 사람일 것이라고 판단하는 조사관이 ***30% 이상***이면 해당 컴퓨터는 튜링 시험을 통과한다.

[Turing, A.M., Computing machinery and intelligence, Mind, 59(236):433-460, 1950)](https://phil415.pbworks.com/f/TuringComputing.pdf)

위는 좀 더 간소한된 것이며 작은 연결 통로로 물건을 주고받는 동작 시험 등이 포함된 `전체 튜링 시험(total Turing test)`도 있다 :  즉, "인간처럼 행동하는 시스템" 이 Turing 이 생각한 AI였다. 

Total Turing Test 통과를 위해서 AI에게 필요한 능력

* Natural Language Processing : 
    * 자연어를 통한 성공적 의사소통 위해
* Knowledge Representation : 
    * 알고있는 것과 들은 것을 저장하기 위해
* Automated Reasoning : 
    * 저장된 정보를 통해 질문에 답하고 새로운 결론을 도출하기 위해
* Machine Learning : 
    * 새로운 상황에 적응하고, 기존 알고 있는 패턴을 이용하여 extrapolation하기 위해.
* Computer Vision : 
    * 물체의 인식을 위해
* Robotics Engineering : 
    * 물체를 조작하고 이동하기 위해 

**Ref.**

1. ref. Wikipeda's [Turing Test](https://ko.wikipedia.org/wiki/%ED%8A%9C%EB%A7%81_%ED%85%8C%EC%8A%A4%ED%8A%B8)
2. Artificial Intelligence : A Modern Approach / 3rd Ed.
3. AI의 모든 것"이란? : [Turing Test](https://atozofai.withgoogle.com/intl/ko/about/)

## Machine Learning 이란.

ML은 "AI를 구현하기 위한 구체적 접근 방식"에 해당한다.  
  
ML은 

* 대량의 데이터와 
* 알고리즘(and optimization)등을 통해, 
* 컴퓨터가 ***작업수행방법***을 스스로 학습하도록 하는 것!

을 가르킨다.

### ML을 위한 다양한 알고리즘 (or 기법)

ML을 위해 제안된 다양한 기법들이 있으며 대략적으로 나누어 보면 다음과 같다.

* Tree계열 : Decision Tree, Random Forrest등
* Support Vector Machine
* Clustering
* ANN ( → Deep Learning)
* Reinforcement Learning

`Artrificial Neural Network (ANN)`이 현재 가장 높은 성능을 보이는 ML기법의 하나인 Deep Learning을 가르킨다. 

##  Representation Learning

입력에 대해 요구되는 출력(~expectation)을 가능한한 정확하게 산출할 수 있는 approximation model을 만드는데 유용한 resentation을 학습데이터를 기반으로 학습하는 것을 가르킴.

> Generally speaking, a good representation is one that makes a subsequentlearning task easier.

## Deep Learning 이란.

엄격하게 애기하면 Deep Learning은 ML의 한 종류이며, Representation Learning 에 속한다. 우수하고 효율적인 Machine Learning을 실현할 수 있는 기법이 Deep Learning이며, 이는 학습데이터로부터 최적의 hierarchy representation을 알아서 추출할 수 있다는 장점에 기인한다.

다음의 Deep Learning의 정의를 살펴보라.

> Deep learning is a ^^particular kind of machine learning^^ that achieves great power and flexibility by ***learning to represent the world*** as **a nested hierarchy of concepts,** with each concept defined in relation to simpler concepts, and more abstract representations computed in terms of less abstract ones.

![http://www.cs.utoronto.ca/~rgrosse/cacm2011-cdbn.pdf](../img/ch00/dl_hiearchy_rep.png)

* DL은 데이터로부터, 스스로 계층적인 representatoin을 추출해내는 능력을 가짐.

## Summary : AI, Machine Learning, and Deep Learning

AI와, ML, 그리고 DL은 다음과 같은 관계를 보인다.

![](img/ch00/ai_ml_dl.png)

**(Narrow) AI** 
: 특정 분야에서 인간처럼, 혹은 그 이상의 성능을 보이는 기술(or system) 또는 그런 기술

* Export System 등

**ML**
: AI를 구현하기 위한 기술. 명시적 프로그래밍이 아닌 데이터로부터 동작을 학습하는 기술

* Decision Tree, SVM, Gradient Boosting

**DL**
: 현재 가장 우수한 성능의 ML을 구현하는 기술

* MLP, CNN, RNN, Transformer





