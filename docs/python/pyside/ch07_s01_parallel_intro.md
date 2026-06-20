---
title: GUI 프로그램에서 Process와 Thread
tags: [GUI, Qt, PySide6, PyQt, Process, Thread, Multithreading, Multiprocessing, QThread, QThreadPool, QProcess]
---

# GUI 프로그램에서 Process와 Thread

> Process(프로세스)와 Thread(스레드)는 software를 실행하는 기본 단위임.

일반적으로 하나의 program은 하나의 process로 시작되며, 각 process는 하나 이상의 thread로 구성됨.

GUI program에서는 특히 하나의 thread, 즉 GUI thread 또는 main thread가 main event loop를 담당하는 것이 일반적임.

* GUI thread는 사용자 입력, timer, repaint 요청, OS에서 전달되는 event 등을 처리함.
* `QApplication.exec()`는 보통 이 main thread에서 Qt event loop를 시작함.
* `exec()`가 별도의 thread를 새로 만드는 것이 아니라, `QApplication` 객체가 생성되고 실행되는 thread가 그대로 GUI thread가 됨.

만약 process와 thread의 개념이 명확하지 않다면 다음 URL을 참고할 것.

* [Process vs Thread](https://ds31x.tistory.com/152)

Python과 Qt binding인 `PyQt` 또는 `PySide`를 활용한 GUI application 개발에서도 이 원칙은 동일하게 적용됨.

Python으로 구현되는 Qt application은 일반적으로 하나의 Python interpreter process 내에서 실행됨. 이 구조에서 시간이 오래 걸리는 작업을 GUI thread에서 직접 수행하면 main event loop가 막혀 사용자 입력과 화면 갱신이 지연됨.

따라서 GUI application에서는 시간이 오래 걸리는 작업을 GUI thread에서 분리하여 실행해야 함.

이를 위해 사용할 수 있는 대표적인 방식은 다음과 같음.

* `QThread`, `QRunnable`, `QThreadPool`을 이용한 multithreading
* `QProcess` 또는 Python `multiprocessing`을 이용한 multiprocessing

---

---

## Multiprocessing과 Multithreading

현대의 multicore CPU는 동시에 여러 작업을 수행할 수 있는 능력을 갖추고 있음.

이러한 hardware의 진보는 multiprocess 및 multithread programming을 통해 더 빠르고 반응성 높은 GUI program 구현을 가능하게 함.

PyQt와 PySide는 multithread 및 multiprocess 구현을 지원하는 여러 class와 도구를 제공함.

대표적으로 다음과 같은 class를 사용할 수 있음.

* `QThread`: 별도 thread를 생성하고 작업을 수행하기 위한 class
* `QRunnable`: thread에서 수행할 작업 단위를 나타내는 class
* `QThreadPool`: 여러 `QRunnable` 작업을 thread pool에 분배하는 class
* `QProcess`: 외부 program을 별도 process로 실행하고 제어하기 위한 class

이러한 class들을 사용하면 GUI thread가 사용자 입력과 화면 갱신에 집중할 수 있으므로, GUI application의 반응성을 유지할 수 있음.

다만 Python 기반 GUI application에서는 Global Interpreter Lock(GIL)을 고려해야 함.

Python의 GIL 때문에 순수 Python code로 작성된 CPU-bound 작업은 multithreading만으로 실제 병렬 계산 성능 향상을 얻기 어려움.

따라서 Python 기반 GUI application에서는 다음과 같이 구분하는 것이 좋음.

* multithreading: GUI 반응성 유지, I/O-bound 작업 처리, GIL을 release하는 library 작업 분리에 적합함.
* multiprocessing: CPU-bound 작업의 실제 병렬 처리, 외부 program 실행, process 단위 격리에 적합함.

> [참고: GIL (Global Interpreter Lock)에 대한 자세한 내용](https://ds31x.tistory.com/680)

---

---

## Multithreading이 유리한 경우

GUI program에서 multithreading은 주로 GUI 반응성을 유지하기 위해 사용됨.

시간이 오래 걸리는 작업을 GUI thread에서 직접 수행하면 main event loop가 block됨. 이 경우 button click, keyboard input, window repaint 같은 event 처리가 지연되며, 사용자는 program이 멈춘 것처럼 느낄 수 있음.

이때 해당 작업을 별도의 worker thread에서 수행하면 GUI thread는 event loop를 계속 처리할 수 있음.

Multithreading은 다음과 같은 경우에 적합함.

* file 입출력, network 요청, database 접근처럼 대기 시간이 긴 I/O-bound 작업을 처리하는 경우
* image loading, data parsing, preprocessing 등 GUI thread를 오래 점유할 수 있는 작업을 분리하는 경우
* worker thread의 진행 상태를 Qt signal-slot mechanism을 통해 GUI thread로 안전하게 전달해야 하는 경우
* NumPy, OpenCV, SciPy처럼 내부적으로 GIL을 release하는 C/C++ 기반 library 연산을 background에서 수행하는 경우

Thread는 process보다 생성 및 context switching 비용이 작고, 같은 process의 memory space를 공유함. 따라서 thread 간 data 교환이 비교적 쉬움.

하지만 GUI application에서 반드시 지켜야 할 원칙이 있음.

> GUI widget은 반드시 GUI thread에서 생성되고 수정되어야 함.

따라서 worker thread에서 `QLabel`, `QPushButton`, `QProgressBar`와 같은 widget을 직접 조작하면 안 됨.

일반적인 구조는 다음과 같음.

* worker thread에서는 계산, I/O, data 처리만 수행함.
* worker thread는 결과나 진행 상태를 signal로 전달함.
* GUI thread의 slot에서 signal을 받아 widget을 갱신함.

즉, worker thread는 작업을 수행하고, GUI thread는 화면을 수정하는 구조로 분리해야 함.

---

---

## Multiprocessing이 유리한 경우

Multiprocessing은 작업을 별도의 process로 분리하여 실행하는 방식임.

Qt 기반 GUI application에서는 `QProcess`를 이용하여 외부 program을 sub-process로 실행할 수 있음. Python 자체의 `multiprocessing` module을 사용할 수도 있음.

Multiprocessing은 각 process가 독립된 memory space를 가지므로 thread보다 생성 비용과 data 교환 비용이 큼.

하지만 process 간 memory가 분리되므로 안정성이 높고, 외부 program의 crash가 main GUI process에 직접 영향을 덜 줌.

또한 각 process가 별도의 Python interpreter와 GIL을 가지므로, 순수 Python CPU-bound 작업을 여러 core에서 실제 병렬로 수행해야 하는 경우에도 유리함.

대표적으로 다음과 같은 경우에 multiprocessing이 적합함.

* 외부 CLI program을 GUI application에서 실행해야 하는 경우
* CPU-bound 작업을 여러 core에서 실제 병렬로 수행해야 하는 경우
* 작업 실패나 crash가 main GUI process에 직접 영향을 주지 않도록 분리해야 하는 경우
* 독립적인 worker program을 실행하고, 표준 출력, file, socket 등을 통해 결과를 받아야 하는 경우

`QProcess`를 사용하면 외부 program의 standard output, standard error, 종료 상태 등을 Qt signal을 통해 처리할 수 있음.

따라서 GUI application은 외부 process를 실행하면서도 main event loop를 block하지 않고 계속 반응성을 유지할 수 있음.

---

---

## Multithreading과 Multiprocessing 비교

앞의 내용을 기준으로 multithreading과 multiprocessing을 비교하면 다음과 같음.

| 구분                        | Multithreading           | Multiprocessing    |
| ------------------------- | ------------------------ | ------------------ |
| 실행 단위                     | 하나의 process 안의 여러 thread | 여러 process         |
| memory 공간                 | process memory 공유        | process별 독립 memory |
| 생성 비용                     | 상대적으로 작음                 | 상대적으로 큼            |
| data 교환                   | 비교적 쉬움                   | 상대적으로 복잡함          |
| GUI 반응성 유지                | 적합함                      | 적합함                |
| I/O-bound 작업              | 적합함                      | 가능하지만 과할 수 있음      |
| 순수 Python CPU-bound 병렬 처리 | GIL 때문에 제한적              | 적합함                |
| 외부 program 실행             | 부적합                      | 적합함                |
| 작업 crash 격리               | 약함                       | 강함                 |

이 비교를 기준으로 보면, GUI 반응성 유지나 I/O-bound 작업 분리에는 multithreading이 적합함.

반면 순수 Python CPU-bound 작업의 실제 병렬 처리나 외부 program 실행에는 multiprocessing이 더 적합함.

따라서 PySide6/PyQt 기반 GUI program에서는 작업의 성격에 따라 thread와 process를 구분해서 선택해야 함.

이 장에서는 먼저 multithreading을 통해 Qt application의 반응성을 유지하는 방법을 살펴보고, 이어서 multiprocessing을 통해 독립된 다른 program을 Qt application에서 실행하는 방법을 소개함.

---

---

## 참고: Python built-in thread와 Qt thread의 차이

Python은 built-in으로 thread를 지원함.

Python standard library의 `threading` module을 사용하면 다음과 같이 별도의 thread를 만들 수 있음.

```python
import threading


def worker():
    print("worker thread")


t = threading.Thread(target=worker)
t.start()
t.join()
```

즉, PyQt나 PySide를 사용하지 않더라도 Python 자체만으로 multithreading을 구현할 수 있음.

하지만 Qt 기반 GUI application에서는 Python의 `threading.Thread`보다 `QThread`, `QRunnable`, `QThreadPool`을 사용하는 경우가 많음.

그 이유는 Qt의 GUI 구조가 다음 요소들과 밀접하게 연결되어 있기 때문임.

* Qt event loop
* signal-slot mechanism
* `QObject`의 thread affinity
* GUI thread에서만 안전한 widget update

Python의 `threading.Thread`는 일반적인 Python code를 별도 thread에서 실행하는 데 적합함.

반면 `QThread`, `QRunnable`, `QThreadPool`은 Qt application과 연동되는 background 작업을 구현하는 데 적합함.

특히 worker thread에서 작업을 수행한 뒤 결과를 GUI에 반영해야 하는 경우에는 Qt의 signal-slot mechanism을 이용하는 것이 안전함.

정리하면 다음과 같음.

| 구분                        | Python `threading.Thread`       | Qt `QThread`, `QRunnable`, `QThreadPool`   |
| ------------------------- | ------------------------------- | ------------------------------------------ |
| 제공 위치                     | Python standard library         | Qt framework                               |
| 주된 목적                     | 일반 Python code의 thread 실행       | Qt application과 연동되는 background 작업         |
| Qt event loop 연동          | 직접 연동되지 않음                      | 연동 가능                                      |
| signal-slot 연동            | 직접 구성해야 함                       | 자연스럽게 연동                                   |
| `QObject` thread affinity | 직접 다루기 어려움                      | Qt 구조와 함께 사용 가능                            |
| GUI widget update         | 직접 하면 위험함                       | signal을 통해 GUI thread에서 처리하는 구조 권장         |
| 사용 상황                     | 일반 Python 작업, 간단한 background 작업 | PyQt/PySide GUI application의 worker thread |

따라서 일반 Python program에서는 `threading.Thread`를 사용할 수 있지만, PyQt나 PySide 기반 GUI program에서는 `QThread`, `QRunnable`, `QThreadPool`을 사용하는 것이 보통 더 적합함.

## 참고: Python과 Qt에서 process를 다루는 대표적인 도구

앞서 살펴본 것처럼 GUI program에서는 작업의 성격에 따라 thread와 process를 구분해서 사용하는 것이 중요함.

Python과 Qt에서 process를 다루는 대표적인 도구는 다음과 같음.

| 도구                                       | 제공 위치                   | 주요 목적                                                      |
| ---------------------------------------- | ----------------------- | ---------------------------------------------------------- |
| `multiprocessing`                        | Python standard library | Python function을 별도 process에서 실행                           |
| `concurrent.futures.ProcessPoolExecutor` | Python standard library | process pool을 이용하여 여러 Python function 호출을 분산 실행            |
| `subprocess`                             | Python standard library | 외부 program 또는 command를 child process로 실행                   |
| `QProcess`                               | Qt framework            | 외부 process를 Qt event loop 및 signal-slot mechanism과 연동하여 실행 |

`multiprocessing`은 Python에서 process 기반 병렬 처리를 직접 다룰 때 사용하는 standard library임.

```python
from multiprocessing import Process


def worker():
    print("worker process")


if __name__ == "__main__":
    p = Process(target=worker)
    p.start()
    p.join()
```

위 예제에서 `Process`는 새로운 Python process를 생성하고, 해당 process에서 `worker()` function을 실행함.

`concurrent.futures.ProcessPoolExecutor`는 `multiprocessing`을 좀 더 높은 수준의 interface로 다룰 수 있게 해주는 process pool API임.

```python
from concurrent.futures import ProcessPoolExecutor


def square(x):
    return x * x


if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(square, range(5)))

    print(results)
```

`ProcessPoolExecutor`는 여러 worker process를 pool로 관리하고, function 호출을 각 process에 분산 실행함.

즉, `ProcessPoolExecutor`는 `multiprocessing`을 대체하는 별도의 최신 실험 기능이라기보다, Python standard library에서 제공하는 high-level process pool interface로 보는 것이 적절함.

반면 `subprocess`는 Python function을 여러 process에 분산 실행하기 위한 도구가 아님.

`subprocess`는 외부 program이나 command를 child process로 실행하기 위한 도구임.

```python
import subprocess


result = subprocess.run(
    ["python", "--version"],
    capture_output=True,
    text=True
)

print(result.stdout)
```

따라서 `subprocess`는 다음과 같은 경우에 사용함.

* 외부 CLI program을 실행해야 하는 경우
* shell command 또는 독립 실행 program을 호출해야 하는 경우
* 실행 결과의 standard output, standard error, 종료 code를 확인해야 하는 경우

`QProcess`는 Qt에서 제공하는 외부 process 실행 class임.

`QProcess`는 외부 process의 standard output, standard error, 종료 상태 등을 Qt signal-slot mechanism과 연동하여 처리할 수 있음.

따라서 PySide6/PyQt 기반 GUI application에서는 외부 process를 실행하고 그 결과를 GUI와 자연스럽게 연결해야 할 때 `QProcess`가 적합함.

정리하면 다음과 같음.

* Python function을 별도 process에서 실행하려면 `multiprocessing`을 사용함.
* 여러 Python function 호출을 process pool에 분산 실행하려면 `ProcessPoolExecutor`를 사용할 수 있음.
* 외부 CLI program이나 command를 실행하려면 `subprocess`를 사용함.
* Qt GUI application에서 외부 process를 event loop와 signal-slot으로 연동하려면 `QProcess`를 사용함.

즉, `multiprocessing`, `ProcessPoolExecutor`, `subprocess`는 Python standard library에 포함된 도구이고, `QProcess`는 Qt framework에서 제공하는 class임.


* `multiprocessing`: Python function을 별도 process에서 실행.
* `concurrent.futures.ProcessPoolExecutor`: process pool 기반의 high-level 병렬 실행 interface.
* `subprocess`: 외부 program이나 command를 child process로 실행.