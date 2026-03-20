---
title: Batch Learning
description: >
  가용한 전체 데이터를 사용하여 학습하는 Batch Learning(Offline Learning)의 
  개념, 장단점, 그리고 Online Learning과의 비교를 설명한다.
tags:
  - batch learning
  - offline learning
  - incremental learning
  - online learning
  - machine learning
---

# Batch Learning

## Batch Learning이란?

* Batch Learning은 가용한 데이터를 모두 사용(test data 등을 직접 본다는 의미는 아님)하여 훈련시킴.
* **Offline Learning** 으로 불림.

일반적으로 정해진 주기마다 훈련시켜, 새 모델로 교체하는 형태를 취함.

## 장단점

**장점 (Advantages)**
* 전체 데이터를 활용하므로 일반적으로 model의 성능(performance)이 안정적임.
* 학습과 서비스가 분리되어 있어 model의 quality 보장이 용이함.
* 재현성(reproducibility)이 높아 디버깅(debugging)이 상대적으로 쉬움.

**단점 (Disadvantages)**
* 새로운 데이터가 추가될 때마다 전체 데이터를 다시 학습해야 하므로,
  시간(time)과 컴퓨팅 자원(computing resource) 소모가 큼.
* **데이터 변화(data drift)에 빠르게 적응하지 못함**.
* 전체 데이터를 메모리(memory)에 적재해야 하므로,
  데이터 크기에 한계가 있음.

## Comparison with Online Learning)

| 항목 | Batch Learning | Online Learning |
|------|---------------|-----------------|
| 학습 시점 | 서비스 전 (offline) | 서비스 중 (online) |
| 학습 데이터 | 전체 데이터 | mini-batch / 개별 instance |
| 모델 업데이트 | 주기적 교체 | 점진적 갱신 |
| 자원 소모 | 높음 | 낮음 |
| 안정성 | 높음 | 상대적으로 낮음 |
| 데이터 변화 적응 | 느림 | 빠름 |

## 참고.

최근 서비스로 사용되는 ML들의 경우,  
Incremental Learning 을 취하는 경우가 많아지고 있으나,  
quality 보장이 쉽지 않은 측면이 있어서 여전히 batch learning 이 선호되는 경우도 많음.

> 개인적으로 공부할 때 사용하는 ML은 모두 batch learning이라고 보면 된다.
