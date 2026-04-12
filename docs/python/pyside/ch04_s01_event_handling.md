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

* 사용자가 마우스를 클릭함
* 키보드 키를 누름
* 창이 다른 창에 가려졌다가 다시 나타남
* 타이머가 만료됨
* 네트워크 데이터가 도착함

이런 모든 사건들이 event임. GUI application은 이 event들에 반응하면서 동작함.

---

## Event Loop - GUI application의 심장

### Event Loop가 필요한 이유

일반적인 프로그램은 위에서 아래로 순차적으로 실행되고 종료됨. 하지만 GUI application은 다름.

* 사용자가 언제 버튼을 클릭할지, 언제 키를 누를지 알 수 없음.
* 아무 일도 없을 때는 대기하다가 event가 발생하면 즉시 반응해야 함.
* 이를 위해 GUI application은 종료 신호가 올 때까지 계속 "event가 있는지 확인하고 처리"하는 **무한 반복 루프** 를 실행함.

이 무한 반복 루프가 바로 **Event Loop** 임.

### Event Loop의 시작

Qt application에서 event loop는 아래 코드로 시작됨.

```python
app = QApplication(sys.argv)
wnd = MW()
sys.exit(app.exec())  # 여기서 event loop 시작 - 종료 신호가 올 때까지 블로킹됨
```

* `app.exec()`는 event loop를 시작하며, **application이 종료될 때까지 반환되지 않음**.
* 창을 닫거나 `QApplication.quit()`가 호출되면 event loop가 종료되고 `exec()`가 반환됨.
* `sys.exit(app.exec())`는 event loop 종료 시 반환되는 종료 코드를 OS에 전달함.

### Event Loop의 동작 원리

Event loop는 background에서 아래와 같은 과정을 반복함.

```
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

**자주 사용되는 `QEvent` subclass**

| Class | 설명 |
|---|---|
| `QMouseEvent` | 마우스 클릭 / 이동 / 휠 관련 event |
| `QKeyEvent` | 키보드 입력 관련 event |
| `QPaintEvent` | widget 화면 갱신 관련 event |
| `QResizeEvent` | 창 크기 변경 관련 event |
| `QCloseEvent` | 창 닫기 관련 event |
| `QTimerEvent` | 타이머 만료 관련 event |

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

> [동기 처리 및 비동기 처리에 대한 참고자료](https://ds31x.tistory.com/655)
---

## Event Handling vs Signals and Slots

Qt는 event를 처리하는 두 가지 방법을 제공함.

### Event Handling

Qt가 제공하는 event handler method를 override하여 원하는 동작을 구현하는 방식.

```python
class MW(QWidget):

    def mousePressEvent(self, event):
        """마우스 클릭 시 Qt가 자동으로 호출하는 event handler."""
        print(f"클릭 위치: {event.position()}")
```

* widget에서 특정 event가 발생하면 Qt가 자동으로 해당 handler를 호출함.
* low-level 처리이므로 custom widget 개발 등에서 사용됨.

### Signals and Slots

Qt 고유의 객체 간 통신 메커니즘. 내부적으로 event handling을 사용하지만, 개발자가 event mechanism을 직접 다루지 않아도 됨.

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

즉, Signals and Slots가 동기 처리만 가능하다는 것은 사실이 아님. connection type에 따라 동기/비동기 처리가 모두 가능함.

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
 
