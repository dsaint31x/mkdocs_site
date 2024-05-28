# The Central Processing Unit (CPU)

> Instruction 을 해석하여 실행하는 장치.  
> ***컴퓨터의 두뇌*** 에 해당.
>
> 다음의 세가지로 구성됨.
>
> * **CU (Control Unit):** instruction에 대한 `fetch`, `decode`, `execute`, `write back` 과정을 제어.
> * **ALU (Arithmetic Logic Unit):** 산술 연산 및 논리 연산을 실제로 수행.
> * **Registers:** 연산에 필요한 데이터를 임시로 저장하며, 연산 결과 저장.

CPU는 위에서 본 것처럼 ALU, Register, Control Unit(or Execution Unit)으로 구성됨  

* 이들 3가지만으로 구성된 CPU의 핵심구성요소를 ***core*** 라고 부르지만, 
* CPU는 이 외에도 cache memory, internal bus 등을 포함하고 있음

---

### 참고 : Core

각종 연산을 하는 CPU의 핵심요소.  

* ALU, 
* Register, 
* Control Unit

로 구성됨.

---

### 참고 : Microprocessor

`MPU`(Micro Processor Unit), `Micro-processor`라는 용어가 혼용됨.

과거 CPU는 여러개의 칩으로 만들어졌으나 현재는 대부분 one-chip으로 구현됨.  
때문에 `micro-processor(하나의 칩으로 구현된 CPU)`와 혼용되어 사용됨. (CPU는 인텔이, MPU는 모토로라가 사용하던 용어)

프로세서(instruction을 처리하는 logic circuit) 중 

* `디바이스의 중심이 되는 것을 cpu`라고 부르고, 
* ^^보조적 역할의 processor는 co-processor라고 부름^^ (그래픽카드가 일종의 co-processor).

> 참고로 microprocessor를 cpu로 하는 pc를 가르켜 microcomputer라고 부르는 경우도 많음.

---

### 참고 : Micro Controller Unit (MCU)

CPU의 기능을 하는 핵심 장치와 그 주변 장치(memory and IO port)들을 포함하고 있는 ***통합형 칩셋*** . 

보통 고성능의 연산이 필요하지 않으면서 ***제어 기능이 필요한 분야*** 에서 사용됨.

MCU 하나 만으로도 LED나 motor등의 다른 부품들을 control할 수 있음.

> 밥솥 등과 같은 전자제품들의 제어를 위한 부품으로 사용되기 때문에  
> 컴퓨터에서 사용되는 Microprocessor에 비해 매우 낮은 연산능력을 가지지만  
> 매우 경제적인 저가로 제작 가능.

[참고자료 : MCU와 Micro-computer, SoC](https://dsaint31.tistory.com/entry/CE-Micro-Controller-Unit-MCU-and-Micro-computer)

---

---

## Arithmetic and Logic Unit (ALU)

instruction 에 따라 데이터에 대해 산술 연산 (arithmetic operation, 덧셈, 뺄셈, 나눗셈, 곱셈 등)과 논리 연산 (logic operation, AND, OR, XOR)을 수행하는 소자


---

---

## Control Unit

CPU가 컴퓨터의 다른 구성 요소와 상호 작용하고 명령을 실행하는 데 필요한 모든 작업을 지시하고 조정하는 역할을 담당.

* CU는 instruction decoding을 수행함: <u>PC(Program Counter)가 가르키는 instruction을 메모리로부터 읽어들이는 `fetch`를 수행</u>하고 이 fetched instruction을 `decoding`함.
* instruction decoding에 따라 CPU의 다른 구성요소들에 지시를 내려 해당 instruction을 `execute`(수행)함.
    * CPU의 구성요소들인 ALU와 레지스터 등에 신호를 보내어 실제 연산을 수행하도록 지시함.
    * 예를 들어, 산술 연산이 필요하다면 ALU에 해당 연산을 수행하도록 신호를 보냄.
* CU는 데이터가 CPU 내부와 컴퓨터 시스템 전체에서 어떻게 이동하는지를 관리함: 
    * 데이터를 메모리와 레지스터, ALU 등으로 전달 및 저장되는 과정을 제어함.
    * 예를 들어, CU는 execute에서 필요한 데이터를 위해 `memory access`를 제어하고,
    * 연산 결과 저장 (`writeback`)을 위한 데이터의 이동을 지시함.

> instruction에 따라, memory와 ALU, I/O device에 제어 신호를 보내고 해당 장치들로부터 신호를 받아 다음 처리를 제어하는 장치
> storage에서 main memory로 data를 load하는 명령어, main memory에서 storage로 data를 save하는 명령어, 특정 address로부터 instruction을 로딩하는 명령어 등에 따라 ***명령을 내리는 장치***.

요약하면,  

***Control Unit은 instruction을 `fetch`하고 `decode`하며, 이를 `execute` 및 `writeback`하기 위해 필요한 제어신호를 보내는 device:*** (이 정의를 개인적으로 가장 좋아함)

* Program counter가 가르키는 address에서 수행할 명령어를 `fetch`하고,
* `fetch`된 instruction을 `decode`하여 `execute` (실행) 및 `memory access`를 수행하고 그 결과가 올바로 저장(`writeback`)되도록 제어신호를 보내고.
* 실제적으로 ALU에게 필요한 연산과 데이터를 제공하고 결과값을 올바른 메모리 장소로 보내는 일들을 담당.

---

**참고**: [Control Unit and Instruction](http://dsaint31.tistory.com/414)

---

Random logic으로 구현할 수 있지만, microcode (microinstruction을 지원하는 memory (=writable ROM 이용)로 구현된 방식) 방식으로 구현되는 경우가 많음.

microcode로 구현된 traffic control은 다음과 같은 memory로 만들어짐.

* instruction의 opcode, mode, counter 등의 조합을 `address`로 삼고,
* 해당 `address` (실제로는 특정 instruction)에 해당하는 적절한 signal을 출력하는 memory.
* control에 사용되는 여러 signal들 각각을 하나의 state라고 보고, 해당 state에 address를 할당한 일종의 state-machine임.

> control unit을 만들기 위해 여러 microcode block이 사용될 수 있고,  
> 하나의 microcode block을 만들기 위해 nanocode block 들이 사용될 수 있음. 

---

---

## Register

주로 ***CPU 내에서 data를 저장하고 있는 memory를 가르킴.***  
가장 빠른 memory이며, CPU의 구성요소.

대표적인 register 들은 다음과 같음.

* `condition code register` : overflow, underflow
* `program counter` (`pc`) : 다음 수행할 instruction이 저장된 메모리 위치를 가르킴.
* `accumulator` : ALU의 operation의 result가 저장되는 register.
* `address extension register` : 주소확장레지스터, MSB를 포함하는 상위주소 부분을 지정하는 데에 사용됨.
* `index register` : relative addressing에서 사용되는 레지스터. 현재 address에 더해질 값을 가지고 있음.
* `indirect address register` : memory에서 읽어들인(fetched) indirect address를 저장하고 있는 register.
* `instruction register` : memory로부터 fetch된 instruction을 저장하고 있는 register
