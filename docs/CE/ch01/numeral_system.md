# Numeral System

Base-`?` System 또는 Radix-`?` System 이라고 불리며, `?`는 base에 해당하는 숫자가 온다.

Numeral system에서는 같은 digit(숫자기호)이라도 어느 자리에 놓여있느냐에 따라 크기가 다르며, 해당 자리에 따라 다른 크기는 base (or raidx)에 의해  결정된다.

## Base R System

$R$은 Base를 의미하며 다음과 같이 표기된다.

$$A_\text{base}=a_{n-1} a_{n-2} \cdots a_1 a_0 . \a_{-1} a_{-2} \cdot a_{-m}$$

위의 값(value)는 다음과 같다.

$$V(A_\text{base}) = \sum^{n-1}_{i=-m} a_i R^i$$

## 주로 사용되는 것들

* $R=10$ : Base-10 systme, Decimal (number) system, 10진수 , `Dec`
* $R=16$ : Base-16 systme, Hexadecimal (number) system, 16진수 `Hex` / `0x`-
* $R=8$ : Base-8 systme, Octal (number) system, 8진수 `Oct` / `0o`-
* $R=2$ : Base-2 systme, Binary (number) system, 2진수 `Bin` / `0b`-

## Python Example

<script src="https://gist.github.com/dsaint31x/91c62f92af9e9033edee3283ef0ea319.js"></script>