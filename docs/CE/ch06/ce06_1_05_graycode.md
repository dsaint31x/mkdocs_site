# Gray Code and Quardrature

## Graycode

Frank Gray (1887-1969)가 개발한 encoding. binary code(이진코드)들과 달리, 인접한 숫자들 간의 차이는 1개의 비트에 불과함.

* 일반적으로 숫자를 하나 증가 또는 감소하는 카운터들에서 최소한의 비트로 빨리 처리가 가능하므로 많이 사용된다.
* 또한, 회전축(shaft)의 위치를 encoding할때, encoder들 간의 propgagation delay가 있더라도 에러가 발생하지 않기 때문에 Quadrature등에서 많이 사용됨.

다음 표는 십진수 0에서 10까지에 대한 binary code와 gray code값을 보여준다.

| | | |
|:---:|:---:|:---:|
|digit|binary|gray|
|0| 0000|0000|
|1|0001|0001|
|2|0010|0011|
|3|0011|0010|
|4|0100|0110|
|5|0101|0111|
|6|0110|0101|
|7|0111|0100|
|8|1000|1100|
|9|1001|1101|
|10|1010|1111|
|11|1011|1110|
|12|1100|1010|
|13|1101|1011|
|14|1110|1001|
|15|1111|1000|

gray code는 binary code로부터 계산된다.

* 맨처음 나오는 1은 그대로 사용.
* 맨 처음 나온 1 이후 자리의 값은 ^^binary code에서 `앞서 있는 자리의 값`과 `현재 값`^^ 을 `XOR` 수행하여 구함.

![graycode](img/graycode.png)

## python library

* [sympy's graycode](https://docs.sympy.org/latest/modules/combinatorics/graycode.html)