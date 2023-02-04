# Overflow and Underflow

`Overflow`
: 처리가능한 범위를 넘어서는 연산 결과가 발생하는 경우를 가르킴. computer에서 overflow 발생시  `condition code register`(CCR)의 overflow에 해당하는 bit가 `1`로 설정된다. 즉 MSB에서 발생한 carry 값이 바로 overflow bit임.

`Underflow`
: 처리가능한 범위보다 작은 연산 결과가 발생하는 경우. float등에서 처리가능한 exponent(지수)의 값이 $-126$ ~ $126$ 인데 $2^{-150}$과 같은 결과가 발생하면 이는 표현(or처리)범위보다 작은 값이며, 이 경우를 underflow라고 함.

## 참고 자료.

* Wikipedia's [Arithmetic underflow](https://en.wikipedia.org/wiki/Arithmetic_underflow)
* 나무 위키's [언더플로](https://en.wikipedia.org/wiki/Arithmetic_underflow)