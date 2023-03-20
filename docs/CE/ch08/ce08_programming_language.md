# Programming Language

어떤 주어진 문제를 해결하기 위해, 인간과 컴퓨터 사이에서 의사 소통을 가능케 하는 인공적인 언어

* 자연어 와 달리 미리 정해진 규칙에 따라 엄격하게 정의됨.
* compiler나 interpreter등을 통해 컴퓨터(기계)가 수행할 수 있는 machine language(기계어)로 변환되어 수행됨.

## 분류

#### 기계친화적인지 인간친화적인지에 따른 분류 : Abstraction 수준에 의한 분류

* Low-level Language
* High-level Language

> 분류 기준 중 가장 명확한 편이나, 개인적으로 기계친화적이라고 느껴지는 언어들도 고급언어라는 게 함정.

#### 작동방식에 따른 구분.

* Compiler Language 
* Interpreter Language (or Scripting Language)

> interpreter language의 성능향상을 위한 JIT등의 기술들로 인해 구분이 모호해지고 있음. 우선 명시적인 compile과정이 없을 경우, interpreter language라고 생각해도 된다. 
> 최근 scripting language는 general purpose programming language보다 특정 domain에 한정된 DSL(domain-specific language)들을 지칭하는 경우가 많아지면서 특정 task나 환경에 국한된 언어들(대부분이 interpreter방식)을 가르키는 데 쓰인다.

참고로 개발자나 programmer라는 명칭을 선호하지, scriptor라고 하면 기분 나뻐하는 경우가 많다.


#### 프로그래밍 작성 기법 별 구분 (paradigm)

* 절차중심 언어
* 객체지향 언어

> 사실 가장 모호한 분류이기도 함.