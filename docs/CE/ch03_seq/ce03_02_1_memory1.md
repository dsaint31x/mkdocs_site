# Memory Component

보다 많은 Bit를 기억하기 위해서는  
`Register`들을 여러 개를 사용하게 됨

> Memory는 
> `A Big Pile of Registers` 
> 에 기반함.

하지만 단순히 여러 `Register`s 를 묶기만 해서는 안 됨.  

여러 `Register`s 가 존재하므로 

* write 시 어느 register에 저장할지를 지정해야 하고,  
* read 시  어느 register에서 data를 읽을지를 지정해야 함.  



## Address

이같은 필요성으로 `Address`가 도입된다.  

> `Address`는
>
> * Memory의 특정 위치를 가르키며 
> * 대상 Data가 Memory의 어디에 저장되어있는지를 나타냄.

---

---

## Memory with Address

`Address`를 이용하는 memory component의 구조는 다음과 같음.

![memory_with_address](img/memory_with_address.png){style="display: block; margin: 0 auto; width:500px;"}

* [`Decoder` (이진수를 one-hot code로)](https://dsaint31.tistory.com/404#--%---Binary-%--Decoder%----)를 통해, `address`를 one-hot code로 변환하여 해당하는 Register를 선택 활성화(각각의 enable pin을 이용)
* [`Selector` (`Mux`)](https://dsaint31.tistory.com/403#--%--Multiplexer)를 이용하여 여럿 연결된 Register의 출력 중 `Address`에 해당하는 Register를 Output으로 선택.
* [`Tri-State` Output](../ch02_co/ce02_04_4_3_tri_state_output.md)을 선택하여 여러 memory components(`Registers`)를 묶음(hook).

> 여러 Output들을 ***하나의 Pin*** 으로 묶을 경우,  
>
> * Open-Drain 또는 
> * [Tri-State](https://dsaint31.me/mkdocs_site/CE/ch03_seq/ce03_02_1_memory1/#memory-with-address) 가 쓰임. 

---

---

## GPIO (General Purpose I/O)

General Purpose I/O는 Chip에서 제공하는 Pin의 수가 한정되어 있기 때문에  
특정 Pin을 **입력과 출력으로 같이 쓰는 경우** 에 사용되는 방식.  
일반적으로 `Tri-State Output` 을 이용하여 구현됨.

> Memory의 경우,  
> **Read와 Write가 동시에 이루어지는 경우가 거의 없기 때문** 에
> 보통 ***GPIO를 이용하여 단자(Pin)의 수를 줄임*** .

--- 

---

## BUS 

`BUS`는 

* 1 Bit의 개별 Signal 대신에 
* ***연관된 Signal들을 묶어서 처리하는 것*** 을 가르킴.

Memory의 경우 다음과 같은 2개의 BUS를 가짐. 

* Address Signal들을 묶은 `Address Bus`, 
* Data Signal들을 묶은 `Data Bus`를 가짐.

---

---

## Simplified Schematics of Memory

다음 그림은  

* 아까의 Memory Component에  
* `Tri-State` 기반의 `GPIO` 와,  
* `Bus`를 도입한 경우에 대한
* Simplified Schematic Representation임.

![simplified_memory](img/simplified_memory.png){style="display: block; margin: 0 auto; width:500px;"}

---

---

## Address Register (Row and Column: Page)

Memory 의 용량이 커질수록 Address의 길이가 길어지며,  
이는 집적화에 큰 장애가 됨.  

* 때문에 Address를 상위, 하위로 나누고 
* Address Register들 (Column Address Register, Row Address Register)과
* Address Strobe들 (`CAS`, `RAS`)를 도입하여 
* Address Bus의 폭을 절반으로 줄여서 사용(일종의 Multiplexing)하는 경우가 많음.

**상위, 하위로 나누는 것** 을 **matrix의 Row와 Column으로 생각** 할 수 있다. 

특히 ***상위 Address (Row address)는 `Page`라고도 불림*** .

사실, `Page` 라는 용어는 여러 가지로 사용되는데, Memory의 주소의 관점에서는 상위 영역을 가리키는데 사용됨: [`MMU`의 `Paging`](../ch05/ch05_06_01_mmu.md) 를 참고.

> 큰 숫자에 해당하는 Address가 **상위 Address** 임.

일반적으로 같이 많이 쓰이는 데이터는  

* 한 `Page` 내에 같이 저장하여  
* ^^Row는 고정하고 Column만 변화시켜 처리하는 방식^^ 으로 동작
* 가능하도록 함으로써, Memory의 입출력 성능을 향상시킴.

![memory_with_address_register](img/memory_with_adress_register.png){style="display: block; margin: 0 auto; width:500px;"}

* `Strobe`는 **Parallel Connection에서 신호를 구분하기 위해 사용하는 신호** 를 가르킴
    * Memory에선 
    * Column Address Strobe (CAS)와 
    * Row Address Strobe (RAS)가 있음.

> `Strobe` 는 콘서트 등에서 깜빡이는 점멸등을 나타내는데에 사용되기도 하는 단어로,  
> 짧은 간격의 깜빡임을 나타냄.  
> 공학에서는 특정작업을 동기화하여 사용하기 위해 이용되는 신호나  
> 특정작업이나 이벤트를 알리는 신호를 가리킴  
> (짧은 간격으로 반복되어 발생하는 경우에 많이 사용됨)
 
* 위의 그림에서 Row와 Column Register에 Parallel 하게
    * $A_{0/2}$과 $A_{1/3}$이 연결되어 있는데
    * `CAS`와 `RAS`를 통해,
    * $A_{0/2}$과 $A_{1/3}$이 Row에 대한 주소 $A_0, A_1$로 쓰이는지
    * 아니면 Column에 대한 주소$A_2, A_3$로 쓰이는지가 구분이 됨.
* Strobe들에 의해 메모리의 속도(Latency)가 결정됨. 
    * ^^일반적으로 Column Access Strobe(`CAS`)가 Memory Latency를 결정함^^ .
 
> 참고: **Latency (지연시간)**
>
> 어떤 작업, 신호, 요청 등이 시작되고 완료되기까지의 시간적 지연 을 가리킴.

---

---

## 읽어볼 자료.

* [Strobe와 Memory Latency관련하여 읽어보면 좋은 자료](http://m.enuri.com/knowcom/detail.jsp?kbno=35825&bbsname=guide&cateno=&page=1)
