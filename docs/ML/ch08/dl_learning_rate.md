---
title: Learning Rate Range Test
tags: [Learning Rate, Hyperparameter, Optimization, Deep Learning, Training]
---

# Learning Rate Range Test

> Learning rate는  
> 모델 학습 과정에서 
> **parameter를 얼마나 크게 업데이트할지를 결정** 하는  
> 중요한 hyperparameter임. 

Learning rate가 

* 너무 작으면 학습이 매우 느려지고, 
* 너무 크면 loss가 불안정하게 증가하거나 발산할 수 있음. 
* 따라서 효율적이고 안정적인 학습을 위해 적절한 learning rate를 선택하는 것이 중요함.

참고자료: [Learning rate 의 중요성](https://dsaint31.tistory.com/633#Learning%20rate%20%EC%9D%98%20%EC%A4%91%EC%9A%94%EC%84%B1-1-7)

---

---

## Learning rate range test

아래에서 기술된 Learning rate range test는 ***적절한 learning rate 범위를 찾기 위한 실험적 방법*** 임. 

* 이 방법의 목적은 최종 모델을 학습시키는 것이 아니라, 
* learning rate 변화에 따라 loss가 어떻게 반응하는지 관찰하고
* 이를 통해 적절한 초기 learning rate를 찾는 것임.

---

### 절차

1. 모델을 랜덤 초기화함.
2. 매우 매우 작은 learning rate에서 학습을 시작함.
3. 학습의 매 iteration마다 learning rate를 일정 비율로 증가시킴.
4. 매우 큰 learning rate 에 이르면 학습 종료.
4. 각 iteration 에서의 loss를 기록함.
5. loss (y축)를 learning rate(x축)에 대한 함수로 시각화함.
6. loss가 감소하다가 **다시 증가( or 발산) 하기 시작하는 지점 (=Turning point)** 을 찾음.
7. 해당 turning point 에서의 learning rate 보다 약간 작은 (1/10 정도로 경험적인 정도를 언급한 문헌 있음) learning rate를 최적의 초기 learning rate로 선택.
8. 모델을 다시 초기화한 뒤, 선택된 초기 learning rate로 정상적인 학습을 수행함.

---

---

## Learning rate range test의 원리

1. Learning rate가 너무 작으면 parameter update가 매우 작아 loss가 거의 감소하지 않음.
2. Learning rate가 적절한 범위에 들어가면 parameter가 효과적으로 update되어 loss가 빠르게 감소함.
3. Learning rate가 지나치게 커지면 update 폭이 과도해져 loss가 증가하거나 발산함.
4. 따라서 loss가 감소하다가 다시 증가하기 시작하는 지점을 통해 학습이 불안정해지는 learning rate 범위를 추정할 수 있음.

> 일반적으로 최종 학습에는 해당 지점보다 약간 1/10 정도 작은 learning rate를 사용함.

---

---

## Learning rate range test 사용 시 주의사항

* 이는 Learning rate마다 별도의 모델을 생성하여 각각 수 iteration씩 학습하는 방식이 아님.
    * 엄밀하게는 이 방식이 공정하다고 볼 수 있으나, 실제 적용하기에 비효율적임. 
    * 하나의 모델을 사용해 수백 iteration 동안 학습하면서 learning rate를 점진적으로 증가시키는 방식으로도 충분함.
    * 이는 초기 학습이 매우 적은 Learning rate로 이루어지기 때문이므로, 반드시 매우 작은 Learning rate 로 시작해야 함.
* Learning rate는 보통 선형 증가보다 매 iteration마다 일정 비율을 곱하는 지수적 증가 방식을 사용함.
    * 예를 들어 $10^{-5}$에서 시작하여 500 iteration 동안 $10$까지 증가시키려면, 매 iteration마다 다음 값을 learning rate에 곱함.

$$
\left(\frac{10}{10^{-5}}\right)^{1/500}
$$

---

---

## Learning rate range test 의  한계

* 엄밀히 애기하면, Learning rate range test로 얻은 결과는 특정 모델, 데이터셋, optimizer, batch size 설정에 대해서만 유효함.
    * Batch size가 크게 변경되면 gradient의 분산과 update 특성이 달라지므로 적절한 learning rate 범위도 달라질 수 있음.
    * Optimizer를 SGD에서 Adam으로 변경하거나 momentum 등의 hyperparameter를 변경한 경우에도 결과가 달라질 수 있음.
    * 모델 구조나 심지어 데이터 전처리가 크게 바뀐 경우에도 다시 수행하는 것이 바람직함.

즉, 학습 설정이 크게 변경되었다면 learning rate range test를 다시 수행하여 적절한 learning rate 범위를 재탐색하는 것이 좋음.

> 다만
> batch size나 기타 설정이 소폭 변경된 경우에는
> 기존 결과를 초기값으로 활용한 뒤, 필요할 때만 추가 실험을 수행할 수 있음.
