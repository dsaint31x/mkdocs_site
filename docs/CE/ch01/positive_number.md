# 양의 정수 표현하기

컴퓨터에서는 대부분 base-2 system (이진수)를 이용하여 bit로 positive integer를 표시함.

다른 방식이 없는 건 아니며, Binary Coded Decimal (BCD)와 같이 base-10에 기반으로 bit로 표시하는 방식이 있지만, 실제 컴퓨터 내부 연산에서는 사용되지 않는다.
(단, BCD와 같은 경우, 일종의 encoding방식으로 숫자 자체를 연산이 아닌 표시하거나 bit로 전달하는 경우 등에 많이 사용되므로 방법에 대해서는 알고 있는 것이 좋음)

> 많은 bit가 할당된 경우, 보다 큰 range의 수를 표현(구분)할 수 있음.

## 프로그래밍 언어에서 "양의 정수"표현

C언어 등에서 `unsigned` 라는 키워드가 붙은 경우, positive만을 표현함.

`unsigned char`, `unsigned short (int)`, `unsigned int`, `unsigned long (int)`, `unsigned long long (int)`등이 양의정수를 나타내는 데이터 타입의 용어이고 이들이 차이는 할당된 bit가 많고 적음임.


* `unsigned char` : 8bits, 1byte
* `unsigned short (int)` : 16bits, 2bytes
* `unsigned long (int)` : 32bits, 4bytes
* `unsigned int` : 32bit, 4bytes
* `unsigned long long(int)` : 64bits, 8bytes

> 64bit computer 기준임 (OS도 64bit).

## 산술연산.

computer의 경우, 2진수의 산술연산에 기반한다.

> Computer의 경우, adder와 multiplier만으로 사칙연산을 수행하는게 일반적임.

1bit의 operand 2개를 더하는 adder를 구현한다면, logic operation의 `AND`와 `XOR`를 이용하여 구할 수 있다.



