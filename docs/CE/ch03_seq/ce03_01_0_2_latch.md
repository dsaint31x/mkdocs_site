# Latches (래치)

> **걸쇠** 라는 뜻으로 ^^자물쇠^^ 의 의미를 가짐.  
> 
> **Gate를 조합** 하여 **1bit의 정보를 기억** 하는 (걸어두는) 역할을 하는 회로를 의미함.

주로 `S-R latech` 에 대한 이해를 통해, 실제 ***1bit의 정보를 기억*** 하는데 많이 사용되는 `flip-flop`을 이해하는 과정으로 배우게 됨. 
(이 flip-flop은 “CPU가 명령어와 데이터를 기억하는데 사용하는 `register`”로 확장되게 됨)  

1bit의 정보를 기억하는 `flip-flop`과의 대표적인 차이점은 clock signal에 대해

* high (or low) 레벨에서 기억이 이루어지는지 아니면 
* rising (or falling) edge에서 기억이 이루어지는지

라고 할 수 있음.

`latch`는 주로 **high 레벨에서 기억**이 이루어지며, `flip-flop`의 경우 주로 **rising edge에서 기억**이 이루어지는 버전이 많이 사용됨. 

## `OR` Latch

***feedback연결*** 과 `OR` gate를 이용하여 1bit의 정보를 기억한다는 점에서 ^^가장 간단한 latch^^.

> 하지만, 기억만 가능(정확히는 set만)할 뿐, 다시 reset할 방법이 없음.

교과서에서만 주로 다루는 latch임.

## `AND`-`OR` Latch

`OR` latch의 feedback connection을 `OR`에 직접 연결하지 않고, `OR` 앞에 연결된 `AND`에 연결하고 동시에 해당 AND에 $\overline{\text{reset}}$ (`reset`입력을 `inverter`에 연결)을 입력시켜 reset 기능을 추가한 latch. 

`OR` Latch에서 reset이 되지 않는 단점을 보완한 것으로 **정보의 기억 및, 기억된 정보의 출력, 기억될 정보의 수정이 가능한 가장 간단한 memory**임.

문제는 symmetric structure가 아니기 때문에 gate간의 propatation delay에 취약함. 

## `S-R Latch` ***

`AND`-`OR` Latch와 같은 역할을 하지만, `NAND`나 `NOR`로 구현하여 symmetric structure를 가지도록 구현된 것이 특징이며, 이름의 `S`와 `R`은 set과 reset을 줄인 말임.  

![SR Latch](img/SR-Latch.png)

흔히 latch라고 하면 `S-R Latch`를 가르킴.

> 초기값 관련한 문제가 디지털 회로등에서 자주 제기된다. $\overline{set}$과 $\overline{rest}$이 동시에 activation되는 경우는 사용하지 않는다.

## Gated `S-R Latch`

clock signal을 입력받아서, 특정 시점의 정보를 기억하도록 `S-R Latch`를 확장한 것이며, 개념적인 `S-R Latch`가 아닌 실제 회로등에서 애기하는 `Latch`는 (특히 synchonization circuit에서) 이 Gated S-R Latch를 가르키는 경우가 많다.  

![gated Latch](img/gated%20latch.png)

S-R Latch의 $\overline{\text{reset}}$과 $\overline{\text{set}}$의 입력단 각각의 앞에 `OR`를 붙이고 각 `OR`에서 $\overline{\text{reset}}$과 $\overline{\text{set}}$의 입력을 받고, 동시에 각 `OR`은 clock이 입력될 동일 $\overline{\text{gate}}$ 입력을 받는 구조임.


위 구조에서 $\overline{\text{reset}}$과 $\overline{\text{set}}$의 입력을 분리하여 받고 있으나, 이 둘은 동시에 1이 될 수 없는 입력이다. 때문에 다음과 같이 하나의 신호로 받아, 하나는 이를 그대로 입력하고 다른 쪽에는 inverter를 거쳐 입력하는 구조로 만드는게 보다 낫다.  

![D Latch](img/D-Latch.png)

이 경우, 입력을 $D$라고 하면, 이 latch는 해당 $D$의 1bit 정보를 $\overline{\text{gate}}$에 따라 지정된 시간만큼 기억하는 memory로 동작하게 된다.

* $\overline{\text{gate}}$가 active인 경우 ($\overline{\text{gate}}=0$)에 D의 signal이 그대로 출력 $Q$에 전달됨.
* 즉, $\overline{\text{gate}}$가 active이 상태에서 $D$의 상태가 변한다면 해당 변화가 그대로 출력 $Q$에 전달

Memory는 일정기간동안 입력을 받기보다 한 순간의 값을 기억하는게 유리한 경우가 많다. 

* 일정기간 동안 입력값이 변할 경우, 어느 값이 기억될지가 알기 어려운 경우가 많기 때문임.
* 이 때문에 Latch보다는 flip-flop이 보다 많이 이용된다.
