# Model이란?

## Model이란?

> It’s simply a specification of a mathematical (or probabilistic) relationship that exists between different variables.

`model`은 쉽게 말해서, 

* 다양한 variable 간의 수학적 혹은 (확률적) 관계를 표현한 것으로 
* function이나 
* transformation 등으로 표현가능함.

> Deep Learning에서는 ANN이 바로 model임. 

---

## ML에서의 Model이란 용어의 사용범위

Model의 의미는 아까 살펴본 것이나, 특정 relation을 1차 함수로 나타낼지 2차 함수로 나타낼지가 구분되듯이 여러 type이 있을 수 있다.

ML에서 `model`이라는 용어는 다음 중 하나를 지칭하는데 사용된다.

1. **type of model** (e.g., Linear Regression) : ML의 알고리즘을 의미하기도 한다.
2. **fully specified model architecture** (e.g., Linear Regression with one input and one output)
3. **the final trained model** : 학습 (or training)을 통해 얻은 결과물에 해당하며, prediction등의 inference에 사용되는 weight과 bias등이 설정된 결과물을 의미함. (e.g., Linear Regression with one input and one output, using $\theta_0=4.85$ and $\theta_1=4.91 \times 10^{-5}$).

`model`이 가리키는 대상이 위와 같이 다양하기 때문에 
**Model selection** 이라는 용어도 다음과 같은 것들을 모두 포함하여 지칭한다. 

- *the type of model* 을 고르는 것. (`CNN`으로 할지 `SVM`으로 한지 등등.)
- *its architecture* 를 설계하는 것. (layer를 몇 개로 할지, 입출력 설계 등등)

당연히 **Training a model** 이라는 용어도 다음과 같이 여러 의미를 가진다. 

- ML의 **algorithm** 을 수행시키는 것.
- *the model parameters* 들을 training dataset에 맞춰 최선의 fitting을 시키는 것(= hopefully make good predictions on new data).
- model의 weights와 bias들의 최적값(loss function을 최소화하는)을 찾는 것.