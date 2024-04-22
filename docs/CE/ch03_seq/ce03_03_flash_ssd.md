# Flash Memory and SSD

## Flash Memory 란?

`Flash Memory`는

* read 의 경우에는 `Random Access Memory (RAM)`같이 동작하며,  
* write 의 경우에는 block-access를 수행하는  

`RAM 같은 EEPROM 유형의 기억장치`.

---

---

## Solid State Disk (SSD) 란?

`Solid State Disk (SSD)`는 

* Flash memory를 Disk Drive 형태로 패키징하면서, 
* Wear Leveling Processor등을 추가하여 

HDD 처럼 Flash memory를 사용하게 한 것.

---

---

## 특징.

* 전기적으로 내용 변경 및 일괄 소거도 가능.
    * `EEPROM`의 일종.
* RAM 같은 ROM.
    * 1bit를 담고 있는 cell별로
    * read의 경우 random access가능!
    * cell이 저장할 수 있는 bit의 크기에 따라 다음으로 구분.
        * Single Level Cell(`SLC`) : 1bit/cell 저장 (=1BPC)
        * Multi Level Cell(`MLC`) : 2bit/cell 저장 (=2BPC)
        * Triple Level Cell(`TLC`) : 3bit/cell 저장 (=3BPC)
        * Quadratic Level Cell(`QLC`) : 4bit/cell 저장 (=4BPC)
    * 읽기 / 쓰기 / 지우기 단위
        * ^^32 or 64개의 `cell`이 연결된 `String`(or Column)이 read 의 최소단위(RAM 과 유사)^^ 가 되며, 
        * ^^16 or 23개의 `String`이 모여 program(=write)의 최소단위인 `Page`(or Row)^^ 를 이루고, 
        * ^^64 or 128개의 `String`이 모여 erase의 최소단위인 `Block`^^ 을 이룸 (NAND Flash 기준).
        * [Memory : Page and Column 참고 내용](./ce03_02_1_memory1.md#address-register-row-and-column)
        * Page와 비슷한 개념으로 segment가 있는데, page는 물리적으로 주소를 나누는 방식(같은 bit size로 나뉨)이고 segment는 논리적으로 나누는 방식(bit size가 다름)임.
    * ***BPC가 커질수록 read time이 커짐(=느려짐)*** : 동시에 수명도 짧아짐.
    * cell을 직렬로 연결할지 병렬로 연결할지에 따라 NAND FLASH와 NOR FLASH로 구성됨.
* 전원이 나가도 기억 유지.
    * ***DRAM 처럼 bucket(=MOSFET+Floating Gate Transistor) 에 전자를 담아 기억하는 방식*** 
    * 하지만, **DRAM과 달리 전자가 새지 않음** (전원을 공급할 필요 없음. 10년가량 기억 가능)
* 쉽게 쓰기 지우기 가능
    * 단, 0에서 1로 변경을 하려면 ^^우선 해당 데이터가 기록된 block 전체를 지우고 다시 기재^^ 해야함.
    * 특정 cell의 정보 만 수정하는 처리가 안됨. 
    * "block (or string) 단위"별로 지우고 다시 쓰기 수행
    * 때문에 Flash memory는 여러 block으로 나누어져 있음.
* 읽기/쓰기 수만번 가능.
    * 데이터를 저장하는 cell 하나당 쓰고 지우는 횟수의 한계가 존재함.
        * BPC가 높을수록 수명이 짧아짐.
    * Flash memory를 Disk Drive 형태로 패키징 한 SSD에서는 셀들을 block으로 묶고, 이들 블록이 몇차례 기록이 되었는지를 카운트하여 구성 block들이 쓰고 지워진 횟수를 일정하게 유지시키는 wear leveling processor가 있음.

---

---

## Flash Memory 종류

### NAND Flash

cell을 직렬로 연결한 방식으로 NOR Flash에 비교하여 

* read time이 느린 단점을 가지나 (page, block 의 각 셀들을 순차적으로 읽어들임), 
* program(=write)와 erase time이 page, block 단위로 이루어짐에 따라 매우 빠름.

Random Access가 안된다는 단점이 있으나, 각 cell에 대한 개별 접근을 위해 요구되는 회로가 없기 때문에
하나의 cell이 차지하는 면적이 NOR Flash 대비 40%수준으로 작고, 이는 높은 집적화와 함께 단위 저장용량에 대해 낮은 제조 단가를 가능하게 함.

저장 매체에 적합한 NAND Flash Memory

* 소형화 및 대용량화 에 유리하면서
* 저장용량단 단가가 낮음.
* read speed가 높지 않아 RAM과 같은 용도로는 사용하기 어려움.

NAND Flash는 높은 집적도의 경제성을 가진 storage 제품을 가능하게 함.

현재 NAND방식은 대용량 Flash Memory 시장에서 가장 널리 사용됨.

---

### NOR Flash

cell을 병렬로 연결한 방식으로, NAND Flash에 비해 

* RANDOM Access를 통한 read time이 6-7배 정도 빠르지만, 
* program (=write)과 erase가 cell단위로 이루어지다보니 NAND에 비해 느린 단점을 가짐.
    * 개별 cell로 작업이 이루어지기 때문에 대용량의 데이터를 쓰거나 지우는 등의 경우 느린 단점을 가짐.

Cell별로 read가 이루어지다보니 Random Access가 가능하다라는 장점이 있으나,

* cell 마다 요구되는 회로로 인해 낮은 집적도와 용량당 높은 제조단가를 가지는 단점을 가짐.
* 저장장치로는 NAND 방식에 밀린 상태.
* 부트로더, firmware 등과 같이 작은 용량의 데이터를 저장하면서 빠른 읽기 속도가 필요한 경우에 사용됨.

마이크로컨트롤러의 부트로더 등에 활용도가 높음.

---

---

## SSD

SSD의 경우, 최근 HDD를 대체하고 있는 추세임.

* 이미 노트북 등의 시장에서는 SSD가 대세로 자리잡음.
* HDD 대비 빠른 읽기/쓰기 가 가능하며 낮은 발열과 소음 이라는 장점을 가짐.
* 주로 대용량 저장을 위한 NAND Flash로 구성됨.
* wear leveling processor를 통해, 전체 device의 읽기/쓰기의 수명을 연장하며 데이터 손실 및 오류 가능성을 줄임.

> Flash Memory의 각 cell 은 일정 횟수의 프로그래밍 및 삭제 작업만이 가능함.  
> 특정 횟수 이상 쓰기/지우기 가 이루어질 경우 수명이 종료되며,  
> 이같은 읽고 쓰여진 정도를 ***wear level*** 이라고 부름.
> 데이터가 자주 업데이트되어 일부 cell이 지나치게 너무 빨리 수명이 종료되어 전체 SSD의 저장능력에 문제가 되지 않도록  
> Wear Level Processor는 모든 cell의 wear level이 균일하게 되도록 도와줌.

---

---

## References

[나무위키's Flash Memory](https://namu.wiki/w/%ED%94%8C%EB%9E%98%EC%8B%9C%20%EB%A9%94%EB%AA%A8%EB%A6%AC)
