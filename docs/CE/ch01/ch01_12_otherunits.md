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

## `half word` 
: `16bit` 에 해당 (ARM 기준).  
초기 컴퓨터가 16bit machine일 때의 `word`였으나,  
컴퓨터가 발전하면서 half를 붙여서 구분.

---

## `long word (or full word)` 
: `32bit` 에 해당 (ARM 기준).  
컴퓨터가 32bit machine일 때의 `word`.  
컴퓨터가 발전하면서 `long`이라는 `prefix`가 붙어서 구분하기 시작.  
일반적으로 `word` 라고 하면 `long word`를 가리키는 경우가 많음.

---

## `word`

* `word` 란 ***컴퓨터가 한 cycle에 처리할 수 있는 단위*** 를 가르킴. 
    * 주소를 가르키는 pointer 변수의 크기라고 생각하면 쉽다.
* 주로 **데이터의 입력, 처리, 저장 및 출력을 수행하는 기본 단위** 를 지칭한다.

위의 word 정의에 따르면, word는 계속 커질 수 밖에 없기 때문에 prefix를 붙여 구분을 함.

`Word` 관련한 Data Types의 크기는 아키텍처나 OS등에 따라 차이가 심한 편이므로  
개발 전에 반드시 확인을 해두는게 좋다.  
다음은 대략적인 경향을 파악하기 위해 일반적인 경우를 소개한다.

### ARM Processor

* `Half Word` : 2bytes
* `Word` : 4bytes
* `Double Word` : 8bytes

### x86 processor (intel, amd)

* `Half Word` : 일반적으로 잘 사용되지 않음.
* `Word` : 2bytes
* `Double Word` : 4bytes
* `Quad Word` : 8bytes

### x64 Processor (Windows)
* `Half Word` : 2bytes
* `WORD` : 2bytes
* `DWORD` : 4bytes
* `QWORD` : 8bytes

---
  
## `double word` 
: 64bit 에 해당 (ARM기준).  
현재의 computer는 64bit machine으로 원래 word의 정의에 따르면, 현재는 `double word`가 word임.   
하지만 하위호환성 등에 대한 고려로, 이를 word라고 하진 않고 `double word`라고 지칭하는 게 일반적임.

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
: Database를 가르키며, 여러 개의 관련된 파일의 집합을 의미하지만,  
일반적으로 `RDBMS`과 같은 ***Database 시스템*** 을 지칭하는데 사용되지  
정보량을 의미하는데엔 잘 사용되지 않는다.

