# Byte Ordering: Little Endian and Big Endian

> Jonathan Swift의 걸리버 여행기의 소인국에서 삶은 달걀을 깰 때,  
> 상대적으로 둥근 쪽(big end)과 날카로운 쪽(little end) 중  
> 어느 쪽으로 깨는지에 따라 big endian과 little endian으로 나뉘어 대립하는 것에 유래됨.

memory에서 byte 단위로 읽고 쓰여지는데, memory에 데이터를 저장할 때의 byte의 순서가 다음의 두 가지 종류가 있음.

![](./img/endian.png){style="display: block; margin: 0 auto; width: 400px;"}

---

## 1. Little Endian

`Intel CPU` 에서 사용됨.

^^Word의 Most Significant Byte(MSB, 상위바이트)가 <span style="color:red;">가장 높은 주소(상위주소)에 저장</span>됨.^^

Little endian에서 ***MSB(상위바이트)는 그림으로 표기시 가장 오른쪽에 위치*** 함.

* 연산에서 유리함
* 낮은 자리의 수가 메모리에서 낮은 주소에 있으므로 연산시 낮은 주소에서 높은 주소로 진행.

---

### 1-1. Example

크기로 4바이트를 가지는 값 `0x12345678` 을  
"8bit(=1byte)의 memory word 4개"를 붙여 만든 ***32bit 크기의 Word*** 에  
`little endian` 으로 저장한다면 다음과 같음.

| memory address | 0x8001 | 0x8002 | 0x8003 | 0x8004 |
| --- | --- | --- | --- | --- |
| value (hex) | 0x78 (LSB) | 0x56 | 0x34 | 0x12 (MSB) |
| value (bin) | 0111 1000 | 0101 0110 | 0011 0100 | 0001 0010 |

- ^^1byte 내에서는 순서가 바뀌지 않는 점^^ 을 유의할 것.

---

## 2. Big Endian

Motorola CPU (주로 unix가 설치된 RISC 시스템의 CPU)에서 사용됨.

Word의 Most Significant Bytes(MSB, 상위바이트)는 가장 낮은 주소(시작주소)에 저장됨.

***Network Byte Ordering*** 으로 네트워크에서 전송시 표준으로 사용됨.


> 사실 Endian (or Byte Ordering)은 이기종간의 통신에서 중요성을 가짐.  
> Intel CPU와 Network Byte Ordering이 다르므로 이를 주의할 것.

* 네트워크 전송 이나 메모리의 값을 직접 읽어들일 때 직관적임.

### 2-1. Example

크기로 4바이트를 가지는 값 `0x12345678` 을  
"8bit(=1byte)의 memory word 4개"를 붙여 만든 ***32bit 크기의 Word*** 에  
`big endian`으로 저장한다면 다음과 같음

| memory address | 0x8001 | 0x8002 | 0x8003 | 0x8004 |
| --- | --- | --- | --- | --- |
| value (hex) | 0x12 (MSB) | 0x34 | 0x56 | 0x78 (LSB) |
| value (bin) | 0001 0010 | 0011 0100 | 0101 0110 | 0111 1000 |

---

## 3. Term : nuxi syndrome

16bit Word를 사용하던 시절의 일화 (=ascii로 생각하면 2글자가 1word로 묶여서 저장됨)

UNIX OS를 PDP-11 (big-endian)에서 IBM Series/1(little-endian)로 porting할 때 byte ordering에 문제가 발생한 사건에서 유래된 용어. 

> byte ordering과 관련된 문제를 가르키는 용어.

해당 사건은 영문은 한 글자가 1byte로 `unix` 를 출력하는 프로그램이 byte ordering이 잘못되어 `nuxi` 라고 출력한 것임 (word가 2byte라 두 글자가 한 워드임.)

---

## Note

`MSB` 는 보통 Most Significant Byte 보다 ***Most Significant Bit*** 로 더 많이 사용됨.

이 글에서는 바이트 단위로 표시하려고 전자를 취함.

---

## References

* [Embed Threads: What is Big-Endian and Little-Endian? Let’s Explain Computer Byte Order!](https://embedthreads.com/what-is-big-endian-and-little-endian-lets-explain-computer-byte-order/)

