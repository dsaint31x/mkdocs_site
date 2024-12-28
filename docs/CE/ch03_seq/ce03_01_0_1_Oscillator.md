---
title: Oscillator
tags: [oscillator, clock, synchronous, pulse, propagation delay]
---
# Oscillator (발진자)

## Oscillator

일정시간에 맞춰 반복되는 ***주기적인 펄스(Pulse)를 발생*** 시켜  
Computer 등에서 ***Time정보를 제공하는 역할*** 을 함.  

![Oscillator](img/Quartz-Crystal-Oscillator.png){style="display:block; margin:0 auto; width:300px"}

CPU 등에서 **동작 클럭 (`Clock`)** 이 해당 CPU가 어떤 빠르기로 동작하는지를 나타내는데,  
이같은 <u>동작 클럭을 제공하는 것이 바로 `Oscillator` </u>임.  

* 주로, ***Piezoelectric effect*** 를 이용하는 Crystal로 만들어진다 (보다 저렴한 ceramic으로 만들어지는 경우도 있음). 
* Crystal (주로 석영,quartz,이 사용됨)에 전기를 가할 경우, 진동이 발생함.
* 이 같은 진동을 발생시키는 특성 때문에 Crystal 에 Feedback 회로를 연결하면 일정 시간 간격으로 반복되는 Pulse를 생성시킬 수 있음.

> 이를 바탕으로 `Clock` Signal을 발생시키는 `Oscillator` 가 만들어진다.  

---

---

## Clock 

> Computer나 Circuit의 동작 pace를 가르킴. 

단위를 보통 `Hz`로 표기되며 초당 몇번의 Pulse signal이 반복되는지로 빠르기를 나타낸다.  

* Computer나 Circuit을 구성하고 있는 여러 Device들은 
* Propagation Delay (전파지연) 등의 시간과 관련된 특성이 다들 다르기 때문에 
* Clock에 맞춰서 정상적인 동작이 이루어지도록 ***동기화(`Synchronization`)*** 되는 경우가 대부분이다. 

> 비동기 방식이 없는 건 아니지만, 이 경우 매우 제어가 어렵다.  

일반적으로 Device들에서 ***시간과 관련된 특성 (`Propagation Delay` 포함)들*** 은 

* 동일 소자라도 온도나 제조공정 에서의 차이 등등으로 인해 
* 꽤나 Variation이 크기 때문에 
* ***통계적인 측정치로 표시*** 되며 
일정 Range(범위)에서 정상동작이 보장되는 특징을 가진다.  

---

---

## 더 살펴보기

* `Pulse` Signal은 신호처리나 디지털 회로 등에서 자주 보게 되는 Signal 중 하나임. 
* 여러 종류가 있으나 일반적으로 `Rectangular Pulse` 를 주로 가르키며 `구형파` 라고도 불림.


참고자료 : wikipedia's [Pulse](https://en.wikipedia.org/wiki/Pulse_(signal_processing))