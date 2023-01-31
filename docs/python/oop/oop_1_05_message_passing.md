# Message Passing

특정 인스턴스의

* 멤버 함수(method)를 호출 함으로서,
* 해당 instance가 abstraction(추상화)하고 있는 object(객체)에 message를 보내어 (=method calling)
* 원하는 **특정 동작** 을 하게 하는 것.

`Sending Message`라고도 불림.

> 비슷한 것으로 `event-driven`이라는 용어도 있다. 이는 특정 event가 발생할 때, 요구되는(또는 원하는) 특정 동작이 수행되도록 method가 호출되는 형태를 의미함.

OOP는 **instance 간에 message를 주고받아 프로그램이 실행**됨.

- 일반적으로 Object는 ***받을 수 있는 message에 대해서만 노출*** 됨.
    - Interface가 바로 받을 수 있는 message(or 공개된 method)를 가르킴.
- 이를 통해 `Data hiding` 이 이루어짐 (← OOP에서 직접 data (or `member variable`)를 access하는 것을 지양함.)

## 예제

```python
class Car:

  def __init__(self, name="Anony"):
    self.name = name
    self.speed = 0

  def start(self,speed=30):
    self.speed = speed

  def stop(self):
    self.speed = 0

  def accelerate(self,speed):
    self.speed = self.speed + speed

  def __str__(self):
    return f"{self.name}:speed={self.speed}"

if __name__ == "__main__":
  a = Car("붕붕이")
  a.start()
  print(a)
  a.accelerate(20)
  print(a)
  a.stop()
  print(a)
```

실제로 method들의 구체적 구현에 상관없이, 개발자는 `Car` 클래스의 instance와 ^^어떻게 ***상호작용*** 할지^^ 를 ***message를 보내는 것(해당 인스턴스의 method호출)으로*** 이들 object를 제어할 수 있음.

