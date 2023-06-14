# The Central Processing Unit (CPU)

> operator (or instruction)을 해석하여 실행하는 장치. 컴퓨터의 두뇌에 해당.

ALU, Register, Control Unit(or Execution Unit)으로 구성됨  
(이들 3가지만으로 구성된 CPU의 핵심구성요소를 core라고 부르며, CPU는 이 외에도 cache memory, internal bus 등을 포함하고 있음)

### 참고 : Core

각종 연산을 하는 CPU의 핵심요소.  

* ALU, 
* Register, 
* Control Unit

을 가르킴.

### 참고 : Microprocessor

`MPU`(Micro Processor Unit), `Micro-processor`라는 용어가 혼용됨.

과거 CPU는 여러개의 칩으로 만들어졌으나 현재는 대부분 one-chip으로 구현됨. 때문에 `micro-processor(하나의 칩으로 구현된 CPU)`와 혼용되어 사용됨. (CPU는 인텔이, MPU는 모토로라가 사용하던 용어)

프로세서(instruction을 처리하는 logic circuit) 중 `디바이스의 중심이 되는 것을 cpu`라고 부르고, ^^보조적 역할의 processor는 co-processor라고 부름^^ (그래픽카드가 일종의 co-processor).

### 참고 : Micro Controller Unit (MCU)

CPU의 기능을 하는 핵심 장치와 그 주변 장치(memory and IO port)들을 포함하고 있는 통합형 칩셋. 보통 고성능의 연산이 필요하지 않으면서 제어 기능이 필요한 분야에서 사용됨.

MCU 하나 만으로도 LED나 motor등의 다른 부품들을 control할 수 있음.

> 밥솥 등과 같은 전자제품들의 제어를 위한 부품으로 사용되기 때문에 컴퓨터에서 사용되는 Microprocessor에 비해 매우 낮은 연산능력의 저가의 제품이 대부분임.

[참고자료 : MCU와 Micro-computer, SoC](https://dsaint31.tistory.com/entry/CE-Micro-Controller-Unit-MCU-and-Micro-computer)

## Arithmetic and Logic Unit (ALU)

instruction 에 따라 데이터에 대해 산술 연산 (arithmetic operation, 덧셈, 뺄셈, 나눗셈, 곱셈 등)과 논리 연산 (logic operation, AND, OR, XOR)을 수행하는 소자

## Control Unit

storage에서 main memory로 data를 load하는 명령어, main memory에서 storage로 data를 save하는 명령어, 특정 address로부터 instruction을 로딩하는 명령어 등에 따라 명령을 내리는 장치.

* Program counter가 가르키는 address에서 수행할 명령어를 fetch하고,
* fetch된 instruction을 decode하여 execute (실행)함.

instruction에 따라, memory와 ALU, I/O device에 제어 신호를 보내고 해당 장치들로부터 신호를 받아 다음 처리를 제어.

Random logic으로 구현할 수 있지만, microcode (microinstruction을 지원하는 memory (=writable ROM 이용)로 구현된 방식) 방식으로 구현되는 경우가 많음.

microcode로 구현된 traffic control은 다음과 같은 memory로 만들어짐.

* instruction의 opcode, mode, counter 등의 조합을 `address`로 삼고,
* 해당 `address` (실제로는 특정 instruction)에 해당하는 적절한 signal을 출력하는 memory.
* control에 사용되는 여러 signal들 각각을 하나의 state라고 보고, 해당 state에 address를 할당한 일종의 state-machine임.

> control unit을 만들기 위해 여러 microcoded block이 사용될 수 있고, 하나의 microcoded block을 만들기 위해 nanocoded block들이 사용될 수 있음. 

## Register

주로 CPU내에서 data를 저장하고 있는 memory를 가르킴. 가장 빠른 memory이며, CPU의 구성요소.

* `condition code register` : overflow, underflow
* `program counter` (`pc`) : 다음 수행할 instruction이 저장된 메모리 위치를 가르킴.
* `accumulator` : ALU의 operation의 result가 저장되는 register.
* `address extension register` : 주소확장레지스터, MSB를 포함하는 상위주소 부분을 지정하는 데에 사용됨.
* `index register` : relative addressing에서 사용되는 레지스터. 현재 address에 더해질 값을 가지고 있음.
* `indirect address register` : memory에서 읽어들인(fetched) indirect address를 저장하고 있는 register.
* `instruction register` : memory로부터 fetch된 instruction을 저장하고 있는 register
