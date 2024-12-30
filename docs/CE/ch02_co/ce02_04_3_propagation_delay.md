---
title: Propagation Delay
tags: [Propagation Delay, Ripple-Carry, Gate]
---

# Propagation Delay

## Definition

**Gate 등에서 Input이 Output에 영향을 미치기까지 걸리는 시간** 을 가르킴.  
(이상적인 회로 설계와 실제 구현 간의 가장 큰 간극에 해당함.)

> Propagation delay (전파지연)에 대한 간단한 설명이 있는 URL.
>   
> * [Propagation Delay 참고 URL](https://dsaint31.tistory.com/409)

* Ripple-Carry Adder 를 사용하지 않는 가장 큰 이유가 바로 Propagation Delay 때문임: 
    * 때문에 Carry Look-Ahead Adder가 사용됨.
* 여러 Device가 연결될 경우, Propagation Delay를 고려해야만 제대로 동작함.

---

---

## Example

![propagation_delay_ex](imgs/propagation_delay_example.png){style="display: block;margin: 0 auto; width:400:}

* 위의 그림에서 Gray Area 에서는 해당 Signal의 값은 보장이 어려움.
* Ideal Device라면 즉시 변하지만, ^^Input에 의해 Output이 변하는데 걸리는 시간(Propagation Delay)^^ 이 바로 Gray Area를 만들어냄.
 