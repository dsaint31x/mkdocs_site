---
title: Filp-Flops
tags: []
---

# Flip-Flops 

> 특정 시점의 1 Bit의 정보를 기억하는 Memory Device.


`Latch`에서는 ^^기억이 이루어지는 특정 시점이 Level^^ 로 결정되지만,  
`Flip-Flop`에서는 **Edge (=Transition Between Logic Level)로 결정** 됨. 

- `Latch`가 특정 Level인 경우 입력을 받아들이므로, 해당 Level 기간동안 입력이 변경될 수 있음.
- `Edge`는 훨씬 짧은 시간동안 입력을 받아들이므로, 해당 시간에 입력이 변경될 확률이 Latch에 비해 매우 낮음 
- `Flip-Flop`은 Edge Triggered Latch 라고도 불림


`Flip-Flop`들을 묶어서 

* 여러 Bits 를 기억하도록 확장한 형태의 `Register` 를 만들고, 
* Clock의 `Rising Edge` (or `Positive Edge`)의 횟수를 세는 `Counter` 로 확장됨.


흔히 다음의 4가지 종류의 `Flip-Flop`s 가 다루어지지만,  
여기선 가장 널리 사용되는 `D Flip-Flop` 만을  살펴본다.

- `SR Flip-Flop`
- `D Flip-Flop` (`Delay Flip-Flop`) : 가장 간단 (`S-R Latch` 3개를 묶어 구현)
- `JK Flip-Flop` : $\overline{\text{set}}, \overline{\text{reset}}$ 이 모두 Active인 경우에 Toggle이 되도록 구현된 `Flip-Flop`
- `T Flip-Flop`

---

---

## D Flip-Flop

Schematic Diagram (7474 or `DM74LS74`)은 다음과 같음.

![D flip-flop Schematic Diagram](img/D_flipflop_schematic.png){style="display: block; margin:0 auto; width:150px"}


- $D$ : input
- $Q$ : output
- $S$ : set, `PR(preset)`, Bubble 있으므로 Active Low인 $\overline{S}$
- $R$ : reset, `CLR(clear)`, Bubble이 있으므로 Active Low인 $\overline{R}$
- CK : Clock Pulse, 삼각형 표시가 `Rising Edge Triggered` 임을 표시.

다음과 같은 데이터 시트를 이용하여 `Flip-Flop` 의 동작을 파악한다.

![sheet](img/D_flip_flop_DM74LS74A.png){style="display: block; margin:0 auto; width:400px"}

* **참고: [D Filp-Flop 7474 의 동작 테이블에 대한 좀 더 자세한 설명](https://dsaint31.tistory.com/699)**

`Gate`로 `D Flip-Flop` 의 구조를 보면 다음과 같음. (`S-R Latch` 3개를 이용함.)


![Gate Design of D Flip-Flop](img/D_flip_flop_design.png){style="display:block; margin:0 auto; width:400px"}

---

---

## Setup and Hold Times.

`Flip-Flop`처럼 edge에서 입력이 이루어지는 경우,  

* ideal하게는 순간의 값이 저장되어야 하나 현실적으로는 그렇지 못하며, 
* 정상적인 입력을 위해서 앞뒤로 시간이 필요하다. 
* 이를 `Setup Time`과 `Hold Time`이라고 부르며 각각의 의미는 다음과 같음.

`setup time`:

- 정상적으로 입력이 이루어지기 위해 입력 signal을 받아들이는 clock edge가 발생하기 전에 input signal이 유지되어야 하는 시간.
- $t_\text{setup}$으로 표기됨.

`hold time`:

- 정상적으로 입력이 이루어지기 위해 입력 signal을 받아들이는 clock edge가 발생한 후에 input signal이 유지되어야 하는 시간.
- $t_\text{hold}$로 표기됨.

이들과 Propagation Delay를 반영한 Timing Diagram은 다음과 같음.


![timing consideration](img/setup_hold_timing_diagram.png){style="display: block; margin:0 auto; width:500px"}


* Latch보다는 입력을 받아들이는 시간이 짧지만, 
* 위의 Timing Diagram에서 보이듯이 
* 입력이 출력으로 반영되기 위한 일정 시간들이 필요함.

