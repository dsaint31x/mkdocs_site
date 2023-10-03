# Batch Normalization

Gradient Vanishing과 Exploding의 위험을 효과적으로 감소시킴.

* Layer parameter가 변함에 따라, 다음 layer에 들어오는 input의 distribution이 바뀌는 ***Internal Covariate Shift*** (ICS) 문제를 Gradient Vanishing and/or Exploding의 원인이라고 가정 (참고로 현재 `BN`의 제안 당시 ICS가정은 다르게 해석되고 있음: [아래 설명](#bn과-ics-가정) 참고).
* 이를 위해 layer의 Input을 standardization을 하고, task 수행에 최적의 분포가 되도록 scaling과 shifting을 학습하여 이를 layer input에 적용.
* 단, `RNN`의 time 방향으로 unrolling된 쪽에 `BN`은 적용해도 큰 효과가 없는 것으로 알려짐 (`RNN`에서는 대신 `Layer Normalization`을 사용한다.)

어찌 보면 ***layer 별로 최적의 input 분포를 가지도록 pre-processing을 해주는 것*** 이 batch normalization이다. (여기서 최적의 분포란 현재 training dataset을 기준으로 task를 가장 잘 수행할 수 있게 해주는 input의 분포를 의미.)

> internal covariate shift를 해결하는 ideal 방법은 layer의 input에 whitening을 가해서, input의 feature들이 서로에 대해 independent (~uncorrelated)하고 각각의 variance가 1이 되도록 해주면 된다.  
>
> 하지만 2015년 `BN`을 제안한 Sergey Ioffe et al.에 따르면  
> 
> * whitening은 covariance matrix 등의 계산이 필요해서 계산량이 너무 많고, 
> * 각 layer의 parameters의 효과를 상쇄시키는 등의 문제점이 있어서 
> * ANN에 직접 적용할 경우 부작용이 컸다고 한다.

---

## BN의 동작 방식.

때문에 `BN`에서는
  
* 일단 input의 features가 ^^이미 uncorrelated라고 가정^^ 하고 
* input mini-batch에 대해 feature 각각을 normalize 시키고 
* 동시에 activation의 ***non-linearity 효과*** 를 보존하는 

***최적의 scaling과 shift를 추가적으로 가해주는 방식*** 을 채택함.  
(이때 scaling factor와 shift factor는 parameter로 처리하여 training dataset에서 최적의 값을 찾도록 처리함).

---

## BN과 ICS 가정

위의 내용은 `BN`이 처음 제안될 당시의 것으로 추가 연구에 따라 다음과 같은 다른 해석이 일반적임.

* 우선, Internal Covariate Shift (ICS)를 `BN`이 실제로 방지하지 못하는 것이 밝여짐. 
* 하지만, 다행스럽게도 ICS가 deep learning의 학습에 지장을 그리 주지 않는 것으로 알려짐. 
* `BN`은 ICS를 막기보다는 optimization landscape에서의 smoothing 효과를 부여하며 
* 이때문에 학습을 향상시키는 것이라는 후속연구가 있음.

때문에 `BN`은 ICS를 해결해서 좋은 성능을 보인다고 해석하기 보다는 

* 각 layer들에 대해 ***"Task를 푸는데 있어서 최적의 분포를 가지는 input"*** 으로 바꾸어주는 특성(`ReLU` 등과도 궁합이 잘 맞음)과 
* optimization landscape smoothing이 이루어지기 때문에

좋은 성능을 보이는 것으로 생각하는게 현재 시점에서는 보다 나은 해석으로 받아들여짐.

* 참고 : [How Does Batch Normalization Help Optimization?](https://arxiv.org/abs/1805.11604)

---

## 장점

* ***Gradient Vanishing과 exploding을 효과적으로 감소시킴*** 에 따라 ^^`sigmoid`를 hidden layer의 activation으로 사용할 수 있을 정도의 성능 향상^^ 을 보임.
* ***Weight initialization이 training에 미치는 효과를 감소*** 시켜서 ^^poor weight initialization에서도 학습이 잘 이루어지게 해줌.^^ (그렇다고 억지로 나쁜 weight initialization을 사용할 필요는 없음)
* ^^learning ratio를 크게 해도 Training이 잘 이루어지게 해 줌^^.
    * `BN` 등장 전에는 learning ratio를 지나치게 크게 할 경우, gradient vanishing 또는 expanding이 심해지는 등의 문제로 학습이 제대로 되기 힘들었음.
* Regularization의 효과를 가짐 
    * 해당 효과는 ***mini-batch size를 크게 해주면 그 효과가 감소*** 하는 단점을 가지지만, 
    * `BN`을 통해서 gradient vanishing 방지와 regularization을 동시에 달성할 수 있음. 
    * 때문에 `BN`은 학습속도를 저하시키는 drop-out을 ANN에서 제거할 수 있게 해줌 (즉, ***overfitting 방지 효과*** 도 가짐.).

---

## 단점

* model에 부가적인 연산이 layer별로 추가되기 때문에 ***계산량이 늘어남***  
    * 하지만 `BN`을 사용할 경우, learning ratio를 크게 잡을 수 있고 수렴속도가 압도적으로 빨리지기 때문에 
    * ^^전체 training에 걸리는 시간은 오히려 짧은 것으로 알려짐^^
    * 단, 이는 training의 경우이고 inference의 속도는 확실히 느려짐. 
    * Inference를 위해서는 `BN`의 scale과 shift를 layer에서 직접 적용하도록 처리함으로서 속도를 향상시킬 수 있음 (`TFLite`에서 이 방식을 통해 `BN` layer를 제거함)
* ***mini-batch의 크기에 영향*** 을 많이 받음. 
    * 지나치게 작은 mini-batch 크기에서는 `BN`이 제대로 동작하기 어려움.
    * 반대로 지나치게 커질 경우, regularization 효과가 감소함.
* RNN 등에서는 Time마다 통계적으로 다른 분포의 input을 가지기 때문에 `BN`의 적용이 쉽지 않음 
    * 때문에 RNN등에서는 feature에 대해 적용되는 `BN`이 아닌 단순한 `gradient clipping`이나 `sample`에 대해 적용되는 ***`layer normalization`이 대신 사용됨.***
    * `BN`은 Time축으로 같은 parameters를 공유하는 RNN에선 그리 효과적이지 않음.

---

## BN의 중요성

`BN`은 매우 효과적인 optimization을 가능하게 하기 때문에, 2015년 `BN`이 제안된 이후 이 기법은 필수적인 layer로 받아들여짐 (`CNN`에서는 거의 필수적으로 사용된다).

---

## 기존 해법과의 비교.

기존의 weight initialization과 activation function을 통한 Gradient vanishing과 exploding 해결방안은 훈련 초기 layer의 input과 output의 variance를 비슷하게 유지시키는 것은 가능했으나 training으로 인해 weights가 변화하게 될 경우 그 효과가 떨어지는 문제점을 가짐.

이에 반해 `BN`은 training 이 진행되면서 각각의 parameters가 훈련되어 layer의 입력(혹은 출력)이 다음 layer에서의 훈련에 적합하도록 조정이 된다는 장점을 가짐.

특정 범위로 gradient를 제한하는 `Gradient Clipping` 은 RNN에서 자주 발생하는 Gradient Exploding을 해결하기 위한 방법으로 더 많이 사용된다. 

Keras에서는 optimizer 객체에서 설정하며 

* gradient vector의 ^^각 element의 값의 크기^^ 를 기준(`clipvalue`)으로 하거나, 
* gradient vector의 ^^norm^^ 을 기준(`clipnorm`)으로 하여 clipping 되도록 설정.

---

## Algorithm

`BN`의 경우, training과 inference 단계에서 조금 다른 처리를 취함.

### Training

standardization을 위해 mini-batch ($B$)의 mean ($\mu_B$)과 variance ($\sigma^2_B$)를 구하고, 이를 바탕으로 normalization을 한 다음, scaling($\gamma$)과 shift ($\beta$)를 수행. 

1. $\displaystyle \mu_B=\frac{1}{m_B}\sum^{m_B}_{i=1}\textbf{x}^{(i)}$
2. $\displaystyle \sigma_B^2=\frac{1}{m_B}\sum^{m_B}_{i=1}\left(\textbf{x}^{(i)}-\mu_B\right)^2$
3. $\displaystyle \hat{\textbf{x}}^{(i)}=\frac{\textbf{x}^{(i)}-\mu_B}{\sqrt{\sigma_B^2+\epsilon}}$ ← Standardization 을 의미함. z-Transform이라고도 불림.
4. $\displaystyle \textbf{z}^{(i)}=\gamma \otimes \hat{\textbf{x}}^{(i)}+\beta$ ← rescaling and shift.

* $\textbf{z}^{(i)}$는 $i$ input instance $\textbf{x}$에 대한 rescaled and shifted version임.
* $\gamma$와 $\beta$는 back-propagation을 통해 학습되는 parameters임.
* 위에서 $\epsilon$은 zero-division을 막아주기 위한 smoothing factor임.

---

### Test (and Inference)

Training 단계와 큰 차이는 없으나 mini-batch에서 구해지는 $\mu_B$와 $\sigma_B^2$를 Inference에선 구할 수 없음.

때문에 Test에서 사용되는 mean과 shift는 Training 과정 중에 mini-batch 별로 구해지는 $\mu_B$와 $\sigma_B^2$ 들을 이용하여 exponential moving averaging (일반적인 구현물에서 사용됨)으로 구하거나 Training dataset 전체의 mean과 variance를 사용한다.

Exponential moving average를 사용할 경우, `momentum`이라는 hyper-parameter가 추가된다. 

$$\hat{\textbf{v}} \leftarrow \hat{\textbf{v}} \times \text{momentum} + \textbf{v} \times (1-\text{momentum})$$

* $\textbf{v}$ : current mini-batch로부터 구해진 mean 또는 standard deviation vector. (feature별로 구해진다는 점을 잊지 말 것)
* $\hat{\textbf{v}}$ : inference에서 사용되게 될 mean과 standard deviation vector.

일반적으로 training dataset이 크거나 mini-batch의 크기가 작을 경우 `momentum`은 커져야 한다. (보통 적어도 0.9정도를 사용.)

> 다음을 참고하라 : Github code [Batch-Normalization](https://github.com/shuuki4/Batch-Normalization/blob/master/BatchNormalization.py)

---

## References


* BEOMSU KIM's [Batch Normalization 설명 및 구현](https://shuuki4.wordpress.com/2016/01/13/batch-normalization-%EC%84%A4%EB%AA%85-%EB%B0%8F-%EA%B5%AC%ED%98%84/)
* [Batch Normalization에 대해서 알아보자](https://velog.io/@choiking10/Batch-Normalization%EC%97%90-%EB%8C%80%ED%95%B4%EC%84%9C-%EC%95%8C%EC%95%84%EB%B3%B4%EC%9E%90)
