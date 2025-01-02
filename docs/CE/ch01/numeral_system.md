---
title: Numeral System
tags: [Base, Radix, Binary, Octal, Hexdecimal, Decimal]
---

# Numeral System

> 컴퓨터에서의 Number Representation(숫자) 표현은 수체계 (진법 시스템)에 대한 이해를 요구함.  
> (특히 2진수 체계)
> Internal Representation 에서 중요.

## Numeral System (수 체계, 진법)

Numeral System은 

* Base-`?` System 또는 Radix-`?` System 이라고 불리며, 
* `?`는 `base`에 해당하는 숫자가 온다.

Numeral system에서는 

* 같은 digit(숫자기호)이라도 어느 자리에 놓여있느냐에 따라 크기가 다르며, 
* 해당 자리에 따라 다른 크기는 `Base` (or `Radix`)에 의해 결정된다.

> `Radix`는 라틴어로 뿌리라는 뜻임. `Base`와 함께 밑수를 의미하며 주로 이론서에 등장.

---

---

## Base R System ( $R$진법 )

$R$은 `Base`를 의미(정확히는 `Radix`)하며 다음과 같이 표기된다.

$$A_\text{base} = A_R=a_{n-1} a_{n-2} \cdots a_1 a_0 \color{red}.\color{black} a_{-1} a_{-2} \cdots a_{-m}$$

* 중간의 빨간색의 dot가 소수점임.

위의 값(value)는 다음과 같다.

$$V(A_\text{base})=V(A_R) = \sum^{n-1}_{i=-m} a_i R^i$$

---

---

## 주로 사용되는 것들

* $R=10$ : Base-10 system, Decimal (number) system, 10진수 , `Dec`
* $R=16$ : Base-16 system, Hexadecimal (number) system, 16진수 `Hex` / `0x`-
* $R=8$ : Base-8 system, Octal (number) system, 8진수 `Oct` / `0o`-
* $R=2$ : Base-2 systm, Binary (number) system, 2진수 `Bin` / `0b`-

---

---

## Python Example

<script src="https://gist.github.com/dsaint31x/91c62f92af9e9033edee3283ef0ea319.js"></script>
