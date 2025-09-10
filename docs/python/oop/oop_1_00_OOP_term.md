# OOP 와 관련 개념들.

앞서 살펴본 OOP에서 나온 가장 중요한 3가지 특성은 다음과 같음.

* `Encapsulation`, 
* `Inheritance`, 
* `Polymorphism` 

최소한 이들을 지원해야 OOP라고 할 수 있기 때문에, OOP를 제대로 사용하기 위해 반드시 이해해야 하는 개념들이다.

또한 이들 개념들과 함께 기억해야할 개념들도 몇가지 더 있는데, 대표적인 것을 추리면 다음과 같다.

`Abstraction`
: 어찌 보면 OOP의 핵심이며, encapsulation도 abstraction을 하는 한 방법이라고 볼 수 있다.

`Modularity` 
: 프로그램을 좀 더 이해하기 쉽고, 작고 관리가 쉬우면서, 서로 interaction하는 조각 으로 나누어 개발하는 방법 또는  
얼마나 프로그램에서 상호 작용하는 구성요소들이 분리되어 있는지 정도를 나타냄.  
OOP 만의 개념이 아니며, 프로그래밍을 넘어서 공학적 문제 해결 방식 중의 하나라고 볼 수 있다.  
OOP에선 Hierarchy (or inheritance) 를 통해 이루어진다.

`Encapsulation`  \*\*\*
: Object에서 ^^중요한 데이터와 세부적인 구현 방법에 대한 사항들을  capsule 로 싸는 형태^^ 로 취함으로 외부에서 직접 접근을 막고, 대신 외부에서 이들을 조작할 수 있는 방법인 interface만을 공개하는 기법을 가리킴.

`Inheritance` \*\*\*
: OOP가 ***modularity (정확히는 Hierarchy)를 달성*** 하기 위한 기법.

`is-a` and `has-a` 
: Object간의 관계 중 가장 기본적인 관계


`Message Passing` 
: Event-Driven, Message-Driven, Sending Message 라고도 불리는 개념으로 Object간의 interaction 방식을 지칭한다.

`Polymorphism` \*\*\*
: Inheritance를 통해 이루어지는 개념 중 하나로 ***동일 message로 여러 종류의 object에게 각각 고유한 task를 수행*** 시킬 수 있게 해줌.