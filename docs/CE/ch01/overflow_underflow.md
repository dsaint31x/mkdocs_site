---
title: Overflow and Underflow
tags: [Overflow, Underflow, CCR]
---

# Overflow and Underflow

`Overflow`  
: 컴퓨터에서 **처리 가능한 범위(range)를 초과** 하는 연산 결과가 발생하는 경우를 가리킴.  
  
  * Overflow가 발생하면 `Condition Code Register`(`CCR`)의 Overflow 비트가 `1`로 설정됨 (or `Flag Register`). 
  * 이는 가장 상위 비트(MSB)에서 발생한 **부호 반전** 또는 연산 결과가 표현 범위를 초과했음을 의미. 
  * 주로 `Overflow`는 부호 있는 연산에서 발생하는 오류를 나타냄 (부호반전이 대표적인 예).

`Underflow`  
: **처리 가능한 범위보다 작은 연산 결과가 발생** 하는 경우를 가르킴.  
  
  * 예를 들어, 부동소수점(floating-point) 연산에서 
  * 지수(exponent)의 표현 가능 범위가 $-126$에서 $126$인 경우, 
  * $2^{-150}$과 같은 값은 표현할 수 있는 범위를 초과함 (표현할 수 없음). 
  * 이 상황을 `Underflow`라고 하며, 
  * 보통 해당 값은 `0`으로 처리되거나 `denormalized` 값으로 변환됨: 많은 경우 `0`으로 처리된다.

관련 Register: [`CCR`](https://dsaint31.me/mkdocs_site/CE/ch04/ce04_04_cpu/#register)

---

---

## 참고 자료.

* Wikipedia's [Arithmetic underflow](https://en.wikipedia.org/wiki/Arithmetic_underflow)
* 나무 위키's [언더플로](https://en.wikipedia.org/wiki/Arithmetic_underflow)