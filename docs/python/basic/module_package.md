# Modules and Packages

## Module

쉽게 생각하면 Python code 로 구성된 file을 가르킨다. Module은 import될 때 각각 고유의 namespace를 가짐 (Namespace의 역할도 수행).

* Python에서 module은 확장자가 `.py`인 파일을 가르킴 (python code를 내용으로 가지는 file).
* 모든 `.py` file들은 python에서 module로서 사용가능함.

Python에서 code의 재사용을 위해 사용되며, 일반적으로 module들이 모여 하나의 프로그램이 된다.

> code의 재사용이란, ^^이전에 정의한 variable과 function, class 등을 다시 code로 정의하지 않고 다시 사용하는 것^^ 을 의미함. module이 없다면 이전에 작성한 code들을 매번 copy and paste 시키거나 기억하고 다시 typing을 해야할 것임.

code의 재사용을 위해 이전에 구현했거나 다른 이가 구현한 `.py`파일의 code를 재사용할 때, 해당 파일의 이름으로 불리는 module을 `import` statement를 사용하여 import한다.

* `ds_cal.py` 라는 file에 있는 code를 사용하고 싶은 경우, `ds_cal` module을 import한다.
* `import ds_cal` 과 같은 `import` statement를 이용함.
* import하면 `ds_cal`이라는 variable이 만들어지며 이는 `module` class (or type)의 object를 참조하게 된다.

Python에서는 이미 standard library로 built-in module을 제공 (Python의 built-in function들은 `__builtins__` 라는 모듈에 속함)하고 있으며, Third party에서 만든 library의 module들과 함께 개발자가 만든 본인의 module들도 import가능하다.

> * `module`을 import할 때, 해당 `module`을 읽어와야하는데 이 경우 ***Module Search Path*** 를 참고하여 python은 module을 읽어들임.  
> * ***Module Search Path*** 에 기재된 path들에서 `module`의 이름을 기준으로 `module`을 읽어들임 (가장 먼저 위치한 path의 `module`에 우선권이 있음).  
> * 기본적으로 현재 작업 디렉토리가 포함되므로 이를 이용하여 `module`에 대해 익히고, 다른 path의 `module`들을 사용하기 위해 ***Module Search Path*** 를 수정하는 방법은 다음 URL을 살펴본다: [Module Search Path and sys.path](https://dsaint31.tistory.com/entry/Python-Module-Search-Path-and-syspath).

참고로 흔히, import가 되는 `.py` 파일을 `module`이라고 부르고 python interpreter에게 수행되기 위해 인자로 넘겨지는 `.py` 파일은 main program 혹은 main script라고 불린다.

> 참고로 `__name__` 은 `.py`파일 즉 `module` 내에서 Python interpreter가 해당 `module`에 할당한 이름, 즉 자기자신의 `module name`을 값으로 가지는 global variable임.  
> 해당 main script로 동작하는 경우엔 `__main__`이라는 문자열을 값으로 가짐.

다음의 예는 `ds_cal.py`를 `module`로 import하는 `ds_run.py`를 통해 간단한 `module` 사용법을 보여준다.

* `ds_cal.py`와 `ds_run.py`는 모두 같은 directory에 위치함.
* 이 두 파일이 있는 directory가 current working directory임.

```Python
# ds_cal.py
def ds_addition(a,b):
    return a+b
```

```Python
#!/bin/env python

# ds_run.py 파일 : main script file.

import ds_cal # 모듈을 import

def main():
    while True:
        try:
            a_str = input('Enter the first operand:')
            a = float(a_str)
            b_str = input('Enter the second operand:')
            b = float(b_str)

            r = ds_cal.ds_addition(a, b)

            print(f'result = {r}')
            break
        except ValueError as ve:
            print('[ValueError] Invalid Input! Try again!')

if __name__ == '__main__':
    main()
```

* `import ds_cal` 을 통해 `ds_cal.py`를 파일명인 `ds_cal`이라는 이름의 module로 사용함.
* 이를 통해 main script파일에서는 `ds_cal.py` 파일의 global scope에 있는 attribute들에 접근을 할 수 있음.
* 실제로 `ds_cal.ds_addition(a, b)`를  호출하여 그 결과를 `r`에 할당함 (모듈 `ds_cal`은 고유의 namespace를 가지며 해당 namespace에 접근하기 위해서 `ds_cal`이라는 모듈명을 prefix로 가짐).
* `module`의 global attribute들에 접근하기위해서는 `module` 이름을 prefix로 사용해야 함(위의 예에서는 `ds_cal`이 prefix로 사용됨).
* 이는 `ds_cal`과 같은 import된 module에 대한 ***Name Space*** 가 생성되었음을 의미하며, 해당 name space에 모듈의 attribute들이 속하게 됨.

### `.` operator

`ds_cal.ds_addition(a, b)`에서 `.` (dot)은 일종의 operator임.

* `.`의 왼쪽에 있는 variable이 가르키는 object를 찾고,
* 해당 object에서 `.`의 오른쪽에 있는 name에 해당하는 object(=attribute)를 찾아내어 접근함.

위의 경우, `ds_cal`이라는 variable에 할당된 object에서 `ds_addition`이라는 `function` attribute를 call하게 됨.

### `import`되는 경우 `module`은 execution(수행)이 이루어짐.

module의 statement들은 import가 되는 경우에도 역시 수행이 되므로 이를 통해 해당 module의 초기화가 가능함.

* 같은 `module`의 import가 여러 번 되어도, 한번만 수행이 된다 (최초로 import 되는 경우). 
* 수행이 되면서 해당 `module`이 초기화가 이루어짐.
* variable과 function의 정의는 당연히 수행이 되어야 하지만 해당 module이 main script로 동작하는 경우만 실행되어야 하는 code들도 수행이 될 수 있음.

```Python
# echo.py

if __name__ == '__main__':
    # main script로 동작
    print(f'main script mode :{__name__}')
else:
    # module로 import 인 경우 수행됨.
    print(f"this is echo's init part : {__name__}")
```

위 module은 import되어 수행되는 경우와 main script로 동작하는 경우가 다른 처리가 이루어지도록 되어 있음.

```Python
# test_echo.py
import echo # echo모듈의 초기화 부분수행됨.
import echo # 최초로 import될 때만 수행되므로 아무 일 이어나지 않음)
```

`test_echo.py`를 main script로 수행시, `echo`모듈에 대한 초기화 부분이 한번만 수행됨을 확인 가능함.


`if __name__ == '__main__':` 로 시작하는 code block이 main script에서만 수행되는 부분이 된다. `__name__` 이 main script로 동작하는 경우에 `__main__` 문자열을 값으로 가짐.

> `__name__` variable은 해당 module의 name에 해당하는 문자열을 값으로 가지는 특별한 variable임.  
> ^^`__`로 시작하고 끝나는 object는 Python 언어에서 특별하게 사용되는 object로서 Python 언어에서 정의하고 있는 대상임을 나타내는데 사용^^ 된다.

다시 한번 강조하지만, import 문이 동일한 module에 대해 호출이 되어도 최초 한번만 수행이 된다. 때문에 특정 Python Interpreter Session이 수행되고 있는 동안에 특정 module의 소스코드 자체가 바뀌더라도 해당 변경사항이 반영되지 않는다.  
이를 위해서는 `importlib` 모듈의 `reload(모듈명)` function을 이용해야 한다. 자세한 사용법은 다음 URL을 참고하라. 
[모듈 변경사항 동적으로 반영하기: `importlib.reload`](https://dsaint31.tistory.com/entry/Python-importlibreload-module-%EC%9E%AC%EC%A0%81%EC%9E%AC)

### 주의 : reassignment.

Python이 제공하는 standard library의 module의 attribute들에 재할당이 가능하다는 단점을 가짐.

다음 code는 `math` module의 `pi`라는 variable에 reassignment가 가능함을 보임.

```
import math

print(math.pi)

math.pi = 72

print(math.pi)
```

`pi`는 $\pi$의 값을 가져야하는데 이같은 reassignment는 많은 문제의 원인이 될 수 있다. 

> 실제 module에 해당하는 file에서 수정이 일어나진 않고, 단순히 memory상에서 `math`의 namespace의 `pi`라는 이름이 가르키는 object가 바뀐 것이므로 해당 Python interpreter의 session에서만 `72`라는 값을 의미하게 되고, 다른 `math` 모듈을 사용하는 session에서는 문제가 없다.

Python에서는 이처럼 고정되어야 하는 상수를 `freeze`할 수가 없다는 단점을 가지고 있음.

## `as`를 통한 alias(별칭) 사용하기.

앞서 예의 `import` statement에서 import된 모듈에 접근은 모듈 파일의 이름을 통해서임.

해당 ^^이름이 너무 긴 경우^^ 나 ^^관례적으로 사용되는 별칭^^ 이 있는 경우엔 ***alias를 지정*** 해주어 모듈의 attribute에 접근함.

해당 alias를 지정하는 `import` statement는 다음과 같음.

```Python
import ds_cal as dc
```

* `import ds_cal`로 import한 경우 `ds_cal.ds_addition(a, b)`.
* `import ds_cal as dc`로 Alias를 `dc`로 지정한 경우 `dc.ds_addition(a, b)` 로 접근 가능함.

> Python 에서 가장 유명한 alias 중 하나는 NumPy 를 가르키는 `np`임.  
> NumPy를 사용하는 경우, `import numpy as np` 가 가장 많이 사용됨.  
> 다른 하나는 `matplotlib.pyplot`의 Alias인 `plt`임.  
> pyplot을 사용하는 경우, `import matplotlib.pyplot as plt` 가 가장 많이 애용됨. 

## 원하는 attribute만 import하기.

현재 `ds_cal.py` 모듈에서 필요한 attribute는 바로 `ds_addition` 함수 뿐임.

이처럼 필요한 attribute의 수가 적고 이름을 정확히 알고 있는 경우 다음과 같이 지정하여 import할 수 있음.

> 이 경우의 최대 장점은 모듈명에 해당하는 prefix가 필요없다는 점임.

```Python
#!/bin/env python

# ds_run02.py 파일 : main script file.

from ds_cal import ds_addition # ds_addition만 지정하여 import 

def main():
    while True:
        try:
            a_str = input('Enter the first operand:')
            a = float(a_str)
            b_str = input('Enter the second operand:')
            b = float(b_str)

            r = ds_addition(a, b) # module prefix 필요없음.

            print(f'result = {r}')
            break
        except ValueError as ve:
            print('[ValueError] Invalid Input! Try again!')

if __name__ == '__main__':
    main()
```

* `from 모듈명 import Attribute0, Attribute1`과 같이 하나의 module에서 여러 Attribute들을 import할 수 있음.

## 특정 module의 모든 attribute 모조리 import

아래와 같은 import문을 사용할 경우, `ds_cal.py` 파일의 모든 global scope의 attribute들을 import한다.

```Python
from ds_cal import *
```

장점은 가장 편하다는 것으로 prefix가 필요없고, import 할 때 필요한 attribute들을 입력해주지 않아도 된다는 것임.

> 정확히 애기하면, 모든 attribute는 아님.  
> `_`로 시작하는 이름을 가지는 attribute들은 import가 이루어지지 않음.

문제는 일반적으로 특정 module에서 어떤 attribute들이 있는지 알기 어렵고, prefix를 사용하지 않기 때문에 name collusion이 발생하기 쉽다. 

> 해당 code의 동작은 알고 있어야하지만, ^^사용은 절대 추천하지 않는다.^^

---

## Packages

Python에서 `module`이 `.py`파일로 구현되는 것처럼, `package`는 `module`들이 포함된 directory로 구현된다.

> Python 2.x 의 경우, `__init__.py`가 있어야 했으나 Python 3.x에서는 필요가 없음. 하지만 호환성을 위해 빈 파일로라도 `__init__.py`를 넣어주는 게 좋음.

`package`를 통해 `module`들은 logically 비슷한 것들끼리 구분짓고 계층화할 수 있다.

다음 예제는 사칙연산을 구현한 `ds_cal.py`를 `farith` package에 두고, 기본 삼각함수 관련 함수를 제공하는 `ds_cal.py`를 `ftri` package로 나누어 제공하면서 `ds_run03.py`에서 모듈로 사용하는 것을 보여줌.

* 같은 파일명임에도 package를 다르게 함으로서 구분이 가능해짐.
* 이 경우 `import`문에서 package 명들도 prefix로 추가를 해줘야함. 

```Python
# ./farith/ds_cal.py

def ds_addition(a,b):
    return a+b

def ds_subtraction(a,b):
    return a-b

def ds_multiplication(a,b):
    return a*b

def ds_division(a,b):
    return a/b
```

```Python
# ./ftri/ds_cal.py

import math

def ds_cos(rad):
    return math.cos(rad)

def ds_sin(rad):
    return math.sin(rad)
```

```Python
#!/bin/env python

# ds_run03.py
import farith.ds_cal as fundamental
import ftri.ds_cal as tri

def main():

    while True:
        try:
            a_str = input('Enter the first operand:')
            a = float(a_str)
            b_str = input('Enter the second operand:')
            b = float(b_str)

            print(f'{a}+{b}={fundamental.ds_addition(a,b)}')

            rad = float(input('Enter the radian to get the value of cosine:'))
            print(f'cos of {rad}={tri.ds_cos(rad)}')
            break
        except ValueError as ve:
            print(ve)

if __name__ == '__main__':
    main()
```

`namespace package`의 경우, 물리적으로 다른 경로(각각의 `sys.path`에 item이어야함.)에 있더라도, 같은 패키지명을 공유할 경우 하나의 package로 Python에서 처리되는 package를 가르킴. 이 경우, 같은 패키지명을 공유하는 모든 subdirectory내에 `__init__.py`가 있어선 안됨 (Python 3.x 이상부터만 사용가능함).

---

## Summary

* Module은 하나의 `.py`파일로 묶여있는 `variable`, `function` 그리고 `class`등의 object의 Collection을 가르킴.
* Module은 고유의 Namespace를 가지며, 관련있는 object들을 묶어서 재사용이 가능하도록 해줌.
* Package는 관련이 있는 module들을 가지고 있는 subdirectory에 해당하며 module들의 이름이 모인 일종의 namespace를 제공함.


---

## References

* Python (3.11.4) 공식설명서[6. 모듈](https://docs.python.org/ko/3/tutorial/modules.html)
* [Module Search Path](https://dsaint31.tistory.com/entry/Python-Module-Search-Path-and-syspath)