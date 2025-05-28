# Object Oriented Programming (OOP)


## OOP란?

OOP는 

* **Object 에 기반** 하여,
* **Object 를 이용** 하고 **Object 를 만들고(정의 및 구현), Object 를 조합** 하여 **프로그래밍** 하는 Program paradigm의 하나.

을 가르킴.

> Programming Paradigm 의 관점에서  
> Structured Programming과 함께 현재 가장 널리 사용되는 Programming paradigm이다. 

## OOP Language가 되려면?

어떤 Programming Language가 OOP Language라고 불리려면 최소한 다음 3가지 특성을 가져야 한다.

- Encapsulation
- Inheritance
- Polymorphism

OOP는 다양한 object들이 서로 상호작용(message passing을 통한)을 통해 실제 세계와 비슷한 모델링으로 프로그래밍을 가능하게 해주는 프로그래밍 패러다임이며, Object에 대한 이해가 OOP를 이해하기 위해 선행되어야 한다.

---

## OOP에서의 SOLID 원칙

OOP에서 S/W 를 더욱 **유지보수** 및 **확장** 하기 쉽게 만들기 위해  
제안된 다섯가지 원칙을 가르킴. 

* 참고: [SOLID 원칙](https://ds31x.tistory.com/431)

다음은 위의 참고 URL의 내용을 간략히 요약한 내용임.

![](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FAi6pJ%2FbtsNCBLiPU3%2FoOWVohvKpmKlicCWa35G10%2Fimg.png){style="display: block; margin:0 auto; width: 400px"}

2000년대 초 Robert C. Martin("Uncle Bob")에 의해 정리된 다섯가지 원칙으로 각 원칙의 머리글자를 따서 SOLID라고 불림.

- Single Responsibility Principle (SRP): 하나의 클래스는 하나의 책임만 가진다.
- Open-Closed Principle (OCP): S/W의 entity는 확장에는 open, 변경에는 closed여야 한다 
    - 기존 코드를 수정하지 않고 확장가능해야함.
- Liskov Substitution Principle (LSP): 자식 클래스는 부모 클래스로 대체될 수 있어야 한다.
    - 1987년 Barbara Liskov 가 제안.
    - S가 T의 subclass(or subtype)이라면, 클래스 T의 객체를 사용하는 모든 부분에서 T 클래스의 객체를 S클래스의 객체로 치환해도 문제가 일어나선 안된다.
    - Polymorphism을 유지해야 함을 강조.
- Interface Segregation Principle (ISP): 
    - Client는 자신이 사용하지 않는 Interface에 의존해선 안됨.
    - 위의 Client는 Interface를 사용하는 code나 class를 의미함.
    - 큰 인터페이스보다 구체적인 여러 인터페이스로 분리할 것을 강조.
- Dependency Inversion Principle (DIP): 고수준의 모듈은 저수준의 모듈에 의존해선 안되며, abstraction (interface나 abstract base class)에만 의존해야 함.
    - abstraction은 구현 및 세부사항에 의존해선 안 됨
    - 세부 사항은 abstraction에 의존해야 함.