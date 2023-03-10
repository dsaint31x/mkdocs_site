# Modularity

Structural Programming(구조적 프로그래밍)의 divide & conquer 와 비슷한 개념으로 **크고 복잡한 문제** 를 좀 더 이해하기 쉽고 ***작고 관리가 쉬운 조각*** 으로 나누고 이 조각들을 독립적으로 개발하고 서로 interaction하도록 하여 복잡한 프로그램을 만드는 방법을 의미함.  
  
작은 조각들을 흔히 `module`이라고 부른다. 

* 구조적 프로그래밍 에서 서브프로그램, 모듈 로 나누어 개발됨.
* OOP 에서는 class, object로 나누어져 개발된다.

## OOP에서 Modularity와 Hierarchy.

- Modularity 등으로 **나누어진 여러 object(객체)들** 의 경우, **서로 비슷한 특성이나 기능을 가질 수 있음**.
- 이 때 보편적인 것을 상위에 두고 특수한 것을 하위에 두는 형태로 계층적 구조로 객체를 배열하는 것을 Hierarchy라고 부름.

Hierarchy를 통해 OOP는 높은 재생산성을 가질 수 있다. 일반적으로 OOP에서의 Hierarchy는 inhertance에 의해 구현된다.