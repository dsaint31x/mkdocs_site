# 시간 및 기억소자들

<figure markdown>
![](./img/time_n_memory_devices.png){width=500, align=center}
</figure>

combinatorial logic과 달리,  

sequential logic의 경우 

* 과거의 출력값에도 영향을 받기 때문에 **memory device가 필요** 
* 현재의 input 이외의 과거 상태 및 현재 상태 값들을 고려하여 출력이 결정되므로 **time을 나타내는 device가 필요**.

---

**Computer에서 시간을 나타내는 device** 는 

* Oscillator 와 
* counter가 대표적이다. 

---

Computer가 사용하는 **Memory Device** 는 단순히 

* `OR` gate에 feedback을 추가한 경우에서부터 
* RAM 을 거쳐 HDD, SSD까지 다양하다. 

대부분의 컴퓨터 개론 관련 교과서들은 gate 기반의 구현물 부터 출발하는데, 여기서도 이 순서를 그대로 따르며  
`Register` 이후의 RAM, ROM, Block Device(or Disk Memory, DM) 등의 Primary Memory와 Secondary Memory는 Computer Structure에서 다룬다.

* `Latch`s **
* `Flip-Flop`s ***
* `Counter`s 
* `Register`s ****
* [Primary Memory and Secondary Memory](../ch04/ce04_01_memory.md) ***

