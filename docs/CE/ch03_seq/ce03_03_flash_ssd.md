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
    * cell이 저장할 수 있는 bit의 크기에 따라 다음으로 구분.
        * Single Level Cell(SLC) : 1bit/cell 저장 (=1BPC)
        * Multi Level Cell(MLC) : 2bit/cell 저장 (=2BPC)
        * Triple Level Cell(TLC) : 3bit/cell 저장 (=3BPC)
        * Quadratic Level Cell(QLC) : 4bit/cell 저장 (=4BPC)
    * 실제로는 32 or 64개의 cell이 연결된 String(or Column)이 read의 최소단위(RAM과 유사)가 되며, 16 or 23개의 String이 모여 program(=write)의 최소단위인 Page(or Row)를 이루고, 64 or 128개의 String이 모여 erase의 최소단위인 Block을 이룸(NAND Flash 기준).
    * BPC가 커질수록 read time이 커짐(=느려짐)
    * cell을 직렬로 연결할지 병렬로 연결할지에 따라 NAND FLASH와 NOR FLASH로 구성됨.
* 전원이 나가도 기억 유지.
    * ***DRAM 처럼 bucket(=MOSFET+Floating Gate Transistor) 에 전자를 담아 기억하는 방식*** 
    * 하지만, **DRAM과 달리 전자가 새지 않음** (전원을 공급할 필요 없음. 10년가량 기억 가능)
* 쉽게 쓰기 지우기 가능
    * 단, 0에서 1로 변경을 하려면 ^^우선 해당 데이터가 기록된 block 전체를 지우고 다시 기재^^ 해야함.
    * 특정 cell의 정보 만 수정하는 처리가 안됨. 
    * "block 단위"별로 지우고 다시 쓰기 수행
    * 때문에 flash memory는 여러 block으로 나누어져 있음.
* 읽기/쓰기 수만번 가능.
    * 데이터를 저장하는 cell 하나당 쓰고 지우는 횟수의 한계가 존재함.
        * BPC가 높을수록 수명이 짧아짐.
    * Flash memory를 Disk Drive 형태로 패키징 한 SSD에서는 셀들을 block으로 묶고, 이들 블록이 몇차례 기록이 되었는지를 카운트하여 구성 block들이 쓰고 지워진 횟수를 일정하게 유지시키는 wear leveling processor가 있음.

## 종류

### NAND Flash

cell을 직렬로 연결한 방식으로 NOR Flash에 비해 read time이 느린 단점을 가지나, program(=write)와 erase time이 page, block단위로 이루어짐에 따라 매우 빠름.

더욱이 cell이 차지하는 면적을 NOR Flash 대비 40%수준이며 제조 단가도 적게 들어감.

위같은 이유로 높은 집적도의 경제성을 가진 제품이 가능하여 현재 Flash Memory시장에서 가장 널리 사용됨.

### NOR Flash

cell을 병렬로 연결한 방식으로 NAND Flash에 비해 read time이 6-7배 정도 빠르지만, program과 erase가 cell단위로 이루어지다보니 매우 느림.

낮은 집적도와 높은 제조단가로 인해 시장규모가 축소되고 있는 상황.


> SSD의 경우, 최근 HDD를 대체하고 있는 추세임.

## References

[나무위키's Flash Memory](https://namu.wiki/w/%ED%94%8C%EB%9E%98%EC%8B%9C%20%EB%A9%94%EB%AA%A8%EB%A6%AC)
