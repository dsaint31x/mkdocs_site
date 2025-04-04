# 양의 정수 표현하기

컴퓨터에서는 대부분 base-2 system (이진수)를 이용하여 positive integer를 표시함.

(이 문서에서 positive integer는 0을 포함한 것으로 생각할 것.)

> 보다 많은 bit가 할당된 경우, 보다 큰 range의 수를 표현(구분)할 수 있음.

이진수 외에 다른 방식이 없는 건 아니다, `Binary Coded Decimal (BCD)`와 같이 ***base-10에 기반으로 숫자를 bit로 표시*** 하는 방식도 있다. 
하지만 `BCD` 등의 다른 방식은 현재 ^^실제 컴퓨터 내부 연산에서는 사용되지 않는다^^.  
(단, `BCD` 와 같은 경우, ^^일종의 encoding 방식으로 숫자 자체를 표시^^ 하거나 ^^bit로 전달하는 경우 등에 많이 사용^^ 되므로 방식에 대한 이해는 필요하다. `BCD`는 ***숫자 심볼*** 을 컴퓨터 내에서 표현하는 데에는 좋은 방식이다.)

> Number를 **연산에 사용하는 것(의미 중심)** 과 **표시및인식 하는 것(Symbol 중심)** 으로 구분하여 생각하라(후자는 number(수)라기 보다 code(기호)에 가깝다).

* `BCD` 관련해서는 다음 Link에서 좀 더 자세히 다룬다. : [BCD (Binary Coded Decimal) System](./code_for_numbers.md)

---

---

## 2진수 대체 표기 (for Human)

컴퓨터는 2진수를 사용하지만, 인간에게 2진수는 너무 길고 읽기 어렵다.  
  
때문에, 기술문서 등에서는 2진수를 직접 기재하기보다는 $^{1}$2진수로 변환이 쉬우면서도 $^{2}$사람이 좀 더 읽기 쉬운 ^^`Hexadecimal Representation (Hex)`을 많이 사용^^ 한다 (이후 살펴보겠지만, 10진수는 2진수로 바로 변환이 좀 까다롭다).

또는 `Octal Representation`(`Oct`, 8진수)로 표현하는 경우도 있지만, 주로 `Hex`로 표기된다. 
2진수 표현에서 4자리씩 잘라서 처리(nibble)하면 쉽게 `Hex`로 변환된다 (참고로 3자리씩 자르면, `Oct`).

---

---

## 프로그래밍 언어에서 "양의 정수"표현

`C`언어 등에서 `unsigned` 라는 키워드가 붙은 경우, ^^positive만을 표현^^ 함.

`unsigned char`, `unsigned short (int)`, `unsigned int`, `unsigned long (int)`, `unsigned long long (int)`등이 양의정수를 나타내는 데이터 타입의 용어이고 이들이 차이는 할당된 bit가 많고 적음임.


* `unsigned char` : 8bits, 1byte
* `unsigned short (int)` : 16bits, 2bytes
* `unsigned long (int)` : 32bits, 4bytes
* `unsigned int` : 32bit, 4bytes
* `unsigned long long(int)` : 64bits, 8bytes

> 64bit computer 에서 사용되는 LLP64 model 기준임 (당연히, OS도 64bit).  
> 
> * [LLP64 vs. LP64 에 대하여](https://ds31x.tistory.com/405)

---

---

## 산술연산.

computer의 경우, ^^2진수의 산술연산에 기반^^ 한다.

> Computer의 경우, **adder와 multiplier** 만으로 사칙연산을 수행하는게 일반적임.

1bit의 operand 2개를 더하는 adder를 구현한다면, logical operation의 `AND`와 `XOR`를 이용하여 구할 수 있다.



