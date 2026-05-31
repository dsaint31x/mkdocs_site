---
title: QThread와 QRunnable의 차이
tags: [GUI, Qt, PySide6, PyQt, Thread, Multithreading, QThread, QRunnable, QThreadPool, Event Loop]
---

# QThread와 QRunnable의 차이

`QThread`와 `QRunnable`은 모두 PyQt와 PySide에서 multithreading을 구현할 때 사용되는 class임.

다만 두 class의 역할은 서로 다르다.

* `QThread`는 하나의 thread 자체를 관리하기 위한 class임.
* `QRunnable`은 thread에서 실행될 하나의 job 또는 task를 표현하기 위한 class임.
* `QRunnable`은 일반적으로 `QThreadPool`에 의해 실행되며, thread의 생성과 재사용은 `QThreadPool`이 담당함.

즉, `QThread`는 thread 자체를 직접 다루는 방식에 가깝고, `QRunnable`은 thread pool에 맡길 작업 단위를 정의하는 방식에 가깝다.

# QThread

## Thread 자체를 다루는 class

`QThread`는 Qt에서 thread를 다루기 위한 class임.

`QThread` instance는 별도의 thread 실행을 시작하고, 해당 thread의 시작, 종료, event loop 등을 제어할 수 있도록 해준다.

다만 정확히는 `QThread` 객체 자체가 곧바로 “새 thread 안에 존재하는 객체”가 되는 것은 아님. `QThread` 객체는 보통 이를 생성한 GUI thread에 속해 있고, `start()`가 호출될 때 새로운 native thread가 만들어진다. 이 새 thread에서 `QThread.run()`이 실행된다.

이 점 때문에 `QThread`를 사용할 때는 다음 두 가지 방식을 구분해야 한다.

1. `QThread`를 상속받고 `run()` method를 override하는 방식
2. `QObject` 기반 worker를 만든 뒤 `moveToThread()`로 worker를 별도 thread로 옮기는 방식

## 1. QThread를 상속받는 방식

가장 직접적인 방식은 `QThread`를 상속받고, `run()` method를 override하는 것임.

```python
class WorkerThread(QThread):
    def run(self):
        # 별도 thread에서 수행할 작업
        ...
```

이 방식에서는 `run()` method 안에 실제 수행할 작업을 작성한다. `start()`가 호출되면 Qt가 새로운 thread를 만들고, 그 thread 안에서 `run()` method를 실행한다.

이 방식은 비교적 단순한 background 작업에는 사용할 수 있다. 예를 들어 별도의 event loop가 필요 없고, 한 번 실행한 뒤 끝나는 계산 작업이나 I/O 작업이라면 `run()` override 방식으로도 충분할 수 있다.

하지만 이 방식은 다음과 같은 점에 주의해야 한다.

* `run()` 안에서 직접 오래 걸리는 작업을 수행하면 해당 thread의 event loop는 따로 돌지 않음.
* `run()` 안에서 `exec()`를 호출해야 해당 thread 내부의 event loop가 동작함.
* `QThread` object 자체는 보통 GUI thread에 속해 있으므로, `QThread` 객체에 slot을 만들고 이를 worker thread에서 실행된다고 가정하면 안 됨.
* 복잡한 signal-slot 기반 작업에는 `QObject` worker를 `moveToThread()`로 옮기는 방식이 더 적합한 경우가 많음.

즉, `QThread`를 상속받아 `run()`을 override하는 방식은 가능하지만, Qt에서 항상 권장되는 유일한 방식은 아님.

## 2. 참고: QObject worker를 moveToThread()로 옮기는 방식

Qt에서 자주 사용되는 또 다른 방식으로, 실제 작업을 수행하는 `QObject` 기반 worker class를 만들고 이를 `moveToThread()`로 별도 thread에 옮기는 방법이 있다.

이 방식은 실무에서 널리 사용되지만, 본 문서에서는 `QThread`와 `QRunnable`의 차이를 설명하는 것이 목적이므로 참고 수준으로만 소개한다. 이후 내용과 정리 표에서는 주로 `QThread`를 상속하여 `run()`을 구현하는 방식과 `QRunnable`을 중심으로 설명한다.

Qt에서 자주 사용되는 다른 방식은 실제 작업을 수행하는 `QObject` 기반 worker class를 만들고, 이 worker object를 `QThread`로 이동시키는 것임.

구조는 다음과 같다.

```python
# QThread 객체 생성 
# 실제 작업을 수행하는 스레드(작업 공간)를 만든다. 
thread = QThread() 

# 작업을 담당할 Worker 객체 생성 
# Worker 안에는 시간이 오래 걸리는 작업(run 메서드)이 들어 있다고 가정한다. 
worker = Worker() 

# Worker 객체를 새로 만든 스레드로 이동 
# moveToThread()를 호출하지 않으면 Worker는 기본적으로 메인(UI) 스레드에서 동작한다. 
# 따라서 별도 스레드에서 작업하려면 반드시 Worker를 해당 스레드로 옮겨야 한다. 
worker.moveToThread(thread) 

# 스레드가 시작되면 Worker의 run() 메서드를 실행 
# thread.start()가 호출되면 started 시그널이 발생하고, 
# 그 시그널이 worker.run에 연결되어 작업이 시작된다. 
thread.started.connect(worker.run) 

# Worker 작업이 끝나면 스레드 종료 
# Worker의 run() 내부에서 finished 시그널을 emit한다고 가정한다. 
# quit()은 스레드의 이벤트 루프를 종료하도록 요청한다. 
worker.finished.connect(thread.quit) 

# Worker 작업이 끝나면 Worker 객체 삭제 예약 
# deleteLater()는 즉시 삭제하지 않고 안전한 시점에 객체를 제거한다. 
# 메모리 누수를 방지하기 위해 자주 사용하는 패턴이다. 
worker.finished.connect(worker.deleteLater) 

# 스레드가 완전히 종료되면 QThread 객체도 삭제 예약 
# 사용이 끝난 스레드 객체를 정리하여 메모리를 해제한다. 
thread.finished.connect(thread.deleteLater) 

# 스레드 시작 
# 내부적으로 새로운 스레드가 생성되고, 
# started 시그널이 발생하면서 worker.run()이 실행된다. 
thread.start()

```

이 방식에서는 `QThread`는 thread의 실행 환경을 제공하고, 실제 작업은 `Worker` object가 담당한다.

이 구조의 장점은 다음과 같음.

* 작업 객체와 thread 관리 객체를 분리할 수 있음.
* worker의 signal과 slot을 Qt 방식으로 명확하게 구성할 수 있음.
* 작업 완료 후 `finished` signal을 통해 thread 종료와 object 정리를 연결하기 쉬움.
* GUI thread와 worker thread 사이의 통신을 signal-slot mechanism으로 안전하게 처리하기 좋음.

따라서 PyQt나 PySide에서 비교적 복잡한 background 작업을 구현할 때는 `QThread`를 직접 상속하는 방식보다, `QObject` worker를 만들고 `moveToThread()`를 사용하는 방식이 더 명확한 경우가 많다.

## 명시적인 thread 관리

`QThread`를 사용하는 경우 개발자는 thread의 생명주기를 비교적 명시적으로 관리해야 한다.

대표적으로 다음과 같은 처리가 필요하다.

* `QThread` instance 생성
* worker object 생성
* worker object를 thread로 이동
* `start()` 호출
* 작업 완료 signal 처리
* `quit()` 또는 `exit()`를 통한 event loop 종료
* `wait()`를 통한 thread 종료 대기
* `deleteLater()` 등을 이용한 object 정리

이처럼 `QThread`는 직접 관리해야 할 부분이 많다.  

때문에 그만큼 코드량은 증가하지만, thread의 시작 시점, 종료 시점, event loop 사용 여부, worker object의 수명 등을 세밀하게 제어할 수 있다는 장점이 있다.

## 상대적으로 많은 resource 사용

각 `QThread`는 실제 native thread와 연결된다. 따라서 많은 수의 `QThread`를 계속 생성하면 thread stack, scheduling, context switching 비용 등이 증가할 수 있다.

몇 개의 장시간 worker thread를 명시적으로 관리하는 경우에는 `QThread`가 적절하다. 하지만 짧은 작업이 많이 발생하는 경우에는 매번 `QThread`를 새로 만들고 제거하는 방식이 비효율적일 수 있다.

이런 경우에는 `QThreadPool`과 `QRunnable`을 사용하는 방식이 더 적합하다.

## 구현 복잡성

`QThread`는 thread를 세밀하게 제어할 수 있다는 장점을 가진다.

하지만 이 장점은 동시에 구현 복잡성으로 이어진다. 특히 다음 사항을 잘못 처리하면 문제가 발생하기 쉽다.

* worker thread에서 GUI widget을 직접 수정하는 경우
* worker object나 `QThread` object가 아직 사용 중인데 먼저 삭제되는 경우
* `quit()`를 호출했지만 event loop가 돌고 있지 않아 기대한 방식으로 종료되지 않는 경우
* signal-slot 연결 방향과 객체가 어느 thread에 속해 있는지(object affinity), 그리고 signal이 어떤 thread에서 어떤 방식으로 전달되는지(직접 호출인지 queued connection인지)를 잘못 이해한 경우
* thread를 강제로 종료하여 resource 정리가 깨지는 경우

따라서 `QThread`는 

* 자유도가 높은 대신, 
* thread와 object의 수명 관리를 정확히 이해하고 사용해야 한다.

# QRunnable

## Thread가 실행할 job을 표현하는 class

`QRunnable`은 thread 자체가 아니라, thread에서 실행될 하나의 job 또는 task를 표현하는 class임.

`QRunnable`은 기본적으로 `run()` method를 제공하며, 개발자는 이 `run()` method를 override하여 실제 수행할 작업을 작성한다.

```python
class WorkerTask(QRunnable):
    def run(self):
        # thread pool의 worker thread에서 수행할 작업
        ...
```

여기서 중요한 점은 `QRunnable`이 thread를 직접 생성하거나 관리하지 않는다는 것이다. `QRunnable`은 어디까지나 “실행할 작업”을 나타내며, 실제 thread 관리는 `QThreadPool`이 담당한다.

## QThreadPool을 통한 실행

`QRunnable`은 일반적으로 `QThreadPool`에 전달되어 실행된다.

```python
pool = QThreadPool.globalInstance()
task = WorkerTask()
pool.start(task)
```

`QThreadPool`은 내부적으로 여러 worker thread를 관리하며, `QRunnable` task가 들어오면 사용 가능한 thread에서 해당 task의 `run()` method를 실행한다.

이 방식의 핵심은 thread를 매번 새로 만들지 않는다는 점임. Thread pool에 이미 존재하는 thread를 재사용하므로, thread 생성과 소멸에 따른 overhead를 줄일 수 있다.

따라서 짧은 작업이 많이 발생하거나, 비슷한 형태의 background task를 반복적으로 처리해야 하는 경우에 `QRunnable`과 `QThreadPool` 조합이 유리하다.

## 상대적으로 간단한 사용법

`QRunnable`은 기본 구조가 단순하다.

개발자는 `run()` method에 수행할 작업을 정의하고, 이를 `QThreadPool.start()`에 넘기면 된다. Thread의 생성, 재사용, 대기열 관리 등은 `QThreadPool`이 담당한다.

따라서 다음과 같은 작업에 적합하다.

* 짧고 독립적인 background task
* 여러 개가 반복적으로 발생하는 작업
* thread의 생명주기를 직접 제어할 필요가 없는 작업
* thread pool에서 제한된 수의 worker thread로 처리하고 싶은 작업

예를 들어 여러 image file을 background에서 읽거나, 여러 network 요청을 병렬적으로 처리하거나, 다수의 작은 preprocessing task를 처리하는 경우에 사용할 수 있다.

## 제한적인 제어

`QRunnable`은 사용법이 간단한 대신, `QThread`처럼 개별 thread를 세밀하게 제어하기는 어렵다.

`QRunnable`은 특정 thread를 직접 소유하지 않는다. 어떤 thread에서 실행될지는 `QThreadPool`이 결정한다. 따라서 개발자가 특정 `QRunnable`에 대해 다음과 같은 제어를 직접 수행하기는 어렵다.

* 특정 thread의 event loop 제어
* 특정 thread의 정확한 시작과 종료 시점 관리
* thread-local한 장기 상태 유지
* 복잡한 signal-slot 기반 worker object 수명 관리
* 개별 thread의 세밀한 종료 처리

다만 `QThreadPool` 차원에서 일부 설정은 가능하다. 예를 들어 최대 thread 개수, thread expiry timeout, task priority 등은 `QThreadPool`을 통해 조절할 수 있다.

즉, `QRunnable`은 개별 thread를 제어하는 도구라기보다, thread pool에 맡길 작업 단위를 정의하는 도구로 보는 것이 정확하다.

## Signal 사용 시 주의점

`QRunnable`은 `QObject`을 상속한 class가 아니므로, 그 자체로 Qt signal을 정의하고 사용하기 어렵다.

따라서 `QRunnable`에서 작업 진행률이나 완료 결과를 GUI thread로 전달하려면, 별도의 `QObject` 기반 signal helper를 함께 사용하는 방식이 자주 사용된다.

예를 들면 다음과 같은 구조를 사용할 수 있다.

```python
class WorkerSignals(QObject):
    finished = Signal()
    result = Signal(object)
    error = Signal(tuple)
    progress = Signal(int)
```

그리고 `QRunnable` 내부에서 이 signal object를 생성하여, 작업 진행률이나 결과를 GUI thread로 전달한다.

이 구조를 사용하면 `QRunnable`의 단순함을 유지하면서도, GUI thread와 안전하게 통신할 수 있다.

# 사용 상황에 따른 선택

## QThread 사용이 적합한 경우

`QThread`는 thread의 생명주기를 세밀하게 제어해야 하는 경우에 적합하다.

대표적으로 다음과 같은 경우에 사용하기 좋다.

* 장시간 유지되는 worker thread가 필요한 경우
* worker object의 signal-slot 구조가 복잡한 경우
* thread 내부에서 event loop가 필요한 경우
* 작업 시작, 중지, 종료 과정을 명확하게 제어해야 하는 경우
* 하나의 thread 안에서 지속적으로 상태를 유지해야 하는 경우
* background service처럼 계속 살아 있는 작업을 구성해야 하는 경우

즉, `QThread`는 “thread 자체를 명시적으로 관리해야 하는 경우”에 적합하다.

## QRunnable 사용이 적합한 경우

`QRunnable`은 비교적 짧고 독립적인 작업을 많이 처리해야 하는 경우에 적합하다.

대표적으로 다음과 같은 경우에 사용하기 좋다.

* 짧은 background task가 반복적으로 발생하는 경우
* 여러 작업을 thread pool에 맡기고 싶은 경우
* thread의 생명주기를 직접 관리할 필요가 없는 경우
* 작업 단위가 서로 독립적인 경우
* thread 생성과 소멸 overhead를 줄이고 싶은 경우
* 제한된 수의 worker thread로 여러 작업을 효율적으로 처리하고 싶은 경우

즉, `QRunnable`은 “thread를 직접 관리하기보다, 실행할 task를 thread pool에 맡기는 경우”에 적합하다.

# 정리

`QThread`와 `QRunnable`은 모두 PyQt와 PySide에서 multithreading을 구현할 때 사용되지만, 관점이 다르다.

`QThread`는 thread 자체를 명시적으로 관리하는 방식이고, `QRunnable`은 `QThreadPool`에 맡길 task를 정의하는 방식임.

따라서 다음과 같이 구분할 수 있다.

| 구분          | QThread                                 | QRunnable + QThreadPool        |
| ----------- | --------------------------------------- | ------------------------------ |
| 핵심 역할       | thread 자체 관리                            | thread pool에서 실행될 task 정의      |
| 실행 방식       | `start()`로 thread 시작                    | `QThreadPool.start()`로 task 실행 |
| 작업 정의       | `run()` override 또는 `QObject` worker 사용 | `run()` override               |
| thread 관리   | 개발자가 비교적 명시적으로 관리                       | `QThreadPool`이 관리              |
| resource 사용 | thread마다 별도 관리 필요                       | 기존 thread 재사용 가능               |
| 제어 수준       | 높음                                      | 제한적                            |
| 구현 복잡도      | 상대적으로 높음                                | 상대적으로 낮음                       |
| 적합한 작업      | 장시간 작업, 복잡한 worker, event loop 필요 작업    | 짧고 독립적인 다수의 task               |

결론적으로, 복잡하고 장시간 유지되는 background 작업에는 `QThread`가 적합하고, 짧고 독립적인 task를 여러 개 처리해야 하는 경우에는 `QRunnable`과 `QThreadPool` 조합이 적합하다.

이어지는 절에서는 먼저 `QThread`를 이용하여 GUI thread와 worker thread를 분리하는 기본 구조를 살펴본다.
