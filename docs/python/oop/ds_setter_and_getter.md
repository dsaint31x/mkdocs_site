# Setter and Getter

Setter와 Getter는 OOP에서 자주 등장하며 다음과 같다.

- 특정 object (어떤 class의 instance) 내부의 상태 (member variable, instance variable, attribute)들의 값을 얻어오는 method들을 ***Getter*** (or ***accessor***)라고 부름.
- 반대로 instance의 내부 상태를 변경하는 method들은 ***setter*** (or ***mutator***)라고 부름.

**예**

`PyQt`에서 `QtWidget`의 내부 상태 중 위치와 크기를 설정하는데 사용된 `mutator`는 바로 `setGeometry` 메소드이고, 값을 확인하는 `getter`는 `geometry` method임.

- `PyQt`의 경우, mutator는 `setXxx` 의 패턴의 이름을 가지고,
- getter의 경우는 얻고자 하는 attribute과 같은 이름의 method로 제공됨 (메서드의 첫 글자는 항상 lowercase임)
