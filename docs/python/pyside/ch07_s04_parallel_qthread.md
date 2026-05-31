---
title: QThread의 기본 사용법
tags: [GUI, Qt, PySide6, PyQt, Thread, Multithreading, QThread, Signal, Slot, Event Loop]
---

# QThread의 기본 사용법

앞서 `QThread`와 `QRunnable`의 차이를 살펴보았다.  
이번 절에서는 `QThread`를 이용하여 PySide 또는 PyQt 기반 GUI application에서 background 작업을 수행하는 기본 구조를 살펴본다.

`QThread`는 PyQt 및 PySide에서 제공하는 Qt class로, Qt framework의 thread 기능을 Python에서 사용할 수 있도록 해준다.

`QThread`는 하나의 thread 실행을 추상화한 class이며, Python application에서 별도의 worker thread를 생성하고 관리할 수 있는 기능을 제공함. 이를 이용하면 GUI thread를 오래 block할 수 있는 작업을 별도의 thread에서 수행하도록 분리할 수 있다.

다만 `QThread`를 사용할 때 다음 사항을 명확히 이해해야 한다.

* `QThread` object 자체가 곧바로 별도 thread 안에서 실행되는 것은 아님.
* `start()`를 호출하면 새로운 native thread가 생성되고, 그 thread 안에서 `run()` method가 실행됨.
* GUI widget은 worker thread에서 직접 수정하면 안 됨.
* Worker thread의 결과는 signal을 통해 GUI thread로 전달하고, GUI thread의 slot에서 widget을 update하는 방식이 권장됨.

즉, `QThread`는 background 작업을 수행하기 위한 thread 실행 환경을 제공하고, GUI update는 signal-slot mechanism을 통해 GUI thread에서 처리하도록 구성하는 것이 기본 원칙임.

# QThread의 주요 method

## run()

`run()` method는 thread가 시작된 뒤, 새 thread 안에서 실행되는 method임.

개발자가 `QThread`를 상속하여 사용할 경우, 이 `run()` method를 override하여 별도 thread에서 수행할 작업을 작성한다.

```python
class WorkerThread(QThread):
    def run(self):
        # 별도 thread에서 수행할 작업
        ...
```

* `run()` method는 일반적으로 직접 호출하지 않는다. 
* 직접 `run()`을 호출하면 새로운 thread가 만들어지는 것이 아니라, 현재 thread에서 일반 method처럼 실행된다.

따라서 `QThread`를 사용할 때는 반드시 `start()`를 호출해야 한다.  

* `start()`가 호출되면 Qt가 새로운 thread를 만들고, 
* 그 thread 안에서 `run()` method를 실행한다.

## start()

`start()` method는 thread 실행을 시작하는 method임.

* `start()`를 호출하면 
* Qt는 새로운 native thread를 생성하고, 
* 해당 thread 안에서 `run()` method가 실행되도록 한다.

즉, `start()`는 단순히 `run()`을 현재 thread에서 호출하는 method가 아니다.  

> 새로운 thread 실행을 시작하고, 그 thread의 entry point로 `run()`이 수행되도록 하는 method임.

```python
self.worker.start()
```

* 이미 실행 중인 `QThread`에 대해 다시 `start()`를 호출하는 것은 적절하지 않다.  
* 따라서 일반적으로 `isRunning()`을 이용하여 thread가 이미 실행 중인지 확인한 뒤 시작하는 방식을 사용하는 것이 권장됨.

## quit()

`quit()` method는 thread의 event loop를 종료하도록 요청하는 method임.

중요한 점은 `quit()`가 항상 `run()` 내부의 작업을 ***즉시 중단시키는 method가 아니라는 점** 이다. 

* `quit()`는 thread 내부에서 event loop가 실행 중일 때, 
* 즉 `exec()`가 호출되어 있는 경우에 그 ***event loop를 종료하도록 요청*** 한다.

따라서 `run()` method 안에서 단순히 반복문을 수행하는 구조라면, `quit()`만으로 그 반복문이 자동으로 중단되지는 않는다.

```python
def run(self):
    for i in range(5):
        time.sleep(1)
```

* 위와 같은 구조에서는 `quit()`보다 cancel flag를 두고, 
* 반복문 안에서 해당 flag를 확인하는 cooperative cancellation 방식이 더 적절하다.

## wait()

`wait()` method는 대상 `QThread`가 종료될 때까지, `wait()`를 호출한 현재 thread를 기다리게 하는 method임.

```python
self.worker.wait()
```

* 인자 없이 호출하면 대상 thread가 종료될 때까지 계속 기다린다. 
* 특정 시간까지만 기다리도록 timeout (ms)을 줄 수도 있다.

```python
is_finished = self.worker.wait(1000)  # 최대 1000 ms 동안 종료를 기다림.
```

* 이 경우 `self.worker`가 1000 ms 안에 종료되면 `True`를 반환하고, 
* 1000 ms가 지났는데도 아직 실행 중이면 `False`를 반환한다.

즉, `wait(1000)`은 

* ***현재 thread를 1000 ms 동안 무조건 쉬게 하는 것*** 이 아니라, 
* ***대상 thread가 1000 ms 안에 종료되는지 기다리는 것*** 임. 
* 따라서 `time.sleep(1)`처럼 단순한 delay와는 의미가 다르다.

예를 들어 application 종료 시점에 worker thread가 완전히 종료된 뒤 다음 정리 작업을 수행해야 한다면 `wait()`를 사용할 수 있다.

주의할 점은 GUI thread에서 `wait()`를 호출하면 GUI thread의 event loop가 block 될 수 있다는 점임.

* 이 경우 GUI가 멈춘 것처럼 보일 수 있으므로, 
* GUI application에서는 thread 종료 처리를 signal-slot 기반으로 구성해야 함.

## terminate()

`terminate()` method는 ***thread를 강제로 종료하는 method임***.

하지만 이 방식은 일반적으로 권장되지 않는다. 

Thread가 어떤 시점에서 강제로 중단될지 알 수 없기 때문에 다음과 같은 문제가 발생할 수 있다.

* file이나 network resource가 정상적으로 닫히지 않을 수 있음.
* lock이 해제되지 않을 수 있음.
* shared data가 불완전한 상태로 남을 수 있음.
* object의 destructor나 cleanup code가 정상적으로 실행되지 않을 수 있음.

따라서 `terminate()`는 가능한 사용하지 않는 것이 좋다. 

Thread를 중단해야 한다면 cancel flag를 사용하여 worker가 스스로 안전하게 종료되도록 만드는 방식이 권장된다.

# QThread의 상태 확인 및 설정 methods

## isRunning()

`isRunning()` method는 thread가 현재 실행 중인지 여부를 반환한다.

```python
if not self.worker.isRunning():
    self.worker.start()
```

GUI에서 button을 여러 번 눌렀을 때 같은 thread가 중복 실행되는 것을 막기 위해 자주 사용된다.

## isFinished()

`isFinished()` method는 thread가 종료되었는지 여부를 반환한다.

Thread의 실행이 끝난 뒤 특정 처리를 해야 하는 경우 상태 확인용으로 사용할 수 있다.

## priority()와 setPriority()

`priority()` method는 thread의 현재 priority를 반환하고, `setPriority()` method는 thread의 priority를 설정한다.

```python
self.worker.setPriority(QThread.Priority.LowPriority)
```

Thread priority는 OS scheduler가 thread를 어떻게 다룰지에 영향을 줄 수 있다. 

* 다만 실제 동작은 OS와 platform에 따라 달라질 수 있으므로, 
* priority 설정만으로 성능이나 실행 순서를 정확히 제어할 수 있다고 가정하면 안 된다.

## stackSize()와 setStackSize()

`stackSize()` method는 thread가 함수 호출 정보, 지역 변수, 반환 주소 등을 저장하기 위해 사용하는 stack memory 영역의 크기를 반환하고,  
`setStackSize()` method는 thread stack size를 설정한다. 

> 여기서 stack이라는 이름은 함수가 호출될 때마다 실행 정보가 후입선출(LIFO, Last In First Out) 구조로 쌓였다가 함수 종료 시 역순으로 제거되는 memory 영역인 call stack에서 유래한 것이다.

일반적인 GUI application에서는 직접 조정할 일이 많지 않다. 하지만 recursion이 깊거나, 특정 platform에서 thread stack 크기 조정이 필요한 경우 사용할 수 있다.

# 예제 코드

아래 코드는 PySide6에서 `QThread`를 상속하여 background 작업을 수행하는 간단한 예제임.

이 예제에서는 worker thread에서 1초 간격으로 block되는 작업을 수행하고, 진행 상태를 signal을 통해 GUI thread로 전달한다. 

GUI thread는 전달받은 message를 이용하여 `QLabel`을 update한다.

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


class WorkerThread(QThread):
    # worker thread에서 GUI thread로 문자열 message를 전달하기 위한 signal.
    update_signal = Signal(str)

    def run(self):
        # 이 method는 start() 호출 후 새 thread 안에서 실행됨.
        # 직접 run()을 호출하면 새 thread가 생성되지 않으므로 주의해야 함.
        for i in range(5):
            time.sleep(1)
            self.update_signal.emit(f"Working {i + 1}")  # 진행 상태를 GUI thread로 전달.

        # 작업 완료 message를 GUI thread로 전달.
        self.update_signal.emit("Task completed!")


class MW(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QThread Example")

        self.init_ui()
        self.show()

    def init_ui(self):
        # GUI widget 생성.
        self.label = QLabel("Thread Example", self)
        self.button = QPushButton("Start Thread", self)

        # button click 시 worker thread 시작.
        self.button.clicked.connect(self.start_thread)

        # layout 설정.
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        # QThread를 상속한 worker thread 객체 생성.
        self.worker = WorkerThread()

        # worker thread에서 발생한 signal을 GUI thread의 slot에 연결.
        # update_label()은 GUI thread에서 호출되므로 QLabel을 안전하게 update할 수 있음.
        self.worker.update_signal.connect(self.update_label)

    def start_thread(self):
        # 이미 thread가 실행 중이면 다시 시작하지 않음.
        # QThread를 중복 실행하는 것을 방지하기 위한 처리임.
        if not self.worker.isRunning():
            self.worker.start()

    def update_label(self, message):
        # GUI widget은 GUI thread에서 update해야 함.
        # worker thread는 직접 QLabel을 수정하지 않고 signal만 emit함.
        self.label.setText(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    wnd = MW()

    sys.exit(app.exec())
```

# 참고: time.sleep()과 QThread.wait()의 차이

위 예제의 `time.sleep(1)`은 CPU 연산이 오래 걸리는 상황을 표현하는 code가 아님.

`time.sleep(1)`은 

* 현재 worker thread를 1초 동안 sleep 상태로 두어, 
* CPU를 점유하지 않은 채 해당 thread가 block되는 상황을 만든다. 
* 즉, file I/O 대기, network response 대기, database query 대기, 외부 process 응답 대기, 외부 장치 응답 대기처럼 
* CPU-bound가 아닌 blocking 작업을 단순화하여 표현한 것임.

`time.sleep()`과 `QThread.wait()`는 모두 호출한 thread를 block시킬 수 있지만, 기준과 목적이 다르다.

| 구분             | `time.sleep(seconds)`                             | `QThread.wait()` / `QThread.wait(milliseconds)` |
| -------------- | ------------------------------------------------- | ----------------------------------------------- |
| 기준             | 시간 경과                                             | 대상 thread의 종료                                   |
| 시간 인자의 의미      | 지정 시간 동안 현재 thread를 sleep 상태로 둠                   | 대상 thread가 지정 시간 안에 종료되는지 기다림                   |
| 호출 대상          | Python의 `time` module 함수                          | 특정 `QThread` instance의 method                   |
| block되는 thread | `time.sleep()`을 호출한 thread                        | `wait()`를 호출한 thread                            |
| 기다리는 대상        | 별도의 대상 없음                                         | 해당 `QThread`의 실행 종료                             |
| 반환값            | 없음                                                | 종료되면 `True`, timeout이면 `False`                  |
| 이 예제에서의 의미     | worker thread가 1초 동안 non-CPU-bound blocking 상태가 됨 | worker thread 종료를 기다리는 동기화 처리                   |

따라서 이 예제의 `time.sleep(1)`은 worker thread 안에서 호출되므로 worker thread만 block된다. 

반대로 GUI thread에서 `self.worker.wait()` 또는 `self.worker.wait(1000)`을 호출하면 GUI thread가 block되어 event loop가 멈출 수 있다.

핵심은 다음과 같음.

* `time.sleep(1)`은 현재 thread를 1초 동안 sleep 상태로 두는 것임.
* `QThread.wait(1000)`은 대상 thread가 1000 ms 안에 종료되는지 기다리는 것임.
* 둘 다 시간을 인자로 받을 수 있지만, `sleep`의 시간은 대기 시간 자체이고, `wait`의 시간은 종료 대기의 최대 허용 시간임.
* 이 예제의 목적은 CPU 연산의 병렬화가 아니라, CPU를 점유하지 않아도 오래 block될 수 있는 작업을 GUI thread 밖으로 분리했을 때 GUI 반응성이 유지됨을 보이는 것임.

# 코드 설명

## WorkerThread class

`WorkerThread`는 `QThread`를 상속한 class임.

```python
class WorkerThread(QThread):
    update_signal = Signal(str)
```

`update_signal`은 

* worker thread에서 GUI thread로 
* 문자열 message를 전달하기 위한 signal이다.

`run()` method 안에서는 background 작업을 수행한다.

```python
def run(self):
    for i in range(5):
        time.sleep(1)
        self.update_signal.emit(f"Working {i + 1}")

    self.update_signal.emit("Task completed!")
```

이 `run()` method는 직접 호출하지 않는다.

* `self.worker.start()`가 호출되면 Qt가 새로운 thread를 만들고, 
* 그 thread 안에서 `run()` method가 실행된다.

## MW class

`MW`는 GUI를 담당하는 main widget class임.

`QLabel`과 `QPushButton`을 만들고, button이 click되면 `start_thread()` method를 호출하도록 연결한다.

```python
self.button.clicked.connect(self.start_thread)
```

또한 `WorkerThread` instance를 만들고, worker thread의 `update_signal`을 `update_label()` slot에 연결한다.

```python
self.worker = WorkerThread()
self.worker.update_signal.connect(self.update_label)
```

이 연결 덕분에 worker thread에서 signal을 emit하면, GUI thread의 `update_label()` method가 호출된다.

## 작업 실행

`start_thread()` method는 thread가 이미 실행 중이 아닐 때만 `start()`를 호출한다.

```python
def start_thread(self):
    if not self.worker.isRunning():
        self.worker.start()
```

> 이는 같은 `QThread`를 중복 실행하는 것을 방지하기 위한 처리임.

## Signal and Slot

이 예제에서 가장 중요한 구조는 ***worker thread가 GUI widget을 직접 수정하지 않는다는 점*** 이다.

Worker thread는 다음과 같이 signal만 emit한다.

```python
self.update_signal.emit(f"Working {i + 1}")
```

GUI update는 main thread의 slot에서 수행된다.

```python
def update_label(self, message):
    self.label.setText(message)
```

이 방식은 PySide와 PyQt에서 multithreading을 사용할 때 매우 중요한 기본 패턴임. 

> GUI widget은 GUI thread에서만 안전하게 수정해야 하며,  
> worker thread와 GUI thread 사이의 통신은 signal-slot mechanism을 사용하는 것이 권장된다.

# 정리

`QThread`는 PySide와 PyQt에서 background 작업을 별도 thread로 분리할 때 사용할 수 있는 class임.

가장 기본적인 사용 방식은 `QThread`를 상속하고 `run()` method를 override한 뒤, `start()`를 호출하여 별도 thread에서 작업을 수행하는 것이다.

다만 GUI widget을 worker thread에서 직접 수정하면 안 되므로, worker thread는 signal을 emit하고 GUI thread의 slot에서 widget을 update해야 한다.

이 예제는 `QThread`의 가장 단순한 사용법을 보여준다. 

> 이후 더 복잡한 구조에서는 `QObject` 기반 worker를 만들고 `moveToThread()`를 사용하는 방식도 함께 고려할 수 있다.
