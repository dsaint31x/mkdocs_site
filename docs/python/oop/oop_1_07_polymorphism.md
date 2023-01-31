# Polymorphism (다형성)

Inheritance를 Hierarchy 구조를 따라서 각각의 Class에 (동일한) 하나의 이름을 부여하는 것 (고유 이름도 있으면서 추가적인 명칭이 있게 됨).

이 경우, 공유되는 하나의 이름(super class를 공유)을 통해 서로 다른 Object가 **같은 message** 에 대해 서로 **다른 고유의 방법으로 응답** 할 수 있게 됨.

- ^^동일한 Class의 ***동일한 이름의 method 호출***^^ 을 통해 각기 다른 Object의 method를 호출할 수 있게 됨.
- 단, 적용가능한 object들은 Inheritance를 통해 Hierarchy구조를 가지고 있으면서 공통의 super class를 가져야 한다.
- Polymorphism은 그리스어로 “여러 형태”를 의미.

## 예제

다음의 예를 보자. 각기 다른 Class의 instance들이지만, super class에서 공유하고 있는 method를 통해 같은 방식으로 호출이 이루어진다.

```python
class Dog:
    def __init__(self,name):
        self.name = name

    def bark(self):
        print("멍멍")

    def __str__(self):
        return f"Dog {self.name}"

class Poodle(Dog):
    def bark(self):
        print("왈왈")
    
    def __str__(self):
        return f"Poolde {self.name}"

class Samoyed(Dog):
    def bark(self):
        print("컹컹")
    def __str__(self):
        return f"Samoyed {self.name}"

if __name__ == "__main__":
    d0 = Poodle("뽀미")
    d1 = Samoyed("삐삐")
    d2 = Samoyed("엘씨")
    l = [d0,d1,d2]

    for c in l:
        c.bark()
        if isinstance(c, Dog):
            print(f"{c} is a Dog.")
        else:
            print(f"{c} is not a Dog.")
```

위의 예에서 같은 method `bark()`로 호출이 이루어지나 실제 구현은 각자의 실제 class type에 맞춰 이루어짐. 이같이 super class의 method를 자신에 맞게 다시 구현하는 것을 (method) over-riding 이라고 한다.

> 다양한 Object들이
동일한 message (혹은 interface. 실제로는 method호출)를 통해 수행 가능. ← 개념적으로 비슷한
상호작용이 가능해짐.
>

## 응용사례

다른 format의 파일, `.txt` 파일을 다루는 object나 `.csv` 파일을 다루는 object, `.png` image 파일을 다루는 object들은 ^^실제로 파일을 작성하는 구현부의 코드는 다르지만^^ 대부분 `save` 또는 `write` 라는 동일한 이름의 method 호출을 통해 파일을 저장하게 된다 : 보다 **직관적이고 효과적인 프로그래밍** 이 가능함.  
  
Python의 경우, 모든 object들이 `Object`를 상속하고 있으며, PyQt의 경우, 모든 object들이 `QObject`를 상속하고 있다. 이를 통해 모든 object들이 공통적으로 가져야 하는 기능들을 공통 super-class에서 가지고 있도록하고 각 class마다 고유의 부분에 맞춰 over-ridding할 수 있게 된다.
  
> 위의 예제에서 `Dog` class를 정의할 때, super-class가 지정되지 않았으나 실제로 `Object`를 상속하고 있다. `isinstance` 또는 `issubclass` 함수를 통해 확인할 수 있음. (Python 3.x에 해당.)

## Summary

Polymorphism은 서로 다른 type의 object(객체)들에게 ^^동일한 방식 (=동일한 method 호출)으로 명령을 내릴 수 있는 기능^^ 을 말한다. 이 때 서로 다른 객체들은 같은 명령을 받지만 제각기 다른 방식으로 명령을 수행할 수 있다.

물론 해당 명령들이 논리적으로 좀더 높은 레벨에서 같은 카테고리에 속하는 경우에 사용된다.