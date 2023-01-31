# Python에서의 Encapsulation 관련 구현.

## Data Hiding 관점

Encapsulation을 엄격히 적용하려면, data에 직접 접근이 아닌 getter나 setter와 같은 method들을 통해서만 이루어져야 한다.

문제는 python에서는 이를 구현하기 쉽지 않다는 점이다. 이를 위해 Python에서 지원하는 기법은 `Name mangling`이다.

다음 코드를 살펴보자.

```python
class Student:
    def __init__(self, name, age):
        self.name = name
        self.__age = age #Naming mangling
        self._job = "test" # 관례적으로 접근하지 말것을 _로 표시.

    def set_name(self,age):
        self.name = name

    def set_age(self,age):
        self.__age = age

    def set_job(self,job):
        self._job = job # 관례상 _가 앞에 있으면 접근하지 말라는 애기임.

    def display(self):
        print(f"{self.name}'s age is {self.__age}")
        print(f"{self.name}'s job is {self._job}")

if __name__ == "__main__":
    s = Student("김 아무개", 21)
    s.name = "박 아무개"
    s._job = "학생" # 관례이므로 강제력이 Name mangling보다 약하다. (그냥 됨)
    s.display()
    print(dir(s))
    # print(s.__dict__) #attribute들을 출력해줌.
```

* `__age`처럼 attribute의 이름에 `__`를 붙이면, python은 이 property에 data hiding을 위한 처리로 실제 이름을 `_Student__age`로 변경하여 관리한다.
* class내에서는 `self.__age`를 사용하여 접근하는 구현이 가능하나, 외부에서 접근하려면 `__age`만으로는 되지 않는다.
* 위 코드에서 `s.__age = 32`는 에러가 뜨진 않지만, 새로운 `__age`라는 property가 추가되고 거기에 32가 value가 된다.
* 만약 `s.__age = 32` 대신 `print(s.__age)`같이 perperty의 value에 접근하는 경우에는 AttributeError가 발생한다. `s._Student_age`는 있지만, `s.__age`는 없기 때문이다.

> 외부에서의 직접적인 접근을 막기 위해 도입된 것이지만...  
> 어떤 의미로는 유명무실하기도 하다. 다 같은 개발자들이니...


> `__dict__`는 해당 object의 attribute들을 dictionary형태로 가지고 있다. 이를 통해 직접 접근을 하여 변경이 가능하다. 즉, Python에서는 엄격한 Encapusulation을 구현할 수 없다.

## property설정.

`property`를 이용하여 encapsulation의 장점을 살리면서 직접 접근하는 것처럼 간단한 코딩도 가능하다.

다음 예제에서 `property`를 사용한 부분을 참고하라.

```python
class Student:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age #Naming mangling
    
    def get_name(self):
        return self.__name
    def set_name(self,name):
        self.__name = name    
    name = property(get_name, set_name)# property 이용
    # name = property() # 위의 라인과 동일한 효과의 3개 라인임.
    # name.getter(get_name)
    # name.setter(set_name)
    
    @property
    def age(self):
        return f"[{self.__age}]"

    @age.setter
    def age(self,age):
        if age < 0:
            self.age = 0
        else:
            self.__age = age
    

    def display(self):
        print(f"{self.__name}'s age is {self.__age}")

if __name__ == "__main__":
    s = Student("김 아무개", 21)
    s.name = "박 아무개" 
    s.age = -10
    print(s.age)
    print("------------")
    print(s.display())
    print("------------")
    print(s.__dict__) # property들은 보이지 않음.
    print("------------")
    print(dir(s)) # property확인 가능.
```

* `s.age = -10`으로 직접 접근하는 것처럼 보이지만, 실제로는 `set_age(self, age)`메서드를 통해 접근된다.
* 재사용이 빈번한 class에서는 권장되는 방식임.
* `name`은 `property` object 를 생성하여 구현.
* `age`는 Decorator `@property`와 `@XXX.setter`를 사용하여 구현됨.




## References

* GeeksforGeek's [Name mangling in Python
](https://www.geeksforgeeks.org/name-mangling-in-python/)