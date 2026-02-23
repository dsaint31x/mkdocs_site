---
title: QApplication
tags: [pyside6, pyqt6, QApplication, event-loop, gui]
---

# QApplication

`QtWidgets.QApplication` class는 PyQt 또는 PySide로 만들어진 GUI Application의 **제어 흐름(Control Flow)** 과 **주요 설정(Settings)** 을 관리하는 핵심 클래스이다.

GUI Application은 여러 개의 Window나 Dialog로 구성될 수 있지만, 이를 총괄하는 **`QApplication` 인스턴스는 반드시 오직 하나만 생성** 되어야 한다.

이 인스턴스는 다음과 같은 중요한 역할을 수행한다.

*   **초기화 및 종료**: 애플리케이션의 시작과 끝을 관리한다.
*   **Event Loop 처리**: 사용자 입력(키보드, 마우스 등)이나 시스템 이벤트를 감지하고 적절한 위젯으로 전달한다.
*   **시스템 설정 감지**: 시스템의 테마, 폰트, 시간 설정 등의 변경을 감지하고 반영한다.

---

## Event Loop와 exec()

모든 GUI 애플리케이션은 **Event-Driven(이벤트 구동)** 방식으로 동작한다. 즉, 프로그램이 실행되면 종료될 때까지 무한히 대기하면서 사용자의 입력을 기다린다.

`QApplication` 인스턴스의 `exec()` 메서드를 호출하면 **Event Loop** 가 시작된다.

1.  **Event Loop 시작**: `app.exec()`가 호출되는 순간, 프로그램은 Event Loop에 진입하여 대기 상태가 된다.
2.  **이벤트 감지 및 분배**: 사용자가 버튼을 클릭하거나 키보드를 누르면, OS는 이를 이벤트로 만들어 애플리케이션의 **Event Queue** 에 넣는다. Event Loop는 이 큐에서 이벤트를 하나씩 꺼내어 적절한 위젯(Event Handler)에게 전달한다.
3.  **종료**: 사용자가 창을 닫거나 종료 명령을 내리면 `exec()` 메서드는 종료 코드를 반환하며 루프를 빠져나온다.

### 코드 예시

일반적으로 다음과 같은 구조로 작성된다.

```python
import sys
from PySide6.QtWidgets import QApplication, QMainWindow

# 1. QApplication 인스턴스 생성 (sys.argv를 전달하여 명령행 인수 처리)
app = QApplication(sys.argv)

# 2. 메인 윈도우 생성 및 표시
window = QMainWindow()
window.show()

# 3. Event Loop 시작 및 종료 코드 처리
# app.exec()는 이벤트 루프를 실행하고, 종료 시 상태 코드를 반환함.
# sys.exit()는 이 코드를 받아 프로그램을 안전하게 종료함.
sys.exit(app.exec())
```

> **참고 (Python 2.x와의 차이)**
> 
> 과거 Python 2.x 시절에는 `exec`가 예약어(keyword)였기 때문에, 충돌을 피하기 위해 `exec_()`라는 이름의 메서드를 사용했었다.
> 하지만 Python 3.x에서는 `exec`가 예약어가 아니므로, `exec()`를 사용하는 것이 표준이다. (호환성을 위해 `exec_()`도 여전히 존재하긴 한다.)

보다 자세한 내용은 [Event Handling Mechanism](https://wikidocs.net/187284)을 참고하라.