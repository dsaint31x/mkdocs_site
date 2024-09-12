# Self-supervised Learning

## 사용되는 경우

Self-supervised Learning은 다음과 같은 상황에서 주로 사용됨.

* label이 없는 데이터가 label이 있는 데이터보다 훨씬 많을 때
* 원래 풀고자 하는 task(main task)를 위한 labelled dataset의 샘플 수가 모델을 훈련시키기에 부족할 때

## 구성 단계

Self-supervised Learning은 위와 같은 경우 다음의 단계로 모델을 훈련시킴.

1. 수가 많은 Unlabelled dataset를 Labeled dataset으로 변경시킬 수 있는 사전 과제(pretext task)를 설정하고 이를 이용하여 모델을 훈련
    * 일종의 pre-training임.
    * 원래 main task 관점에서는 label 이 없는 dataset이지만, pretext task 덕에 labelled dataset 이 되며
    * 결국 supervised leanring 으로 학습이 가능해짐: pretext task 의 경우임을 주의할 것.
2. 해당 모델을 main task에 맞게 미세 조정(fine-tuning) 수행 
    * 모델의 출력단의 구조가 변경될 수도 있음.
    * 2번 과정에서는 main task에 맞게 label이 주어진 소수의 dataset을 사용함.

## Pretext Task    

Pretext task는 데이터 자체에서 매우 쉽게 label을 만들어낼 수 있어야 함. 

* 예를 들어, 문장의 일부를 가리고 그 부분을 예측하게 하는 것임. 
* 이런 방식의 pretext task를 잘 수행하도록 훈련되는 모델은 해당 dataset의 중요한 특징들을 학습하게 됨.
* 반드시 pretext task로 학습된 내용은 main task를 수행하는 데에 도움이 되어야 함.

대표적인 예로 자연어 처리에서 BERT 모델이 사전 훈련으로 사용하는 마스크 언어 모델링이 있음.

## 장점

Self-supervised Learning의 장점:

* label 없는 대량의 데이터 활용 가능
* 데이터의 일반적인 특징(representative feature)을 잘 학습할 수 있음
* 주요 과제에 적용 시 적은 양의 레이블된 데이터로도 좋은 성능 달성 가능

## 결론1

Self-supervised Learning은 

* dataset의 관점에서 pretext task에 대한 훈련은 레이블 없는 데이터를 사용하므로, 일종의 unsuperivsed learning임.
* 하지만 해당 학습 과정은 label을 생성하고 나서 수행되므로 지도 학습(supervised learning) 기법으로 진행됨.  
* 더욱이, 최종 모델을 훈련시킬 때에도 labeled dataset을 사용하는 supervised learning 이 수행됨.)
* 일종의 전이 학습(transfer learning)의 한 형태로 볼 수 있음.​​​​​​​​​​​​​​​​


즉, self-supervised learning이 적용되는 task 는 사실상 supervised learning과 같음.

> Unsupervised Learning의 task 가 주로 clustring, dimentionality reduciton, novelit (or outlier) detection 인 점을 주의할 것.  
> Self supvised Laerning은 task의 관점에서 unsupervised learning과 차이를 보이고, 주어진 dataset 의 측면에서 supervised learning과 차이를 가짐.  
> 일종의 Knowledge Transfer의 한 종류라고도 할 수 있음. 

## 결론2

Self-supervised Learning은 ***Supervised Learning을 위한 Knowledge Transfer Technique*** 이라고도 볼 수 있음.

* unsupervised learning 나 semi-supervised learning을 수행하고 얻은 knowledge를 (=pre-training for pretext task)
* final goal(=main task)을 위한 supervised learning에 transfer하는 방식을 취한다. (=downstream에 맞는 topper layer를 교체하는 등의 방식)

## Example

Pretext task로 context prediction을 unsupervised learning으로 수행하고, 이를 knowledge transfer시켜 원래 task를 수행.

* Doersch, Carl, Abhinav Gupta, and Alexei A. Efros. "Unsupervised visual representation learning by context prediction." Proceedings of the IEEE international conference on computer vision. 2015.

