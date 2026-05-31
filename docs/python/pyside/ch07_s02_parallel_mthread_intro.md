---

title: GUI 프로그램에서 Multithreading이 필요한 이유
tags: [GUI, Qt, PySide6, PyQt, Thread, Multithreading, QThread, QThreadPool, QRunnable, Event Loop]
---------------------------------------------------------------------------------------------------

# GUI 프로그램에서 Multithreading이 필요한 이유

앞서 설명했던 것처럼, PyQt나 PySide와 같은 GUI framework에서 multithreading이 필요한 주된 이유는 **GUI의 반응성을 유지하기 위해서** 임.

* GUI를 갖는 application은 사용자가 발생시키는 event를 지연 없이 처리하여, 
* 사용자의 입력에 최대한 즉각적으로 반응해야 한다. 

이를 위해 GUI application에서는 

* 일반적으로 main thread, 즉 GUI thread가 event loop를 실행하면서 
* user input, paint event, timer event, window event 등을 처리한다.

문제는 **시간이 오래 걸리는 작업이 GUI thread에서 수행될 경우 발생** 한다.  

* GUI thread가 해당 작업을 처리하느라 event loop로 돌아오지 못하면, 
* 사용자의 입력이나 화면 갱신 event가 제때 처리되지 않는다. 
* 이 경우 GUI가 멈춘 것처럼 보이거나, OS에 의해 “응답 없음” 상태로 표시될 수 있다.

Multithreading은 이러한 문제를 줄이기 위한 대표적인 방법임. 

* 시간이 오래 걸리는 작업을 GUI thread가 아닌 별도의 worker thread에서 수행하도록 분리하면, 
* GUI thread는 계속해서 event loop를 돌며 사용자의 입력과 화면 갱신을 처리할 수 있다.

## 1. 반응성 유지

GUI application의 주 thread, 즉 **GUI thread는 event loop를 실행하며 사용자의 입력을 처리하고 화면을 update한다.**

만약 이 thread에서 시간이 오래 걸리는 작업을 직접 실행하면, GUI thread가 event loop를 정상적으로 처리하지 못하게 된다. 그 결과 button click, keyboard input, mouse event, window repaint 등이 지연되며, application이 멈춘 것처럼 보일 수 있다.

이는 사용자에게 해당 program이 정상 동작 중인지 확인하기 어렵게 만들며, 결과적으로 나쁜 UX를 제공하게 된다.

Multithreading을 사용하면 시간이 오래 걸리는 작업을 별도의 worker thread에서 처리할 수 있다.  
이를 통해 main event loop가 계속 원활히 동작하도록 만들 수 있으며, GUI는 작업 수행 중에도 사용자 입력에 반응할 수 있다.

## 2. 효율적인 자원 사용

현대의 computer system은 대부분 multicore processor를 사용한다. 따라서 여러 작업을 동시에 수행할 수 있는 hardware 기반은 이미 갖추어져 있음.

* 다만 Python 기반의 PyQt 또는 PySide application에서는 이 부분을 구분해서 이해해야 한다. 
* Python의 Global Interpreter Lock(GIL) 때문에, 
* 순수 Python code로 작성된 CPU-bound 작업은 multithreading만으로 여러 core를 완전히 활용하는 병렬 계산 성능 향상을 얻기 어렵다.

따라서 PyQt나 PySide에서 **multithreading은 다음과 같은 경우에 더 현실적인 이점** 을 가진다.

* **GUI thread와 worker thread를 분리** 하여 GUI 반응성을 유지하는 경우
* file I/O, network I/O, database 접근처럼 대기 시간이 긴 I/O-bound 작업을 처리하는 경우
* **C/C++로 구현되어 내부적으로 GIL을 release하는 library 작업을 수행** 하는 경우
* 작업의 진행 상태를 signal-slot mechanism을 통해 GUI thread로 전달해야 하는 경우

즉, Python GUI application에서 multithreading의 핵심 목적은 단순히 계산 속도를 높이는 것이 아니라, **GUI thread를 block하지 않도록 작업을 분리** 하는 데 있음.

> CPU-bound 작업을 실제로 여러 core에서 병렬 수행해야 한다면,  
> `multiprocessing`이나 `QProcess`를 이용한 별도 process 실행이 더 적합하다고 볼 수 있음.

## 3. 비동기 작업 수행

Networking, 대용량 file 처리, database query, image loading, preprocessing 등은 **GUI application에서 비동기적으로 수행하는 것이 적합한 작업들** 임.

* 이러한 작업을 GUI thread에서 직접 수행하면 작업이 끝날 때까지 event loop가 block될 수 있다. 
* 반면 multithreading을 사용하면 해당 작업을 background에서 실행하고, 
* 작업의 진행 상태나 완료 결과를 main thread에 전달하는 구조로 구현할 수 있다.

PyQt와 PySide에서는 일반적으로 이같은 작업들은 worker thread에서 작업을 수행하고, 결과는 signal을 통해 GUI thread로 전달하는 것이 좋다.  
이후 GUI thread에서 slot을 통해 label, progress bar, button, text widget 등의 GUI widget을 update한다.

이 구조를 사용하면 사용자는 작업이 수행되는 동안에도 GUI를 조작할 수 있고, program은 진행률 표시나 취소 button 등을 통해 더 나은 UX를 제공할 수 있다.

> 주의할 점은 **worker thread에서 GUI widget을 직접 수정하지 않는 것임**. 
> 
> * GUI widget의 생성과 수정은 원칙적으로 GUI thread에서 수행해야 하며, 
> * worker thread는 data 처리와 I/O 작업만 담당하고 
> * GUI 갱신은 signal-slot을 통해 GUI thread에 맡기는 방식이 권장된다.

## 4. Timeout 및 취소 가능한 작업

GUI에서 수행되는 작업이 지나치게 긴 실행 시간을 요구하거나, network 지연 또는 외부 장치 응답 지연 등으로 인해 **사용자가 실행 도중 작업을 취소해야 하는 경우** 가 있을 수 있다.

Multithreading을 사용하면 이러한 작업을 GUI thread와 분리하여 관리할 수 있다. 

* 예를 들어 worker thread에서 장시간 작업을 수행하게 하고, 
* GUI thread에서는 cancel button, timeout timer, progress dialog 등을 통해 사용자의 조작을 계속 받을 수 있다.

다만 **thread를 강제로 종료하는 방식은 일반적으로 권장되지 않는다**. 

* Thread를 무리하게 중단하면 
* resource 정리, lock 해제, file close, shared data consistency 등에 문제가 발생할 수 있기 때문이다.

따라서 PyQt나 PySide에서는 

* 보통 **worker object 내부에 cancel flag** 를 두고, 
* 작업 중간중간 해당 flag를 확인하여 안전하게 종료하는 
* ***cooperative cancellation*** 방식을 사용한다. 

Timeout이 필요한 경우에도 

* `QTimer` 등을 사용하여 
* 일정 시간 후 cancel signal을 보내고, 
* worker thread가 이를 확인하여 스스로 종료되도록 구성하는 방식이 안전하다.

즉, multithreading은 

* 작업을 "쉽게 강제 종료"하기 위한 수단이라기보다, 
* 긴 작업을 GUI thread와 분리하고, 
* 취소나 timeout을 처리할 수 있는 구조를 만들기 위한 수단으로 이해하는 것이 적절하다.

# 구현 방법

PyQt나 PySide에서 multithreading을 구현하는 방법은 크게 다음 두 가지로 나눌 수 있다.

1. `QThread` class를 사용하는 방법
2. `QRunnable`과 `QThreadPool`을 사용하는 방법

`QThread`는 

* 독립적인 thread를 만들고, 
* 해당 thread에서 worker object를 실행하는 방식에 적합하다. 
* 작업의 수명 관리가 필요하거나, 
* signal-slot을 통해 진행 상태와 결과를 명확히 주고받아야 하는 경우에 자주 사용된다.

`QRunnable`과 `QThreadPool`은 

* 짧은 작업이나 반복적으로 발생하는 background task를 thread pool에서 처리할 때 적합하다. 
* **매번 thread를 새로 만들지 않고, thread pool에 작업을 맡기는 방식** 이므로 
* **많은 수의 작은 작업을 처리할 때 유리** 하다.

각 방식은 application의 요구사항과 작업의 성격에 따라 선택될 수 있지만, 공통적인 목적은 동일하다. 

> 시간이 오래 걸리는 작업을 GUI thread에서 분리하여 main event loop가 block되지 않도록 만드는 것임.

GUI application에서 multithreading을 적절히 사용하는 것은 사용자 경험을 크게 향상시키고, application의 구조를 안정적으로 만드는 데 중요한 역할을 한다. 

이어지는 절에서는 `QThread`를 이용하는 방법과 `QThreadPool`을 이용하는 방법을 순서대로 살펴본다.
