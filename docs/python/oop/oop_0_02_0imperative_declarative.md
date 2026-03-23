---
title: "Declarative Programming Language vs. Imperative Programming Language"
tags: [Programming, Paradigm, Declarative, Imperative, Turing Completeness]
---

# 참고: Declarative Programming Language vs. Imperative Programming Language

> Structured Programming과 OOP(Object-Oriented Programming)의 차이를 보기 전에,
> Declarative Programming과 Imperative Programming의 구분을 먼저 이해해두는 것이 도움이 된다.
 
Structured Programming은 

* Imperative Programming 내부의 한 기법에 해당하며,
* Declarative Programming과는 다른 축의 분류 개념이다.

---

## Declarative Programming Language

> Declarative Programming Language는
> 프로그램이 **무엇(what)을 원하는지** 를 기술한다.  

즉, 결과나 관계를 명시하며, 그것을 **어떻게(how) 계산할지에 대한 절차는 명시하지 않는다.**

대표적인 예는 다음과 같다.

- SQL (Structured Query Language)
- Prolog

예를 들어 SQL에서는:

- 어떤 데이터를 조회할 것인지(Query의 결과 집합)를 기술한다.
- 테이블 간의 관계를 정의한다.
- 원하는 조건을 기술한다.

그러면 Database Engine이 내부적으로 실행 계획(Execution Plan)을 수립하여 해당 결과를 생성한다.

즉, Declarative Programming에서는 개발자가 **결과 또는 관계를 선언** 하며,  
그 결과를 도출하기 위한 실행 절차는 시스템이 결정한다.

---

## Imperative Programming Language

> Imperative Programming Language는
> 프로그램이 **어떻게(how) 동작해야 하는지** 를 명시한다.

Imperative programming language는 명시적으로 instruction들을 기재하여 컴퓨터가 어떻게(how) 동작할지를 기술한다.

즉, 실행할 instruction들을 순서대로 기술하며, 프로그램의 제어 흐름(control flow)을 직접 정의한다.

프로그래머는 다음을 명시적으로 작성한다.

- 어떤 순서로 실행할 것인지
- 어떤 조건에서 분기할 것인지
- 어떤 상태를 변경할 것인지

Imperative Programming Language의 일반적 특성은 다음과 같다.

- 상태 변경(state mutation)을 지원한다.
- 명령이 순차적으로 실행된다.
- 메모리 갱신이 가능하다.

대표적인 예는 다음과 같다.

- C
- Python
- Java

* 상태 변경을 지원.
* 명령을 순차적으로 실행.
* 메모리 갱신이 가능함.

## 참고: Truing Completness: 범용프로그래밍 언어에게 요구되는 3가지.

일반적으로 범용 Imperative Programming Language 는 다음의 세가지를 지원하는게 일반적임.
(사실, 일부 Declarative language 도 아래를 지원하기도 함)

1. variable assignment (state mutation, 메모리 접근)
2. loops (iteraton 또는 recursion)
3. conditions (=conditional branching)

위의 조건은 imperative programming language의 조건이라기 보다는  
범용 계산모델을 만들기 위한  
범용 Programming Language가 갖춰야 하는 요건이다.  
(Turing Completeness를 만족하기 위한 조건)  

실제로 일부 **Declarative Language 역시 재귀(recursion)와 조건을 통해 Turing Complete해질 수 있다.**

---

## 요약.

- Declarative Programming Language는 **“what”에 집중** 한다.  
  원하는 결과나 관계를 기술하며, 실행 방법은 시스템이 결정한다.

- Imperative Programming Language는 **“how”에 집중** 한다.  
  필요한 instruction과 실행 순서를 직접 기술한다.

- Turing Completeness를 만족하려면  
  상태 표현, 반복(또는 재귀), 조건 분기와 같은 계산적 요소가 필요하다.

정리하면,  

* Declarative Programming은 원하는 상태를 선언하는 방식에 가깝고,  
* Imperative Programming은 목표를 달성하기 위한 절차를 직접 서술하는 방식에 가깝다.
 
Declarative programming languages로는 내가 원하는 것을 알려주는 형태로 지시를 내린다면,  
Imperative programming language는 task를 수행하기 위해 해야하는 일을 하나하나 순서대로 지시를 내리는 것으로 생각할 수 있다.
