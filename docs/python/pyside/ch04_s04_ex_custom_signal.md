---
title: Custom Signal 만들기
description: PySide6에서 Custom Signal을 정의하고 emit하는 방법, class variable로 선언해야 하는 이유, Event Handling을 Signals and Slots 메커니즘으로 대체하는 패턴, 실용 예제.
tags:
  - Qt
  - PySide6
  - PyQt6
  - signal
  - slot
  - custom signal
  - Signal
  - pyqtSignal
  - emit
  - QObject
date: 2025-04-12
---

# Custom Signal

## 개요

앞서 살펴본 예제들은 모두 Qt가 미리 정의해둔 ***built-in Signal*** 을 사용한 경우임.

그런데 실제 application을 개발하다 보면,  
Qt가 제공하지 않는 ***고유한 notification*** 이 필요한 상황이 발생함.

이때 개발자가 직접 정의하여 사용하는 것이 ***Custom Signal*** 임.

Custom Signal을 사용하면 object가 다른 object에게  
자신의 ***상태 정보나 데이터*** 등을 전달할 수 있으며,  
해당 정보를 넘겨받는 object는  
Custom Signal에 연결된 Slot을 통해 이를 획득하게 됨.

---

Custom Signal의 활용을 GUI programming으로 한정짓는다면,

* 특정 widget에서 어떤 event에 대한 Custom Signal을 추가하여,
* 기존의 Event Handling에서 method overriding으로 event를 처리하던 것을,
* Signals and Slots 메커니즘으로 대체할 수 있게 해줌.

즉, Event Handler 안에서 Custom Signal을 emit하고,  
해당 Signal에 연결된 Slot에서 실제 처리를 수행하는 패턴임.

이 패턴의 장점은 ***event 발생 지점과 처리 로직을 분리*** 할 수 있다는 것임.  
Event Handler를 overriding하는 방식은 처리 로직이 해당 widget class에 종속되지만,  
Custom Signal을 사용하면 외부의 다른 object에서 Slot으로 처리할 수 있으므로  
재사용성과 유지보수성이 높아짐.

## Custom Signal 사용 방법

Custom Signal을 정의하고 사용하는 일반적인 절차는 다음과 같음.

### 1. `QObject`를 상속한 class를 정의함

Custom Signal을 가지는 class는 반드시 ***`QObject`를 상속*** 해야 함.

`QWidget`, `QMainWindow` 등은 모두 `QObject`의 subclass이므로  
별도로 `QObject`를 상속할 필요 없이 Custom Signal을 정의할 수 있음.

### 2. `Signal` factory로 Custom Signal을 ***class variable*** 로 선언함

PySide6에서는 `QtCore.Signal`을,  
PyQt6에서는 `QtCore.pyqtSignal`을 사용하여 Custom Signal을 생성함.

다음의 코드를 참고:

```Python
from PySide6.QtCore import Signal

class MW(QMainWindow):
    # Custom Signal 선언 (int argument 1개를 전달).
    change_pixmap = Signal(int)
```

> PyQt6의 경우에는 다음과 같음.
>
> ```Python
> from PyQt6.QtCore import pyqtSignal
>
> class MW(QMainWindow):
>     change_pixmap = pyqtSignal(int)
> ```

여기서 ***반드시 class variable로 선언해야 한다*** 는 점이 중요함.

`__init__()` 안에서 `self.change_pixmap = Signal(int)`처럼  
***instance variable로 정의하면 동작하지 않음.***

그 이유는 다음과 같음.

* Qt의 ***`QMetaObject`*** (meta-class system)는 class 정의 시점에 Signal을 인식하고, 내부적으로 C++ signal-slot system과 연결함.
* `__init__()` 안에서 instance variable로 정의하면 class 정의 시점에 `QMetaObject`가 이를 감지할 수 없음.
* 따라서 `connect()`나 `emit()`이 정상 동작하지 않게 됨.

### 3. Signal을 emit해야 하는 위치에서 `emit()`을 호출함

Custom Signal의 `emit()` method를 호출하면  
연결된 모든 Slot에 해당 Signal이 전달됨.

```python
# int argument를 함께 전달하여 emit.
self.change_pixmap.emit(1)
```

### 4. Custom Signal에 Slot을 연결함

built-in Signal과 동일하게 `connect()`를 사용하여 Slot을 연결함.

```python
self.change_pixmap.connect(self.change_pixmap_handler)
```

## 예제: Custom Signal로 Event Handling 대체

다음 코드는 `+` key와 `-` key를 누르면  
표시되는 숫자 이미지가 0~9 사이에서 순환(circular)하며 변경되는 예제임.

이 예제의 핵심은 다음과 같음.

* `keyPressEvent()`에서 직접 이미지를 변경하지 않음.
* 대신 Custom Signal(`change_pixmap`)을 emit하고,  
  연결된 Slot(`change_pixmap_handler`)에서 이미지를 변경함.
* 즉, ***Event Handler에서는 Signal만 emit*** 하고,  
  ***실제 처리 로직은 Slot에 위임*** 하는 패턴임.

```python
import os
import sys

from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QKeyEvent, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)


class MW(QMainWindow):
    """
    QMainWindow는 QObject를 상속하므로
    Custom Signal을 class variable로 선언할 수 있음.
    """

    # Custom Signal 선언.
    # int argument 1개를 전달함.
    # 반드시 class variable로 선언해야 함.
    change_pixmap = Signal(int)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.fstr = os.path.dirname(os.path.abspath(__file__))
        self.setGeometry(100, 100, 200, 300)
        self.setWindowTitle("Custom Signal Ex")
        self.setup_main_wnd()
        self.show()

    def setup_main_wnd(self):
        self.idx = 0

        # Custom Signal에 Slot을 연결함.
        self.change_pixmap.connect(self.change_pixmap_handler)

        layout = QVBoxLayout()

        info_label = QLabel(
            "<p>Press <i>+</i> or <i>-</i> to change image</p>"
        )
        info_label.setTextFormat(Qt.TextFormat.RichText)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)

        self.img_label = QLabel()

        img_path = os.path.join(self.fstr, "img", "0.png")
        pixmap = QPixmap(img_path)
        if pixmap.isNull():
            print(f"이미지 로딩 실패: {img_path}")
        self.img_label.setPixmap(
            pixmap.scaled(
                QSize(180, 250),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.img_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def keyPressEvent(self, event: QKeyEvent):
        """
        key press Event Handler.

        + 또는 - key 입력 시
        이미지 변경을 위한 Custom Signal을 emit함.

        이 method에서 이미지를 직접 변경하지 않고,
        Custom Signal을 emit하여
        연결된 Slot에서 처리하게 함.
        """

        if event.key() == Qt.Key.Key_Plus:
            self.change_pixmap.emit(1)
        elif event.key() == Qt.Key.Key_Minus:
            self.change_pixmap.emit(-1)

        # 기본 key event 처리를 위해 반드시 호출해야 함.
        # 이를 생략하면 하위 widget의 key 입력 기능,
        # menu 단축키, focus 이동 등의
        # Qt 기본 event 전달 흐름이 중단됨.
        super().keyPressEvent(event)

    def change_pixmap_handler(self, offset: int):
        """
        Custom Signal(change_pixmap)에 연결된 Slot.

        Parameters
        ----------
        offset : int
            이미지 index의 변화량.
            change_pixmap Signal이 emit할 때
            전달하는 argument임.
        """

        self.idx = (self.idx + offset) % 10

        img_path = os.path.join(
            self.fstr, "img", f"{self.idx}.png"
        )
        pixmap = QPixmap(img_path)
        if pixmap.isNull():
            print(f"이미지 로딩 실패: {img_path}")
        self.img_label.setPixmap(
            pixmap.scaled(
                QSize(180, 250),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    sys.exit(app.exec())
```

> 실행을 위해서는 script 파일과 같은 directory에  
> `img/` 폴더를 만들고, `0.png` ~ `9.png` 이미지 파일을 준비해야 함.

위 코드의 흐름은 다음과 같음.

1. 사용자가 `+` key를 누름.
2. OS에서 native key event가 발생함 (Spontaneous Event).
3. Qt가 이를 `QKeyEvent`로 변환하여 `keyPressEvent()`가 호출됨.
4. `keyPressEvent()`에서 `self.change_pixmap.emit(1)`을 호출함.
5. Custom Signal `change_pixmap`이 `int` argument `1`과 함께 emit됨.
6. 연결된 Slot인 `change_pixmap_handler(self, offset)`이 호출됨.
7. `offset` 값에 따라 이미지 index를 변경하고 화면을 갱신함.

> `self.idx = (self.idx + offset) % 10`에서  
> Python의 `%` 연산은 음수에 대해서도  
> 양수 결과를 반환하므로 별도의 경계 처리가 필요 없음.  
> 예: `(-1) % 10` → `9`

### Event Handling 방식과의 비교

위 예제에서 Custom Signal을 사용하지 않고  
`keyPressEvent()`에서 직접 이미지를 변경하는 방식도 가능함.

```python
def keyPressEvent(self, event: QKeyEvent):
    if event.key() == Qt.Key.Key_Plus:
        self.change_pixmap_handler(1)
    elif event.key() == Qt.Key.Key_Minus:
        self.change_pixmap_handler(-1)
    super().keyPressEvent(event)
```

이렇게 해도 동일하게 동작함.

그럼에도 Custom Signal을 사용하는 이유는  
다음의 기능을 **보다 더 간결하고 직관적으로 구현** 할 수 있음:

* ***느슨한 결합(loose coupling)*** : Event Handler가 처리 로직을 직접 알 필요 없이, Signal만 emit하면 됨.  
  어떤 Slot이 연결되어 있는지는 Event Handler의 관심사가 아님.
* ***복수의 Slot 연결*** : 하나의 Custom Signal에 여러 Slot을 연결할 수 있음.  
  예를 들어, 이미지 변경과 동시에 log 기록, status bar 갱신 등을 각각 별도 Slot으로 처리할 수 있음.
* ***재사용성*** : Custom Signal을 가진 widget을 다른 application에서 재사용할 때, Slot만 교체하면 다른 동작을 수행할 수 있음.

> Event Handling에서도  
> `installEventFilter()` 메커니즘을 사용하면  
> 유사한 효과를 얻을 수 있음.
>   
> 다만, Signal-Slot 방식이  
> 코드의 가독성과 유지보수 측면에서 더 자연스러움.

물론 아주 단순한 경우에는 

* Event Handler에서 직접 처리하는 것이  
* 더 간결하고 명확할 수 있음.

Custom Signal은 ***widget의 재사용이 빈번하거나,  
복수의 object가 동일한 event에 반응해야 하는 경우,  
또는 Qt의 Model-View Architecture를 활용하는 경우*** 에 특히 유용함.

## Custom Signal을 별도 class에 정의하는 방법

위 예제에서는 `MW`(`QMainWindow` subclass) 자체에 Custom Signal을 선언했지만,  
***별도의 `QObject` subclass*** 에 Custom Signal을 정의하는 방법도 가능함.

```python
from PySide6.QtCore import QObject, Signal


class DsSignal(QObject):
    """Custom Signal을 가지는 별도 class."""

    change_pixmap = Signal(int)
```

이 경우 사용 방법은 다음과 같이 달라짐.

```python
class MW(QMainWindow):
    def __init__(self):
        super().__init__()
        # 별도 class의 instance를 생성함.
        self.signal = DsSignal()
        self.signal.change_pixmap.connect(
            self.change_pixmap_handler
        )

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Plus:
            # instance를 통해 emit함.
            self.signal.change_pixmap.emit(1)
        ...
```

이 방식은 Signal 정의를 widget class로부터 분리할 수 있다는 장점이 있음.

다만, 대부분의 경우에는 해당 widget class에 직접 Custom Signal을 선언하는 것이  
더 간결하고 직관적이므로, 별도 class로 분리하는 것은  
***Signal을 여러 class에서 공유하거나 재사용해야 하는 경우*** 에 고려하면 됨.

## Signal 선언 시 argument type 지정

`Signal()` factory는 전달할 argument의 ***type을 지정*** 하여 선언함.

```python
# argument 없음.
no_arg_signal = Signal()

# int argument 1개.
int_signal = Signal(int)

# str argument 1개.
str_signal = Signal(str)

# 복수의 argument.
multi_signal = Signal(int, str)
```

emit할 때 전달하는 argument는  
선언 시 지정한 type 및 개수와 일치해야 함.

```python
self.no_arg_signal.emit()
self.int_signal.emit(42)
self.str_signal.emit("hello")
self.multi_signal.emit(42, "hello")
```

> 선언과 emit의 argument가 일치하지 않으면 runtime error가 발생함.

## Summary 

* Custom Signal은 Qt가 제공하지 않는 고유한 notification이 필요할 때 개발자가 직접 정의하는 Signal임.
* 반드시 ***`QObject`를 상속한 class의 class variable*** 로 선언해야 함. instance variable로는 동작하지 않음.
* PySide6에서는 `Signal()`, PyQt6에서는 `pyqtSignal()`을 사용하여 생성함.
* Event Handler에서 Custom Signal을 emit하고 Slot에서 처리하는 패턴을 통해, ***Event Handling을 Signals and Slots 메커니즘으로 대체*** 할 수 있음.
* 이 패턴은 느슨한 결합, 복수 Slot 연결, 재사용성, cross-thread 지원 등의 장점을 제공함.
* 단순한 경우에는 Event Handler에서 직접 처리하는 것이 더 간결할 수 있으므로, 상황에 맞게 선택하면 됨.

> Custom Signal에 대한 보다 자세한 내용은 다음 문서를 참고할 것.
>
> * [Signals & Slots — Qt for Python](https://doc.qt.io/qtforpython-6/overviews/signalsandslots.html)
> * [PySide6.QtCore.Signal](https://doc.qt.io/qtforpython-6/PySide6/QtCore/Signal.html)