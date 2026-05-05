---
title: Signals and Slots 예제 (Connection Type별)
description: PySide6에서의 Signals and Slots 개념, 용어 정리, Event Handling과의 비교, 그리고 DirectConnection/QueuedConnection/AutoConnection 3가지 Connection Type별 실용 예제.
tags:
  - Qt
  - PySide6
  - PyQt6
  - signal
  - slot
  - connect
  - DirectConnection
  - QueuedConnection
  - AutoConnection
  - QThread
date: 2025-04-12
---

# Signals and Slots

## 개요

Signals and Slots는 ***Qt 고유의 object 간 communication 기법*** 임.

Event 처리에 많이 활용되지만,  
본래 목적은 `QObject`를 상속한 ***여러 object 간의 느슨한 결합(loose coupling)*** 을 통한 communication임.

> 기존의 callback이나 interface를 활용한 방식보다  
> object 간의 coupling이 약하다(느슨하다)는 것이 주요 장점임.

실제로 PySide6 application에서 object 간 communication이 필요한 경우,  
Event Handling보다 Signals and Slots를 사용하는 것이 일반적임.

* ***Event Handling*** 은 low-level event 처리(keyboard, mouse 등)나 비동기 처리(`postEvent` 등)에 적합함.
* ***Signals and Slots*** 는 widget 간 상호작용이나 application logic 간의 고수준(high-level) communication에 적합함.

이 두 메커니즘은 대립 관계가 아니라 ***상호 보완적*** 임.

## 주요 용어

### Signal

어떤 interaction(≈ event)이 일어났음을 알리는 ***notification*** 에 해당함.

* 해당 interaction이 일어난 widget(object)에서 생성(emit)됨.
* 연결(connected)되어 있는 ***Slot*** 으로 전달됨.
* Signal을 통해 관련 data를 argument로 전달하는 것도 가능함.

대표적인 예로, 사용자가 button을 클릭할 때 발생하는 `clicked` Signal이 있음.

### Slot

특정 Signal이 발생할 때 수행되도록 연결(hook up)된 ***method 또는 function*** 을 가리킴.

* 일반적인 Python method나 function이 Slot이 될 수 있음.
* `lambda` function이나 built-in function도 Slot으로 사용 가능함.
* PySide6 widget에 이미 정의된 method(public slots)도 Slot으로 사용 가능함.
    * 예: [`QLabel`의 public slots](https://doc.qt.io/qt-6/qlabel.html#public-slots)

특히 widget에 미리 정의된 method를 Slot으로 사용하면  
***widget 간의 상호작용*** 을 간결하게 구현할 수 있음.

### Connection

Signal의 `connect()` method를 통해 해당 Signal과 Slot을 연결하는 것임.  
hook up이라고도 불림.

* 하나의 Signal에 복수의 Slot을 연결할 수 있음 (1:N).
* 복수의 Signal을 하나의 Slot에 연결할 수도 있음 (N:1).
* `type` 키워드 파라메터로 Connect Type을 지정할 수 있음.

```python
button.clicked.connect(self.button_clicked)
```

위 코드는 `QPushButton` instance의 `clicked` Signal에  
`self.button_clicked` method를 Slot으로 연결하는 예임.

* `type` 파라미터에 argument를 지정하지 않았으므로 
* 기본값인 AutoConnection 으로 동작.

### Emit (Activation)

Signal이 발생(emit)하여 연결된 Slot이 실행되는 것을 의미함.

> 복수의 Signal이 연결된 Slot에서는  
> `self.sender()`를 통해 Signal을 보낸 object를 확인할 수 있음.  
> `sender()`는 `QObject`에 정의된 method이므로 모든 Qt object에서 호출 가능함.

## Signals and Slots vs. Event Handling

Signals and Slots는 Event System과 ***별개의 메커니즘*** 이지만,  
connection type에 따라 내부적으로 Event System을 활용하는 경우가 있음.

| 항목 | Event Handling | Signals and Slots |
|:---|:---|:---|
| 추상화 수준 | Low-level | High-level |
| 주요 용도 | keyboard, mouse 등 세밀한 event 처리 | widget 간 communication, application logic 연결 |
| 처리 방식 | Event Handler method overriding | Signal-Slot connection |
| coupling | widget class에 종속적 | object 간 느슨한 결합 |

## Connection Type

`connect()` 호출 시 ***connection type*** 을 지정할 수 있음.  
Connection type에 따라 Slot이 호출되는 방식과 시점이 달라짐.

| Connection Type | 동작 방식 | Event System 사용 여부 |
|:---|:---|:---|
| `Qt.ConnectionType.DirectConnection` | Signal emit 시 Slot을 즉시 호출 (동기) | 사용 안 함 (직접 함수 호출) |
| `Qt.ConnectionType.QueuedConnection` | `QMetaCallEvent`를 receiver의 posted event queue에 등록 (비동기) | Posted Event 활용 |
| `Qt.ConnectionType.AutoConnection` | 같은 thread → Direct, 다른 thread → Queued (기본값) | 상황에 따라 다름 |

> `connect()`에서 connection type을 생략하면  
> 기본값인 `Qt.ConnectionType.AutoConnection`이 적용됨.

### Connection Type Examples

다음 세 가지 예제를 통해 각 connection type의 동작 차이를 살펴봄.

| 예제 | Connection Type | 핵심 포인트 |
|:---|:---|:---|
| 예제 1 | `DirectConnection` | Slot이 emitter의 thread에서 즉시 실행됨 |
| 예제 2 | `QueuedConnection` | Slot이 receiver의 thread에서 비동기적으로 실행됨 |
| 예제 3 | `AutoConnection` | 같은 thread / 다른 thread 여부에 따라 자동 결정됨 |

#### 예제 1: DirectConnection

다음 코드는 button을 클릭하면 `clicked` Signal이 발생하고,  
`DirectConnection`으로 연결된 Slot이 ***즉시 실행*** 되는 예제임.

`DirectConnection`은 Signal이 emit된 시점에  
Slot을 ***일반 함수 호출처럼 동기적으로 즉시 실행*** 함.

Event System을 거치지 않으며,  
`QEvent`도 생성되지 않고, `event()`나 `notify()`도 호출되지 않음.

```python
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MW(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("DirectConnection Ex")
        self.resize(380, 180)

        self.label = QLabel("Button을 클릭하면 Slot이 즉시 실행됨.")
        self.button = QPushButton("Click Me")

        # DirectConnection: Slot이 즉시 호출됨.
        self.button.clicked.connect(
            self.on_clicked,
            Qt.ConnectionType.DirectConnection,
        )

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def on_clicked(self):
        """
        DirectConnection으로 연결된 Slot.

        Signal이 emit되면 이 method가
        emit한 thread에서 즉시 호출됨.
        Event System을 거치지 않는 직접 함수 호출임.
        """

        import threading

        tid = threading.current_thread().name
        print(f"[DirectConnection] on_clicked() called in: {tid}")
        self.label.setText(
            f"Slot executed directly in: {tid}"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    window.show()
    sys.exit(app.exec())
```

위 코드의 흐름은 다음과 같음.

1. 사용자가 button을 클릭함.
2. `clicked` Signal이 emit됨.
3. `DirectConnection`이므로 `on_clicked()`가 ***즉시 호출*** 됨.
4. `threading.current_thread().name`으로 확인하면 `MainThread`에서 실행됨을 알 수 있음.

> `DirectConnection`은 같은 thread에서 Signal-Slot을 연결할 때  
> 가장 단순하고 직관적인 방식임.  
> 단, Slot이 ***Signal을 emit한 thread*** 에서 실행되므로,  
> cross-thread 상황에서 사용하면 thread-safety 문제가 발생할 수 있음.

`DirectConnection`의 cross-thread 문제를 구체적으로 살펴보면 다음과 같음.

worker thread에서 Signal을 emit하고,  
main thread에 있는 widget의 method가 `DirectConnection`으로 연결되어 있다고 가정함.

```python
# worker thread에서 실행되는 코드
self.work_done.emit("result")
```

```python
# main thread의 widget에 정의된 Slot
def on_work_done(self, message):
    self.label.setText(message)       # GUI widget 조작
    self.progress_bar.setValue(100)    # GUI widget 조작
```

이 경우 `DirectConnection`이므로 `on_work_done()`은  
emit한 ***worker thread에서 즉시 실행*** 됨.

문제는 Qt의 GUI widget이 ***main thread에서만 안전하게 접근 가능*** 하다는 점임.  
worker thread에서 `QLabel.setText()`나 `QProgressBar.setValue()`를 호출하면  
다음과 같은 문제가 발생할 수 있음.

* ***crash*** : main thread가 동시에 같은 widget을 rendering 중이면 내부 상태가 충돌하여 segmentation fault 등이 발생할 수 있음.
* ***화면 깨짐*** : widget의 internal state와 실제 화면 표시가 불일치하여 rendering artifact가 나타날 수 있음.
* ***race condition*** : main thread와 worker thread가 동시에 같은 widget의 속성을 읽고 쓰면 예측 불가능한 결과가 발생함.

이러한 문제가 항상 즉시 나타나는 것이 아니라  
timing에 따라 간헐적으로 발생하기 때문에 디버깅이 어려움.

따라서 ***cross-thread 상황에서는 `QueuedConnection`을 사용*** 하여  
Slot이 receiver의 Event Loop에서 실행되도록 해야 함.  
`AutoConnection`(기본값)을 사용하면 Qt가 thread affinity를 자동으로 판단하여  
cross-thread 시 `QueuedConnection`으로 동작하므로,  
명시적으로 `DirectConnection`을 지정하지 않는 한 이 문제는 일반적으로 발생하지 않음.

#### 예제 2: QueuedConnection

다음 코드는 worker thread에서 Signal을 emit하고,  
`QueuedConnection`으로 연결된 Slot이  
***main GUI thread의 Event Loop에서 비동기적으로 실행*** 되는 예제임.

`QueuedConnection`은 Signal이 emit될 때  
Qt가 내부적으로 `QMetaCallEvent`를 생성하여  
receiver가 속한 thread의 ***posted event queue*** 에 등록함.

따라서 Slot은 receiver의 Event Loop가 해당 event를 처리할 때 호출됨.

```python
import sys
import time

from PySide6.QtCore import QThread, Qt, Signal
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Worker(QThread):
    """
    별도의 thread에서 작업을 수행하고
    완료 시 Signal을 emit하는 worker.
    """

    work_done = Signal(str)

    def run(self):
        import threading

        tid = threading.current_thread().name
        print(f"[Worker] run() executing in: {tid}")

        # 시간이 걸리는 작업을 simulation.
        time.sleep(1)

        self.work_done.emit(f"Work completed in: {tid}")


class MW(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("QueuedConnection Ex")
        self.resize(420, 180)

        self.label = QLabel(
            "Button을 누르면 worker thread에서 작업 후\n"
            "main thread의 Slot이 비동기로 호출됨."
        )
        self.button = QPushButton("Start Worker")
        self.button.clicked.connect(self.start_worker)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def start_worker(self):
        self.button.setEnabled(False)
        self.label.setText("Worker thread 실행 중...")

        self.worker = Worker()

        # QueuedConnection: Slot이 receiver(main)의
        # Event Loop에서 비동기적으로 실행됨.
        self.worker.work_done.connect(
            self.on_work_done,
            Qt.ConnectionType.QueuedConnection,
        )

        self.worker.start()

    def on_work_done(self, message):
        """
        QueuedConnection으로 연결된 Slot.

        Worker thread에서 emit된 Signal이
        main thread의 posted event queue에 등록된 뒤,
        main thread의 Event Loop가 처리할 때 호출됨.
        """

        import threading

        tid = threading.current_thread().name
        print(f"[QueuedConnection] on_work_done() called in: {tid}")
        print(f"[QueuedConnection] message: {message}")

        self.label.setText(
            f"Result: {message}\n"
            f"Slot executed in: {tid}"
        )
        self.button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    window.show()
    sys.exit(app.exec())
```

위 코드의 흐름은 다음과 같음.

1. 사용자가 `Start Worker` button을 클릭함.
2. `Worker` thread가 시작되어 `run()`이 별도 thread에서 실행됨.
3. 작업 완료 후 `work_done` Signal이 worker thread에서 emit됨.
4. `QueuedConnection`이므로 Qt가 `QMetaCallEvent`를 생성하여 main thread의 posted event queue에 등록함.
5. Main thread의 Event Loop가 해당 event를 처리할 때 `on_work_done()`이 호출됨.
6. `threading.current_thread().name`으로 확인하면 Slot이 `MainThread`에서 실행됨을 알 수 있음.

실행 시 console 출력은 다음과 같음.

* `[Worker] run() executing in: Dummy-1` (또는 유사한 thread 이름)
* `[QueuedConnection] on_work_done() called in: MainThread`
* `[QueuedConnection] message: Work completed in: Dummy-1`

핵심은 ***Signal은 worker thread에서 emit되었지만, Slot은 main thread에서 실행*** 된다는 점임.

이 방식이 중요한 이유는 다음과 같음.

* Qt의 GUI widget은 ***main thread에서만 안전하게 접근*** 할 수 있음.
* Worker thread에서 직접 widget을 조작하면 crash나 undefined behavior가 발생할 수 있음.
* `QueuedConnection`을 사용하면 worker thread의 결과를 main thread의 Event Loop를 통해 안전하게 widget에 반영할 수 있음.

#### 예제 3: AutoConnection (가장 중요)

다음 코드는 `AutoConnection`(기본값)을 사용하여  
***같은 thread에서 emit하면 Direct, 다른 thread에서 emit하면 Queued*** 로  
자동 결정되는 동작을 확인하는 예제임.

하나의 Slot에 대해 connection type을 명시하지 않고,  
emit하는 thread에 따라 동작이 달라지는 것을 관찰함.

```python
import sys
import time

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Worker(QThread):
    """
    별도의 thread에서 Signal을 emit하는 worker.
    """

    notify = Signal(str)

    def run(self):
        import threading

        tid = threading.current_thread().name

        time.sleep(0.5)
        self.notify.emit(f"from worker thread ({tid})")


class MW(QWidget):
    """
    AutoConnection 동작을 확인하는 main window.

    같은 Signal-Slot 연결이라도 emit하는 thread에 따라
    DirectConnection 또는 QueuedConnection으로 자동 결정됨.
    """

    manual_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("AutoConnection Ex")
        self.resize(460, 260)

        self.label = QLabel(
            "AutoConnection은 emit하는 thread에 따라\n"
            "Direct 또는 Queued로 자동 결정됨."
        )

        self.btn_same = QPushButton(
            "Emit from Main Thread (→ Direct)"
        )
        self.btn_worker = QPushButton(
            "Emit from Worker Thread (→ Queued)"
        )

        self.btn_same.clicked.connect(self.emit_from_main)
        self.btn_worker.clicked.connect(self.start_worker)

        # AutoConnection (기본값): connect()에
        # connection type을 지정하지 않으면 AutoConnection임.
        self.manual_signal.connect(self.on_notify)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btn_same)
        layout.addWidget(self.btn_worker)
        self.setLayout(layout)

    def emit_from_main(self):
        """
        Main thread에서 Signal을 emit함.

        Sender와 receiver가 같은 thread이므로
        AutoConnection은 DirectConnection으로 동작함.
        """

        import threading

        tid = threading.current_thread().name
        print(f"\n[Main] emit_from_main() in: {tid}")
        print("[Main] before emit")
        self.manual_signal.emit(f"from main thread ({tid})")
        print("[Main] after emit")

    def start_worker(self):
        """
        Worker thread에서 Signal을 emit하게 함.

        Sender와 receiver가 다른 thread이므로
        AutoConnection은 QueuedConnection으로 동작함.
        """

        self.btn_worker.setEnabled(False)

        self.worker = Worker()

        # 동일한 Slot에 연결하되, connection type은 기본값(Auto).
        self.worker.notify.connect(self.on_notify)
        self.worker.finished.connect(
            lambda: self.btn_worker.setEnabled(True)
        )

        self.worker.start()

    def on_notify(self, message):
        """
        AutoConnection으로 연결된 Slot.

        같은 thread에서 emit되면 즉시 호출되고,
        다른 thread에서 emit되면 Event Loop를 통해 호출됨.
        """

        import threading

        tid = threading.current_thread().name
        print(f"[Slot] on_notify() called in: {tid}")
        print(f"[Slot] message: {message}")

        self.label.setText(
            f"Signal: {message}\n"
            f"Slot executed in: {tid}"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    window.show()
    sys.exit(app.exec())
```

**Main thread에서 emit한 경우**:

`Emit from Main Thread` button을 누르면 console 출력은 다음과 같음.

* `[Main] emit_from_main() in: MainThread`
* `[Main] before emit`
* `[Slot] on_notify() called in: MainThread`
* `[Slot] message: from main thread (MainThread)`
* `[Main] after emit`

핵심은 `[Slot] on_notify()`가 `[Main] after emit`보다 ***먼저*** 출력된다는 점임.

Sender(MW)와 receiver(MW)가 같은 thread에 있으므로  
`AutoConnection`이 ***`DirectConnection`으로 동작*** 하여  
Slot이 emit 흐름 안에서 즉시 실행됨.

**Worker thread에서 emit한 경우:**

`Emit from Worker Thread` button을 누르면 console 출력은 다음과 같음.

* `[Slot] on_notify() called in: MainThread`
* `[Slot] message: from worker thread (Dummy-1)`

Sender(Worker)와 receiver(MW)가 다른 thread에 있으므로  
`AutoConnection`이 ***`QueuedConnection`으로 동작*** 하여  
Slot이 main thread의 Event Loop에서 비동기적으로 실행됨.

**`AutoConnection` 의 동작 방식 정리:**

| emit 위치 | AutoConnection 동작 | Slot 실행 시점 |
|---|---|---|
| Main thread (same thread) | `DirectConnection` | emit 호출 흐름 안에서 즉시 |
| Worker thread (different thread) | `QueuedConnection` | main thread Event Loop가 처리할 때 |


* Signals and Slots는 Event System과 ***독립된 메커니즘*** 이지만, `QueuedConnection`에서는 내부적으로 Posted Event를 활용함.
* `DirectConnection`은 일반 함수 호출과 동일하게 즉시 실행되며, Event System을 거치지 않음.
* `QueuedConnection`은 cross-thread 상황에서 ***thread-safety를 보장*** 하는 핵심 방식임.
* `AutoConnection`(기본값)은 sender와 receiver의 thread affinity에 따라 Direct 또는 Queued를 자동 결정함.
* 일반적인 경우 `connect()`에서 connection type을 명시하지 않고 `AutoConnection`을 사용하면 됨.

## Signal이 전달하는 추가 데이터

Signal은 종류에 따라 Slot에 추가적인 ***argument를 전달*** 함.

예를 들어, `QPushButton`의 `clicked` Signal은  
별도의 argument 없이 "클릭되었다"는 사실만 알리는 반면,  
`QCheckBox`의 `toggled` Signal은 check 여부를 나타내는 `bool` 값을,  
`QButtonGroup`의 `buttonClicked` Signal은 클릭된 button의 reference를  
각각 Slot에 넘겨줌.

### Signal이 전달하는 arguments 확인 방법

특정 Signal이 어떤 argument를 전달하는지 확인하는 방법은 다음과 같음.

* ***Qt 공식 API 문서*** 에서 해당 widget의 Signals 섹션을 확인하는 것이 가장 정확함.
    * 예: [`QCheckBox`의 parent class인 `QAbstractButton`의 Signals](https://doc.qt.io/qt-6/qabstractbutton.html#signals)에서 `toggled(bool checked)`를 확인할 수 있음.
    * 예: [`QButtonGroup`의 Signals](https://doc.qt.io/qt-6/qbuttongroup.html#signals)에서 `buttonClicked(QAbstractButton *button)`을 확인할 수 있음.
* ***PySide6 공식 문서*** 에서도 동일한 정보를 확인할 수 있음.
    * 예: [`PySide6.QtWidgets.QAbstractButton` Signals](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QAbstractButton.html#signals)
* Python 코드에서 ***`help()`*** 를 사용하여 확인하는 것도 가능함.

```python
from PySide6.QtWidgets import QCheckBox
help(QCheckBox.toggled)
```

> Signal의 argument를 모르는 상태에서 Slot을 작성하면  
> parameter 개수 불일치로 runtime error가 발생하므로,  
> API 문서에서 Signal의 signature를 반드시 확인해야 함.

### 예제: Signal Argument 활용

다음 코드는 `QCheckBox`와 `QButtonGroup`을 이용하여  
Signal이 Slot에 전달하는 argument를 활용하는 예제임.

* `QButtonGroup.buttonClicked` Signal은 클릭된 ***button의 reference*** 를 Slot에 전달함.
* `QCheckBox.stateChanged` Signal은 ***check 상태를 나타내는 `int` 값*** 을 Slot에 전달함.
* 복수의 Signal이 연결된 Slot에서는 `self.sender()`를 통해 Signal을 보낸 object를 확인할 수 있음.

```python
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QCheckBox,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class MW(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Signal Argument Ex")
        self.resize(380, 280)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("What is most important?"))

        # QButtonGroup: 복수의 button을 그룹으로 관리함.
        self.bg = QButtonGroup(self)

        self.cb01 = QCheckBox("1. faith")
        self.cb02 = QCheckBox("2. hope")
        self.cb03 = QCheckBox("3. love")

        for cb in (self.cb01, self.cb02, self.cb03):
            layout.addWidget(cb)
            self.bg.addButton(cb)

        # 기본값: exclusive mode (하나만 선택 가능).
        self.bg.setExclusive(True)

        # buttonClicked Signal은 클릭된 button의 reference를
        # argument로 Slot에 전달함.
        self.bg.buttonClicked.connect(self.on_button_clicked)

        self.dp_label = QLabel("")
        layout.addWidget(self.dp_label)

        # 별도의 checkbox로 exclusive mode를 전환함.
        self.mode_cb = QCheckBox("Check for multiple selection")

        # stateChanged Signal은 check 상태를 나타내는
        # int 값을 argument로 Slot에 전달함.
        self.mode_cb.stateChanged.connect(self.on_mode_changed)
        layout.addWidget(self.mode_cb)

        self.setLayout(layout)

    def on_button_clicked(self, button):
        """
        QButtonGroup.buttonClicked Signal의 Slot.

        이 Signal은 클릭된 button의 reference를
        argument로 전달함.

        Parameters
        ----------
        button : QAbstractButton
            클릭된 button의 reference.
            buttonClicked Signal이 전달하는 argument임.
        """

        text = button.text()
        print(f"[buttonClicked] selected: {text}")
        self.dp_label.setText(f"Selected: {text}")

    def on_mode_changed(self, state):
        """
        QCheckBox.stateChanged Signal의 Slot.

        이 Signal은 check 상태를 나타내는 int 값을
        argument로 전달함.
        Qt.CheckState.Checked(2) 또는
        Qt.CheckState.Unchecked(0) 등의 값이 전달됨.

        Parameters
        ----------
        state : int
            check 상태를 나타내는 값.
            stateChanged Signal이 전달하는 argument임.
        """

        if state == Qt.CheckState.Checked.value:
            self.bg.setExclusive(False)
            print("[stateChanged] multiple selection enabled")
        else:
            self.bg.setExclusive(True)
            print("[stateChanged] exclusive selection enabled")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    window.show()
    sys.exit(app.exec())
```

위 코드에서 주목할 점은 다음과 같음.

* `on_button_clicked(self, button)`: 
    * `button` parameter는 개발자가 임의로 추가한 것이 아니라, 
    * `buttonClicked` Signal이 전달하는 argument임. 
    * API 문서에서 `buttonClicked(QAbstractButton *button)`으로 명시되어 있음.
* `on_mode_changed(self, state)`: 
    * `state` parameter는 `stateChanged` Signal이 전달하는 argument임. 
    * API 문서에서 `stateChanged(int state)`로 명시되어 있음.
* `self.sender()`: 
    * 복수의 Signal이 하나의 Slot에 연결된 경우, 
    * 어떤 object가 Signal을 emit했는지 확인할 때 사용함.
    * `QObject`에 정의되어 있으므로 모든 Qt object에서 호출 가능함.

## Summary

Signals and Slots 는 

* Qt 고유의 object 간 communication 기법 으로 
* 전통적인 Event handling 대신에 Qt기반의 GUI에서 이벤트 처리에 사용됨.

Signals and Slots 는

* connection type에 따라 동기식/비동기식 으로 동작함.
* 이를 정리하면 다음과 같음:

| 항목 | DirectConnection | QueuedConnection | **AutoConnection** |
|---|---|---|---|
| 동작 방식 | 즉시 함수 호출 (동기) | posted event queue 등록 (비동기) | 자동 결정 |
| Slot 실행 thread | Signal을 emit한 thread | receiver가 속한 thread | 상황에 따라 다름 |
| Event System 사용 | 사용 안 함 | `QMetaCallEvent`를 Posted Event로 활용 | 상황에 따라 다름 |
| 주요 사용 상황 | 같은 thread 내 communication | cross-thread communication | 일반적 사용 (기본값) |
| thread-safety | cross-thread 시 ***주의 필요*** | thread-safe | thread-safe |

Signals and Slots 에서

* signal 은 event에 대한 일종의 notification이고,  
* slot은 특정 signal이 emit된 경우 수행되도록 연결된 method 임.
* signal 은 연결된 slot 에 추가적인 argument를 전달할 수 있음.

마지막으로, custom signal 도 만들 수 있음 (이는 다음 문서에서 보다 자세히 다룸) :

---

---

## 참고자료

Signals and Slots에 대한 보다 자세한 내용은 다음 문서를 참고할 것.

* [Signals & Slots — Qt for Python](https://doc.qt.io/qtforpython-6/overviews/signalsandslots.html)
* [Signals and Slots — PyQt Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/signals_slots.html)