---
title: Qt Event와 Event Handling
description: PyQt/PySide6에서의 Event 추상화, Event Loop 동작 원리, 전달 방식 종류(Spontaneous/Posted/Sent), Signals and Slots과의 비교.
tags:
  - Qt
  - PySide6
  - PyQt6
  - event
  - event handling
  - event loop
  - signal
  - slot
  - QEvent
date: 2025-04-12
---

# Qt에서 Event와 Event Handling

## Event란?

GUI application에서 **event** 란 사용자 또는 시스템에서 발생하는 모든 종류의 "사건"을 의미함.

흔한 예를 들면 다음과 같음:

* 사용자가 마우스를 클릭함
* 키보드 키를 누름
* 창이 다른 창에 가려졌다가 다시 나타남
* 타이머가 만료됨
* 네트워크 데이터가 도착함

GUI application은 이 event들에 반응하면서 동작함.

조금 더 일반적인 관점에서 event를 설명한다면, event는 프로그램을 수행할 때 프로그램 내부/외부에 존재하며 상호작용하는 관련된 객체 들간의 상호작용의 단위(?) 라고 볼 수 있다.

> 즉, Event는 프로그램의 내/외부에서 발생하는 상태 변화의 notification unit (통지 단위) 이라고 생각해도 된다.

* 앞의 설명에서 *객체(object)* 는 OS의 서비스일 수도 있고, 프로그램 사용자일 수도 있으며, 프로그램 내부의 특정 class의 instance, 또는 다른 스레드일 수도 있다.
* 이들이 상호작용하여 프로그램이 수행되는 것이며,
* 이들 상호작용에서 어떤 사건(=프로그램의 상태가 변경되어야 하는 사건)이 발생할 때를 event가 발생했다 고 한다.

> 상호작용 과정에서 특정 상호작용(=사건=상태변화)이 발생함을 전달하는 단위가 event 임.

좀 더 구체적인 예를 들면 다음과 같음:

* 메모장 프로그램 상에서 사용자가 출력 버튼을 누르는 경우, **출력 이벤트** 가 발생 했다고 볼 수 있고,
* 사용자가 컴퓨터를 종료하려고 종료버튼을 누를 경우, 동작 중인 메모장 프로그램이 종료해야한다는 메시지를 **OS로부터 받게 되는 것** 도 일종의 이벤트가 발생한 것이라고 할 수 있다.

---

## Event Loop - GUI application의 심장

### Event Loop가 필요한 이유

일반적인 프로그램은 위에서 아래로 순차적으로 실행되고 종료됨.  

하지만 GUI application은 다름.

* 사용자가 언제 버튼을 클릭할지, 언제 키를 누를지 알 수 없음.
* 아무 일도 없을 때는 대기하다가 event가 발생하면 즉시 반응해야 함.
* 이를 위해 GUI application은 종료 신호가 올 때까지 계속 "event가 있는지 확인하고 처리"하는 **무한 반복 루프** 를 실행함.

이 무한 반복 루프가 바로 **Event Loop** 임.

### Event Loop의 시작

Qt application에서 event loop는 아래와 같은 코드로 시작됨:

```Python
app = QApplication(sys.argv)
wnd = MW()
sys.exit(app.exec())  # 여기서 event loop 시작 - 종료 신호가 올 때까지 블로킹됨
```

* `app.exec()`는 event loop를 시작하며, **application이 종료될 때까지 반환되지 않음**.
* 창을 닫거나 `QApplication.quit()`가 호출되면 event loop가 종료되고 `exec()`가 반환됨.
* `sys.exit(app.exec())`는 event loop 종료 시 반환되는 종료 코드를 OS에 전달함.

### Event Loop의 동작 원리

Event loop는 background에서 아래와 같은 과정을 반복함.

```Python
while (!exit) {

    while (!posted_event_queue_is_empty) {   // 1. Posted event 처리
        process_next_posted_event();
    }

    while (!spontaneous_event_queue_is_empty) {  // 2. Spontaneous event 처리
        process_next_spontaneous_event();
    }

    while (!posted_event_queue_is_empty) {   // 3. 2번 처리 중 새로 생긴 Posted event 처리
        process_next_posted_event();
    }

}
```

위는 일종의 pseudo code로 event loop의 동작을 기술하고 있음.  
`QApplication` 객체의 `exec()` 메서드가 호출되는 순간부터 다음이 반복됨.

1. Qt의 event loop 가 동작하기 시작 하여
2. 대기 queue에 있는 events를 pop하고,
3. 해당 popped events 의 처리를 시작시킴.
4. 이는 해당 `QApplication`의 객체가 종료될 때까지 반복됨.

> 참고로, PyQt Application에서 `QApplication` instance는 하나만 생성 되며, 오직 하나의 event loop만 반복실행된다.


**주의 - Event Loop를 블로킹하면 안 됨**

* Event loop는 한 번에 하나의 event만 처리함.
* slot 등에서 오래 걸리는 작업(예: 대용량 파일 읽기, 네트워크 요청)을 수행하면 그동안 event loop가 멈춤.
* Event loop가 멈추면 UI가 응답하지 않아 **화면이 굳어버리는(freezing) 현상** 이 발생함.
* 오래 걸리는 작업은 별도의 thread(`QThread`)로 분리하는 것을 권장함.

---

## Event 추상화 - `QEvent`

Qt는 event를 `QEvent` class로 추상화하며, event 종류에 따라 subclass를 제공함.

**Event 발생 및 전달 흐름**

1. event가 발생하면 Qt는 해당 event를 추상화한 `QEvent` subclass의 instance를 생성함.
2. event의 종류에 따라 전달 방식이 다르지만, 최종적으로 처리 대상 `QObject` instance의 `event()` method를 통해 전달됨.
3. `event()` method는 event를 직접 처리하지 않고, event type에 따라 적절한 **event handler** 를 호출함.

> Qt의 Widget들은  
>
> * 자신의 기능에 따라 적절한 `event()` 메서드가 구현되어 있으며
> * 이를 통해 **이미 구현되어 제공되는 Event Handler들과 연결** 이 되어 있다.

**자주 사용되는 `QEvent` subclass**

| Class | 설명 |
|---|---|
| `QMouseEvent` | 마우스 클릭 / 이동 / 휠 관련 event |
| `QKeyEvent` | 키보드 입력 관련 event |
| `QPaintEvent` | widget 화면 갱신 관련 event |
| `QResizeEvent` | 창 크기 변경 관련 event |
| `QCloseEvent` | 창 닫기 관련 event |
| `QTimerEvent` | 타이머 만료 관련 event |

**Qt의 Widget에 구현된 기본 handlers**

| Event Handler  | 발생 시점 | 전달되는 Event 객체  | 설명  |
| --- | --- | --- | --- |
| `paintEvent()`      | widget을 다시 그려야 할 때            | `QPaintEvent`  | `QPainter`를 이용한 custom drawing을 구현할 때 사용함. |
| `mousePressEvent()` | mouse button을 눌렀을 때           | `QMouseEvent`  | click 위치, button 종류 등을 확인할 때 사용함.   |
| `keyPressEvent()`   | keyboard key를 눌렀을 때           | `QKeyEvent`    | 특정 key 입력이나 shortcut 처리를 구현할 때 사용함. |
| `resizeEvent()`     | widget 크기가 변경되었을 때            | `QResizeEvent` |  새 크기에 맞춰 내부 상태나 drawing 영역을 갱신할 때 사용함.     |
| `closeEvent()`      | widget 또는 window가 닫히려 할 때     | `QCloseEvent`  | 닫기 허용 여부를 결정하거나 저장 확인 dialog를 띄울 때 사용함.     |
| `focusInEvent()`    | widget이 keyboard focus를 얻었을 때 | `QFocusEvent`  | focus 표시나 입력 상태 초기화에 사용함.      |

이 Event Handler를 override하여 re-implementation 하면

* 해당 Widget 에서의 관련 event 에 대한 동작이 완전히 변경됨을 의미한다.
* 높은 수준의 Customized Widgets가 이 방식을 이용하여 구현된다.

---

## Event 전달 방식 종류

Qt에서 event는 전달 방식에 따라 아래 세 가지로 나뉨.

| 종류 | 발생 주체 | 처리 방식 | 설명 |
|---|---|---|---|
| **Spontaneous event** | OS | 비동기 | OS가 발생시키며, system queue에 push됨. event loop에 의해 pop되어 처리됨 |
| **Posted event** | Qt / application | 비동기 | Qt가 관리하는 queue에 push됨. event loop에 의해 pop되어 처리됨 |
| **Sent event** | Qt / application | 동기 | 발생 즉시 처리 대상 object로 전달되어 동기 처리됨 |

**Spontaneous event의 대표적인 예**

* `QMouseEvent`, `QKeyEvent` - OS의 mouse / keyboard interrupt에서 비롯됨.

**비동기 처리의 장점 - Compressible event**

* 특정 widget의 update가 연속으로 여러 번 발생하는 경우, 비동기 처리에서는 다시 그려야 할 영역의 합집합을 대상으로 **한 번의 update로 합쳐지는 최적화** 가 가능함.
* 이런 event들을 **Compressible event** 라고 부르며, paint event / move event 등이 해당됨.

> **참고자료**  
> 
> * [동기 처리 및 비동기 처리에 대한 참고자료](https://ds31x.tistory.com/655)

---

## Event Handling vs Signals and Slots

Qt는 event를 처리하는 두 가지 방법을 제공함.

### Event Handling

Qt가 제공하는 event handler method를 override하여 원하는 동작을 구현하는 방식.

다음은 마우스의 버튼이 눌려질 대 발생하는 이벤트를 처리하는 `mousePressEvent()` 이벤트 핸들러를 override 하는 단순한 예제임:

```python
class MW(QWidget):

    def mousePressEvent(self, event):
        """마우스 클릭 시 Qt가 자동으로 호출하는 event handler."""
        print(f"클릭 위치: {event.position()}")
```

* widget에서 특정 event가 발생하면 Qt가 자동으로 해당 handler를 호출함.
* low-level 처리이므로 custom widget 개발 등에서 사용됨.

앞서 설명한대로 Event별로 처리하는 Event Handler (실제로 widget의 method) 들은
해당 Event가 발생한 Widget의 특정 메서드로서 미리 메서드 이름 이 정해져 있다.  
Event Handling은 이들을 override를 하기 때문에 Event Handler의 이름과 parameters등을 지정하고 있는 header를 변경해선 안 됨.

> 참고로, C++에서는 `virtual function` 으로 Event Handler들이 제공되므로  
> 개발자는 원하는 Event를 처리할 수 있는 virtual function을 제공하는 class를 상속받아  
> 이를 구현하는 형태로 Event Handling을 한다.  
> `virtual function`은 C++에서 runtime polymorphism (or dynamic polymorphism)을 위해 제공된 기능으로 "컴파일 시간에 어떤 함수가 호출될지 결정되는 일반 Member function"의 override와 달리, **runtime에 호출될 실제 함수가 결정되는 특징** 을 가짐. C++에서 `virtual`이라는 키워드를 통해 명시적으로 선언하여 지정됨.  
> Python은 method를 호출할 때(즉, runtime)에 객체의 실제 타입을 확인하고 그에 해당하는 method를 동적으로 찾아내기 때문에 기본적으로 C++ virtual function과 유사하게 모든 method가 동작한다고 보면 됨.

### Signals and Slots

Qt 고유의 객체 간 통신 메커니즘.  

* `signal`은 특정 상태 변화나 action 발생을 알리는 notification이고,
* `slot`은 해당 signal에 반응하여 실행되는 method 임.

Signals and Slots는 Qt의 meta-object system을 기반으로 동작하며,
개발자가 `QEvent`, `event()`, `event handler`를 직접 다루지 않고도
object 간 통신 및 GUI Application에서의 event처리 등을 구현할 수 있게 해줌.

다음은 `QPushButton` 객체인 `button`의 `clicked` signal에 대한 slot으로  같은 클래스에 구현된 메서드 `on_button_clicked`를 지정하는 간단한 예제임:

```python
button.clicked.connect(self.on_button_clicked)
```

* 구현이 단순하고 직관적임.
* 객체 간 loosely coupling을 유지하면서 효과적인 정보 교환이 가능함.
* 일반적인 GUI application 개발에서는 signals and slots만으로도 충분한 경우가 대부분임.

### 동기 / 비동기 처리 비교

Event Handling과 Signals and Slots의 동기/비동기 처리 방식을 비교하면 아래와 같음.

| 방식 | 처리 방식 |
|---|---|
| Event Handling (Spontaneous / Posted) | 비동기 |
| Event Handling (Sent) | 동기 |
| Signals and Slots (Direct connection, 같은 thread) | 동기 |
| Signals and Slots (Queued connection, 다른 thread) | 비동기 |

보통 간단한 예제 프로그램의 signals and slots 에서 event 처리가 동기적인 경우(Direct connection)가 많으나, 비동기 처리가 되는 경우도 있음에 주의할 것.

emit이 이루어진 object와 slot이 있는 object가 다른 스레드에 속할 경우엔, emit 의 결과로 `QMetaCallEvent` object가 생성되고 이는 posted event queue에 push 되어 비동기 처리 가 된다.

> Qt는 signal을 emit한 현재 thread와 receiver object가 속한 thread를 기준으로 direct/queued를 결정함.
> 엄밀히 애기하면 이는 `connect()`에서 connect type을 지정하지 않은 경우를 가리키는 `Qt.ConnectionType.AutoConnection`의 경우에 해당하는 설명임.  
> `connect()` 할 때, connect type 를 명시적으로 지정(`type`키워드 인자로)가능함:
>
> * `Qt.ConnectionType.AutoConnection`
> * `Qt.ConnectionType.DirectConnection`
> * `Qt.ConnectionType.QueuedConnection`

즉, Signals and Slots의 경우, connection type에 따라 동기/비동기 처리가 모두 가능함.

* 일반적인 direct connection에서는 signal을 emit한 시점에 slot이 즉시 호출됨.
    * event loop에서 처리하는 queue를 사용하지 않음.
    * 함수 호출처럼 현재 call stack에서 바로 실행됨.

* 반면 queued connection에서는 slot 호출 요청이 receiver thread의 event queue에 등록되고,
  receiver thread의 event loop에 의해 나중에 실행됨.
    * Qt 내부적으로는 posted event 형태로 처리됨.
    * main thread의 event loop가 아니라 receiver object가 속한 thread의 event loop에서 처리됨.
    * 단, receiver object가 main thread에 속해 있으면 main thread의 event loop에서 처리됨.

> 일반적인 GUI application에서는 connect type을 생략해도 되고, thread를 넘나드는 통신에서 동작 방식을 명확히 제어하고 싶을 때만 명시하면 충분함.

### 어떤 방식을 선택할까?

**Signals and Slots 권장 상황**

* 버튼 클릭, 텍스트 변경 등 일반적인 GUI 상호작용 처리.
* 객체 간 통신이 필요한 경우.
* 대부분의 GUI application 개발에서는 이 방식으로 충분함.

**Event Handling 권장 상황**

* custom widget 개발 - widget의 painting, mouse/keyboard 동작을 직접 제어해야 하는 경우.
* Qt의 기본 event 처리 동작을 세밀하게 override해야 하는 경우.

---

## References

* [Another Look at Events - Qt Quarterly](https://doc.qt.io/archives/qq/qq11-events.html)
    * [위의 pdf인쇄본](https://blog.kakaocdn.net/dna/V48Cl/btrXbDmG2ua/AAAAAAAAAAAAAAAAAAAAAEqnLEysrJWg5SoU4lx1N_m6sosEQPzj0wSUvobxxZJq/Another%20Look%20at%20Events.pdf?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1777561199&allow_ip=&allow_referer=&signature=2rOkhL3%2FRtyWmMjcYFrmM%2B9w7o8%3D&attach=1&knm=tfile.pdf)
 
