---
title: Qt Event Handling 구현 및 예제
description: PySide6에서의 Event Handler overriding, Event Loop 동작, Spontaneous/Posted/Sent Event 전달 방식별 실용 예제(keyPressEvent, paintEvent, closeEvent).
tags:
  - Qt
  - PySide6
  - PyQt6
  - event
  - event handling
  - event handler
  - event loop
  - QKeyEvent
  - QCloseEvent
  - paintEvent
  - update
  - close
date: 2025-04-12
---

# Event Handling 구현

Event별로 처리를 담당하는 ***Event Handler*** 는  
<u>해당 Event가 발생한 Widget의 특정 method</u>로,  
***method 이름이 미리 정해져*** 있음.

---

개발자는 Event Handling을 다음과 같이 수행:

* 해당 event의 handler에 해당하는 method를 ***overriding*** 하여
* ***해당 Event 발생 시의 처리를 reimplement*** 하거나,
* 해당 method 내부에서 `if-else` 구문을 통해 **원하는 기능만 추가하는 방식** 으로 구현함.

> overriding이므로  
> method의 이름과 parameter 등을 규정하는 ***header(=signature)는 변경할 수 없음***.

예를 들어, keyboard key가 눌렸을 때 호출되는 Event Handler는 다음과 같이 정해져 있음.

```python
def keyPressEvent(self, event):
    ...
```

다음과 같이 method의 이름을 임의로 바꾸거나 parameter를 제거하면,  
Qt는 이를 key press event handler로 인식하지 못함.

```python
# 잘못된 예: Qt가 인식하지 못함.
def key_press_event(self):
    ...
```

즉, Event Handling은 개발자가 임의의 method를 만들어 연결하는 방식이 아니라,  
***Qt가 미리 정해둔 Event Handler method를 subclass에서 overriding*** 하는 방식임.

---

Event Handler를 overriding한다고 해서  
항상 모든 동작을 완전히 새로 작성해야 하는 것은 아님.

* 필요한 조건만 직접 처리하고,  
* 나머지는 ***parent class의 기본 Event Handler*** 로 넘기는 방식도 자주 사용됨.

```python
def keyPressEvent(self, event):
    if event.key() == Qt.Key.Key_Escape:
        self.close()
        return  # ESC key는 직접 처리.

    # 그 외의 key event는 parent class의 기본 처리에 위임.
    super().keyPressEvent(event)
```

이 방식은 기존 widget의 기본 동작을 유지하면서  
특정 event에 대한 기능만 추가할 때 유용함.

---

이러한 이유로,  
자주 사용되는 Event와 해당 Event Handler를 짝지어 정리해두는 것이 좋음.

---

---

## Event Loop

`QApplication`의 `exec()` method를 호출하면  
Qt의 ***Event Loop가 시작*** 됨.

Event Loop는 다음을 반복 수행함:

* 대기 queue에서 event를 꺼내고 (pop),
* 해당 event를 target object에 dispatch하여 처리시킴.

이 loop는 해당 `QApplication` instance가 종료될 때까지 반복됨.

이 때문에 PySide6 application에서 `QApplication` instance는 일반적으로 ***하나만 생성*** 되며,  
main GUI thread에서는 ***하나의 main Event Loop*** 가 동작함.

> 단, worker thread에서도 별도의 event loop를 실행할 수 있음.  
> 따라서 "event loop가 하나뿐이다"라는 표현은 **main GUI thread 기준** 으로 이해해야 함.

## Event 전달 방식별 처리 흐름

Event 전달 방식에 따라 Event Handling의 흐름이 달라짐.

### Spontaneous Event

* OS / window system에서 발생한 native event(mouse, keyboard, window expose 등)에서 비롯됨.
* 해당 event는 OS의 **system event queue** (예: Windows Message Queue, X11 Event Queue, macOS Cocoa Event Queue)에 먼저 저장됨.
* Qt의 `QAbstractEventDispatcher`가 이 system event queue에서 native event를 가져옴.
* Qt는 이를 적절한 `QEvent` subclass instance로 변환하여 target object에 전달함.
* 이때 target object의 `event()` method가 먼저 호출되고, `event()` 내부에서 event type에 따라 정해진 Event Handler(예: `keyPressEvent()`, `paintEvent()` 등)로 dispatch됨.

### Posted Event

* Qt 내부 또는 application code에서 ***posted event queue*** 에 등록된 뒤 나중에 처리됨.
* 비동기적 처리가 이루어짐: 등록 시점과 처리 시점이 분리되어 있음.
* Event Loop가 posted event queue에서 해당 event를 꺼낼 때 처리됨.
* 일부 event는 처리 전에 ***compression(압축)*** 이 이루어질 수 있음.
    * 대표적으로 paint event의 경우, 여러 번 요청된 repaint를 하나로 합쳐 처리할 수 있음.

### Sent Event

* queue에 넣어지지 않고 ***곧바로 처리*** 됨.
* 동기적 처리: 호출한 코드의 실행 흐름 안에서 즉시 Event Handler가 실행됨.
* Event Handler의 처리가 끝난 뒤에야 호출 측으로 제어가 돌아옴.

---

| 구분 | 발생 주체 | queue 사용 여부 | 처리 시점 |
|:---|:---|:---:|:---|
| Spontaneous Event | OS / window system | 사용 | Event Loop가 입력 event를 dispatch할 때 |
| Posted Event | Qt / application | 사용 | Event Loop가 queue에서 꺼내 처리할 때 |
| Sent Event | Qt / application | 사용 안 함 | 호출 흐름 안에서 즉시 |

> Qt의 Event Handling mechanism에 대해 보다 자세한 내용은 다음 문서를 참고할 것.
>
> * [Another Look at Events](https://doc.qt.io/archives/qq/qq11-events.html)
> * [Events and Filters for Qt](https://doc.qt.io/qt-6/eventsandfilters.html)

---

---

## 예제

앞서 살펴본 event 전달 방식에 맞추어  
다음 세 가지 예제를 살펴볼 것임.

| 구분 | 예제 상황 | 사용 Event | Event Handler |
|:---|:---|:---|:---|
| Spontaneous Event | 실제 keyboard 입력으로 window 닫기 | `QKeyEvent` | `keyPressEvent()` |
| Posted Event | `update()` 호출에 의한 repaint | paint event | `paintEvent()` |
| Sent Event | `close()` 호출에 의한 닫기 요청 | `QCloseEvent` | `closeEvent()` |

### 예제 1: Spontaneous Event

다음 코드는 사용자가 실제 keyboard에서 `ESC` key를 누르면 window를 닫는 예제임.

Keyboard 입력은 OS / window system에서 발생한 native event에서 비롯됨.  
Qt는 이를 `QKeyEvent`로 변환하고,  
현재 keyboard focus를 가진 widget에 전달함.

따라서 이 예제는 대표적인 ***Spontaneous Event*** 처리 예제임.

```python
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow


class MW(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setGeometry(100, 100, 360, 200)
        self.setWindowTitle("Spontaneous Event Ex")

        label = QLabel(
            """
            <p>
                Press the <b>ESC</b> key
                to quit this program.
            </p>
            """
        )

        self.setCentralWidget(label)

    def keyPressEvent(self, event):
        """
        key press event를 처리하는 Event Handler.

        사용자가 실제 keyboard key를 누르면,
        OS / window system에서 native key event가 발생하고,
        Qt는 이를 QKeyEvent로 변환하여 이 method로 전달함.
        """

        if event.key() == Qt.Key.Key_Escape:
            print("ESC key pressed by real keyboard input.")
            self.close()
            return

        # ESC 이외의 key event는 parent class의 기본 처리에 위임.
        super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    sys.exit(app.exec())
```

위 코드의 흐름은 다음과 같음.

1. 사용자가 실제 keyboard에서 `ESC` key를 누름.
2. OS / window system에서 native key event가 발생함.
3. Qt가 이를 `QKeyEvent`로 변환함.
4. 현재 keyboard focus를 가진 widget의 `keyPressEvent(self, event)`가 호출됨.
5. `event.key()`를 통해 어떤 key가 눌렸는지 확인함.
6. `ESC` key이면 `self.close()`를 호출하여 window를 닫음.

> Keyboard key에 대한 event는 `QKeyEvent`가 추상화하고 있으며,  
> 해당 instance는 현재 keyboard focus를 가진 widget에 전달됨.
>
> * key를 누르는 경우의 Event Handler: `keyPressEvent()`
> * key를 떼는 경우의 Event Handler: `keyReleaseEvent()`
>
> 두 Event Handler 모두 `QKeyEvent` instance를 argument로 받으며,  
> `QKeyEvent.key()` method는 눌린 key를 나타내는 `Qt.Key` enum 값을 반환함.

### 예제 2: Posted Event

다음 코드는 button을 누를 때마다 원의 위치를 바꾸고,  
`update()`를 호출하여 widget을 다시 그리도록 요청하는 예제임.

이 예제에서 명심할 점은 다음과 같음:

* ***`update()`가 `paintEvent()`를 즉시 호출하지 않는다*** 는 것임.
* `update()`는 "이 widget은 다시 그려져야 한다"는 repaint request를 Qt에 등록함.  
* 이 request는 Event Loop에 의해 나중에 처리되며,  그 결과로 `paintEvent()`가 호출됨.

> 이같은 처리 방식이 일반적인 이유는 GUI 어플리케이션에서 하나의 사용자 동작이 여러 상태 변경을 연속으로 일으키는 경우가 많기 때문임.
>
> 예를 들어 button 하나를 눌렀을 때
>
> * 내부 data가 변경되고
> * 여러 widget의 표시 값이 바뀌고
> * layout이나 drawing 영역도 함께 갱신될 수 있음.
>
> 이때 상태가 하나 바뀔 때마다 즉시 `repaint`를 수행하면, 아직 최종 상태가 되기 전의 중간 상태까지 모두 그리게 됨.
> 결국 사용자가 실제로 볼 필요가 없는 화면을 여러 번 그리는 셈이므로 불필요한 drawing 비용이 발생함.
> 
> `update()`는 이런 문제를 피하기 위해 즉시 `repaint`를 수행하지 않고, "나중에 다시 그려야 함"이라는 repaint request만 등록함.
> 이후 Event Loop가 여러 repaint request를 모아 처리하면, widget은 최종 상태를 기준으로 한 번만 그려질 수 있음.
>
> 따라서 `update()`를 사용하면 중간 상태에 대한 불필요한 drawing을 줄이고, GUI가 입력 처리와 화면 갱신 사이에서 더 안정적으로 응답성을 유지할 수 있음.

즉, `update()`는 실무에서 가장 자주 만나는 ***Posted Event 계열 흐름*** 중 하나임.

```python
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Canvas(QWidget):
    def __init__(self):
        super().__init__()

        self.circle_x = 50
        self.circle_y = 60
        self.radius = 20

        # QWidget이 그림을 그릴 영역을 가지도록 최소 크기 지정.
        self.setMinimumSize(320, 180)

    def move_circle(self):
        """
        원의 위치를 변경한 뒤 update()를 호출함.

        update()는 paintEvent()를 즉시 호출하지 않음.
        repaint request를 event queue에 등록하고,
        Event Loop가 나중에 paintEvent()를 호출하게 함.
        """

        # 1. 원의 x좌표를 이동시킴.
        self.circle_x += 20

        if self.circle_x > 280:
            self.circle_x = 50

        # 2. repaint request를 등록함.
        print("[1] before update()")
        self.update()
        print("[2] after update()")
        print("[3] paintEvent() has not necessarily been called yet")

    def paintEvent(self, event):
        """
        widget을 다시 그려야 할 때 Qt가 호출하는 Event Handler.

        update()에 의해 등록된 repaint request가
        Event Loop에서 처리되면 이 method가 호출됨.
        """

        print("[4] paintEvent() called")

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.drawText(
            10,
            20,
            "Click the button. update() schedules paintEvent().",
        )

        painter.drawEllipse(
            self.circle_x - self.radius,
            self.circle_y - self.radius,
            self.radius * 2,
            self.radius * 2,
        )


class MW(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setWindowTitle("Posted Paint Event Ex")
        self.resize(380, 260)

        self.canvas = Canvas()
        self.button = QPushButton("Move Circle")

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.button.clicked.connect(self.canvas.move_circle)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    sys.exit(app.exec())
```

실행 후 button을 누르면 console 출력은 다음과 같은 순서를 보임.

* `[1] before update()` 출력
* `[2] after update()` 출력 : `update()`가 repaint 전에 먼저 return함.
* `[3] paintEvent() has not necessarily been called yet` 출력
* `[4] paintEvent() called` 출력 : Event Loop가 나중에 처리함.

핵심은 `[2] after update()`가 `[4] paintEvent() called`보다 ***먼저*** 출력된다는 점임.

즉, `update()`는 painting을 즉시 수행하지 않음.  
Widget을 다시 그려야 한다는 request만 Qt에 등록하고 바로 return함.  
실제 painting은 Event Loop가 나중에 처리함.

위 코드의 흐름은 다음과 같음.

1. Button click으로 `move_circle()`이 호출됨.
2. `self.circle_x` 값을 변경함.
3. `self.update()`를 호출하여 repaint request를 등록함.
4. `update()`는 즉시 return함.
5. Event Loop가 나중에 paint event를 처리함.
6. Qt가 `paintEvent(self, event)`를 호출함.
7. `QPainter`를 이용하여 변경된 위치에 원을 그림.

다시 강조하지만, 
`update()`가 실용적인 이유는 다음과 같음.

* GUI에서 data나 상태가 바뀐 뒤 화면을 다시 그릴 때 가장 흔히 사용됨.
* 여러 번 `update()`가 호출되어도 Qt가 repaint 요청을 합쳐서(compression) 처리할 수 있음.
* 따라서 불필요한 중복 drawing을 줄일 수 있음.
* Custom widget을 만들 때 `paintEvent()`와 함께 거의 항상 등장하는 패턴임.

#### 참고: `update()` vs. `repaint()`

반면 `repaint()`는 성격이 다름.

```python
self.repaint()
```

`repaint()`는 내부적으로 `QWidget::sendEvent()`를 사용하여  
paint event를 ***동기적으로 즉시 전달*** 함.  
따라서 `repaint()`를 호출하면 그 호출 흐름 안에서 곧바로 `paintEvent()`가 실행됨.

이는 `repaint()`가 ***Sent Event 방식*** 으로 동작한다는 것을 의미함.

| Method | 전달 방식 | 처리 시점 | 특징 |
|:---|:---|:---|:---|
| `update()` | Posted Event (비동기) | Event Loop가 나중에 처리 | compression 가능, 일반적으로 권장됨 |
| `repaint()` | Sent Event (동기) | 호출 즉시 `paintEvent()` 실행 | compression 불가, 즉시 갱신이 필요한 경우에만 사용 |
| `paintEvent()` | — | — | 실제 drawing code를 작성하는 Event Handler |

일반적인 GUI code에서는 `repaint()`보다 ***`update()`를 우선적으로 사용*** 하는 것이 권장됨.

### 예제 3: Sent Event

다음 코드는 간단한 문서 편집기 형태의 window에서  
`Close Window` button을 누르면 `self.close()`를 호출하는 예제임.

`close()`는 widget을 바로 닫는 단순 함수가 아님.  
해당 widget에 `QCloseEvent`를 ***동기적으로 전달*** 하고,  
`closeEvent(self, event)`를 호출함.

이때 `closeEvent()` 안에서

* `event.accept()`를 호출하면 window가 닫힘.
* `event.ignore()`를 호출하면 window 닫기가 취소됨.

즉, `closeEvent()`는 실제 application에서 다음과 같은 상황에 자주 사용됨.

* 저장하지 않은 내용이 있을 때 닫기 전 확인
* 종료 전 resource 정리
* Background 작업 중 종료 방지
* System tray로 숨기고 실제 종료는 막기

이 예제에서는 `close()` 호출로 인해 `QCloseEvent`가 즉시 전달되고,  
`closeEvent()`가 실행되는 흐름을 ***Sent Event*** 의 실용적 예로 다룸:

```python
import sys

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MW(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setWindowTitle("Sent Close Event Ex")
        self.resize(420, 220)

        self.label = QLabel(
            "Close Window button을 누르면 self.close()가 호출됨.\n"
            "self.close()는 QCloseEvent를 발생시키고,\n"
            "closeEvent(self, event)가 즉시 호출됨."
        )

        self.unsaved_checkbox = QCheckBox(
            "Unsaved changes가 있다고 가정"
        )
        self.unsaved_checkbox.setChecked(True)

        self.close_button = QPushButton("Close Window")
        self.close_button.clicked.connect(self.request_close)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.unsaved_checkbox)
        layout.addWidget(self.close_button)
        self.setLayout(layout)

    def request_close(self):
        """
        Sent Event 흐름을 보여주는 method.

        close()를 호출하면 QWidget은 QCloseEvent를 생성하여
        현재 widget의 closeEvent()로 즉시 전달함.
        queue를 거치지 않고 호출 흐름 안에서 바로 처리됨.
        """

        print("[1] before self.close()")
        closed = self.close()
        print("[3] after self.close()")
        print(f"[4] close result: {closed}")

    def closeEvent(self, event: QCloseEvent):
        """
        window가 닫히려 할 때 호출되는 Event Handler.

        사용자가 title bar의 X button을 눌러도 호출되고,
        code에서 self.close()를 호출해도 호출됨.
        """

        print("[2] closeEvent() called")

        if self.unsaved_checkbox.isChecked():
            reply = QMessageBox.question(
                self,
                "Confirm Close",
                "저장하지 않은 변경 사항이 있음.\n"
                "정말 닫겠는가?",
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            if reply == QMessageBox.StandardButton.Yes:
                print("close accepted")
                event.accept()
            else:
                print("close ignored")
                event.ignore()

            return

        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    sys.exit(app.exec())
```

실행 후 `Close Window` button을 누르고,  
확인 dialog에서 `Yes`를 선택하면 console 출력은 다음과 같음.

* `[1] before self.close()` 출력
* `[2] closeEvent() called` 출력 : `close()` 호출 흐름 안에서 즉시 실행됨.
* `close accepted` 출력
* `[3] after self.close()` 출력 : `closeEvent()` 처리가 끝난 뒤 return함.
* `[4] close result: True` 출력

핵심은 `[2] closeEvent() called`가 `[3] after self.close()`보다 ***먼저*** 출력된다는 점임.

즉, `self.close()`는 

* 닫기 요청을 queue에 넣고 나중에 처리하는 방식이 아니라,  
* 호출 흐름 안에서 `QCloseEvent`를 전달하고  
* `closeEvent()`의 처리 결과를 확인한 뒤 return함.

확인 dialog에서 `No`를 선택하면 다음과 같은 흐름이 됨.

* `[1] before self.close()` 출력
* `[2] closeEvent() called` 출력
* `close ignored` 출력
* `[3] after self.close()` 출력
* `[4] close result: False` 출력

이 경우 `event.ignore()`가 호출되므로 window는 닫히지 않음.

위 코드의 흐름을 정리하면 다음과 같음.

1. 사용자가 `Close Window` button을 누름.
2. `request_close()` method가 호출됨.
3. `self.close()`가 호출됨.
4. Qt가 `QCloseEvent`를 생성하여 현재 widget에 즉시 전달함.
5. 현재 widget의 `closeEvent(self, event)`가 호출됨.
6. 저장하지 않은 변경 사항이 있다고 판단되면 확인 dialog를 띄움.
7. 사용자가 `Yes`를 선택하면 `event.accept()`로 닫기를 허용함.
8. 사용자가 `No`를 선택하면 `event.ignore()`로 닫기를 취소함.
9. `closeEvent()` 처리가 끝난 뒤 `self.close()`가 return함.

## `update()`와 `close()`의 차이

Posted Event와 Sent Event의 차이는  
호출 전후의 출력 순서를 비교하면 명확해짐.

`update()`의 경우 (Posted Event):

* `[1] before update()` 출력
* `[2] after update()` 출력 ← `update()`가 먼저 return함.
* `[3] paintEvent() has not necessarily been called yet` 출력
* `[4] paintEvent() called` 출력 ← Event Loop가 나중에 처리함.

`update()`는 repaint request를 등록하고 바로 return함.  
실제 painting은 나중에 이루어짐.

`close()`의 경우 (Sent Event):

* `[1] before self.close()` 출력
* `[2] closeEvent() called` 출력 ← `close()` 호출 흐름 안에서 즉시 실행됨.
* `[3] after self.close()` 출력 ← `closeEvent()` 처리가 끝난 뒤 return함.
* `[4] close result: True` 출력

`close()`는 `QCloseEvent`를 즉시 전달하고,  
`closeEvent()`의 처리 결과에 따라 window를 닫을지 결정한 뒤 return함.

## 정리

| 구분 | Spontaneous Event | Posted Event | Sent Event |
|:---|:---|:---|:---|
| 발생 주체 | OS / window system | Qt / application | Qt / application |
| 예제 | 실제 keyboard 입력 | `update()`에 의한 repaint request | `close()`에 의한 close request |
| 사용 API | 직접 호출하지 않음 | `update()` | `close()` |
| queue 사용 | OS 입력 queue 경유 | Qt posted event queue 사용 | queue 사용 안 함 |
| 처리 시점 | Event Loop가 입력 event를 dispatch할 때 | Event Loop가 repaint request를 처리할 때 | 호출 흐름 안에서 즉시 |
| 처리 방식 | 비동기 | 비동기 | 동기 |
| 사용 Event | `QKeyEvent` | paint event | `QCloseEvent` |
| Event Handler | `keyPressEvent()` | `paintEvent()` | `closeEvent()` |

---

* 사용자의 실제 keyboard 입력처럼 OS에서 비롯된 event는 ***Spontaneous Event*** 흐름으로 처리됨.
* Widget의 상태가 바뀐 뒤 `update()`를 호출하면 repaint request가 등록되고, Event Loop에 의해 나중에 `paintEvent()`가 호출됨.
* `close()`를 호출하면 `QCloseEvent`가 즉시 전달되고, `closeEvent()`에서 닫기 허용 여부를 결정할 수 있음.
* Posted Event와 Sent Event의 차이는 event class 자체보다 ***전달 방식과 처리 시점*** 에 있음.
* Event Handling의 핵심은 `keyPressEvent()`, `paintEvent()`, `closeEvent()` 같은 Event Handler를 subclass에서 overriding하여 원하는 동작을 구현하는 것임.