# Path (경로)

파일 시스템 내에서 **특정 파일(혹은 디렉토리)의 위치를 나타내는 양식**

## Absolute Path (**절대** 경로)

- 현 작업디렉토리(cwd)와 관계없이 절대적 위치

## Relative Path (**상대** 경로)

- 현 작업디렉토리를 기준으로 상대적 위치를 가르킴.

> 보다 자세한 내용은 다음 URL을 참고할 것.
>
> * [Path (경로)란](https://dsaint31.tistory.com/222)

---

## Python의 path관련 참고사항

python인터프리터에서 실행되는 python 소스 파일의 absolute path를 확인하는 코드

```python
import os
print(__file__)
print(os.path.abspath(__file__))
```

- 중간에 *shortcut(바로가기)* 등이 있는 경우, 실제 위치를 보고 싶을 때는 `os.path.realpath(__file__)` 를 사용.
- 실행되고 있는 `.py` 소스파일이 있는 폴더 경로만을 확인하기 위해서는 다음을 이용.
    
    ```python
    print(os.path.dirname(os.path.realpath(__file__)) )
    ```
    

현재 python이 수행되고 있는 working directory를 확인하는 코드는 다음과 같음.

```python
import os
print(os.getcwd()) # current working directory
```

working directory를 변경하는 코드는 다음과 같음.

```Python
import os
print(f"before: {os.getcwd()}")
os.chdir("/home/dsaint31/")
print(f"after: {os.getcwd()}")
```