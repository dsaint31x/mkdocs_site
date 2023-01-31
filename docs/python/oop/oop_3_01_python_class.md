# Python에서의 Class

## Class 도 Python에서는 instance임.

다음이 Python에서 Class와 Object의 실체를 말해준다.

* 모든 Object는 `Object`를 super-class로 가진다.
* 모든 Class는 `type`이라는 Class의 instance이다.

우리가 `Samp1` 이라는 class를 정의하고, `a`라는 이름의 variable을 `Samp1`의 instance로 할당한 경우는 다음과 같음.

```python
class Samp1:
    pass

a = Samp1()
```

이 경우, `type` 클래스를 이용하여 다음과 같이 호출시 다음과 같은 결과를 얻을 수 있음.

```python
>>> type(a)
<class '__main__.Samp1'>
>>> type(Samp1)
<class 'type'>
```

* `a`는 `__main__`모듈의 `Samp1` 타입의 instance
* `Samp` class는 `type` 타입의 instance

Python에서는 모든 것이 Object(=instance)이기 때문에 Class도 functionn도 심지어 int, float 같은 자료형도 object, 즉 instance이다.  
  
Python이 모든 것이 instance이므로 모든 것이 특정 변수명에 할당될 수 있다. 즉, Class도 Function도 할당 가능하다.

> 재미있는 것은 `type`는 함수가 아닌 callable object이다. 즉 `type`의 타입을 출력해보면 `type` class로 나온다. (우리가 만든 custom class들도 타입이 `type`임)

다음 코드를 수행해서 결과를 확인해보자.

```python
class Samp1:
    pass

def Func1():
    pass

a = Samp1
b = Func1

c = 7

print(f"a's type:{type(a)}")
print(f"Samp1's type:{type(Samp1)}")
print(f"Func1's type:{type(Func1)}")
print(f"b's type:{type(b)}")
print(f"Literal 7's type:{type(7)}")
print(f"c's type:{type(c)}")
print(f"int's type:{type(int)}")
```

## 동적으로 class attribute 추가 및 제거하기.

Python에서는 모든 것이 object이므로 특정 variable name에 assignment가 가능하다. 또한 dynamic langauge로서 변수형과 이름을 정의하고 나서 값을 할당하는 것이 아닌, instance가 메모리에 할당되는 때가 바로 assignement 이루어지는 시점이라는 특징을 가진다.  
  
이 두 특성이 조합되면, class의 동적으로 attribute들을 추가하고 삭제할 수 있게 된다.

다음 코드를 보면, 동적으로 class에 attribute들을 추가하고 있다. `del`을 사용한다면 동적으로 제거도 된다.

```python
class Samp:
    def get_x(self):
        return self.x

def some_method(self): # closuer기법으로 self를 기억.

    def func():
        print(f"hi! : {self.x}")
    return func

class SampTwo:
    def get_x(self):
        return self.x

if __name__ == "__main__":
    s = Samp()
    s.x = 23 #주석처리시 에러.
    s.dynamic_get = some_method(s)
    s.dynamic_get()

    print("------------")
    s2 =SampTwo()
    s2.x = 77
    s2.dynamic_get = some_method(s2)
    s2.dynamic_get()
    s2.x = 33
    s2.dynamic_get()
    print("------------")
    s2.dynamic_get_one = some_method(s)
    s2.dynamic_get_one()
    s.x = 2323
    s2.dynamic_get_one() # 이런 유연성은 안쓰는게 낫지 않을까?
    print("------------")
    print(s.get_x())
    print("------------")
    del s.x
    print(s.get_x()) # attribute가 제거되어 AttributeError가 발생함.
```
