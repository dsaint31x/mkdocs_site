# Model based Learning

> Training dataset 으로부터  
> 일반화된 Model을 만들어(=학습) prediction에 이용하는 방식을  
> `Model based Learning`이라고 부름.
> 
> **Inductive (귀납적) Learning** 이라고도 불림.

![](../img/ch00/model_based_learning.png){style="display: block; margin: 0 auto; width:350px"}

* 위 그림에서 학습의 결과로 만들어진 model은 바로 검은색 dash line이 된다.
* 새로 주어진 data point *x* 는 dash line에 의해 삼각형으로 prediction된다.
* 만일 model이 만들어지지 않는 [instance based learning](./ch00_31_instance_based_learning.md)이라면, 사각형으로 prediction될 것이다. (`k=3`인 k-NN이라면)

즉, 데이터 자체를 그대로 저장하지 않고, 모델을 통해 일반화 하여 표현!!


> **참고: 머신러닝에서 model 이란?**
> 
> * 입력을 받아 출력을 내는 함수(function)
> * 특정 데이터셋에서 data instance와 label (or target) 간 관계를 근사(approximation)하는 대상
>     * 관계를 매핑(mapping) 또는 변환(transformation)으로 이해
>     * 이는 function 형태로 표현 가능
>     * 특히, supervised learning에서는 model을 function으로 간주해도 큰 문제 없음.
> 
> ML에서 model은 다음과 같은 또 다른 의미를 가지기도 함.
> 
> * features와 label간의 approximation 를 생성하는 알고리즘(algorithm) 또는 방법(method)
> * 인공 신경망(Artificial Neural Network)에서 층(layer)들이 쌓인 아키텍처(architecture)
> 

Model Based Learning은 보통 다음과 같은 순서로 진행됨.

1. Data 분석
2. 해당 Training data에 적절할 model을 선택.
3. 해당 model을 training dataset으로 학습 (cost func.최소화시키는 optimization)
4. 이후 inference 수행 (새로운 data point들에 대한 prediction)

[간단한 실습용 ipynb](https://gist.github.com/dsaint31x/8048847863cf09145b192247742d0207)

ML에서 대부분의 경우는 model based learning 임.