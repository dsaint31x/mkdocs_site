# Negative Number

컴퓨터에서 bit로 음수를 표현하는 방법은 크게 다음의 3가지가 있음.

* Sign and Magnitude
* 1's Complement (1의 보수)
* 2's Complement (2의 보수) \*\*

가장 널리 사용되는 방식은 **2's Complement** 이며, 앞의 방법들은 이를 이해하기 위한 stepping stone정도로 생각해도 된다.

## Sign and Magnitude

가장 simple한 방법. 

* MSB는 sign을 나타낸다.
* 나머지 bit들은 positive integer의 경우와 마찬가지로 magnitude를 나타냄.

> 공학에서 magnitude는 크기, 양 등을 나타내며, 보통 0이상의 양수를 value로 가짐.

`Sign and Magnitude`는 단점으로 `+0`과 `-0`의 표현이 각각 존재하게 된다. (같은 수이니 하나로 표현되어야 하는데 2개의 다른 표현형이 존재함.) 또한 logic operation으로 arithmetic operation을 구현하기 쉽지 않음.

## 1's Complement (1의 보수)

positive inteager표현에서 모든 bit에 `NOT`연산을 취함으로서 대응되는 negative inteager를 구하는 방법.

> `011` (=+3)의 모든 bit에 `NOT`을 취하면, `100`이 되며 이를 -3으로 삼는 방법이다. MSB가 `1`이면 negative가 됨.

`Sign and Magnitude`와 마찬가지로 `+0`과 `-0`의 표현이 각각 존재한다.

## 2's Complement ***

2's complement는 negative integer를 구할 때 우선 1's complment을 구하고 여기에 1을 더해준다.

> `011` (=+3)을 예로 들면 1's complement인 `100`에 1을 더한 `101`이 바로 -3의 표현형이 된다.

zero에 대한 표현형이 하나가 되며, artithmetaic operation을 구하기도 간단하다.



