# OOP vs. Structured Programming 

Structured Programming은 Edsger wybe dijkstra (에츠허르 위베 데이스크라, 1930-2002)가 1968년 제안한 프로그래밍 패러다임이다. 

OOP는 Alan curtis kay (앨런케이, 1940- )의 small talk(1976)로 대중화된 것으로 알려져 있으며, 현재 가장 인기있는 프로그래밍 패러다임 (Simula-67이 최초로 많이 인식됨)이다.

---

## 비교하기

이 둘을 비교한 표는 다음과 같다.

|OOP|	Structured Programming|
|----|----|
|Object간의 역할과 관계, 즉 상호작용이 중심.|	Function이 중심. 모든 프로그램은 Functional decomposition이 이루어짐.|
|Object-orientation	| Procedure-orientation|
|데이터는 감추어지고, 행위(Method)만 공개됨. 
Object는 필요한 데이터와 function을 같이 묶어서 가지고 있음.  (Encapsulation, Data hiding)	|데이터는 변수로 노출되며, function과 관련된 변수에 대한 이해가 필요.(function에 맞추어진 data에 해당하는 변수가 같이 있어야 하나 분리되어 있음)|
|필요한 데이터와 function이 Object로 묶여 있기 때문에, 모듈화가 자연스럽게 이루어지고 재사용성이 높음.	| 처리 프로세스에 초점을 두고 있으며, 프로세스와 관련된 데이터가 드러나있음. 재사용성을 위해서 함수와 데이터 모두 파악해야 함|
| 순서보다는 메시지 기반으로 수행됨 (message passing) | 순차적인 알고리즘으로 수행됨.|

---

이를 좀더 간략하게 정리하면 다음과 같다.


| OOP	| Structured Programming|
|----|----|
|Object, Relation 중심	| Function, Procedure 중심|
|메시지 기반|	순차적 수행|
|Data hiding	| Data 노출|

---

## 참고자료: 창시자들

### Edsger wybe dijkstra (에츠허르 위베 데이크스라)
    
네덜란드의 Computer Scientist. 1972년 튜링상 수상.
    
- 1930~2002
- ALGOL개발(고급언어의 조상님,50년대)
- 1968년 ***구조적 프로그래밍*** 시대 개척 (Goto Statement Considered Harmful)
- SW 공학과 Structured programming의 시대를 연 선구자.
- 최단거리 알고리즘이나 세마포어등의 개념을 연구, 제안.

---

### Alan curtis kay (앨런케이)
    
미국의 Computer Scientist. 2003년 튜링상 수상.
    
- 1940 ~
- Small talk 개발 (70년대) : 제록스 파크 (PARC)에서.
- OOP의 개척자
    
> The best way to predict the future is to invent it.

---

## 프로그래밍 언어 분류.

* 명령형 프로그래밍 언어 (Imperative Programming Language)
    * 절차적 프로그래밍 언어 (Procedural Programming Language)
        * 구조적 프로그래밍 언어 (Structured Programming Language) \*\*
    * 객체지향 프로그래밍 언어 (Object Oriented Programming Language) \*\*\*
* 선언적 프로그래밍 언어 (Declarative Programming Language)
    * 논리형 프로그래밍 언어 (Logic Programming Language)
    * 함수형 프로그래밍 언어 (Functional Programming Language) \*\*\*

---

**객체지향언어 (Object-Oriented Language) vs. 객체기반 프로그래밍 (Object-Based Language)**

- OOL
    - Java, C++ (OOP와 SOP의 혼합), Python, C#
- OBL객체기반 프로그래밍
    - Object 의 핵심 개념(Encapsulation, Inheritance, Polymorphism)을 제한적 지원.
    - Class 나 Inheritance 등의 기능이 제한적인 경우 많음.
    - Java Script (Inheritance보다 Prototype chain을 이용)
    - VBScript
---

**객체지향언어를 사용한다는 것이 OOP를 의미하진 않는다.**

> 심지어 **Python** 은 fundamental data type(=primitive data type or unboxed data type)이 없이 모든 것이 Object 인 언어이다. 
> 재미있는 것은 그럼에도 구조적으로 또는 순차적으로 프로그래밍하기가 쉽다는 점이며 엄격한 OOP를 적용하기가 쉽지않다는 점이다.
> (Java는 반강제적으로 OOP를 따르게 하는 것과 차이가 있다.)