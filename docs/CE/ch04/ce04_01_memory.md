# Memory (기억장치)

컴퓨터는 어찌보면 ^^입력된 데이터들을 처리하고 그 결과를 출력하는 장치^^ 라고 볼 수 있다. 

데이터 처리는 데이터 등에 해당하는 여러 bit를 조작해야만 하며, 이들을 저장할 장소가 필연적으로 요구된다. 

***컴퓨터에서 bit들을 저장하는 장소를 `memory` (기억장치)라고 부른다.***

## Memory Location and Address

memory에 대한 접근은 `address`를 통해 이루어짐.

- address가 다르면 memory내의 위치가 다름.
- Memory의 각 1 byte별로 address를 할당하는 Byte oriented addressing이 사용됨.

<figure markdown>
![](./img/memory_lane.jpeg)
</figure>

위 그림에서 집들은 1byte의 같은 크기를 가지는 각각의 `memory location`을 의미한다.

- 각각의 집(memory location)에는 `byte address`가 할당되어 있음.
- 64bit computer의 경우 이런 memory location이 $2^{64}(=n)$개 존재할 수 있음.
- Memory Lane = Memory bus, City Center = CPU

Memory의 address를 지정할 때, `byte`들을 2개, 4개, 또는 8개를 묶어서 지정하는게 일반적이다. 현재의 64bit computer에서는 8개의 byte를 묶어서 한번에 지정한다.

## Memory Address and OS

64bit computer인지 32bit computer인지는 실제로는 CPU 내의 memory(기억장치)인 register의 크기로 결정됨. 

> 64bit computer 는 CPU 내의 register의 크기가 64bit임.
> 

memory에 저장된 값을 **CPU가 접근** 하기 위해서 ***cpu내 register에 address가 저장*** 되므로 몇 비트 컴퓨터이냐에 따라 가용 memory의 한계가 결정됨.

- 16bit computer는 memory address를 $2^{16}$가지로 지정 가능. 이는 2bytes로 address를 지정함을 의미. (16bit를 word라고 자주 부름)
- 32bit computer는 memory address를 $2^{32}$가지로 지정 가능. 이는 4bytes로 address를 지정함을 의미. (32bit를 long word라고 자주 부름)
- 64bit computer는 memory address를 $2^{64}$가지로 지정 가능. 이는 8byte로 address를 지정함을 의미.

64bit computer의 경우, $2^{64}$ bytes에 해당하는 address를 가질 수 있으나, 실제 memory addressing에는 ***전체 64bit 중 하위 48bit만 사용*** 함.

- `C`언어에서의 **pointer variable (포인터 변수)**의 크기(자료형의 크기)를 보면, 해당 memory address가 어느정도 크기인지를 알 수 있음.
- 64bit computer가 제대로 동작하려면, HW 측면 외에도 SW 적으로도 64bit가 지원되어야 함.
- 무엇보다 OS부터 64bit OS를 설치해야 함.

## Nonaligned Access

32bit Computer의 경우, Memory에서 32bit word 단위로 읽어들일 때 **4개의 byte가 묶여서 읽어들여짐.** 

하지만, 4개의 byte가 address 순서에 따라 묶어져서 처리되므로, 아래 그림처럼 5,6,7,8의 byte address는 하나의 word로 묶어 처리할 수 없기 때문에, 2번의 access가 필요하게 된다.

<figure markdown>
![](./img/not_aligned_access.jpeg)
</figure>

- 참고로 일반적으로 `int` type으로 수치 데이터를 다루는 것이 가장 빠름.
- 하지만 실수형 데이터(real number)를 다룰 때는 `double`이나 `float` 중 에서 골라야 함(정수형보다는 느림.). : 라이브러리에서 기본으로 지정된 것을 사용하는게 가장 좋다.

# price/performance ratio and Access time

`register`
: 속도는 최고이나 가장 비싸고 많은 데이터 저장이 어려움. CPU 내부에 위치. ALU등이 바로 사용하는 작은 크기의 데이터를 담고 있음. (flip-flop으로 구성됨)

`SRAM (Cache)`
: register보단 느리나 충분한 속도를 가짐. register보단 동일 가격에 보다 많은 데이터를 저장할 수 있음. CPU 내부에 위치 (register보다는 거리가 멀리 있으며 거리순에 따라, l1, l2, l3등으로 나뉨)

`DRAM` 
: 주기억장치로 많이 사용됨. SRAM보다는 느리지만 가성비는 보다 나음. 보통 RAM이라고 하면 DRAM을 가르킴

`HDD`
: 보조기억장치의 대표격으로 속도는 매우 느리지만, 같은 비용에 매우 많은 데이터를 저장 가능함.

`SSD` 
: HDD를 대신하는 보조기억장치로 떠오르고 있음. HDD보다 빠른 ACCESS를 보이나 비용이 아직은 HDD보다 높음.

<figure markdown>
![](./img/memory_types.jpeg)
<figcaption>ref. https://wisetrue.tistory.com/m/173 </figcaption> 
</figure>

- capacitance (용량)은 아래로 갈수록 커짐.
- `throughout`은 `단위시간당 처리량(속도)`로 위로 갈수록 커짐.

## References

* [The Secret Life of Programs, ch4](https://nostarch.com/foundationsofcomp)
* [윌리의 Technical References](https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=techref&logNo=222246966805)