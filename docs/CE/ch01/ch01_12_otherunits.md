---
title: Units for bit.
tags: [Bit, Bytes, Word, Field, Record]
---

# bit 관련 단위.

bit는 `0`,`1`의 값을 갖는 ^^information의 최소단위^^ 이기 때문에 너무 작은 정보량임.

정보량을 나타내기 위해 보다 큰 표현 단위가 필요해짐에 따라 다음과 같은 단위들이 나옴.

## `bit` 
: information의 최소단위

---

## `nibble` 
: `4bit` 에 해당하는 단위. (현재는 많이 사용되지 않는다.) 16진수와 묶여서 사용됨.

---

## `byte` 
: `8bit` 에 해당.  
    주로 사용되는 단위들 중에서 가장 작음.(bit는 너무 작아 안쓰임) 

---

## `word`

word는 

* computer architecture에서
* CPU(or Processor)가 기본 단위로 다루는
* data unit을 가리키는 용어이다.

다만 word의 크기는 bit나 bytes와 달리 고정되어 있지 않음.

> word는
>
> * 특정 machine의 pointer 크기나
> * 한 clock cycle에 처리할 수 있는 data 크기로 이해하는 경우도 있으나,
> 
> 엄밀하게 애기하면 이들과 항상 같지 않으므로 주의해야 함.

초보자 입장에서는 word를 “CPU가 기준 단위처럼 다루는 data 크기” 정도로 이해하는 것이 좋음:

* Computer architecture, ISA, ABI, API 등등 word라는 용어가 사용된 계층에 따라
* 크기가 달라질 수 있으므로 주의 해야 한다.

**참고:**

| 계층 |	정의 |
|---|---|
|Computer Architecture	|computer architecture는 computer system의 구조, 구성 요소, 동작 방식, 그리고 hardware와 software 사이의 설계 원리를 다루는 분야이다.
|ISA	|ISA는 software가 processor를 제어하기 위해 사용할 수 있는 instruction, register, addressing mode, data type 등을 정의한 processor의 programmer-visible interface이다.
|ABI	|ABI는 compiled binary가 특정 OS와 processor 환경에서 실행될 수 있도록 calling convention, register 사용, data layout, alignment, symbol naming 등을 정한 binary-level interface이다.
|API	|API는 source code 수준에서 program이 OS, library, framework의 기능을 사용하기 위해 호출하는 function, data type, constant, object 등의 source-level interface이다.

* `word`는 computer architecture 문맥에서 등장하는 일반적인 용어이다.
* ISA 문서에서는 `word`, `doubleword` 같은 용어가 instruction의 operand 크기를 설명하는 데 사용될 수 있다.
& ABI 문맥에서는 `word` 자체를 새로 정의한다기보다는, pointer size, data type size, alignment, calling convention처럼 compiled binary가 실제로 데이터를 배치하고 전달하는 규칙을 정한다.
* 반면 Windows API의 `WORD`, `DWORD`, `QWORD`는 ISA나 ABI 용어가 아니라 Windows API에서 source code 수준으로 제공하는 type name이다.

따라서 엄밀히 애기하면, `word`, pointer 크기, `WORD`는 구분해야 함.

* `word`는 architecture/ISA 문맥의 기본 data unit 용어이고,
* pointer 크기는 ABI에 의해 실제 실행 환경에서 정해지며,
* `WORD`는 Windows API에서 정의한 자료형 이름이다.

다음은 대략적인 경향을 파악하기 위해 일반적인 경우를 소개한다.

### ARM ISA 경우

AArch32와 AArch64 등

* `Halfword` : 2bytes
* `Word` : 4bytes
* `Doubleword` : 8bytes

### x86 ISA 계열

x86 ISA 계열에서는 역사적 하위 호환성으로 인해 ARM의 경우보다 크기가 작은 편임.

* `Halfword` : 일반적으로 잘 사용되지 않음.
* `Word` : 2bytes
* `Doubleword` : 4bytes
* `Quadword` : 8bytes

> x86-64 system이 64-bit machine이라고 해서 word가 8 bytes가 되는 것은 아님에 유의.

### API 문맥에서의 WORD, DWORD, QWORD

Windows API에서는 WORD, DWORD, QWORD 같은 type name을 사용한다.

이들은 ISA가 직접 정의한 용어가 아니라 Windows API에서 source code 수준으로 제공하는 자료형 이름임:

* `WORD`: 2 bytes
* `DWORD` :	4 bytes
* `QWORD` : 8 bytes

참고로 `DWORD`는 Double Word의 약자이지만, Windows API 문맥에서는 4 bytes를 의미한다.

64-bit Windows에서 pointer는 보통 8 bytes이지만, 하위호환성 문제로 여전히 `WORD`는 2 bytes이고 `DWORD`는 4 bytes로 유지된다.

---

## `field` 
: 여기서부터는 정량적인 단위라기보다 논리적인 단위임.  
***파일 구성의 최소 단위.***  
아이템 혹은 항목이라고도 불림. 오늘날엔 주로 DB의 열(`Column`)을 의미함.

---

## `record` 
: 하나 이상의 관련된 field가 모여 구성됨.  
오늘날엔 주로 DB의 행(`Row`)을 의미함.

---

## `block` 
: 하나 이상의 관련된 Record가 모여 구성됨.  
주로 **최소 I/O단위** 로 많이 사용됨 (block 단위로 입출력이 이루어지는 device가 보편환되었기 때문).  
물리적 Record로 불림.

---

## `file` 
: 프로그램 구성의 기본 단위.  
Storage에서 사람이 인식하는 기본 저장 단위이다.

---

## `DB` 
: Database를 가리키며, 여러 개의 관련된 파일의 집합을 의미하지만,  
일반적으로 `RDBMS`과 같은 ***Database 시스템*** 을 지칭하는데 사용되지  
정보량을 의미하는데엔 잘 사용되지 않는다.

