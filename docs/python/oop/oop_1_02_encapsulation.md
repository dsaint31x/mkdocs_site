# Encapsulation (and Data Hiding)

Encapsulation (캡슐화)는 Object에서 중요한 데이터와 세부적인 구현 방법에 대한 사항들을 숨기고, 대신 외부에서 이들을 조작할 수 있는 방법인 interface만을 공개하여 해당 interface로만 내부의 데이터 및 세부적 구현이 수행되도록 **abstraction** 하는 기법을 가르킨다.

> 엄격하게, encapsulation을 고려해서 Abstraction이 이루어질 경우, 해당 Object의 data에 직접 접근이 불가하다.

달리 애기하면, 서로 관련이 있는 data와 해당 data에 대한 operation을 묶어서 abstraction을 한 이후에 operation만을 공개하여 반드시 해당 operation들을 통해 data에 접근하도록 하는 것을 encapsulation이라고 한다. 내부의 data를 숨겨서 직접 접근을 막기 때문에 data hiding이라고도 불린다.

## 장점

- Object의 사용자는 **interface만을 알고 있으면 충분히 객체를 사용** 가능.
    - (1) 내부 구현의 변화 등에 종속되지 않고
    - (2) 원래 객체의 설계자가 원하는 방향으로 객체를 사용되도록 강제할 수 있음 (=설계자 의도와 다른 사용을 막음).
- ex: 자동차 액셀사용법 (사용자는 자동차 내부를 몰라도 차를 몰 수 있음)

## 단점

- 개발자 입장에서는 직접 접근하는게 편한 경우도 많지만, getter나 setter등의 method로만 접근해야 하기 때문에 필요한 코딩량이 늘어나기 쉽다.
- Python의 경우 `property()`를 통해, `property` Object를 생성하거나, decorator `@property`와 `@X.setter`를 통해 이를 해결하고 있다.

## 결론

Encapsulation은

- Attribute (or Data) 와
- 해당 attribute를 다루는 방법 (method)

을 묶어내고, 이들 중 해당 method 만을 외부에 공개한다 (← Data hiding).

> C++, Java의 경우, 매우 엄격한 encapsulation이 가능하지만,  
> Python에서는 우회할 수 있는 방법이 있어서 엄격한 구현이 쉽지 않음. [참고](./oop_3_02_python_encapsulation.md)

