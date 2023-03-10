# Representation of data within a computer system.

## Data vs. Information

![](../ch01/img/data_information.png)

`Data`
: 어떤 처리가 이루어지지 않은 상태의 character(문자)나 number(수치), image(그림) 등으로 ***단순히 측정하고 수집된 것*** 을 의미함. 어떤 의미나 목적을 포함하지 않고 수집 측정된 raw data를 의미. 주로 컴퓨터에 입력되는 데이터를 의미.  
`단순한 사실의 나열`이라고 생각하면 됨.

`Information`
: 어떠한 목적이나 의도에 맞게 data를 가공 처리한 것. 어떤 목적에 의해 유용하게 사용할 수 있는 것을 information이라고 함.  
`의미있는 Data`라고 생각하면 됨.

data를 처리하여 information으로 만들고, 해당 information으로 decision making이나 task가 수행된다.

![](../ch01/img/data_info2.jpg)

* original : [정보의 진화단계](http://egloos.zum.com/yjhyjh/v/39721)

하지만 많은 경우, data와 information은 구분하지않고 사용된다. 

>보통 input으로 사용되는 ^^측정 등으로 획득된 data를 raw data^^ 라고 부르며, 이후엔 거의 data라고 부름.

## Computer and Data

Computer의 또다른 정의는 다음과 같다.  

    외부로부터 입력된 값을 받아들여 처리한 결과를 출력시키거나 장래에 사용하기 위해 보관하는 장치

이를 줄여서 말하면 ***Data를 처리하여 information를 얻는 장치*** 라고 할 수 있다.

> Computer의 다른 이름인 Electronic Data Processing System(EDPS), Automatic Data Processing System(ADPS) 들이 data processing에 초점을 둔 경우이다.

Computer가 다루는 information들은 다음과 같다.

* Data
    * Numerical data : number (real number, natural number, integer, ...)
    * Non-numerical data : Letter (or `char`acter), Symbol
* Data structure (자료구조)
    * Linear Lists, 
    * Trees, 
    * Rings, 
    * etc
* Program (Instruction set)

## Data Representation

Computer 가 다루는 data들은 computer의 내부 및 외부에서 다양한 representation을 가지게 된다.

![](../ch01/img/data_representation.png)

> 주로 내부에서 사용되는 표현은 주로 계산을 위한 경우로  이진수를 기반으로 하는 numerical data 중심이며, ^^외부와의 Information exchange (정보교환) 을 위해 사용되는 표현은 code^^ 등을 기반으로하는 non-numerical data 중심이라고 볼 수 있다.

다음과 같이 data 종류 및 용도에 따라 Interal Represetation과 External Represenataion으로 바뀌어 컴퓨터에서 사용된다. 

`Numbers` (for computing)
: Most of numbers stored in the computer are eventually changed by some kinds of calculations

* Internal Representation ***for calculation*** efficiency.
* Final results need to be converted to as External Representation for presentability.

`Alphabets`, `Symbols`, and `some Numbers` 
: Elements of these information do not change in the course of processing

* No needs for Internal Representation since they are not used for calculations
* External Representation ***for processing and presentability***

## Operations

Computer가 data를 처리하는 연산을 가르킴. computer가 수행하는 작업을 가르키는 instruction과 비슷하게 사용되는데 operation은 주로 숫자 또는 논리 연산을 의미하고 instruction은 자료의 로딩, 복사 등의 컴퓨터가 수행하는 작업들이 기본 단위를 의미하는 경우로 많이 사용됨.

> Operation은 수학 등으로 정의하면, empty set이 아닌 `set`에서 2개의 element를 이용하여 제 3의 element를 만드는 것을 가르킴.

Operation의 구분은 operand (피연산자)에 따라 다음과 같이 구분됨.

* Unary
    * 1개의 operand(or input), 1개의 output.
    * `shift`, `move`, `not`
* Binary
    * 2개의 operand(or input), 1개의 output.
    * `and`, `or`, 사칙연산

operand 의 type에 따라 다음으로도 나뉨.

* Numearical Operator
* Logic Operator



