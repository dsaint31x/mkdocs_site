# Batch Normalization

Gradient Vanishing과 Exploding의 위험을 효과적으로 감소시킴.

* Layer parameter가 변함에 따라, 다음 layer에 들어오는 input의 distribution이 바뀌는 ***internal covariate shift*** 문제를 Gradient Vanishing and/or Exploding의 원인이라고 가정.
* 이를 위해 layer의 Input을 standardization을 하고, task 수행에 최적의 분포가 되도록 scaling과 shifting을 학습하여 이를 layer input에 적용.

어찌 보면 layer 별로 최적의 input 분포가 되도록 pre-processing을 해주는 것이 batch normalization이다. (여기서 최적의 분포란 현재 training dataset을 기준으로 task를 가장 잘 수행할 수 있게 해주는 input의 분포를 의미.)

> internal covariate shift를 해결하는 방법은 layer의 input에 whitening을 가해서, input의 feature들이 서로에 대해 independent (=uncorrelated)하고 각각의 variance가 1이 되도록 해주면 된다. 하지만 2015년 `BN`을 제안한 Sergey Ioffe et al.에 따르면  whitening은 covariance matrix 등의 계산이 필요해서 계산량이 너무 많고, 각 layer의 parameters의 효과를 상쇄시키는 등의 문제점이 있어서 ANN에 직접 적용할 경우 부작용이 컸기 때문에 일단 input의 features가 이미 uncorrelated라고 가정하고 input mini-batch에 대해 feature 각각을 normalize 시키고 activation non-linearity 효과를 죽이지 않도록 최적의 scaling과 shift를 추가적으로 가해줌 (이때 scaling factor와 shift factor는 parameter로 처리하여 training dataset에서 최적의 값을 찾도록 처리함.)

## 장점

* Gradient Vanishing과 exploding을 효과적으로 감소시킴에 따라 `sigmoid`를 hidden layer의 activation으로 사용할 수 있을 정도의 성능을 보임.
* Weight initialization이 training에 미치는 효과를 감소시켜서 poor weight initialization에서도 학습이 잘 이루어지게 해줌.(그렇다고 억지로 나쁜 weight initialization을 사용할 필요는 없음)
* learning ratio를 크게 잡아도 Training이 잘 이루어지게 해줌.
    * `BN` 등장 전에는 learning ratio를 지나치게 크게 작을 경우, gradient vanishing 또는 expanding이 심해지는 등의 문제로 학습이 제대로 되기 힘들었음.
* mini-batch size를 크게 해주면 그 효과가 떨어지기는 하지만, 어느정도의 regularization 효과를 부가적으로 가지기 때문에 학습속도를 저하시키는 drop-out을 ANN에서 제거할 수 있게 해줌.

## 단점

* model에 부가적인 연산이 layer별로 추가되기 때문에 계산량이 늘어남 (learning ratio를 크게 잡을 수 있고 수렴속도가 압도적으로 빨리지기 때문에 전체 training에 걸리는 시간은 오히려 짧은 것으로 알려짐)
* 이 때문에 training 중에는 어느정도 상쇄가 가능하나 inference의 속도는 확실히 느려지나, `BN`의 scale과 shift를 layer에서 직접 계산하도록 함으로서 속도를 향상시킬 수 있음 (`TFLite`에서 이를 통해 `BN` layer를 제거함)
* mini-batch의 크기에 영향을 많이 받음. 지나치게 작은 mini-batch 크기에서는 `BN`이 제대로 동작하기 어려움.
* RNN 등에서는 Time마다 통계적으로 다른 분포의 input을 가지기 때문에 `BN`의 적용이 쉽지 않음 (때문에 RNN등에서는 feature에 대해 적용되는 `BN`이 아닌 단순한 `gradient clipping`이나 `sample`에 대해 적용되는 layer normalization이 대신 사용됨)

위의 단점들은 대부분이 해결방안이 같이 기재되어 있다. 이는 `BN`이 얼마나 ANN학습에 필수적인 기법인지를 보여준다. 2015년 `BN`이 제안된 이후 이 기법은 필수적인 layer가 되었다 (CNN에서는 거의 필수적으로 사용된다).

> `Gradient Clipping` 은 RNN에서 자주 발생하는 Gradient Exploding을 해결하기 위한 방법으로 optimizer 객체에서 설정하며 gradient vector의 각 element의 값의 크기를 기준(`clipvalue`)으로 하거나, gradient vector의 norm을 기준(`clipnorm`)으로 하여 clipping이 일어남.


## 기존 해법과의 비교.

기존의 weight initialization과 activation function을 통한 Gradient vanishing과 exploding 해결방안은 훈련 초기 layer의 input과 output의 variance를 비슷하게 유지시키는 것은 가능했으나 training으로 인해 weights가 변화하게 될 경우 그 효과가 떨어지는 문제점을 가짐.

이에 반해 `BN`은 training 이 진행되면서 layer들에게 최적의 input을 제공함으로써 internal covariate shift를 효과적으로 막아줌.

## Algorithm

### Training

standardization을 위해 mini-batch ($B$)의 mean ($\mu_B$과 variance ($\sigma^2_B$)를 구하고, 이를 바탕으로 normalization을 한 다음, scaling($\gamma$)과 shift ($\beta$)를 수행. 

1. $\displaystyle \mu_B=\frac{1}{m_B}\sum^{m_B}_{i=1}\textbf{x}^{(i)}$
2. $\displaystyle \sigma_B^2=\frac{1}{m_B}\sum^{m_B}_{i=1}\left(\textbf{x}^{(i)}-\mu_B\right)^2$
3. $\displaystyle \hat{\textbf{x}}^{(i)}=\frac{\textbf{x}^{(i)}-\mu_B}{\sqrt{\sigma_B^2+\epsilon}}$ ← Standardization 을 의미함. z-Transform이라고도 불림.
4. $\displaystyle \textbf{z}^{(i)}=\gamma \otimes \hat{\textbf{x}}^{(i)}+\beta$ ← rescaling and shift.

* $\textbf{z}^{(i)}$는 $i$ input instance $\textbf{x}$에 대한 rescaled and shifted version임.
* $\gamma$와 $\beta$는 back-propagation을 통해 학습되는 parameters임.
* 위에서 $\epsilon$은 zero-division을 막아주기 위한 smoothing factor임.

### Test (and Inference)

Training 단계와 큰 차이는 없으나 mini-batch에서 구해지는 $\mu_B$와 $\sigma_B^2$를 Inference에선 구할 수 없음.

때문에 Test에서 사용되는 mean과 shift는 Training 과정 중에 mini-batch 별로 구해지는 $\mu_B$와 $\sigma_B^2$ 들을 이용하여 exponential moving averaging (일반적인 구현물에서 사용됨)으로 구하거나 Training dataset 전체의 mean과 variance를 사용한다.

Exponential moving average를 사용할 경우, `momentum`이라는 hyper-parameter가 추가된다. 

$$\hat{\textbf{v}} \leftarrow \hat{\textbf{v}} \times \text{momentum} + \textbf{v} \times (1-\text{momentum})$$

* $\textbf{v}$ : current mini-batch로부터 구해진 mean 또는 standard deviation vector. (feature별로 구해진다는 점을 잊지 말 것)
* $\hat{\textbf{v}}$ : inference에서 사용되게 될 mean과 standard deviation vector.

일반적으로 training dataset이 크거나 mini-batch의 크기가 작을 경우 `momentum`은 커져야 한다. (보통 적어도 0.9정도를 사용.)

> 다음을 참고하라 : Github code [Batch-Normalization](https://github.com/shuuki4/Batch-Normalization/blob/master/BatchNormalization.py)


## References


* BEOMSU KIM's [Batch Normalization 설명 및 구현](https://shuuki4.wordpress.com/2016/01/13/batch-normalization-%EC%84%A4%EB%AA%85-%EB%B0%8F-%EA%B5%AC%ED%98%84/)
