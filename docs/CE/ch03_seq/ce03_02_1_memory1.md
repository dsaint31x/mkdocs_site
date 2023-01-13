# Memory Component

보다 많은 bit를 기억하기 위해서는 register들을 많이 사용해야하는데, 이 경우 어느 register에 저장할지를 지정해야하고, 이를 다시 load할 때도 어느 register에서 load할지를 알아야 함.  

이같은 필요성으로 `address`가 도입된다. `address`는 memory의 특정 위치를 가르키며 실제 data가 memory의 어디에 저장되어있는지를 나타낸다.

## Memory with Address

`address`를 이용한 memory component의 구조는 다음과 같음.

![memory_with_address](img/memory_with_address.png)

* `Decoder` (이진수를 one-hot code로)를 통해, `address`를 이용하여 실제 저장된 register를 선택.
* `Selector` (`Mux`)를 이용하여 여럿 연결된 register의 출력 중 `address`에 해당하는 register의 출력을 출력.
* `tri-state` output을 선택하여 여러 memory component들을 묶음.

> 여러 output들을 하나의 핀으로 묶을 경우, open-drain 또는 tri-state 가 쓰임. 

## GPIO and BUS

General Purpose I/O는 chip에서 제공하는 pin의 수가 한정되어 있기 때문에 특정 핀들을 입력과 출력으로 같이 쓰는 경우를 애기함. `tri-state` 를 이용하여 구현됨.

> memory의 경우, read와 write가 동시에 이루어지는 경우가 거의 없기 때문에 이를 이용한 GPIO를 이용하여 단자(핀)의 수를 줄임.

BUS는 1bit의 개별 signal 대신에 연관된 signal들을 묶은 것으로 Memory의 경우 address signal들을 묶은 Address bus, data signal들을 묶은 Data bus를 가짐.

다음 그림은 아까의 Memory component에 `tri-state`를 적용하여 입출력 단자를 공유하고, Bus를 도입한 schematic representation임.

![simplified_memory](img/simplified_memory.png)

## Address Register (Row and Column)

Memory 의 용량이 커질수록 address의 길이가 길어지며, 이는 집적화에 큰 장애가 됨. 때문에 address를 상위, 하위로 나누고 register와 address strobe를 도입하여 address bus의 폭을 절반으로 줄여서 사용(일종의 multiplexing)하는 경우가 많음.

상위, 하위로 나누는 것을 matrix의 row와 column으로 생각할 수 있다. 특히 상위 Address (Row address)는 `Page`라고도 불림.

일반적으로 같이 많이 쓰이는 데이터는 한 페이지내에 같이 저장되어 Row는 고정하고 column만 변화시켜 처리하는 방식으로 동작하여 입출력 성능을 향상시킴.

![memory_with_address_register](img/memory_with_adress_register.png)

* parallel connection에서 신호를 구분하기 위해 사용하는 신호임.
* 위의 그림에서 row와 column register에 parallerl하게 $A_{0/2}$과 $A_{1/3}$이 연결되어 있는데 strobe를 통해, $A_{0/2}$과 $A_{1/3}$이 row에 대한 주소 $A_0, A_1$로 쓰이는지 아니면 column에 대한 주소$A_2, A_3$로 쓰이는지가 구분이 됨.
* strobe에 의해 메모리의 속도(latency)가 결정됨. 일반적으로 Column Access Strobe(CAS)가 memory latency를 결정함.


# Random Access Memory (RAM)

위에서 살펴본 것처럼 Address를 통해 위치를 지정하여 읽고 쓰는 방식의 memory를 random access memory (RAM)라고 부른다. 컴퓨터를 조립할 때 사용하는 RAM이 바로 random acces memory의 약어임.

> 주로, `Volatile Memory`라는 점을 주의할 것 (전원이 꺼지면 데이터가 사라짐). Core RAM이라는 Non-volatile RAM이 초기에 있었으나 사용해 본적은 없음.

RAM은 크게 다음과 같은 두 종류로 나뉜다.

* Static RAM (SRAM)
    - static(정적) : refresh가 필요없음. 전원이 공급되는 기억한 데이터를 유지하기 위한 recharge등이 필요없음.
* Dynamic RAM (DRAM)
    - dynamic(동적) : capacitor를 사용하기 때문에 leakeage current로 인해 recharge가 주기적으로 필요함.

> 컴퓨터 조립등의 경우에 흔히 애기하는 RAM은 Dynamic RAM의 일종임.

SRAM은 flip-flop, register 처럼 gate (좀더 정확히는 transistor)로 만들어진 Memory로 Transistor를 다량으로 집적(1bit 기억하는 D Flip-Flop에 6개의 Nand가 들어감)시켜야 저장용량이 커지는 구조라 대용량 memory로 만들기가 어렵다 (1셀당 6개의 tr). 즉, 용량당 들어가는 비용이 매우 큰 구조임. 하지만 속도 측면에서는 훨씬 높은 성능을 자랑함.

* on-chip memory로 쓰임. (CPU의 L1-Cache 등)
* 용량별 단가가 높으나 빠른 속도와 낮은 소비전력이 장점.
* 전원이 꺼지면 데이터가 사라지나, 전원이 켜있는 한 refresh(또는 충전)이 필요없음.

DRAM은 capacitor를 이용하여 필요한 transistor의 수를 대폭 줄인 memory이다. 실제로 기생 capcitor(Tr제조시 생기는 capcitor)를 활용하는 기술 등의 발전으로 인해 집적도가 매우 높게 구현(1셀당 1개 tr, 1개 c)이 가능하여 대용량의 memory에서 채택되는 방식이다. capcitor를 사용하기 때문에 누설전류로 인한 데이터 소실을 막기 위한 주기적인 충전이 필요(전력효율이 낮음)하고 SRAM에 비해 속도가 느림.

* computer의 main memory로 사용됨.
* 소비전력이 높고 속도도 느리지만, 용량별 단가가 SRAM대비 압도적으로 낮고, 고밀도 집적화가 가능함.
* 초기에는 비동기식이었으나, Synchronous Dynamic RAM (SDRAM)이 개발된 이후로는 system bus와 동기화되어 사용됨.
  
SDRAM은 Synchronous Dynamic RAM을 가르키며, Single Data Rate SDRAM (SDR SDRAM, SDR)에서 시작하여 Double Data Rate SDRAM (DDR SDRAM, DDR)으로 발전했으며, DDR의 경우 DDR5까지 개발된 상태임.

# 읽어볼 자료.

[strobe와 memory latency관련하여 읽어보면 좋은 자료](http://m.enuri.com/knowcom/detail.jsp?kbno=35825&bbsname=guide&cateno=&page=1)

[SDR과 DDR 관련 좋은 자료.](https://blog.naver.com/techref/222261992447)