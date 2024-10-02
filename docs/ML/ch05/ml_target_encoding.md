---
tags:
  - feature-engineering
---

# FE: Target Encoding (or Mean Encoding, Response Encoding)

Categorical Variable을 encoding하는 방법 중의 하나.  

* Kaggle 등에서 많이 쓰이는 편이나 
* ***overfitting의 위험*** 때문에 
    * Smoothing, 
    * Ordered Target Encoding이나 
    * permutation등의 기법 등과 
* 같이 사용되지 ***단독으로는 사용하기 어려움***.

---

## one-hot encoding and label encoding과 비교.

One-hot encoding이나 Label encoding의 경우 

* ***구분*** 만을 할 뿐 
* 할당되는 numeric value에 순서 등의 의미를 부여하지 않는 게 일반적

Target Encoding

* 현재 task를 수행하는데에 
* 보다 효과적인 ***"의미를 갖는 숫자"을 값으로 할당*** 한다.

---

## 방법

쉽게 애기하면, 

* 현재 task에서 구하고자 하는 Target의 값을 이용하여 
* encoding을 한다.

가장 유명한 **`Oredered Target Encoding`** 을 예를 들어 설명하면 다음과 같음.

"education_level" 이 high, medium, low 의 세 분류로 나뉘어지고, 다른 column들과 함께 "income"을 맞추는 regression task를 수행한다고 하자.

* `Label Encoding`을 사용하면 "education_level"에 0, 1, 2와 같은 숫자를 각 category를 구분할 수 있도록 다르게만 할당하지만,
* `Target Encoding`은 
  * "education_level"이 high인 sample 들을 뽑고, 이들의 "income"의 평균치를 구한 후 이를 "education_level"의 값으로 할당하는 방식으로 동작함. 
  * 이를 medium, low 에도 적용하면 
  * "education_level" categorical variable은 3개의 다른 숫자값을 가지면서 task를 잘 예측할 수 있는 정보를 가지게 된다.

---

## 장점은 ...

Target encoding을 사용할 경우, 

* one-hot encoding에 비해서 적은 수의 dimension을 가지면서 
* task를 수행하는데 유용한 정보를 가지는 value를 가지는 categorical variable이 된다.

---

## 단점은 ...

* Target의 값을 사용하기 때문에 data leakage가 발생하고 이는 `over-fitting`으로 이어진다.
* 더욱이 mean과 같은 대표값으로만 사용(ordered target encoding)하기 때문에 원래 target에 있는 통계적인 분포 정보와 차이가 있으며
* 이같은 차이는 over-fitting 의 위험도를 높인다.

---

## 개선 방안

가장 간단한 방법으로는 ***`Smoothing` 기법*** 이다.

이는 

* 해당 category의 평균을 그대로 사용하는 것이 아닌, 
* 전체 dataset의 global mean과 해당 category의 mean의 weighted sum을 사용한다. 
* 이 때 weight는 hyper-parameter인 ***smooth factor*** (보통 $\alpha$로 표기)로 결정된다.

수식은 다음과 같음.

$$
\text{code}_c = \frac{n_c\mu_c + \alpha \mu_g }{n_c + \alpha}
$$

* $\text{code}_c$ : category $c$에 할당되는 code. 할당되는 변수값
* $n_c$ : category $c$에 속한 sample 수
* $mu_c$ : category $c$에 속한 sample들의 target value의 mean.
* $mu_g$ : target의 평균치
* $\alpha$ : 
    * smoothing 정도를 결정. 
    * 클수록 전체 평균이 비슷한 값이 만들어지므로 
    * 각 category에 할당된 code의 값이 비슷해진다.

해당 smoothing 외에도, 

* 전체 dataset을 k-fold cross validation처럼 여러 subset으로 나누고 
* 이들 subset에서 Target encoding을 수행하여 
* 하나의 category의 데이터가 k 개의 다른 값을 가지도록 하는 방법(`k-fold target encoding`)도 있다.

가장 유명한 Target Encoding은 **`Ordered target encoding`** 이다. 

---

## 더 읽어보면 좋은 자료

* [Getting Deeper into Categorical Encodings for Machine Learning](https://towardsdatascience.com/getting-deeper-into-categorical-encodings-for-machine-learning-2312acd347c8)
* [Categorical Value Encoding 과 Mean Encoding](https://dailyheumsi.tistory.com/120) : mean encoding 부분을 참고.
