---
title: CPU Summary
tags: [CPU, Core, ALU, Control Unit, Registers, MCU, MPU, Coprocessor, Processor]
---

# The Central Processing Unit (CPU)

> Instruction 을 해석하여 실행하는 장치.  
> ***컴퓨터의 두뇌*** 에 해당.
>
> 다음의 세가지로 구성됨.
>
> * **`CU` (Control Unit):** instruction에 대한 `fetch`, `decode`, `execute`, `write back` 과정을 제어.
> * **`ALU` (Arithmetic Logic Unit):** 산술 연산 및 논리 연산을 실제로 수행.
> * **`Registers`:** 연산에 필요한 데이터를 임시로 저장하며, 연산 결과 저장.

`CPU`는 위에서 본 것처럼 `ALU`, `Register`, `Control Unit`(or `Execution Unit`)으로 구성됨  

* 이들 3가지만으로 구성된 CPU의 핵심구성요소를 ***`Core`*** 라고 부르지만, 
* `CPU`는 이 외에도 `Cache Memory`, `Internal Bus` 등을 포함하고 있음

---

### 참고 : Core

각종 연산을 하는 `CPU`의 핵심요소.  

* `ALU`, 
* `Registers`, 
* `Control Unit`

로 구성됨.

---

### 참고 : Microprocessor

`MPU`(Micro Processor Unit), `Micro-processor`라는 용어가 혼용됨.

과거 CPU는 여러개의 칩으로 만들어졌으나 현재는 대부분 one-chip으로 구현됨.  
때문에 `micro-processor(하나의 칩으로 구현된 CPU)`와 혼용되어 사용됨.  
(CPU는 인텔이, MPU는 모토로라가 사용하던 용어)

프로세서(instruction을 처리하는 logic circuit) 중 

* `디바이스의 중심이 되는 것을 CPU`라고 부르고, 
* ^^보조적 역할의 processor는 `Co-Processor`라고 부름^^ (그래픽카드가 일종의 `Co-Processor`).

> 참고로 Microprocessor를 CPU로 하는 PC를 가르켜 Micro-Computer 라고 부르는 경우도 있음.

---

### 참고 : Micro Controller Unit (`MCU`)

CPU의 기능을 하는 핵심 장치와 그 주변 장치(memory and IO port)들을 포함하고 있는 ***통합형 칩셋*** .

Micro-Controller, Micro Control Unit 이라고도 불림.

보통 고성능의 연산이 필요하지 않으면서 ***제어 기능이 필요한 분야*** 에서 사용됨.

`MCU` 하나 만으로도 LED나 Motor등의 다른 부품들을 control할 수 있음.

> 밥솥 등과 같은 전자제품들의 제어를 위한 부품으로 사용되기 때문에  
> 컴퓨터에서 사용되는 `Micro-Processor`에 비해 매우 낮은 연산능력을 가지지만  
> 매우 경제적인 저가로 제작 가능.

[참고자료 : MCU와 Micro-computer, SoC](https://dsaint31.tistory.com/419)

---

---

## Arithmetic and Logic Unit (ALU)

instruction 에 따라 데이터에 대해 산술 연산 (arithmetic operation, 덧셈, 뺄셈, 나눗셈, 곱셈 등)과 논리 연산 (logic operation, AND, OR, XOR)을 수행하는 소자


---

---

## Control Unit (CU, 제어장치)

> Control Unit은 Instruction을 Fetch, Decoding하고,  
> Processing Unit (ALU+Register)을 통해 Instruction을 실행시킴.

CPU가 컴퓨터의 다른 구성 요소와 상호 작용하고 명령을 실행하는 데 필요한 모든 작업을 지시하고 조정하는 역할을 담당.

* `CU`는 Instruction Decoding을 수행함: 
    * <u>`PC`(Program Counter)가 가르키는 Instruction을 메모리로부터 읽어들이는 `Fetch`를 수행</u>하고
    *  이 Fetched Instruction을 `Decoding`함.
* Instruction Decoding에 따라 CPU의 다른 구성요소들(주로 `ALU`)에 지시를 내려 해당 Instruction을 `Execute`(수행)시킴.
    * CPU의 구성요소들인 `ALU`와 `Registers` 등에 신호를 보내어 실제 연산을 수행하도록 지시함.
    * 예를 들어, 산술 연산이 필요하다면 `ALU`에 해당 연산을 수행하도록 신호를 보냄.
* `CU`는 Data가 ***CPU 내부*** 와 ***컴퓨터 시스템 전체*** 에서 어떻게 이동하는지를 관리함: 
    * Data를 `Memory`와 `Registers`, `ALU` 등으로 전달 및 저장되는 과정을 제어함.
    * 예를 들어, 
        * `CU`는 Execute에서 필요한 Data를 위해 `Memory Access`를 제어하고,
        * 연산 결과 저장 (`Write Back`)을 위한 Data의 이동을 지시함.

> instruction에 따라, memory와 ALU, I/O device에 제어 신호를 보내고 해당 장치들로부터 신호를 받아 다음 처리를 제어하는 장치
> storage에서 main memory로 data를 load하는 명령어, main memory에서 storage로 data를 save하는 명령어, 특정 address로부터 instruction을 로딩하는 명령어 등에 따라 ***명령을 내리는 장치***.

요약하면,  

***Control Unit은 Instruction을 `Fetch`하고 `Decode`하며, 이를 `Execute` 및 `Writeback`하기 위해 필요한 제어신호를 보내는 Device:*** (이 정의를 개인적으로 가장 좋아함)

* Program Counter가 가르키는 Address에서 수행할 Instruction를 `Fetch`하고,
* `Fetch`된 Instruction을 `Decode`하여 `Execute` (실행) 및 `Memory Access`를 수행하고 그 결과가 올바로 저장(`Writeback`)되도록 제어신호를 보내고.
* 실제적으로 `ALU`에게 필요한 연산과 데이터를 제공하고 결과값을 올바른 메모리 장소로 보내는 일들을 담당.

---

**참고**: [`Control Unit` and `Instruction`](http://dsaint31.tistory.com/414)

---

Random Logic으로 구현할 수도 있지만, 1960년 대 이후로는  
`Microcode` [=Micro-Instruction을 지원하는 Memory (=Writable ROM 이용)로 구현된 방식] 방식으로 구현되는 경우가 더 일반적임.

Microcode로 구현된 Traffic Control은 다음과 같은 Memory (주로 ROM, `Non-Volatile`)로 만들어짐.

* Instruction의 Opcode, Mode, Counter 등의 조합을 `Address`로 삼고,
* 해당 `Address` (실제로는 이 `Address`는 특정 `Instruction`임)에 해당하는 적절한 Signal을 출력하는 Memory.
* Control에 사용되는 여러 Signal들 각각을 하나의 State라고 보고, 해당 State에 Address를 할당한 일종의 State-Machine임.

> `Control Unit`을 만들기 위해 여러 `Microcode Block`이 사용될 수 있고,  
> 하나의 `Microcode Block`을 만들기 위해 `Nanocode Block` 들이 사용될 수 있음. 

요약하면,  
`Microcode`는 CPU의 `Control Unit(제어 장치)`가  
`Machine Code`(기계어 명령어)`를 해석하고 실행하는 데 사용되는 ***저수준의 코드*** 임.  

* `Machine Code`(기계어명령어)는 CPU 의 명령어 집합 아키텍처(`ISA`)에 정의된 ***고수준***  명령어 (`Microcode`에 비해서 고수준). 
* 이 `Machine Code`는 `Microcode`에 의해 ***더 작은 단위의 마이크로연산으로 분해*** 됨. 
* 각 마이크로연산은 CPU의 특정 하드웨어 기능을 제어하는 데 사용
* `Writable ROM` 등에 저장되며, 일종의 `Firmware` 라고 볼 수 있음.
    * Firmware: 
        * 하드웨어를 제어하고, 하드웨어와 소프트웨어 간의 인터페이스를 제공하는, 
        * 읽기 전용 메모리(ROM), Flash Memory, 혹은 이와 유사한 Non-Volatile(비휘발성) 메모리에 저장된 소프트웨어.
    * Firmware에 대한 자세한 참고자료: 
        * [Firmware란](../ch03_seq/ce03_05_hw_and_sw.md#firmware)


> **Random Logic** 이란:
>
> Random Logic는 
> 
> * CPU 내부의 다양한 기능을 구현하는데 
> * 필요한 디지털 회로들을 조합하여 
> * 특정 동작을 수행하도록 만드는 방법.  
>
> 이는 일반적으로 트랜지스터, 게이트, 플립플롭 등의 기본 논리 소자를 이용해 조합 논리회로 및 순차 논리회로를 설계하는 것을 의미함.

---

---

## Register

주로 ***CPU 내에서 Data를 저장하고 있는 Memory를 가르킴.***  

* 1 Bits 저장에 6개의 NAND (=3개의 D Flip-Flop) 사용.
*  SRAM (Static RAM rlqks)

가장 빠른 Memory이며, CPU 의 구성요소에 속함 (`Core`의 구성요소이기도).

대표적인 Register 들은 다음과 같음.

* `Condition Code Register (CCR)`:
    * `O`: overflow, `U`: underflow, `S`: sign flag, `C`: carry flag
    * `I`: interrupt flag, `SU`: supervisor flag
* `Program Counter (PC)`: ***다음 수행할 Instruction이 저장된 메모리 Address*** 를 가르킴.
* `Instruction Register (IR)`: Memory로부터 Fetch된 Instruction을 저장하고 있는 Register
    * `Control Unit` 이 해석하여, ALU에게 연산을 시키거나 다른 부품에 제어신호를 보냄. 
* `Accumulator` : `ALU`의 Operation의 Result가 저장되는 Register.
* `Stack Pointer`: Memory의 Stack 영역에서 최상단 데이터의 주소를 가리킴.
* `Address Extension Register` : 주소확장레지스터, MSB를 포함하는 상위주소 부분을 지정하는 데에 사용됨.
* `Base Register` : Relative Addressing에서 사용되는 레지스터. 현재 address에 더해질 값을 가지고 있음.
* `Indirect Address Register`: Memory에서 읽어들인(Fetched) Indirect Address를 저장하고 있는 register.
* `General Purpose Register`: 범용 목적으로 사용되는 레지스터. Data, Instruction, Address 모두 젖아 가능. 

