---
title: Python zip() Function
tags: [python, zip, iterable, iterator, built-in]
---

# Python `zip()` 튜토리얼 

## 0. 사전 지식

* [iterator 와 iterable, generator](https://dsaint31.tistory.com/501)

## 1. 한 줄 정의

`zip()`은

> zip은 여러 `iterable`에서 같은 iteration 단계에서 생성된 값들을 묶어 `tuple`로 반환하는 `iterator` 생성 함수.

중요한 점:

* 각 `iterable`(주로 `list`객체)에서 **차례대로 꺼낸 값(item)** 을 `tuple` 로 묶어냄.
* 결과는 `iterator`.

## 2. 가장 기본 예제

```python
a = [1, 2, 3]
b = ['a', 'b', 'c']

print(list(zip(a, b)))
```

결과:

```python
[(1, 'a'), (2, 'b'), (3, 'c')]
```

위의 예에서 zip은 다음처럼 동작:

1. `a`에서 `1`을 꺼냄
2. `b`에서 `'a'`를 꺼냄
3. `(1, 'a')`로 묶음
4. 다음 값들도 같은 방식 반복

즉, **같은 순서(iteration)에서 나온 값들이 묶임.**

## 3. 길이가 다른 iterable 객체들이 인자인 경우

```python
a = [1, 2, 3, 4]
b = ['x', 'y']

print(list(zip(a, b)))
```

결과:

```python
[(1, 'x'), (2, 'y')]
```

zip은

* 인자로 주어진 여러 `iterable` 중 
* 하나라도 더 이상 꺼낼 값이 없으면 멈춤.
* **가장 짧은 `iterable` 길이에 맞춰서 종료됨.**


## 4. for문에서 가장 많이 사용

```python
names = ["Alice", "Bob", "Charlie"]
scores = [90, 85, 100]

for name, score in zip(names, scores):
    print(name, score)
```

출력:

```
Alice 90
Bob 85
Charlie 100
```

* zip이 `(name, score)` 튜플을 하나씩 만듦
* `for`문이 그것을 풀어서 사용

## 5. index 를 사용하는 것이 아님.

zip은

* 각 `iterable`에서 **차례대로 꺼낸 값** 을 묶음
* index가 없는 `generator`에서도 잘 동작

```python
def gen():
    for i in range(3):
        yield i * 10

a = [1, 2, 3]
b = gen()

print(list(zip(a, b)))
```

결과:

```
[(1, 0), (2, 10), (3, 20)]
```

## 6. zip은 iterator 임

```python
a = [1, 2]
b = [3, 4]

z = zip(a, b)

print(list(z))
print(list(z))
```

결과:

```
[(1, 3), (2, 4)]
[]
```

* 한번 전체 item에 대한 iteration이 수행되고 나면 `iterator` 객체는 비어짐.
* 여러 차례 iteration을 할 수 있는 `iterable` 객체와 다른 점.
* `zip()`의 반환값은 `iterator` 객체임.

## 7. 딕셔너리 만들기

```python
keys = ['name', 'age']
values = ['Alice', 25]

d = dict(zip(keys, values))
print(d)
```

결과:

```
{'name': 'Alice', 'age': 25}
```

* `zip()`을 활용하여 `dict`객체를 만들 수 있음. 


## 8. unpacking과 같이 사용하는 예

```python
pairs = [(1, 'a'), (2, 'b'), (3, 'c')]

a, b = zip(*pairs)

print(a)
print(b)
```

결과:

```
(1, 2, 3)
('a', 'b', 'c')
```

`*`는 묶인 튜플들을 다시 풀어주는 역할(unpacking)을 수행.

asterisk 를 통해 packing과 unpacking이 이루어지는 데 이에 대해 자세한 건 다음을 참고:

* [asterisk `*` 사용하기 : unpacking, packing](https://ds31x.tistory.com/57)


## 요약

* zip은 여러 `iterable`에서 **같은 순서로 꺼낸 값들을 묶음**
* 꺼내진 값들을 `tuple` 로 묶음.
* 가장 짧은 `iterable` 기준으로 멈춘다
* `iterator` 객체를 반환한다
