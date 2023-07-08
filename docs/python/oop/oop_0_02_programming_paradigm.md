# Programming Paradigm

[Paradigm 이란](https://dsaint31.tistory.com/entry/Paradigm-패러다임)


간단히 애기해서 `programming paradigm`이란 **programming을 인식하고 이해하고 수행하는 방식(인식의 틀)** 이라고 할 수 있다. 
  
(사람에 따라 다르지만) 크게 나누면, imperative programming(명령형 프로그래밍)과 declarative programming(선언형 프로그래밍)으로 나누어지는데 이 문서에서는 imperative programming(명령형 프로그래밍)에서 가장 많이 접할 수 있는 패러다임들을 정리한다.

> 프로그래밍 패러다임은 정말 수도 없이 많다. 현재의 프로그래밍 언어들은 다양한 패러다임을 지원하고 있기 때문에 칼로 자르듯이 구분하기 쉽지 않다. C,C++과 Java, Python에 익숙한 사람의 관점에서 이해하고 있는 내용이라는 전제를 가지고 읽어보길 권한다. 이 내용은 Python이나 C++, Java, C를 공부하기 앞서 가지고 있으면 좋은 사전지식 정도, 그리고 OOP를 이해하기 위한 포석 정도로 여겨두면 좋을 거 같다.

## Non Structured Programming

- Procedural Programming (순차적인 프로그래밍) 를 가르킴.
- 초기 paradigm : 사실 paradigm이라기 보다 다른 paradigm이 나오면서 항상 이렇게 프로그래밍하면 안된다 라고 애기하는 대상으로 더 많이 기억됨.
- `goto`문 등으로 인한 프로그램의 해석이 쉽지 않고 ***재사용성** 등이 매우 떨어짐.*
    - 변호를 한다면... 초기에는 재사용을 고려할 필요가 없던 시절에 사용된 방식임.

## Structured Programming

- `goto`문을 제거한 방식.
- **Module 로 분리** 하여 **재사용성 을 강화** 시킴.
- C, Pascal 등에서 **Function(or Procedure)이 가장 대표적인 module** 임(Python의 module과 헷갈리지 말 것).
- ***Procedural Orientation (절차 기반)*** 이라고도 불린다.
    - 기본적으로는 **순차적인 알고리즘** 중심임.
    - **Data를 처리하는 프로시저** 에 초점을 맞춤.
    - 때문에 재사용하기 위해서는 **Data(변수 로 추상화)와 프로시저(함수 로 추상화)를 모두 잘 이해** 하고 있어야 함.

> Structured Programming은 ***Imperative Programming의 subset***이라고도 볼 수 있다. Imperative Programming에서 소스코드의 유지 보수 및 명확성 등을 위해 modular design과 control structure( loop and conditional block)등의 사용을 강조한 것임.

## Object Oriented Programming

- Java, C++이 대표적인 OOP language.
- Object 위주(oriented)로 프로그래밍이 됨.
    - Object : 작용의 대상이 되는 쪽
    - Oriented : 어떤 대상으로 뜻이 쏠리어 향함, 어떤 대상 위주. 어떤 대상 선호
- ^^**Structured programming** 이 function을 중심으로 작업^^ 하는 것과 달리 ^^**object를 중심** 으로 작업^^.
- Message Orientation (or Message-Driven, 메시지 기반) ← message passing을 사용.
    - 순서가 없이 *message를 기반* 으로 동작함.
    - Object(객체) 간의 message 전달을 통해 상호 작용.
    - Graphic User Interface를 제공하는 SW에서 어느 버튼이 먼저 눌러질지를 알기 어려움. 버튼이 눌러지는 event가 발생하고, 이 event에 해당하는 메시지가 관련 object에게 전달되어 동작이 시작되는 걸 생각해보라 (Event-driven이라고도 불린다).

> 현재 OOP Language라고 불리는 경우, 최소한 다음 세가지 특성을 지원한다.  
>
> * Encapsulation
> * Inheritance
> * Polymorphism

OOP는 imperative programming의 subset이라고 보기는 어렵다. Class의 instance를 Object로 지칭하면서 Object 위주로 programming을 하는 것임. OOP는 이를 위해 기존의 imperative programming에서 없었던 `class`,`object`, `encapsulation`, `inheritance`, `polymorphism`등의 개념이 도입되었음.
---

다음은 OOP와 Structured Programming을 1:1로 비교하여 그 특징들을 파악해 보겠다.

