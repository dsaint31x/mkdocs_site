---
tags: [Super Computer, Mainframe, Mini-computer,Workstation, PC, Microcomputer, Laptop, Desktop]
---

# 컴퓨터 분류.

## 사용목적에 따른 분류.

* 전용 컴퓨터 
    * Special-Purpose Computer
    * Single-Purpose Computer
* 범용 컴퓨터 (General-Purpose Computer)

---

---

![](./img/computer_classification.png){style="display: block; margin: 0 auto; width:500px"}

## 처리능력에 따른 분류. ***

아래로 갈수록 크기와 성능이 떨어진다.

* `Super-Computer` 
    * 기상관측 및 예보, 우주항공 등
* `Mainframe` (Big Iron, 대형컴퓨터)
    * 은행, 정부기관, 대학.
    * 금융권에서는 최근까지도 Mainframe기반인 경우가 많았음.
    * 1952년 공개된 1세대 컴퓨터 [IBM-701](https://en.wikipedia.org/wiki/IBM_701)과 1954년 공개된 [**IBM-704**](https://ko.wikipedia.org/wiki/IBM_704)를 최초의 Mainframe으로 본다 ([Fortran](../ch08/ce08_pl_intro.md#Fortran)이 이 IBM-704에서 프로그래밍을 하기 위해 개발됨).
* `Mini-computer` (Midrange Computer, 미니컴퓨터, 소형컴퓨터)
    * Mainframe과 비슷한 역할을 하되, 크기와 성능이 감소한 형태.
    * 1964년 [DEC](https://ko.wikipedia.org/wiki/%EB%94%94%EC%A7%80%ED%84%B8_%EC%9D%B4%ED%81%85%EB%A8%BC%ED%8A%B8_%EC%BD%94%ED%8D%BC%EB%A0%88%EC%9D%B4%EC%85%98)가 개발한 [PDP-8](https://ko.wikipedia.org/wiki/PDP-8)이 **상업적으로 성공** 한 최초의 Mini-computer (12[bit](../ch01/ch01_10_bit.md#bit-binary-digit) [word](../ch01/ch01_12_otherunits.md#word)).
        * 참고로 1970년에 출시된 Mini-computer인 PDP-11로 PDP-7의 UNIX 운영체제([Assembly Language](https://dsaint31.me/mkdocs_site/CE/ch08/ce08_assembly_language/)로 작성됨)를 [재작성( ***porting*** , 포팅)](https://dsaint31.me/mkdocs_site/CE/ch15/ce15_2_4_portability/)하기 위해 만들어진 언어가 [`C` 언어](https://dsaint31.me/mkdocs_site/CE/ch08/ce08_pl_intro/#c)임.
        * PDP-7도 Mini-computer 이며, 1965년에 출시되었음 (PDP-8보다 늦음).
    * 기업체, 학교, 연구소
* `Workstation` 
    * `PC` 규모에 Mini-computer 수준의 성능을 집약시키려는 시도.
    * High-End PC의 발전에 따라 위치가 모호해짐.
* `PC` (`Micro Computer`)
    * `Microprocessor`를 CPU로 사용하는 컴퓨터.
    * 다음과 같은 세부적인 분류가 이루어짐.
        * `Desktop`
        * `Laptop`
        * `Notebook`
        * `Palmtop` (Smart Phone에 의해 없어진 카테고리?)

---

### 참고: `Micro-Processor` :  

학술적(?)으로 이야기하면,  
* 기계어 코드(machine code)를 실행하기 위해 
* 실행과정을 단계별로 나누어 처리를 위한 microcode(마이크로 코드)를 작성하고,  
* 이 마이크로 코드에 의해 단계적으로 처리하는 논리회로를 가리키나,  

> **단일 Chip에 CPU 의 기능을 통합한 것** 을 가리키는 용도로 더 많이 사용됨.

---

### 참고: `Micro Computer` 의 경우, 

CPU가 `Micro-Processor` 였고,  
PC로 사용되었기 때문에  
초기 `PC`를 가리키는 용어로 많이 사용됨.  

오늘날에는  

* `PC`보다 좀 더 성능이 낮으면서 
* 작은 규모의 programmable control이 필요한 경우 사용되는 
* 컴퓨터 시스템을 가리키는 경우에 많이 사용됨.  
 
> 참고로, **Micro-Computer** 는 Embedded System이나 `Micro-Controller` 와도 자주 혼용됨.

---

---

## 참고자료:

* [Micro Controller Unit (MCU) and Micro-computer](https://dsaint31.tistory.com/419)
* [Machine Code와 Microcode의 차이점 비교 및 설명](https://ds31x.tistory.com/319)

---

---

## 취급 데이터에 따른 분류

> 컴퓨터는 처리하는 데이터의 형태에 따라  
> **디지털 컴퓨터**, **아날로그 컴퓨터**, 그리고 이 둘을 결합한 **하이브리드 컴퓨터** 로 분류

오늘날 컴퓨터는 대부분 Digital Computer로 digital data를 다루지만,  
Analog Data를 다루는 `Analog Computer` 와 이 둘을 결합한 `Hybrid Computer`도 존재.

Analog Computer의 경우, 많은 분야에서 `Embedded Computer` 로 대체되었음.  
(`Embedded Computer`는 Analog Data를 직접 처리하기 보다는 AD Converter를 통해 디지털로 변환해 처리하는 차이를 가짐).

Analog Computer는 ^^Continuous Data (실제적으로 Analog Data)^^ 를 직접 다루며,  
^^증폭회로 (Op-Amp)^^ 및 저항, capacitor등의 다양한 전기적 요소로 구성됨.  
아날로그인 연속적인 물리량을 직접 처리하여 결과를 산출하기 때문에 Digital Computer 보다  
소량의 실제 데이터에 대한 빠른 처리가 요구되는 분야에 많이 이용됨.  
디지털 컴퓨터에 비해 특정 분야에서 한정되어 활용되며, 자동차 엔진 제어 시스템, 의료 기기 등이 주로 사용되는 영역임.
 

> Analog Computer와 달리  
> Digital Computer는 주로 `arithmetic operations` 과 `logic operations`를 사용. 

Hybrid Computer는 아날로그와 디지털 컴퓨터의 기능을 결합하여 두 가지 유형의 장점을 모두 활용하는 시스템을 가리킴.

* 아날로그 구성 요소는 미분 방정식과 복잡한 시뮬레이션을 실시간으로 처리하는 데 사용되며, 
* 디지털 구성 요소는 논리 연산과 데이터 저장을 담당

일반적으로 컴퓨터는 Digital Computer 를 가리키는 경우가 많음.
