# Setter and Getter

Setter와 Getter는 OOP에서 자주 등장하며 다음과 같다.

- 특정 object (어떤 class의 instance) 내부의 상태 (member variable, instance variable, attribute)들의 값을 얻어오는 method들을 ***Getter*** (or ***accessor***)라고 부름.
- 반대로 instance의 내부 상태를 변경하는 method들은 ***setter*** (or ***mutator***)라고 부름.

**예**

`PyQt`에서 `QtWidget`의 attribute들 중 *위치* 와 *크기* 를 설정하는데 사용되는 `mutator`는 바로 `setGeometry` 메서드이고, 값을 확인하는 `getter`는 `geometry` 메서드로 제공됨.

- `PyQt`의 경우, mutator는 `setXxx` 의 패턴의 이름을 가지고,
- getter의 경우는 얻고자 하는 attribute과 같은 이름의 method로 제공됨 (메서드의 첫 글자는 항상 lowercase임)

---

Encapsulation을 엄격히 지키기 위해서는 필요하지만, 꽤 코딩할 때 귀찮은 경우도 많다. 적절한 균형이 필요하며, 때문에 Python등에서는 `property` decorator등을 제공하여 setter와 getter 의 장점을 살리면서 코딩에서 쉽게 적용하도록 해주는 기능들을 제공한다.

Python의 `proerty`와 encapulation (data hiding관점에서)에 대해 관심이 있다면 다음 문서를 참고하라 : [Python의 Encapuslation](https://dsaint31.me/mkdocs_site/python/oop/oop_3_02_python_encapsulation/)
