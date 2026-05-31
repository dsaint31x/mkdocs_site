---
title: QThread의 wait와 GUI Thread Blocking
tags: [GUI, Qt, PySide6, PyQt, Thread, Multithreading, QThread, Signal, Slot, Event Loop, wait]
---

# QThread의 wait와 GUI Thread Blocking

앞서 `QThread`의 기본 사용법을 살펴보았다. 이번 절에서는 여러 개의 `QThread`를 동시에 실행하고, 이들이 모두 종료될 때까지 기다리는 경우를 살펴본다.

이 예제의 핵심은 `QThread.wait()`를 어디서 호출하느냐에 따라 GUI application의 반응성이 크게 달라진다는 점임.

`QThread.wait()`는 대상 thread가 종료될 때까지, 이를 호출한 현재 thread를 block시키는 method이다. 따라서 GUI thread에서 `wait()`를 호출하면 GUI thread의 event loop가 멈추고, 그동안 GUI는 사용자 입력이나 화면 갱신에 반응하지 못한다.

# wait()의 동작 방식

`QThread.wait()`는 대상 `QThread`의 실행이 끝날 때까지, `wait()`를 호출한 thread를 block시키는 method임.

여기서 중요한 점은 `wait()`가 block시키는 대상이 “기다림의 대상 thread”가 아니라, “`wait()`를 호출한 현재 thread”라는 점이다.

예를 들어 다음과 같이 호출하면,

```python
self.worker.wait()
```

`self.worker`가 block되는 것이 아니다. `self.worker`가 종료될 때까지, 이 코드를 실행한 현재 thread가 block된다.

GUI button의 slot 안에서 위 코드를 호출했다면, 현재 thread는 보통 GUI thread이다. 따라서 GUI thread가 block되고, 그동안 Qt event loop는 사용자 입력, repaint event, timer event 등을 처리하지 못한다. 이 경우 application은 실제로는 worker thread에서 작업 중이더라도, 사용자 입장에서는 멈춘 것처럼 보일 수 있다.

`wait()`는 인자로 timeout을 받을 수도 있다.

```python
is_finished = self.worker.wait(1000)
```

이 코드는 현재 thread를 최대 1000 ms 동안 block하면서, `self.worker`가 그 안에 종료되는지 기다린다. 1000 ms 안에 종료되면 `True`를 반환하고, 시간이 지났는데도 아직 실행 중이면 `False`를 반환한다.

즉, `wait(1000)`은 “현재 thread를 1000 ms 동안 무조건 쉬게 하는 method”가 아니다. 정확히는 “대상 thread가 1000 ms 안에 종료되는지 기다리는 method”임.

이 점에서 `time.sleep()`과 의미가 다르다.

| 구분             | `time.sleep(seconds)`                                  | `QThread.wait(milliseconds)`   |
| -------------- | ------------------------------------------------------ | ------------------------------ |
| 기준             | 시간 경과                                                  | 대상 thread의 종료                  |
| 시간 인자의 의미      | 현재 thread를 지정 시간 동안 sleep 상태로 둠                        | 대상 thread가 지정 시간 안에 종료되는지 기다림  |
| 기다리는 대상        | 없음                                                     | 특정 `QThread`의 종료               |
| block되는 thread | `sleep()`을 호출한 thread                                  | `wait()`를 호출한 thread           |
| 반환값            | 없음                                                     | 종료되면 `True`, timeout이면 `False` |
| 주 용도           | delay, polling interval, non-CPU-bound blocking 상황 단순화 | thread 종료 동기화                  |

따라서 `wait()`는 thread 종료 시점을 동기화해야 할 때 사용할 수 있다. 예를 들어 application 종료 직전에 worker thread가 완전히 끝난 뒤 resource를 정리해야 하는 경우에는 `wait()`가 필요할 수 있다.

하지만 GUI thread에서 `wait()`를 직접 호출하는 것은 신중해야 한다. GUI thread가 block되면 event loop가 멈추므로, GUI가 응답하지 않는 상태가 될 수 있기 때문이다.

정리하면 다음과 같음.

* `wait()`는 대상 thread를 멈추는 method가 아님.
* `wait()`는 대상 thread가 끝날 때까지 현재 thread를 기다리게 하는 method임.
* `wait()`를 GUI thread에서 호출하면 GUI event loop가 block될 수 있음.
* `wait(timeout)`은 timeout 시간 동안 무조건 쉬는 것이 아니라, 대상 thread의 종료를 timeout 안에서 기다리는 것임.
* GUI application에서는 가능하면 `finished` signal이나 별도 monitor thread 등을 이용하여 GUI thread가 직접 `wait()`하지 않도록 구성하는 것이 좋음.

이어지는 Example 0은 일부러 GUI thread에서 `wait()`를 호출하여 GUI가 block되는 구조를 보여준다. 반면 Example 1은 별도의 `MonitorThread`에서 `wait()`를 호출하도록 하여, GUI thread의 event loop가 계속 동작할 수 있게 만든 구조이다.

# Example 0: GUI Thread에서 wait()를 호출하는 경우

아래 코드는 PySide6를 사용하여 여러 worker thread를 실행하고, 모든 thread가 종료될 때까지 기다리는 GUI application의 예제임.

이 예제에서는 "Start All Threads" button을 누르면 모든 worker thread가 시작되고, 각 thread의 진행 상태가 각각의 progress bar에 반영된다.

* 다만 모든 thread를 시작한 직후 GUI thread에서 `wait_for_threads_to_finish()` method를 호출한다. 
* 이 method 내부에서는 각 worker thread에 대해 `wait()`를 호출하므로, 모든 worker thread가 종료될 때까지 GUI thread가 block된다.

따라서 이 예제는 `wait()`의 문제점을 보여주기 위한 예제이다.  
GUI application 구조로는 권장되지 않는다.

## 작동 방식

1. 사용자가 "Start All Threads" button을 클릭함.
2. 모든 worker thread가 시작됨.
3. 모든 worker thread가 시작된 직후, GUI thread에서 `wait_for_threads_to_finish()`가 호출됨.
4. `wait_for_threads_to_finish()`는 모든 worker thread가 종료될 때까지 `wait()`를 호출함.
5. 이 동안 GUI thread의 event loop가 block되므로, GUI가 응답하지 않는 상태가 될 수 있음.
6. 모든 worker thread가 종료되면 status label이 `"All threads completed!"`로 update됨.
7. 이후 GUI thread가 다시 event loop를 처리할 수 있게 됨.

## 코드

```python
import sys
import time

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class WorkerThread(QThread):
    # 진행 상태를 int 값으로 전달하기 위한 signal.
    update_signal = Signal(int)

    def __init__(self, thread_id):
        super().__init__()
        self.thread_id = thread_id

    def run(self):
        # start() 호출 후 새 worker thread 안에서 실행됨.
        for i in range(101):
            time.sleep(0.1)
            self.update_signal.emit(i)


class MW(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QThread wait() Blocking Example")

        self.init_ui()
        self.show()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        self.status_label = QLabel("Click 'Start All Threads' to run the threads", self)
        self.layout.addWidget(self.status_label)

        self.start_all_button = QPushButton("Start All Threads", self)
        self.start_all_button.clicked.connect(self.start_all_threads)
        self.layout.addWidget(self.start_all_button)

        self.progress_bars = []
        self.threads = []
        self.buttons = []

        for i in range(3):
            label = QLabel(f"Thread {i + 1} Example", self)

            progress_bar = QProgressBar(self)
            progress_bar.setRange(0, 100)

            button = QPushButton(f"Start Thread {i + 1}", self)
            button.clicked.connect(self.make_start_thread(i))

            self.layout.addWidget(label)
            self.layout.addWidget(progress_bar)
            self.layout.addWidget(button)

            worker = WorkerThread(i)
            worker.update_signal.connect(progress_bar.setValue)

            self.progress_bars.append(progress_bar)
            self.threads.append(worker)
            self.buttons.append(button)

    def make_start_thread(self, index):
        def start_thread():
            if not self.threads[index].isRunning():
                self.threads[index].start()

        return start_thread

    def start_all_threads(self):
        self.status_label.setText("Threads are running...")

        for thread in self.threads:
            if not thread.isRunning():
                thread.start()

        # 주의:
        # 이 method는 GUI thread에서 호출됨.
        # 따라서 내부에서 wait()를 호출하면 GUI thread가 block됨.
        self.wait_for_threads_to_finish()

    def wait_for_threads_to_finish(self):
        for thread in self.threads:
            # 대상 worker thread가 종료될 때까지 현재 thread를 block함.
            # 현재 thread가 GUI thread이므로 GUI event loop가 멈출 수 있음.
            thread.wait()

        self.status_label.setText("All threads completed!")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    wnd = MW()

    sys.exit(app.exec())
```

## 코드 설명

### WorkerThread class

`WorkerThread`는 `QThread`를 상속받아 구현한 worker thread class임.

```python
class WorkerThread(QThread):
    update_signal = Signal(int)
```

`update_signal`은 worker thread에서 progress value를 GUI thread로 전달하기 위한 signal이다.

`run()` method에서는 0부터 100까지 값을 증가시키며, 각 단계에서 `update_signal`을 emit한다.

```python
def run(self):
    for i in range(101):
        time.sleep(0.1)
        self.update_signal.emit(i)
```

여기서 `time.sleep(0.1)`은 CPU-bound 연산을 의미하지 않는다. 

* CPU를 점유하지 않은 채 
* worker thread가 일정 시간 block되는 상황을 단순화하여 표현한 것임.

### MW class

`MW` class는 GUI의 주요 widget을 구성한다.

각 worker thread마다 다음 widget과 객체를 생성한다.

* `QLabel`
* `QProgressBar`
* 개별 thread 시작 button
* `WorkerThread` instance

각 worker thread의 `update_signal`은 해당 progress bar의 `setValue()` slot에 연결된다.

```python
worker.update_signal.connect(progress_bar.setValue)
```

따라서 worker thread에서 signal을 emit하면, GUI thread에서 progress bar가 update된다.

### start_all_threads()

`start_all_threads()` method는 모든 worker thread를 시작한다.

```python
def start_all_threads(self):
    self.status_label.setText("Threads are running...")

    for thread in self.threads:
        if not thread.isRunning():
            thread.start()

    self.wait_for_threads_to_finish()
```

문제는 그 다음에 GUI thread에서 곧바로 `wait_for_threads_to_finish()`를 호출한다는 점이다.

### wait_for_threads_to_finish()

`wait_for_threads_to_finish()` method는 모든 worker thread에 대해 `wait()`를 호출한다.

```python
def wait_for_threads_to_finish(self):
    for thread in self.threads:
        thread.wait()

    self.status_label.setText("All threads completed!")
```

`QThread.wait()`는 대상 thread가 종료될 때까지 현재 thread를 block한다. 여기서 현재 thread는 GUI thread이므로, 모든 worker thread가 끝날 때까지 GUI thread의 event loop가 멈춘다.

즉, 이 예제는 `wait()`의 동작을 이해하기에는 좋지만, GUI application 구조로는 권장되지 않는다.

# Example 1: MonitorThread를 이용하여 GUI Blocking 줄이기

앞선 Example 0의 문제는 GUI thread에서 직접 `wait()`를 호출한다는 점이다.

이를 개선하기 위해 별도의 `MonitorThread`를 만들고, 이 monitor thread가 worker thread들의 종료를 기다리도록 할 수 있다.

이 경우 `wait()`는 GUI thread가 아니라 monitor thread 안에서 호출된다. 따라서 worker thread들이 종료될 때까지 기다리는 동안에도 GUI thread의 event loop는 계속 동작할 수 있다.

아래 코드는 Example 0보다 더 안전하게 구성한 버전이다.

* 실행할 때마다 새로운 `WorkerThread` instance를 생성함.
* 이미 실행 중인 worker thread는 중복 실행하지 않음.
* `MonitorThread`가 이미 실행 중이면 중복 생성하지 않음.
* `MonitorThread` 완료 후 reference를 정리함.
* 실행 중인 thread가 있는 동안에는 main window를 닫지 못하도록 하여, 실행 중인 `QThread` object가 파괴되는 상황을 방지함.

## 작동 방식

1. 사용자가 "Start All Threads" button을 클릭함.
2. 실행 중이 아닌 worker thread들을 새로 생성하고 시작함.
3. `MonitorThread`가 시작됨.
4. `MonitorThread`는 각 worker thread에 대해 `wait()`를 호출함.
5. 이때 block되는 것은 GUI thread가 아니라 `MonitorThread`임.
6. 모든 worker thread가 종료되면 `MonitorThread`가 `all_done` signal을 emit함.
7. GUI thread는 이 signal을 받아 status label을 update함.

## 수정된 코드

```python
import sys
import time

# QThread: Qt의 thread abstraction.
# Signal: thread 간 안전하게 데이터를 전달하기 위한 Qt signal.
from PySide6.QtCore import QThread, Signal

# 예제 GUI를 구성하기 위한 widget들.
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class WorkerThread(QThread):
    # 진행 상태(0~100)를 GUI로 전달하기 위한 signal.
    # emit(int) 형태로 사용됨.
    update_signal = Signal(int)

    def __init__(self, thread_id):
        super().__init__()

        # 단순 식별용 ID.
        self.thread_id = thread_id

    def run(self):
        """
        start()가 호출되면 Qt가 새 OS thread를 생성하고,
        그 thread 안에서 run()을 실행한다.

        여기서는 0~100까지 진행률을 증가시키며
        주기적으로 signal을 emit한다.
        """
        for i in range(101):
            # 실제 작업을 단순화하여 표현한 코드.
            # CPU를 계속 사용하는 계산이 아니라
            # 일정 시간 대기하는 상황을 가정한다.
            time.sleep(0.1)

            # 진행률을 GUI thread로 전달.
            # Qt의 queued connection을 통해
            # GUI thread에서 안전하게 처리된다.
            self.update_signal.emit(i)


class MonitorThread(QThread):
    # 모든 worker thread가 종료되었음을 알리는 signal.
    all_done = Signal()

    def __init__(self, threads):
        super().__init__()

        # 감시 대상 worker thread 목록.
        self.threads = threads

    def run(self):
        """
        모든 worker thread가 종료될 때까지 기다린다.

        중요한 점:
        wait()를 호출하는 주체가 GUI thread가 아니라
        MonitorThread라는 것이다.

        따라서 wait()로 인해 block되는 것은
        MonitorThread이며 GUI event loop는 계속 동작한다.
        """
        for thread in self.threads:
            # 대상 worker thread가 종료될 때까지 대기.
            thread.wait()

        # 모든 worker가 종료되었음을 알림.
        self.all_done.emit()


class MW(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QThread Monitor Example")

        # 각 worker에 대응하는 progress bar 저장.
        self.progress_bars = []

        # 각 worker에 대응하는 개별 실행 버튼 저장.
        self.buttons = []

        # 현재 활성 worker thread를 저장.
        #
        # index 0 -> Thread 1
        # index 1 -> Thread 2
        # index 2 -> Thread 3
        #
        # worker가 종료되면 해당 위치를 None으로 되돌린다.
        self.worker_threads = [None, None, None]

        # 현재 실행 중인 monitor thread.
        # 실행 중이 아니면 None.
        self.monitor_thread = None

        self.init_ui()
        self.show()

    def init_ui(self):
        # 전체 widget을 수직으로 배치하는 layout.
        self.layout = QVBoxLayout(self)

        # 현재 상태를 표시하는 label.
        self.status_label = QLabel(
            "Click 'Start All Threads' to run the threads",
            self,
        )
        self.layout.addWidget(self.status_label)

        # 모든 worker를 한 번에 실행하는 버튼.
        self.start_all_button = QPushButton("Start All Threads", self)
        self.start_all_button.clicked.connect(self.start_all_threads)
        self.layout.addWidget(self.start_all_button)

        # worker 3개에 대한 UI 생성.
        for i in range(3):
            label = QLabel(f"Thread {i + 1} Example", self)

            progress_bar = QProgressBar(self)
            progress_bar.setRange(0, 100)

            button = QPushButton(f"Start Thread {i + 1}", self)

            # 각 버튼은 자신에게 대응하는 worker만 실행.
            button.clicked.connect(self.make_start_thread(i))

            self.layout.addWidget(label)
            self.layout.addWidget(progress_bar)
            self.layout.addWidget(button)

            self.progress_bars.append(progress_bar)
            self.buttons.append(button)

    def make_start_thread(self, index):
        """
        index별 실행 함수를 생성한다.

        lambda를 직접 사용하는 대신 별도 함수를 만들어
        현재 index 값을 안전하게 캡처한다.
        """

        def start_thread():
            self.start_worker_thread(index)

        return start_thread

    def create_worker_thread(self, index):
        """
        새로운 WorkerThread를 생성하고
        필요한 signal-slot 연결을 수행한다.
        """
        worker = WorkerThread(index)

        # worker가 emit한 진행률 값을
        # 해당 progress bar에 반영.
        worker.update_signal.connect(
            self.progress_bars[index].setValue
        )

        # worker 종료 시 정리 작업 수행.
        #
        # finished signal은 GUI thread로 전달되므로
        # 안전하게 UI를 갱신할 수 있다.
        worker.finished.connect(
            lambda idx=index, w=worker: self.on_worker_finished(idx, w)
        )

        return worker

    def start_worker_thread(self, index):
        """
        특정 worker 하나만 실행한다.
        """
        current_worker = self.worker_threads[index]

        # 이미 실행 중이면 중복 실행하지 않는다.
        if current_worker is not None and current_worker.isRunning():
            return

        # 새 실행을 위해 progress 초기화.
        self.progress_bars[index].setValue(0)

        # 실행 중에는 버튼 비활성화.
        self.buttons[index].setEnabled(False)

        # 새로운 worker 생성.
        worker = self.create_worker_thread(index)

        # 현재 worker 저장.
        self.worker_threads[index] = worker

        # 실제 thread 시작.
        worker.start()

    def on_worker_finished(self, index, worker):
        """
        worker 종료 시 호출된다.
        """

        # 현재 저장된 worker와
        # 종료된 worker가 동일한 경우에만 정리.
        #
        # 예제 규모에서는 큰 차이가 없지만
        # reference 관리 실수를 방지하는 습관이다.
        if self.worker_threads[index] is worker:
            self.worker_threads[index] = None

        # 다시 실행할 수 있도록 버튼 활성화.
        self.buttons[index].setEnabled(True)

    def start_all_threads(self):
        """
        모든 worker를 실행하고,
        MonitorThread를 통해 종료를 감시한다.
        """

        # 이미 monitor가 실행 중이면
        # 전체 실행을 중복 시작하지 않는다.
        if self.monitor_thread is not None and self.monitor_thread.isRunning():
            return

        self.status_label.setText("Threads are running...")

        # 전체 실행 중에는 버튼 비활성화.
        self.start_all_button.setEnabled(False)

        # MonitorThread가 감시할 worker 목록.
        workers_to_monitor = []

        for index in range(3):
            current_worker = self.worker_threads[index]

            # 이미 실행 중인 worker는
            # 새로 만들지 않고 감시 대상에만 추가.
            if current_worker is not None and current_worker.isRunning():
                workers_to_monitor.append(current_worker)
                continue

            # 새 실행을 위해 progress 초기화.
            self.progress_bars[index].setValue(0)

            # 실행 중에는 개별 버튼 비활성화.
            self.buttons[index].setEnabled(False)

            # 새 worker 생성.
            worker = self.create_worker_thread(index)

            self.worker_threads[index] = worker

            workers_to_monitor.append(worker)

            # worker 시작.
            worker.start()

        # 모든 worker 종료를 감시할 monitor 생성.
        self.monitor_thread = MonitorThread(workers_to_monitor)

        # 모든 worker 종료 시 상태 label 갱신.
        self.monitor_thread.all_done.connect(
            self.update_status_label
        )

        # monitor 종료 시 후처리.
        self.monitor_thread.finished.connect(
            self.on_monitor_finished
        )

        # monitor 시작.
        self.monitor_thread.start()

    def update_status_label(self):
        """
        모든 worker가 종료되었을 때 호출된다.
        """
        self.status_label.setText("All threads completed!")

    def on_monitor_finished(self):
        """
        MonitorThread 종료 후 정리 작업.
        """

        # 전체 실행 버튼 다시 활성화.
        self.start_all_button.setEnabled(True)

        # monitor reference 제거.
        self.monitor_thread = None

    def closeEvent(self, event):
        """
        창 닫기 요청 처리.

        실행 중인 thread가 있는 상태에서
        QWidget이 파괴되면 다음과 같은 문제가 발생할 수 있다.

        QThread: Destroyed while thread is still running

        이를 방지하기 위해 실행 중인 thread가 있으면
        창 닫기를 거부한다.
        """

        # 현재 실행 중인 worker 목록 수집.
        running_workers = [
            worker
            for worker in self.worker_threads
            if worker is not None and worker.isRunning()
        ]

        # monitor 실행 여부 확인.
        monitor_running = (
            self.monitor_thread is not None
            and self.monitor_thread.isRunning()
        )

        # 하나라도 실행 중이면 종료 거부.
        if running_workers or monitor_running:
            self.status_label.setText(
                "Threads are still running. Wait until they finish."
            )

            event.ignore()
            return

        # 실행 중인 thread가 없으면 정상 종료.
        super().closeEvent(event)


if __name__ == "__main__":
    # Qt application 객체 생성.
    app = QApplication(sys.argv)

    # 메인 윈도우 생성.
    wnd = MW()

    # Qt event loop 시작.
    sys.exit(app.exec())
```

# 코드 설명

## WorkerThread class

`WorkerThread`는 실제 background 작업을 수행하는 `QThread` subclass임.

```python
class WorkerThread(QThread):
    update_signal = Signal(int)
```

`update_signal`은 worker thread에서 GUI thread로 진행률 값을 전달하기 위한 signal이다.

```python
def run(self):
    for i in range(101):
        time.sleep(0.1)
        self.update_signal.emit(i)
```

* `time.sleep(0.1)`은 CPU-bound 계산을 수행하는 code가 아니다. 
* CPU를 점유하지 않은 채 worker thread가 일정 시간 block되는 상황을 표현하기 위한 code임.

## MonitorThread class

`MonitorThread`는 worker thread들이 모두 종료될 때까지 기다리는 역할을 수행한다.

```python
class MonitorThread(QThread):
    all_done = Signal()
```

`all_done` signal은 모든 worker thread가 종료되었을 때 GUI thread에 알리기 위한 signal이다.

```python
def run(self):
    for thread in self.threads:
        thread.wait()

    self.all_done.emit()
```

* 중요한 점은 이 `wait()`가 GUI thread에서 호출되지 않는다는 것이다. 
* `MonitorThread`의 `run()` 안에서 호출되므로, block되는 것은 monitor thread이다.

따라서 worker thread들이 끝날 때까지 기다리는 동안에도 GUI thread는 계속 event loop를 처리할 수 있다.

## MW class의 변경점

Example 1에서는 worker thread를 미리 만들어 두고 계속 재사용하지 않는다. 대신 실행할 때마다 새로운 `WorkerThread` instance를 생성한다.

```python
self.worker_threads = [None, None, None]
```

각 index에 대응하는 현재 worker thread는 `self.worker_threads`에 저장한다. 

* worker가 종료되면 
* `on_worker_finished()`에서 해당 reference를 `None`으로 되돌린다.

```python
def on_worker_finished(self, index, worker):
    if self.worker_threads[index] is worker:
        self.worker_threads[index] = None

    self.buttons[index].setEnabled(True)
```

이렇게 하면 이미 종료된 `QThread` object를 재사용하려는 상황을 피할 수 있다. 

* Qt에서는 `QThread` instance를 한 번 실행하고 종료한 뒤 다시 `start()`하는 것이 기술적으로 가능하지만, 
* 실제 application에서는 thread 내부 상태, signal 연결, 실행 중 사용한 resource 등을 어떻게 관리하느냐에 따라 예상하지 못한 문제가 발생할 수 있다. 
* 따라서 예제에서는 실행할 때마다 새로운 `WorkerThread` instance를 생성하여 thread의 생명 주기를 명확하게 관리하는 방식을 사용하였다.

## start_all_threads()

`start_all_threads()`에서는 현재 실행 중인 worker가 있으면 그대로 monitor 대상에 포함하고, 실행 중이 아닌 worker는 새로 만들어 시작한다.

```python
def start_all_threads(self):
    # 이미 MonitorThread가 실행 중이라면 중복 실행을 막음.
    # MonitorThread는 worker thread들의 종료를 감시하는 역할을 하므로,
    # 여러 개가 동시에 실행될 필요가 없음.
    if self.monitor_thread is not None and self.monitor_thread.isRunning():
        return

    # 사용자에게 현재 작업이 진행 중임을 표시.
    self.status_label.setText("Threads are running...")

    # 전체 실행 버튼을 비활성화하여 사용자가 다시 누르지 못하게 함.
    # MonitorThread가 종료되면 on_monitor_finished()에서 다시 활성화됨.
    self.start_all_button.setEnabled(False)

    # 이번 실행에서 MonitorThread가 감시해야 할 worker thread 목록.
    workers_to_monitor = []

    # 예제에서는 worker thread가 3개이므로 index 0~2를 순회.
    for index in range(3):
        # 현재 index에 연결된 worker thread를 가져옴.
        current_worker = self.worker_threads[index]

        # 이미 해당 worker가 실행 중이라면 새로 생성하지 않음.
        # 현재 실행 중인 worker도 MonitorThread가 감시해야 하므로
        # 감시 목록에 추가한 뒤 다음 index로 넘어감.
        if current_worker is not None and current_worker.isRunning():
            workers_to_monitor.append(current_worker)
            continue

        # 새 worker를 시작하는 경우:
        
        # progress bar를 초기화.
        self.progress_bars[index].setValue(0)

        # 작업이 진행되는 동안 개별 시작 버튼을 비활성화.
        self.buttons[index].setEnabled(False)

        # 새로운 WorkerThread instance 생성.
        worker = self.create_worker_thread(index)

        # 현재 index에 대한 worker reference 저장.
        # worker 종료 시 on_worker_finished()에서 None으로 정리됨.
        self.worker_threads[index] = worker

        # MonitorThread가 감시할 목록에 추가.
        workers_to_monitor.append(worker)

        # 실제 worker thread 시작.
        worker.start()

    # 모든 worker thread의 종료를 감시할 MonitorThread 생성.
    self.monitor_thread = MonitorThread(workers_to_monitor)

    # 모든 worker가 종료되면 상태 label을 갱신.
    self.monitor_thread.all_done.connect(self.update_status_label)

    # MonitorThread 자체가 종료되면 버튼 재활성화 및 reference 정리.
    self.monitor_thread.finished.connect(self.on_monitor_finished)

    # MonitorThread 시작.
    # 내부 run()에서 각 worker에 대해 wait()를 호출하지만,
    # GUI thread가 아닌 MonitorThread가 block되므로 GUI는 계속 응답 가능.
    self.monitor_thread.start()
```

* `MonitorThread`가 실행 중인 동안에는 
* 전체 실행 button을 비활성화하여 monitor thread가 중복 생성되지 않도록 한다.

## closeEvent()

실행 중인 thread가 있는 상태에서 window가 닫히면, Python wrapper가 정리되면서 Qt 쪽에서 다음과 같은 문제가 발생할 수 있다.

```text
QThread: Destroyed while thread is still running
```

이를 피하기 위해 이 예제에서는 실행 중인 thread가 있으면 window close를 막는다.

```python
def closeEvent(self, event):
    # 현재 실행 중인 worker thread들을 수집함.
    # self.worker_threads에는 WorkerThread instance 또는 None이 저장되어 있음.
    # None이 아니면서 isRunning()이 True인 thread만 추려냄.
    running_workers = [
        worker
        for worker in self.worker_threads
        if worker is not None and worker.isRunning()
    ]

    # MonitorThread가 존재하고 현재 실행 중인지 확인함.
    # MonitorThread 역시 QThread이므로 실행 중인 상태에서 객체가
    # 파괴되면 문제가 발생할 수 있음.
    monitor_running = (
        self.monitor_thread is not None and self.monitor_thread.isRunning()
    )

    # worker thread 또는 monitor thread 중 하나라도 실행 중이면
    # window close를 허용하지 않음.
    #
    # 실행 중인 QThread 객체가 있는 상태에서 widget이 파괴되면
    # 다음과 같은 오류가 발생할 수 있음.
    #
    # QThread: Destroyed while thread is still running
    #
    # 따라서 사용자가 thread 종료를 기다리도록 안내하고,
    # close event를 무시함.
    if running_workers or monitor_running:
        self.status_label.setText("Threads are still running. Wait until they finish.")

        # close 요청을 취소함.
        # event.ignore()를 호출하면 window는 닫히지 않음.
        event.ignore()
        return

    # 실행 중인 thread가 하나도 없는 경우에만
    # 부모 클래스의 closeEvent()를 호출하여 정상적으로 window를 닫음.
    super().closeEvent(event)
```

실제 application에서는 단순히 close를 막는 대신, cancel flag를 사용하여 worker thread에 종료를 요청하고, 종료가 완료된 뒤 application을 닫도록 구성할 수 있다.

# 정리

`QThread.wait()`는 대상 thread가 종료될 때까지 현재 thread를 block하는 method임.

따라서 GUI thread에서 `wait()`를 호출하면 GUI thread의 event loop가 멈추고, application이 응답하지 않는 것처럼 보일 수 있다.

반면 별도의 monitor thread에서 `wait()`를 호출하면, worker thread들의 종료를 기다리는 동안 GUI thread는 계속 event loop를 처리할 수 있다.

이 예제의 핵심은 다음과 같음.

* `wait()`는 대상 thread가 아니라 `wait()`를 호출한 thread를 block함.
* `wait(timeout)`의 timeout은 단순 sleep 시간이 아니라, 대상 thread 종료를 기다리는 최대 시간임.
* GUI thread에서 `wait()`를 호출하면 GUI가 멈출 수 있음.
* Worker thread나 monitor thread에서 `wait()`를 호출하면 GUI thread의 event loop는 계속 동작할 수 있음.
* GUI update는 worker thread나 monitor thread에서 직접 수행하지 않고, signal-slot mechanism을 통해 GUI thread에서 수행해야 함.
* 실행 중인 `QThread` object가 삭제되지 않도록, Python reference와 thread lifetime을 함께 관리해야 함.

다만 `MonitorThread`를 사용하는 방식은 `wait()`의 동작을 설명하기 위한 예제 구조로 이해하는 것이 좋다. 실제 application에서는 작업 수, 작업 성격, 재사용 여부에 따라 `QThreadPool`, `QRunnable`, `finished` signal count, 또는 별도의 task manager 구조를 고려할 수 있다.
