# Modules and Packages

## Module

쉽게 생각하면 Python code 로 구성된 file을 가르킨다.

* Python에서 module은 확장자가 `.py`인 파일을 가르킴 (python code를 내용으로 가지는 file).
* 모든 `.py` file들은 python에서 module로서 사용가능함.

code의 재사용을 위해 이전에 구현했거나 다른 이가 구현한 `.py`파일의 code를 재사용할 때, 해당 파일의 이름으로 불리는 module을 `import` statement를 사용하여 import한다.

* `ds_cal.py` 라는 file에 있는 code를 사용하고 싶은 경우, `ds_cal` module을 import한다.
* `import ds_cal` 과 같은 `import` statement를 이용함.

Python에서는 이미 standard library로 여러 built-in module들을 제공하고 있으며, Third party에서 만든 library의 module들과 함께 개발자가 만든 본인의 module들도 import가능하다.

> * `module`을 import할 때, 해당 `module`을 읽어와야하는데 이 경우 ***Module Search Path*** 를 참고하여 python은 module을 읽어들임.  
> * ***Module Search Path*** 에 기재된 path들에서 `module`의 이름을 기준으로 `module`을 읽어들임 (가장 먼저 위치한 path의 `module`에 우선권이 있음).  
> * 기본적으로 현재 작업 디렉토리가 포함되므로 이를 이용하여 `module`에 대해 익히고, 다른 path의 `module`들을 사용하기 위해 `Module Search Path`를 수정하는 방법은 추후 살펴본다.

참고로 흔히, import가 되는 `.py` 파일을 `module`이라고 부르고 python interpreter에게 수행되기 위해 인자로 넘겨지는 `.py` 파일은 main program 혹은 main script라고 불린다.

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
* 실제로 `ds_cal.ds_addition(a, b)`를  호출하여 그 결과를 `r`에 할당함.
* `module`의 global attribute들에 접근하기위해서는 `module` 이름을 prefix로 사용해야 함(위의 예에서는 `ds_cal`이 prefix로 사용됨).
* 이는 `ds_cal`과 같은 import된 module에 대한 ***Name Space***가 생성되었음을 의미하며, 해당 name space에 모듈의 attribute들이 속하게 됨.

## `as`를 통한 alias(별칭) 사용하기.

앞서 예의 `import` statement에서 import된 모듈에 접근은 모듈 파일의 이름을 통해서임.

해당 이름이 너무 긴 경우나 관례적으로 사용되는 별칭이 있는 경우엔 alias를 지정해주어 모듈의 attribute에 접근함.

해당 alias를 지정하는 `import` statement는 다음과 같음.

```Python
import ds_cal as dc
```

* `import ds_cal`로 import한 경우 `ds_cal.ds_addition(a, b)`.
* `import ds_cal as dc`로 Alias를 `dc`로 지정한 경우 `dc.ds_addition(a, b)` 로 접근 가능함.

> Python 에서 가장 유명한 alias 중 하나는 NumPy 를 가르키는 `np`임.  
> Numpy를 사용하는 경우, `import numpy as np` 가 가장 많이 사용됨.  
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

## 특정 module의 모든 attribute 모조리 import

아래와 같은 import문을 사용할 경우, `ds_cal.py` 파일의 모든 global scope의 attribute들을 import한다.

```Python
from ds_cal import *
```

장점은 가장 편하다는 것으로 prefix가 필요없고, import 할 때 필요한 attribute들을 입력해주지 않아도 된다는 것임.

문제는 일반적으로 특정 module에서 어떤 attribute들이 있는지 알기 어렵고, prefix를 사용하지 않기 때문에 name collusion이 발생하기 쉽다. 

> 해당 code의 동작은 알고 있어야하지만, 사용은 절대 추천하지 않는다.

---

## Packages

Python에서 `module`이 `.py`파일로 구현되는 것처럼, `package`는 `module`들이 포함된 directory로 구현된다.

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
