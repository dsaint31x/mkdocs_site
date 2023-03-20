# Real Number

실수를 bit로 표현하는 방법을 알기 이전에 2진수로 소수를 표현할 수 있어야 한다.

* 다음 URL을 참고 : [소수의 2진수 표현](https://www.notion.so/mmmil/1-The-Internal-Language-of-Computers-07104725d17643feafb37c615f327d01#cdf5f63a0ff043d1a888441fb61e3976)
* 소수까지 2진수로 표현하게 되면, 실수에 대한 2진수 표현이 가능해진다. 

일단 실수의 2진수 표현을 bit로 표현하는 방법은 크게 다음 두가지로 나뉜다.

* `Fixed-Point Representation` : 기존의 integer를 표현하던 방식을 그대로 사용. (특정 자리의 bit로는 integer부분을 표현하고, 나머지 부분은 소수부분을 표현. DSP에서 사용됨.)
* `Floating-Point Representation` : 위의 경우처럼 소수점의 위치가 고정되지 않고 변경됨. scientific notation (과학적표기법)에 기반.

> Scientific Notation : [참고 URL](https://dsaint31.tistory.com/entry/%EC%B8%A1%EC%A0%95%EC%B9%98%EC%97%90%EC%84%9C-%EC%9C%A0%ED%9A%A8%EC%88%AB%EC%9E%90-%ED%99%95%EC%9D%B8-%EB%B0%8F-%EA%B3%BC%ED%95%99%EC%A0%81-%ED%91%9C%EA%B8%B0%EB%B2%95)

일반적으로 computer에서는 Floating-point represetation이 사용되며, 일부 Digital Signal Processing (DSP) System에서만 fixed-point representation이 사용된다. 이는 동일한 크기의 bit로 표현할 수 있는 수의 range(범위)가 Fixed-point representation이 Floating-point representation에 비해 너무나 적은 범위로 제한되기 때문이다.  
실제로 컴퓨터로 Physics분야의 연산을 해야할 경우, Fixed-point representation로는 200bit이상의 데이터 타입을 필요할 정도로 낭비가 심하다.

> Planck’s constant ($6.63 × 10^{–34}$ joule-seconds) 와 Avogadro’s constant ($6.02 × 10^{23}$ molecules/mole)를 같이 사용하는 경우를 생각해보라.

## Floating-Point Representation

부동소수점이라고 번역되며, ***유효숫자를 가지는 측정치*** 를 사용할 수 밖에 없는 과학 및 이공학 분야의 Scientific Notation을 기반으로 실수를 표현한다.  

소수점이 고정되지 않지만, 고정된 유효숫자 자리수를 가지기 때문에 ^^큰 수를 표현할 때는 정밀도가 떨어지고^^, ^^아주 작은 수들을 표현하여 정밀하게 사용될 때는 나타낼 수 있는 수의 크기가 작아진다^^. 수의 표현 범위(range)와 정밀도(precision)은 trade-off 관계인데, Floating-Point Representation은 Fixed-point representation와 비교할 경우, 이 두가지 측면에서 모두 우수한 성능을 보인다 (가변적으로 집중이 이루어짐). 

> `측정치`란 측정기구나 방식에 의해 의미를 가지는 수의 범위가 결정되며, 때문에 모든 경우 측정치는 일종의 근사치(approximation)이지 정확한 값이 아니다. 이를 반영한 Scientific Notation은 수(number)를 표시할 때 ***의미를 가지는 유효숫자들만*** 을 표현하며 불확실성의 정도를 같이 나타낸다.  
> 이를 기반으로 하는 Floating-Point Representation도 결국 근사치를 표시하는 방법이라고 할 수 있고, 때문에 1/3과 같이 정확한 숫자 표현이 아닌 현재 사용가능한 bit에서 가장 에러가 적은 근사치를 표시하게 된다.

줄여서 `float` 라고 불리며, 컴퓨터 프로그래머들에게 `float`는 그냥 real number의 다른 이름으로 인식될 정도로 널리 사용되고 있다.

Floating-Point Representation를 제한된 크기의 bit로 나타내는 방법은 IEEE에 의해 `IEEE754로 표준화`가 되어 있다. 

* 할당된 bit가 많아질수록 ***정밀도*** 가 향상된다. 때문에 32bit float를 single precision floating point number (단정도 부동소수), 64bit를 double precision floating point number (배정도 부동소수)라고 부른다.
* 0으로 나눈 결과처럼, 숫자가 아닌 결과에 대한 표현 (`NaN`, Not a Number의 약자)들도 쉽게 처리할 수 있다는 장점을 가진다.

IEEE754를 간략히 설명한 다음 URL을 참고하라. : [Float 표현하기 : IEEE754](https://dsaint31.tistory.com/entry/CE-Float-%ED%91%9C%ED%98%84%ED%95%98%EA%B8%B0-IEEE754)
