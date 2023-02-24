# MSB and LSB

MSB는 Most Significant Bit의 약어이고, LSB는 Least Significant Bit의 약어임.

> Computer people are fond of three-letter acronyms! 

2진수 표기시 가장 왼쪽에 있는 bit가 MSB이고, 가장 오른쪽에 있는 bit가 LSB가 됨.  

![msb and lsb](img/msb_lsb.png)

    내 월급(or 용돈)을 2진수로 표기시 어느 자리 숫자가 중요한지를 생각해보면 쉽게 해당 용어를 익힐 수 있다.

* positive integer 만을 표시하는 `unsigned` 경우에는 가장 큰 자리수가 된다.
* negative integer를 고려할 경우, MSB는 positive인지 negative인지를 나타내는 sign이 됨.
    * `0` : positive.
    * `1` : negative.