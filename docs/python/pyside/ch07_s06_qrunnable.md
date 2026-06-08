---
title: QRunnable과 QThreadPool
tags: [PySide6, Qt, QRunnable, QThreadPool, QThread, moveToThread, Thread, Signal, Slot]
---

# QRunnable과 QThreadPool

`QRunnable`과 `QThreadPool`은 Qt 프레임워크에서 제공하는 클래스로,

* 멀티스레딩 작업을 효율적으로 관리하기 위해 사용됨.
* 이들은 `QThread`와는 다르게 동작하며, 특히 작업을 기반으로 한 스레딩 모델에 초점을 맞춤.

`QRunnable`과 `QThreadPool`을 사용하는 방식은 특히 많은 수의 독립적인 작업을 관리해야 할 때 `QThread`를 직접 사용하는 것보다 효율적임.

* `QThreadPool`을 사용하면 thread의 생성 및 관리를 직접 처리하지 않아도 됨.
* thread pool 내부의 thread를 재사용하므로, thread 생성 및 파괴에 따른 오버헤드를 상대적으로 줄일 수 있음.

---

---

## QRunnable

`QRunnable`은 일종의 작업을 추상화한 가벼운 클래스라고 할 수 있음.

주의할 점은 `QRunnable`이 `Thread`를 추상화한 class가 아니라는 점임.

* `QRunnable`은 thread 자체가 아니라, thread에서 수행될 작업 단위를 나타냄.
* 이 클래스를 상속받아 사용자 정의 작업을 구현할 수 있음.
* 이는 `QRunnable`을 상속한 후 `run()` method를 override하여 이루어짐.
* 해당 `run()` method가 실제 수행할 작업에 해당함.

중요한 점은 `QRunnable` 자체는 thread를 생성하거나 관리하지 않는다는 점임.

대신 `QThreadPool`이 `QRunnable`을 실제 실행할 thread들을 관리함.

따라서 `QRunnable`을 background thread에서 실행하려면 일반적으로 `QThreadPool.start()`를 통해 실행해야 함.

단, `run()` method를 직접 호출하는 것도 문법적으로는 가능함. 하지만 이 경우 thread pool을 사용하는 것이 아니라, 현재 thread에서 일반 method를 호출하는 것에 불과함.

즉, `QRunnable`을 멀티스레딩 작업으로 사용하려면 `QThreadPool`을 통해 실행해야 함.

이는 여러 thread로 동작해야 하는 작업을 효과적으로 thread pool에 분산 수행시키는 경우에 유리함.

추가적으로 주의할 점은 `QRunnable` 이 `QObject`의 subclass가 아님.

> signal과 slot을 포함할 수 있는 class는 QObject 또는 그 subclass 이기 때문에, `Signal` 객체를 class attribute로 가질 수 없음.

### 주요 method

#### run()

`run()` method는 작업이 실행될 로직을 포함함.

* 실제 수행할 작업을 구현함.
* `QRunnable`이 `QThreadPool`에 의해 실행될 때 호출됨.
* 이 method는 `QThreadPool` 내부의 worker thread에서 실행됨.
* 따라서 `run()` 내부에서 GUI widget을 직접 수정하면 안 됨.
* GUI 갱신은 signal-slot을 통해 main thread에서 수행되도록 해야 함.

#### autoDelete()

`autoDelete()`는 작업 완료 후 `QRunnable` 객체가 자동 삭제되는지 여부를 반환함.

* 기본값은 `True`임.
* 기본 설정에서는 `QThreadPool`이 `run()` 수행 후 해당 `QRunnable` 객체를 자동으로 삭제함.
* 따라서 일반적으로 `QRunnable` 객체는 1회성 작업 객체로 취급해야함.

#### setAutoDelete(bool autoDelete)

`setAutoDelete()`는 `autoDelete` 속성을 설정함.

* 작업 완료 후 객체가 자동 삭제되어야 하는지 여부를 결정함.
* `False`로 설정하면 작업 완료 후 자동 삭제되지 않음.
* 이 경우 객체의 생명주기 관리는 프로그래머가 직접 신경써야 함.

---

---

## QThreadPool

`QThreadPool`은 thread pool을 추상화한 클래스로, thread pool 작업을 조정 및 관리함.

이 클래스를 사용하면 thread 생성과 관리의 복잡성을 줄이고, 작업을 효율적으로 스케줄링할 수 있음.

`QThreadPool`은 내부적으로 여러 thread를 관리하고, queue에 추가된 `QRunnable` 객체들을 사용 가능한 thread에 배정하여 실행함.

> 생성 및 관리를 thread pool에 맡기기 때문에 개발자가 관리하기 힘든 수준의 많은 작업을 실행할 때 유리한 방식임.
> 반면, 소수의 thread에 대해 정교한 실행 cycle 관리가 필요한 경우에는 `QThread`를 직접 사용하는 방식이 더 적절할 수 있음.

`QThreadPool`은 지정된 수의 thread를 사용하여 queue에 추가된 `QRunnable` 객체들을 실행함.

각 Qt application에는 global thread pool이 존재하며, `QThreadPool.globalInstance()`를 통해 접근할 수 있음.

### 주요 method

#### start(QRunnable runnable, int priority=0)

`start()` method는 `QRunnable` 객체를 pool에 추가하고, 관리 중인 thread를 통해 실행시킴.

* 선택적 `priority` 매개변수를 통해 작업의 우선순위를 설정할 수 있음.
* 높은 우선순위의 작업이 대기 queue에서 먼저 수행될 수 있음.
* 현재 active thread 수가 `maxThreadCount()`에 도달한 경우, 인자로 넘겨진 `QRunnable` 객체는 대기 queue에 추가됨.
* 사용 가능한 thread가 생기면 대기 중인 작업의 `run()` method가 실행됨.

#### maxThreadCount()

`maxThreadCount()`는 pool에서 동시에 실행할 수 있는 최대 thread 수를 반환함.

#### setMaxThreadCount(int maxThreadCount)

`setMaxThreadCount()`는 pool에서 동시에 실행할 수 있는 thread의 최대 수를 설정함.

예를 들어 최대 thread 수를 2로 설정하면, 동시에 실행되는 작업은 최대 2개로 제한됨. 나머지 작업은 queue에서 대기함.

#### waitForDone(int msecs=-1)

`waitForDone()`은 pool에 있는 모든 작업이 완료될 때까지 대기함.

* 선택적 `msecs` 매개변수를 통해 최대 대기 시간(ms)을 설정할 수 있음.
* 기본값 `-1`은 무한 대기를 의미함.
* GUI thread에서 호출하면 event loop가 막혀 화면이 멈출 수 있으므로 주의해야 함.

#### activeThreadCount()

`activeThreadCount()`는 현재 활성 thread 수를 반환함.

여기서 활성 thread는 현재 작업을 실행 중인 thread를 의미함.

#### tryStart(QRunnable runnable)

`tryStart()`는 실행 중인 thread 수가 `maxThreadCount()`보다 작은 경우에만 인자로 넘겨진 `QRunnable` 작업을 시작함.

* 즉시 실행 가능한 thread가 있으면 작업을 시작하고 `True`를 반환함.
* **즉시 실행 가능한 thread가 없으면 작업을 queue에 추가하지 않고 `False`를 반환함**.
* 대기 queue에 넣지 않고, 즉시 수행 가능한 경우에만 작업을 실행하려고 할 때 사용함.

#### clear()

`clear()`는 아직 시작되지 않고 대기 queue에 있는 작업들을 제거함.

* 이미 실행 중인 작업은 영향을 받지 않음.
* 이미 `run()` method가 시작된 작업은 중단되지 않음.
* 실행 중인 작업을 중단하려면 별도의 cancel flag를 두고 `run()` 내부에서 확인하는 cooperative cancellation 방식이 필요함.

---

---


## 참고 - QThread 상속 방식, moveToThread 방식, QRunnable/QThreadPool 방식 비교

Qt에서 background 작업을 수행하는 대표적인 방식은 크게 다음 3가지로 구분할 수 있음.

* `QThread`를 상속받아 `run()`을 override하는 방식
* `QObject` 기반 worker를 만들고 `moveToThread()`로 옮기는 방식
* `QRunnable`과 `QThreadPool`을 사용하는 방식

세 방식 모두 background thread를 활용할 수 있지만, 설계 관점은 서로 다름.

| 방식                             | 핵심 개념                                                             | 적합한 경우                                             | 장점                             | 단점                                             |
| ------------------------------ | ----------------------------------------------------------------- | -------------------------------------------------- | ------------------------------ | ---------------------------------------------- |
| `QThread` 상속 방식                | `QThread`를 상속하고 `run()` method를 override하여 thread에서 수행할 작업을 직접 작성 | 단순한 background 작업을 별도 thread에서 한 번 수행하는 경우         | 구조가 직관적이고 코드가 짧음               | thread 자체와 작업 logic이 한 class에 섞이기 쉬움           |
| `moveToThread()` 방식            | 작업을 수행할 `QObject` worker를 만들고, 해당 객체를 별도 `QThread`로 이동            | 오래 살아 있는 worker 객체가 signal-slot으로 계속 명령을 받아야 하는 경우 | thread와 worker logic을 분리할 수 있음 | 구조가 상대적으로 복잡하고 signal-slot 연결, 종료 처리 등을 신경써야 함 |
| `QRunnable` + `QThreadPool` 방식 | 개별 작업을 `QRunnable`로 만들고, `QThreadPool`이 해당 작업들을 thread pool에 배정   | 많은 수의 독립적인 작업을 반복적으로 실행하는 경우                       | thread 재사용으로 생성/파괴 비용을 줄일 수 있음 | 개별 작업의 정교한 lifecycle 관리에는 부적합함                 |

### QThread 상속 방식

`QThread`를 상속하는 방식은 `QThread` class를 직접 상속하고, `run()` method 안에 background 작업을 작성하는 방식임.

```python
class WorkerThread(QThread):
    def run(self):
        # background thread에서 수행할 작업
        ...
```

이 방식은 단순한 작업을 별도 thread에서 수행할 때 이해하기 쉬움.

하지만 작업 logic이 `QThread` class 내부에 들어가기 때문에, thread 자체와 worker logic이 강하게 결합되는 문제가 생길 수 있음.

즉, 다음 두 개념이 하나의 class에 섞이기 쉬움.

* thread의 실행 단위
* 실제 수행할 작업 logic

따라서 단순 예제에서는 편하지만, 복잡한 프로그램에서는 유지보수성이 떨어질 수 있음.

### moveToThread 방식

`moveToThread()` 방식은 실제 작업을 수행하는 객체를 `QObject` 기반 worker로 만들고, 해당 worker 객체를 별도의 `QThread`로 이동시키는 방식임.

```python
worker = Worker()
thread = QThread()

worker.moveToThread(thread)
thread.start()
```

이 방식에서는 `QThread`가 thread의 event loop를 담당하고, 실제 작업은 worker 객체의 slot에서 수행됨.

따라서 thread 관리와 작업 logic을 분리할 수 있음.

이 방식은 다음과 같은 경우에 적합함.

* worker 객체가 오래 살아 있어야 하는 경우
* signal-slot을 통해 worker에게 여러 번 명령을 보내야 하는 경우
* thread 내부에서 event loop가 필요한 경우
* 작업 시작, 중단, 재시작, 종료 흐름을 비교적 정교하게 관리해야 하는 경우

다만 구조가 상대적으로 복잡함.

특히 다음 처리를 명확히 해야 함.

* `thread.started`와 worker slot 연결
* worker 종료 signal 처리
* `thread.quit()` 호출
* `thread.wait()` 호출
* worker 객체와 thread 객체의 `deleteLater()` 처리

따라서 단발성 작업이 많을 때는 다소 과한 구조가 될 수 있음.

### QRunnable + QThreadPool 방식

`QRunnable`과 `QThreadPool` 방식은 thread 자체가 아니라 작업 단위에 집중하는 방식임.

```python
task = Task()
pool.start(task)
```

이 방식에서는 사용자가 thread를 직접 만들거나 종료하지 않음.

* 작업은 `QRunnable`로 정의함.
* 실행은 `QThreadPool`에 맡김.
* `QThreadPool`은 내부 thread를 재사용함.
* 사용 가능한 thread가 없으면 작업은 queue에서 대기함.

따라서 다음과 같은 경우에 적합함.

* 독립적인 작업이 많음
* 각 작업이 비교적 짧거나 단발성임
* thread를 직접 생성하고 제거하는 비용을 줄이고 싶음
* 동시에 실행할 작업 수를 제한하고 싶음

반면 다음과 같은 경우에는 적합하지 않을 수 있음.

* 특정 worker 객체가 계속 살아 있어야 함
* 하나의 thread에 지속적으로 명령을 보내야 함
* 작업의 중단, 재시작, 상태 관리를 세밀하게 해야 함
* thread 내부 event loop를 적극적으로 사용해야 함

이런 경우에는 `QObject` worker와 `moveToThread()` 조합이 더 적절할 수 있음.

### 선택 기준

세 방식을 간단히 정리하면 다음과 같음.

| 목적                                     | 적절한 방식                                 |
| -------------------------------------- | -------------------------------------- |
| 단순한 background 작업을 하나의 thread에서 수행     | `QThread` 상속 방식                        |
| 오래 살아 있는 worker 객체를 별도 thread에서 운용     | `QObject` worker + `moveToThread()` 방식 |
| 많은 수의 독립 작업을 thread pool에 분산 실행        | `QRunnable` + `QThreadPool` 방식         |
| thread lifecycle을 직접 제어해야 함            | `QThread` 또는 `moveToThread()` 방식       |
| thread 생성/파괴 비용을 줄이고 싶음                | `QRunnable` + `QThreadPool` 방식         |
| signal-slot 기반으로 worker에게 반복 명령을 보내야 함 | `moveToThread()` 방식                    |

즉, `QRunnable`과 `QThreadPool`은 thread 자체를 소유하고 제어하려는 방식이 아니라, 작업을 thread pool에 던지고 실행을 맡기는 방식임.

따라서 많은 독립 작업을 처리할 때는 적합하지만, 특정 thread나 worker 객체의 생명주기를 정교하게 제어해야 하는 경우에는 `QThread` 기반 방식이 더 적절함.

---

---


## 예제 코드: QRunnable과 QThreadPool 사용

아래는 `QRunnable`, `QThreadPool`, `Signal`, `Slot`을 사용하여 여러 작업을 동시에 실행하고, 각 작업의 진행 상태를 `QLabel`을 통해 업데이트하는 PySide6 기반 예제 코드임.

중요한 점은 `QRunnable`에서 GUI widget을 직접 수정하지 않는다는 점임.

* background thread에서는 signal만 emit함.
* 실제 `QLabel` 수정은 main thread의 slot에서 수행됨.

또한 `QRunnable`은 `QObject`을 상속하지 않으므로, signal을 직접 class attribute로 선언하는 구조는 적절하지 않음.

따라서 아래 예제에서는 `TaskSignals`라는 `QObject` 기반 class를 따로 두고, 이 객체가 signal을 담당하도록 구성함.

### 예제 코드

```python
import sys
import time

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget


class TaskSignals(QObject):
    # QRunnable은 QObject가 아니므로 Signal을 직접 선언하지 않음.
    # 대신 QObject를 상속한 별도 class에서 signal을 선언함.
    update_signal = Signal(str, int)


class Task(QRunnable):
    def __init__(self, num):
        super().__init__()

        # num은 label index로도 사용하므로 0부터 시작함.
        self.num = num

        # 작업 진행 상태를 main thread로 전달하기 위한 signal 객체.
        self.signals = TaskSignals()

    def run(self):
        # 이 method는 QThreadPool 내부의 worker thread에서 실행됨.
        # 따라서 이 안에서 QLabel 같은 GUI widget을 직접 수정하면 안 됨.
        for i in range(101):
            time.sleep(0.1)  # 작업을 모방하기 위한 시간 지연

            # GUI 갱신 요청은 signal을 통해 main thread로 전달함.
            # num은 0부터 시작하지만, 사용자에게 보여줄 때는 1부터 표시함.
            self.signals.update_signal.emit(
                f"Task {self.num + 1}: {i}% completed",
                self.num
            )

        # 작업 완료 메시지 전송.
        self.signals.update_signal.emit(
            f"Task {self.num + 1}: Task completed!",
            self.num
        )


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        # QRunnable은 thread 자체가 아니라 task이므로,
        # 화면 표시도 Thread가 아니라 Task로 표현함.
        self.labels = [
            QLabel(f"Task {i + 1}: Waiting to start...", self)
            for i in range(3)
        ]

        for label in self.labels:
            self.layout.addWidget(label)

        self.start_button = QPushButton("Start All Tasks", self)
        self.start_button.clicked.connect(self.start_tasks)
        self.layout.addWidget(self.start_button)

        # Qt application 전체에서 공유되는 global thread pool 사용.
        self.pool = QThreadPool.globalInstance()

    @Slot()
    def start_tasks(self):
        # 버튼을 여러 번 눌러 동일한 작업들이 중복 등록되는 것을 막음.
        self.start_button.setEnabled(False)

        for i in range(3):
            # 각 작업마다 QRunnable 객체를 새로 생성함.
            # 기본 autoDelete=True이므로 작업 완료 후 QThreadPool이 객체를 정리함.
            task = Task(i)

            # 작업을 시작하기 전에 signal-slot connection을 먼저 수행해야 함.
            # start() 이후에 connect하면 작업이 먼저 signal을 emit할 수 있음.
            task.signals.update_signal.connect(self.update_label)

            # QRunnable 작업을 thread pool에 추가함.
            # 실제 run()은 QThreadPool 내부 worker thread에서 실행됨.
            self.pool.start(task)

    @Slot(str, int)
    def update_label(self, message, idx):
        # 이 slot은 main thread에서 실행되므로 GUI widget 수정 가능.
        self.labels[idx].setText(message)

        # 모든 task가 완료되면 버튼을 다시 활성화함.
        if all(label.text().endswith("Task completed!") for label in self.labels):
            self.start_button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec())
```

---

---

## 코드 설명

### TaskSignals class

`TaskSignals` class는 `QObject`을 상속받아 signal을 제공하는 class임.

```python
class TaskSignals(QObject):
    update_signal = Signal(str, int)
```

`QRunnable`은 `QObject`이 아님.

따라서 

* `QRunnable` 안에 
* 직접 `Signal`을 class attribute로 선언하는 방식은 적절하지 않음.

이 예제에서는 `TaskSignals` 객체를 따로 두고, `Task`가 해당 객체를 통해 signal을 emit하도록 구성함.

### Task class

`Task` class는 `QRunnable`을 상속받아 정의됨.

각 `Task` instance는 다음을 가짐.

* 고유 번호 `num`
* 진행 상태를 전달하기 위한 `signals`

```python
class Task(QRunnable):
    def __init__(self, num):
        super().__init__()
        self.num = num
        self.signals = TaskSignals()
```

`run()` method에서는 0부터 100까지의 진행 상태를 0.1초 간격으로 업데이트하고, 각 단계마다 main window에 상태를 보고함.

단, 여기서 직접 `QLabel`을 수정하는 것이 아니라, signal을 emit함.

```python
self.signals.update_signal.emit(
    f"Task {self.num + 1}: {i}% completed",
    self.num
)
```

이 signal은 `MainWindow.update_label()` slot에 연결되어 main thread에서 처리됨.

### MainWindow class

`MainWindow` class는 application의 UI 구성을 담당함.

* 여러 개의 `QLabel`로 각 task의 상태를 표시함.
* 시작 button을 제공함.
* `QThreadPool.globalInstance()`를 통해 global thread pool을 사용함.

```python
self.pool = QThreadPool.globalInstance()
```

`start_tasks()` slot은 시작 button이 클릭될 때 호출되며, 3개의 `Task` 객체를 생성하여 thread pool에 추가함.

```python
task = Task(i)
task.signals.update_signal.connect(self.update_label)
self.pool.start(task)
```

여기서 중요한 점은 signal-slot connection을 `self.pool.start(task)`보다 먼저 수행한다는 점임.

작업을 먼저 시작한 뒤 signal을 연결하면, 작업이 빠르게 signal을 emit하는 경우 일부 signal을 놓칠 수 있음.

### update_label() slot

`update_label()` slot은 task에서 전달한 message와 index를 받아 해당 label을 수정함.

```python
@Slot(str, int)
def update_label(self, message, idx):
    self.labels[idx].setText(message)
```

이 slot은 GUI thread에서 실행되므로 `QLabel`을 안전하게 수정할 수 있음.

작업이 모두 완료되면 시작 button을 다시 활성화함.

```python
if all(label.text().endswith("Task completed!") for label in self.labels):
    self.start_button.setEnabled(True)
```

---

---

## 참고 - @Slot() decorator

`@Slot()` decorator는 PySide6에서 해당 method가 Qt slot으로 사용됨을 명시적으로 나타냄.

```python
@Slot()
def start_tasks(self):
    ...
```

```python
@Slot(str, int)
def update_label(self, message, idx):
    ...
```

`@Slot()` decorator는 필수는 아니지만, signal과 연결되는 method에 붙이는 것이 권장됨.

사용 시 다음과 같은 장점이 있음.

* 해당 method가 slot으로 사용됨을 코드상에서 명확히 표현할 수 있음.
* signal-slot connection 시 필요한 metadata를 명확히 제공할 수 있음.
* `@Slot(str, int)`처럼 인자 signature를 명시하여 signal과 slot의 연결 의도를 분명히 할 수 있음.
* thread 간 signal-slot 연결을 다루는 경우, slot의 소속 thread와 queued connection 처리 의도를 더 명확히 할 수 있음.

PySide6의 `@Slot()`은 C++ Qt의 `slots` / `Q_SLOTS` 같은 확장 macro와 keyword와 유사하게, 해당 Python method를 Qt slot으로 명시적으로 등록하는 역할을 함.

> 이는 C++ Qt의 MOC 최적화라고 볼 수도 있으나, 아주 엄밀하게는 차이가 있음:
> 
> * MOC는 C++ Qt에서 사용하는 Meta-Object Compiler임. 
> * C++ Qt의 `slots` / `Q_SLOTS`는 moc가 처리하여 meta-object code를 생성. 
> * 반면, PySide6의 @Slot()은 Python binding layer를 통해 Qt meta-object system에 slot metadata를 등록하는 방식임.
> PySide6의 @Slot()을 "C++ Qt의 MOC 최적화"라고 직접 표현하는 것은 자제하는 것이 좋음.

따라서 다음처럼 설명하는 것이 더 정확함.

> PySide6에서 `@Slot()`은 Python method를 Qt slot으로 명시적으로 등록하는 역할을 하며, signal-slot connection의 의도를 명확히 하고 runtime overhead를 줄이는 데 도움이 됨.

---

---

## 정리

`QRunnable`과 `QThreadPool`은 thread 자체를 직접 다루기보다, 작업을 thread pool에 맡기는 방식임.

다음과 같이 구분할 수 있음.

* `QThread`: thread 자체의 생성, 실행, 종료 cycle을 명시적으로 다루는 방식
* `QRunnable`: thread에서 수행할 작업 단위를 표현하는 방식
* `QThreadPool`: 여러 `QRunnable` 작업을 재사용 가능한 thread들에 분배하는 방식

많은 독립 작업을 효율적으로 처리할 때는 `QRunnable`과 `QThreadPool`이 적합함.

반면 특정 worker object가 오래 살아 있으면서 signal-slot으로 계속 명령을 받아야 하는 구조라면 `QObject` worker와 `QThread` 조합이 더 적절함.
