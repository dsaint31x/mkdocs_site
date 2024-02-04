# Object (객체) 란

- 보거나 만질 수 있는 사물 (공간을 차지하고 있는 물질적인 사물)
- OOP에선 **Concept(개념)** 도 **Object** 임.
- Application(응용프로그램)에서, 명확한 한계와 의미를 가지고 있는 ***사물*** 이나 ***개념***, 혹은 이것들의 ***Abstraction(추상화)*** 를 가르킴.

> OOP 에서는 하나의 소프트웨어 시스템을 여러 개의 Object (객체)로 구성된 것으로 봄.

---

### 참고: Python에서의 Object란?

다음의 속성을 가진 데이터 덩어리 (a chunk of data)를 가르킴.

1. type: 해당 object가 무엇인지 또는 무엇을 할 수 있는지를 정의함.
2. id: 다른 objects과 구분되는 unique id를 가짐. (이게 같을 경우 동일 object)
3. value: 앞서의 type에 의해 object가 가질 수 있는(또는 할당되는) value의 범위가 결정됨. 같은 bytes로 표현되더라도 type이 다르면 다른 value로 해석될 수 있음 (자연수 65와 upper case A의 경우를 예로 들 수 있음.)
4. reference count: garbage collection등을 위해 해당 object가 얼마나 많은 곳에서 사용되는지를 count 함.

* 참고자료: [Garbage Collection 이란](https://dsaint31.tistory.com/497)
---

## OOP란

Object Oriented Programming 의 약자로 

* **Object 에 기반** 하여,
* **Object 를 이용** 하고 **Object 를 만들고(정의 및 구현), Object 를 조합** 하여 **프로그래밍** 하는 Program paradigm의 하나.

을 가르킴.

---

## Simulation 과 OOP

최초의 OOP 언어인 **"Simula67"** 은 Simulation을 위해 만들어진 언어임.

* Class, Object 등의 개념 자체가, 실세계를 어떻게 묘사할지 (=simulation) 에서 출발했다는 애기임.

달리 말하면, **OOP** 라는 것은 현실세계를 어떻게 프로그래밍으로 시뮬레이션 할지의 관점 으로 진행된다고 할 수 있음.

> OOP의 원조로 가장 대중적으로 인정받는 프로그래밍 언어는 ***Smalltalk-76*** 이지만, 이는 ***Simula-67*** 에 많은 영향을 받음. 이를 반영하여 위에서는 최초의 OOP 언어로 Simular-67을 선택했다. (누가 최초냐는 항상 논쟁거리다. 하늘 아래 완벽한 새 것이 없는 터라..)
>

---

Object를 이해했으니, 이제 Programming Paradigm의 개념을 살펴보자.

