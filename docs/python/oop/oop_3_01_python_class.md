# Python에서의 Class

## Class 도 Python에서는 instance임.

다음이 Python에서 Class와 Object의 실체를 말해준다.

* 모든 Object는 `object`를 super-class로 가진다.
* 모든 Class는 `type`이라는 Class의 instance이다.

우리가 `Samp1` 이라는 class를 정의하고, `a`라는 이름의 variable을 `Samp1`의 instance로 할당한 경우는 다음과 같음.

```python
class Samp1:
    pass

a = Samp1()
```

이 경우, `type` 클래스(=callable class)를 이용하여 다음과 같이 호출시 다음과 같은 결과를 얻을 수 있음.

```python
>>> type(a)
<class '__main__.Samp1'>
>>> type(Samp1)
<class 'type'>
```

* `a`는 `__main__`모듈의 `Samp1` 타입의 instance
* `Samp1` class는 <u>`type` 타입의 instance</u>

Python에서는 모든 것이 object(=instance)이기 때문에  
Class도 function도 모두 object임.

> Python에서 특히 function은 first class object임.
>
> 참고: [First-class Object](https://ds31x.tistory.com/43)

심지어 `int`, `float` 같은 자료형도 `object`, 
즉, 객체이며 instance 임.  
  
Python이 모든 것이 `instance`이므로  
^^모든 것이 특정 변수명에 할당될 수 있다.^^

즉, Class도, Function도 할당 가능하다.

> 재미있는 것은 `type`은  
> function이 아닌 callable object이다. 
> 즉 `type`의 타입을 출력해보면 `type` class로 나온다.  
> (우리가 만든 custom class들도 타입이 `type`임)
>
> 단, `type` 클래스는 조금 특별해서, `mro`를 확인하려면 다음과 같이 사용한다.
> ```type.mro(type)```
> `int`의 경우, `int.mro()`나 `type.mro(int)` 모두 사용 가능한 것과 차이가 있음.

다음 코드를 수행해서 각 경우 데이터 형을 확인해보자.

```python
class Samp1:
    pass

def Func1():
    pass

a = Samp1()
b = Func1

c = 7

print(f"a's type:{type(a)}")         # a's type:<class '__main__.Samp1'>
print(f"Samp1's type:{type(Samp1)}") # Samp1's type:<class 'type'>

print(f"Func1's type:{type(Func1)}") # Func1's type:<class 'function'>
print(f"b's type:{type(b)}")         # b's type:<class 'function'>

print(f"Literal 7's type:{type(7)}") # Literal 7's type:<class 'int'>
print(f"c's type:{type(c)}")         # c's type:<class 'int'>
print(f"int's type:{type(int)}")     # int's type:<class 'type'>
```

> `literal`은 ^^데이터 값 자체를 나타내는 표현^^ 을 가르킨다.  
> 
> * [literal에 대한 자세한 참고 자료](https://dsaint31.tistory.com/462))


---

## 동적으로 class에 attribute 추가 및 제거하기.

Python에서는 모든 것이 object이므로  
^^항상 특정 variable name에 assignment가 가능^^ 하다. 

또한 dynamic language이기 때문에, 

* 변수형과 이름을 정의하고 나서 값을 할당하는 것이 아닌, 
* ***instance가 메모리에 할당되는 때*** 가 
* 바로 ^^assignment 이루어지는 시점^^ 이라는 특징을 가진다.  

이 두 특성이 조합되면,  
class의 동적(dynamically)으로 attribute들을 추가하고 삭제할 수 있게 된다.

> 하지만 권하지 않는다. 이를 사용하다보면 정말 debug가 어렵다.

다음 코드를 보면, 동적으로 class에 attribute들을 추가하고 있다. `del`을 사용한다면 동적으로 제거도 된다.

```Python
import types

class MyClass에
    def __init__(self, x):
        self.x = x

def greet(self):
    print(f"Hello, {self.x}")

# ================
# Special Case
# 특정 instance에만 특정 instance method를 추가.
obj = MyClass("test")
obj.greet = types.MethodType(greet, obj) # instance에만 사용가능.

obj.greet()

del obj.greet

# n_obj = MyClass("new")
# n_obj.greet() # error! greet is bound into only obj instance

# ================
# Instance Method를 동적 추가.
MyClass.greet1 = greet

obj1 = MyClass("obj2")
obj1.greet1()
obj.greet1()

# ================
# Class Method를 동적 추가.
def desc(cls):
    print(f"This is {cls.__name__}")

MyClass.desc = classmethod(desc)

MyClass.desc()
obj.desc()

# ================
# Static Method를 동적 추가.
def copyright():
    print(f"GPL!")

MyClass.copyright = staticmethod(copyright)

MyClass.copyright()
obj.copyright()
```

절대로 동적으로 attribute를 추가하거나 삭제하는 것은 권하지 않는다.

* 위의 예에서는 instance attribute만을 동적으로 추가, 삭제했지만,
* class attribute를 동적으로 추가 및 삭제 가능함.

일반적으로 모든 attribute 들은 가급적 constructor에서 추가해 놓는 게 좋다.
