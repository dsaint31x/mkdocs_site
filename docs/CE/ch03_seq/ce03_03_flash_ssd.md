# Flash Memory and SSD

`Flash Memory`는

* read 의 경우에는 `Random Access Memory (RAM)`같이 동작하며,  
* write 의 경우에는 block-access를 수행하는  

`RAM 같은 EEPROM 유형의 기억장치`.

`Solid State Disk (SSD)`는 

Flash memory를 Disk Drive 형태로 패키징하면서, Wear Leveling Processor등을 추가하여 HDD처럼 Flash memory를 사용하게 한 것.


## 특징.
* 전기적으로 내용 변경 및 일괄 소거도 가능.
    * EEPROM의 일종.
* RAM 같은 ROM.
    * 1bit를 담고 있는 cell별로
    * read의 경우 random access가능!
* 전원이 나가도 기억 유지.
    * ***DRAM 처럼 bucket 에 전자를 담아 기억하는 방식*** 
    * 하지만, **DRAM과 달리 전자가 새지 않음** (전원을 공급할 필요 없다.)
* 쉽게 쓰기 지우기 가능
    * 단, 0에서 1로 변경을 하려면 ^^우선 해당 데이터가 기록된 block 전체를 지우고 다시 기재^^ 해야함.
    * 특정 cell의 정보 만 수정하는 처리가 안됨. 
    * "block 단위"별로 지우고 다시 쓰기 수행
    * 때문에 flash memory는 여러 block으로 나누어져 있음.
* 읽기/쓰기 수만번 가능.
    * 1비트를 저장하는 셀 하나당 쓰고 지우는 횟수의 한계가 존재함.
    * Flash memory를 Disk Drive 형태로 패키징 한 SSD에서는 셀들을 block으로 묶고, 이들 블록이 몇차례 기록이 되었는지를 카운트하여 구성 block들이 쓰고 지워진 횟수를 일정하게 유지시키는 wear leveling processor가 있음.

> SSD의 경우, 최근 HDD를 대체하고 있는 추세임.