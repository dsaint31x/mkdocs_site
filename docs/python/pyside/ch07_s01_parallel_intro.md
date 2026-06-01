---
title: GUI 프로그램에서 Process와 Thread
tags: [GUI, Qt, PySide6, PyQt, Process, Thread, Multithreading, Multiprocessing, QThread, QThreadPool, QProcess]
---

# GUI 프로그램에서 Process와 Thread

> Process(프로세스)와 Thread(스레드)는 software를 실행하는 기본 단위임.

일반적으로 하나의 program은 하나의 process로 시작되며, 각 process는 하나 이상의 thread로 구성됨.  

GUI program에서는 

* 특히 하나의 thread, 즉 GUI thread 또는 **main thread** 가 **main event loop를 담당** 하여, 
* process 내에서 사용자 입력이나 OS에서 전달되는 event를 처리하는 것이 일반적임.

만약 process와 thread의 개념이 명확하지 않다면 다음 URL을 참고할 것: 

* [Process vs Thread](https://ds31x.tistory.com/152)

Python과 Qt binding인 `PyQt` 또는 `PySide`를 활용한 GUI application 개발에서도 이 원칙은 동일하게 적용된다. 

Python으로 구현되는 Qt application은 

* 일반적으로 하나의 Python interpreter process 내에서 실행되며, 
* `QApplication` 객체의 `exec()` method 호출을 통해 **현재 thread에서 main event loop가 시작** 된다. 
* 이때 `exec()`가 별도의 thread를 새로 시작하는 것이 아니라, 
* 보통 `QApplication` 객체가 생성되고 실행되는 main thread가 그대로 GUI thread가 된다.

이 구조에서 multithreading이나 multiprocessing을 적용할 경우, 시간이 오래 걸리는 작업을 GUI thread에서 분리하여 실행할 수 있다.  
이를 통해 GUI thread가 event 처리와 화면 갱신에 집중할 수 있으므로, GUI program의 반응성을 유지하거나 향상시킬 수 있다.

---

---

## Multiprocessing과 Multithreading

현대의 multicore CPU는 동시에 여러 작업을 수행할 수 있는 능력을 갖추고 있으며, 

* 이러한 hardware의 진보는 
* multiprocess 및 multithread programming을 통해 
* 보다 빠르고 반응성 높은 GUI program을 가능하게 한다.

PyQt와 PySide는 multithread 및 multiprocess 구현을 지원하는 다양한 class와 도구를 제공한다.  
이들을 활용함으로써 개발자는 현대 computing 환경의 이점을 활용하여, 효율적이고 강력한 GUI application을 제작할 수 있다.

조금 더 구체적으로, PyQt와 PySide에서는 

* `QThread` class나 `QThreadPool` 등을 사용하여 
* 복잡한 작업을 background thread에서 처리하거나, 
* `QProcess` class를 이용하여 외부 program을 GUI application에서 sub-process로 실행시킬 수 있다. 

이러한 방법은 GUI application의 main event loop를 실행하는 GUI thread가 user interaction과 화면 갱신에 집중할 수 있도록 하여, 더 빠르고 반응성 높은 application 구현을 가능하게 해준다.

다만 Python에서는 ***Global Interpreter Lock(GIL)*** 의 영향으로, 순수 Python code로 작성된 CPU-bound 작업은 multithreading만으로 실제 병렬 계산 성능 향상을 얻기 어렵다. 

* 따라서 Python 기반 GUI application에서 **multithreading은 주로 GUI 반응성 유지, I/O-bound 작업 처리, 또는 내부적으로 GIL을 release하는 library 작업을 분리** 하는 데 유리하다. 
* 반면 **CPU-bound 작업을 실제로 병렬 계산** 해야 하는 경우에는 **multiprocessing** 이나 외부 process 실행이 더 적합할 수 있다.

> [**참고: GIL (Global Interpreter Lock) 에 대한 자세한 내용**](https://ds31x.tistory.com/680)

---

---

## Multithreading이 유리한 경우

GUI program에서 시간이 오래 걸리는 작업을 수행할 때, GUI의 반응성을 유지하거나 향상시키기 위해 multithreading이 자주 사용된다. 

* 이는 thread가 process보다 생성 및 context switching 비용이 작고, 
* 같은 process의 memory space를 공유하므로 thread 간 data 교환이 비교적 쉽기 때문이다.

PyQt와 PySide에서도 multithreading을 활용하여, application이 복잡한 작업을 수행하면서도 사용자의 입력에 지연 없이 반응할 수 있도록 만들 수 있다. 

이는 시간이 오래 걸리는 작업을 application의 event loop를 실행하는 GUI thread가 아닌, 별도의 worker thread에서 실행함으로써 가능하다.

대표적으로 다음과 같은 경우에 multithreading이 적합하다.

* file 입출력, network 요청, database 접근처럼 대기 시간이 긴 I/O-bound 작업을 처리하는 경우
* image loading, data parsing, preprocessing 등 GUI thread를 오래 점유할 수 있는 작업을 분리하는 경우
* Qt signal-slot mechanism을 통해 worker thread의 진행 상태를 GUI thread로 안전하게 전달해야 하는 경우
* 내부적으로 GIL을 release하는 C/C++ 기반 library 연산을 background에서 수행하는 경우

이때 주의할 점은 **GUI widget을 직접 수정하는 작업은 반드시 GUI thread에서 수행해야 한다** 는 점이다. 

* Worker thread에서 `QLabel`, `QPushButton`, `QProgressBar`와 같은 widget을 직접 조작하면 
* thread-safety 문제가 발생할 수 있다. 
* 따라서 worker thread에서는 계산이나 **I/O 작업만 수행** 하고, 
* 결과는 signal을 통해 GUI thread로 전달한 뒤 GUI thread에서 widget을 갱신하는 방식이 권장된다.

---

---

## Multiprocessing이 유리한 경우

`QProcess`를 이용한 ***multiprocessing은 더 독립적인 작업을 별도의 process로 실행시킬 때 사용*** 된다. 

* 예를 들어, 외부의 독립된 utility software, 
* 특히 CLI를 채택하고 있는 독립된 utility software를 GUI application에서 실행시키는 경우에는 multiprocessing이 multithreading보다 적합하다.

Multiprocessing은 각 process가 독립된 memory space를 가지므로 thread보다 생성 비용과 data 교환 비용은 크다.  

하지만 process 간 격리가 잘 되기 때문에, 외부 program 실행이나 실패 가능성이 있는 독립 작업을 GUI application과 분리하여 처리하기에 적합하다. 
또한 **Python의 GIL 영향을 process 단위로 피할 수 있으므로, CPU-bound 작업을 실제 병렬로 수행해야 하는 경우에도 multiprocessing이 유리** 할 수 있다.

대표적으로 다음과 같은 경우에 multiprocessing이 적합하다.

* 외부 CLI program을 GUI application에서 실행해야 하는 경우
* CPU-bound 작업을 여러 core에서 실제 병렬로 수행해야 하는 경우
* 작업 실패나 crash가 main GUI process에 직접 영향을 주지 않도록 분리해야 하는 경우
* 독립적인 worker program을 실행하고, 표준 출력이나 file, socket 등을 통해 결과를 받아야 하는 경우

PyQt와 PySide에서는 `QProcess`를 이용하여 외부 program을 실행하고, 해당 process의 standard output, standard error, 종료 상태 등을 signal을 통해 처리할 수 있다. 이를 이용하면 GUI application은 외부 process를 실행하면서도 main event loop를 block하지 않고 계속 반응성을 유지할 수 있다.

이 장에서는 먼저 multithreading을 통해 Qt application의 반응성을 유지하는 방법을 살펴보고, 이어서 multiprocessing을 통해 독립된 다른 program을 Qt application에서 실행하는 방법을 소개한다.

---

---


## 참고: Python built-in thread와 Qt thread의 차이

Python은 built-in으로 thread를 지원한다.  
Python standard library의 `threading` module을 사용하면 다음과 같이 별도의 thread를 만들 수 있다.

```python
import threading


def worker():
    print("worker thread")


t = threading.Thread(target=worker)
t.start()
t.join()
```

즉, PyQt나 PySide를 사용하지 않더라도 Python 자체만으로 multithreading을 구현할 수 있음.

하지만 Qt 기반 GUI application에서는 Python의 `threading.Thread`보다 `QThread`, `QRunnable`, `QThreadPool`을 사용하는 경우가 많다. 

* 이유는 Qt의 GUI 구조가 event loop, signal-slot mechanism, `QObject`의 thread affinity와 밀접하게 연결되어 있기 때문이다.
* Python의 `threading.Thread`는 일반적인 Python code를 별도 thread에서 실행하는 데 적합하다. 
* 반면 `QThread`와 `QRunnable`은 Qt object, Qt event loop, signal-slot 구조와 연동되는 background 작업을 구현하는 데 적합하다.

> 특히 ***GUI widget은 반드시 GUI thread에서 생성되고 수정*** 되어야 한다. 
> 
> * 따라서 worker thread에서 작업을 수행한 뒤, 결과를 GUI에 반영해야 하는 경우에는 
> Qt의 signal-slot mechanism을 이용하는 것이 안전하다. 

이런 이유로 PyQt나 PySide 기반 GUI program에서는 Python built-in thread보다 Qt에서 제공하는 threading class를 사용하는 방식이 더 자연스럽다.

정리하면 다음과 같다.

| 구분                | Python `threading.Thread`    | Qt `QThread`, `QRunnable`, `QThreadPool`   |
| ----------------- | ---------------------------- | ------------------------------------------ |
| 제공 위치             | Python standard library      | Qt framework                               |
| 주된 목적             | 일반 Python code의 thread 실행    | Qt application과 연동되는 background 작업         |
| GUI 연동            | 직접 처리해야 함                    | signal-slot mechanism과 자연스럽게 연동            |
| event loop 연동     | Qt event loop와 직접 연동되지 않음    | Qt event loop와 연동 가능                       |
| GUI widget update | 직접 하면 위험함                    | signal을 통해 GUI thread에서 처리하는 구조 권장         |
| 사용 상황             | 일반 I/O 작업, 간단한 background 작업 | PyQt/PySide GUI application의 worker thread |

따라서 일반 Python program에서는 `threading.Thread`를 사용할 수 있지만, PyQt나 PySide 기반 GUI program에서는 `QThread`, `QRunnable`, `QThreadPool`을 사용하는 것이 보통 더 적합하다.

