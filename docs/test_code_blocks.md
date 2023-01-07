# Code blocks


## material의 code block의 다양한 기능 테스트.

It's some difficult.

```
import tensorflow as tf
```

---
``` py title="test.py" 
import tensorflow as tf # (1)

def bubble_sort(itmes):
  for i in range(len(items)):
    for j in range(len(items) - 1 - i):
      if items[j] > itmes[j+1]:
        items[j], items[j+1] = items[j+1], items[j]
```

---

``` py hl_lines="2 3" linenums="1"
def bubble_sort(items):
    for i in range(len(items)):
        for j in range(len(items) - 1 - i):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
```



---


1. :man_raising_hand: 이건 code annotation임. `code`, __formatted text__, images, ... 등등의 markdown에서 사용가능한 것들을 포함할 수 있음.
