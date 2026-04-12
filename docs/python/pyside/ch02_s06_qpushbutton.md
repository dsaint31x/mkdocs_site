---
title: QPushButton Widget
description: 사용자 클릭 입력을 받는 대표적인 Qt Button Widget. Signals and Slots 개념 및 주요 Methods 포함.
tags:
  - Qt
  - PySide6
  - PyQt6
  - QPushButton
  - QAbstractButton
  - widget
  - GUI
  - signal
  - slot
date: 2025-04-12
---

# `QPushButton` Widget

**module** : `QtWidgets`

GUI에서 사용자로부터 입력을 받는 대표적인 button widget.

* 사용자가 마우스로 click (또는 손가락으로 터치)하면 `clicked` signal을 emit하여 정해진 task를 수행하게 함.
* `QAbstractButton` class의 subclass임.
* text 또는 icon으로 버튼의 용도를 사용자에게 표시함.

공식 문서:

* Qt6 C++ : [https://doc.qt.io/qt-6/qpushbutton.html](https://doc.qt.io/qt-6/qpushbutton.html)
* PySide6 : [https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QPushButton.html](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QPushButton.html)

---

## Signals and Slots 간단 소개

Qt 고유의 event 처리 메커니즘으로, 객체 간의 통신을 위해 고안됨.

**동작 순서**

1. 사용자 입력 등 event가 발생하면 widget이 해당 **signal** 을 emit함.
2. signal에 미리 연결(connect)해둔 **slot** 이 호출됨.
3. slot은 개발자가 구현한 method 또는 function으로, event 발생 시 수행할 task를 담고 있음.

**Signal**

* widget이 특정 event가 발생했음을 알리는 알림(notification).
* signal의 종류에 따라 추가 데이터를 slot에 argument로 전달하기도 함.
* widget의 signal 외에 개발자가 custom signal을 직접 정의할 수도 있음.

**Slot**

* signal의 receiver(수신자 / handler).
* Python 및 PyQt의 built-in function도 slot으로 사용 가능함.
* 동일한 signal에 여러 slot을 연결할 수 있으며, 하나의 slot이 여러 signal에 연결될 수도 있음.

**Signal 연결 방법**

```python
# button의 clicked signal에 button_clicked 메서드를 slot으로 연결
button.clicked.connect(self.button_clicked)
```

* `self`는 slot이 속한 main window instance를 가리킴.
* signal을 발생시킨 widget과 다른 객체의 method도 slot으로 사용 가능함.

**여러 signal에 하나의 slot 연결 시**

* `self.sender()`로 signal을 emit한 widget instance를 확인할 수 있음.

---

## 주요 Signals

| Signal | 발생 조건 | Slot 전달 인자 |
|---|---|---|
| `clicked(checked)` | 버튼이 클릭될 때 (press 후 release 완료) | `bool` (checkable 버튼인 경우 checked 상태) |
| `pressed` | 버튼이 눌릴 때 (press 시점) | 없음 |
| `released` | 버튼이 release될 때 | 없음 |
| `toggled(checked)` | checkable 버튼의 상태가 변경될 때 | `bool` |

**`clicked` vs `pressed` / `released`**

* `clicked` - press 후 release까지 완료된 시점에 emit됨. 일반적인 버튼 클릭 처리에 사용함.
* `pressed` / `released` - press와 release를 각각 별도로 처리해야 하는 경우에 사용함.

---

## 주요 Methods

| Method | 설명 |
|---|---|
| `QPushButton(text, parent)` | text와 parent widget을 인자로 받아 instance 생성 |
| `setText(str)` | 버튼에 표시될 text 설정 |
| `text()` | 현재 버튼의 text를 반환 |
| `setIcon(QIcon)` | `QtGui.QIcon` instance로 버튼의 icon 설정 |
| `setIconSize(QSize)` | `QtCore.QSize` instance로 icon 크기 고정 |
| `setEnabled(bool)` | `False`이면 버튼을 disabled 상태로 설정 - 사용자 입력 불가 |
| `resize(w, h)` | 버튼 크기 재설정 (`QWidget`에서 상속) |
| `adjustSize()` | 현재 설정된 text에 맞게 버튼 크기를 자동으로 재조정 |

**Icon 설정 상세**

Icon이란 GUI에서 해당 동작을 사용자가 직관적으로 인식할 수 있게 해주는 작은 이미지로, 버튼이나 메뉴 항목의 symbol에 해당함. Tool bar 등에서 특히 많이 사용됨.

`setIcon()` - `QtGui.QIcon` instance를 인자로 전달하여 버튼의 icon을 설정함.

```python
from PySide6.QtGui import QIcon

self.push_button.setIcon(QIcon("img/icon.png"))
```

* image 경로는 `os.path` 또는 `pathlib.Path`를 이용하여 current working directory에 무관하게 처리하는 것을 권장함.
* 참고: [os 모듈을 통한 file 및 directory 처리](https://ds31x.tistory.com/25)

`setIconSize()` - `QtCore.QSize` instance로 icon의 크기를 고정함. resize 관련 이슈를 방지하기 위해 icon은 고정 크기로 사용하는 경우가 많음.

```python
from PySide6.QtCore import QSize

self.push_button.setIconSize(QSize(30, 30))
```

**런타임에서의 동적 변경**

* `setIcon()`과 `setIconSize()`는 초기화 시뿐만 아니라 runtime에서 특정 event 발생 시 호출하여 icon 이미지와 크기를 동적으로 변경하는 것도 가능함.

---

## Example - text / icon / text+icon 버튼 비교

`QWidget`을 상속한 main window에 `QLabel` 1개와 `QPushButton` 3개를 배치한 예제.

* **icon + text 버튼** - `setIcon()`과 text를 함께 사용.
* **icon 전용 버튼** - text 없이 `setIcon()` + `setIconSize()`만 사용.
* **text 전용 버튼** - icon 없이 text만 사용.
* 각 버튼의 `clicked` signal에 slot을 연결 - 클릭 시 `QLabel`의 text가 변경됨.
* `hello_label`은 slot에서 접근해야 하므로 `self.hello_label`로 instance attribute로 생성함.
* image 경로는 `os.path`로 스크립트 위치 기준으로 계산함.
* PySide6 우선으로 import하고, 없으면 PyQt6로 fallback 처리함.

```python
# ds_button.py
import sys
import os

try:
    from PySide6.QtWidgets import (
        QApplication, QWidget,
        QLabel, QPushButton,
    )
    from PySide6.QtGui import QFont, QIcon
    from PySide6.QtCore import Qt, QSize
    qt_modules = 'PySide6'
except ImportError:
    try:
        from PyQt6.QtWidgets import (
            QApplication, QWidget,
            QLabel, QPushButton,
        )
        from PyQt6.QtGui import QFont, QIcon
        from PyQt6.QtCore import Qt, QSize
        qt_modules = 'PyQt6'
    except ImportError:
        print("PySide6 또는 PyQt6가 설치되어 있지 않습니다.")
        sys.exit(1)

print(f"Using {qt_modules} binding.")


class MW(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('QPushButton Example')
        self.setup_main_wnd()
        self.show()

    def setup_main_wnd(self):
        # text label - slot에서 접근하므로 instance attribute로 생성
        self.hello_label = QLabel(self)
        self.hello_label.setText('Hello, World and Qt!')
        self.hello_label.setFont(QFont('Arial', 15))
        self.hello_label.resize(230, 40)
        self.hello_label.move(10, 20)

        # 아래 줄을 주석 해제하여 정렬 / 배경색 동작 확인 가능
        # self.hello_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # PySide6 / PyQt6 모두 동작
        # self.hello_label.setAlignment(Qt.AlignCenter)                # PySide6 전용 (하위 호환)
        # self.hello_label.setStyleSheet("background-color: yellow")

        # 스크립트 위치 기준으로 image 경로 계산
        base_dir = os.path.dirname(os.path.realpath(__file__))
        img_path = os.path.join(base_dir, 'img/world.png')

        # icon + text 버튼
        it_button = QPushButton("icon and text button", self)
        it_button.setIcon(QIcon(img_path))
        it_button.clicked.connect(self.it_btn_clicked)
        it_button.resize(150, 50)
        it_button.move(50, 70)

        # icon 전용 버튼 (text 없음)
        icon_button = QPushButton(self)
        icon_button.setIcon(QIcon(img_path))
        icon_button.setIconSize(QSize(120, 30))  # icon 크기 명시적으로 고정
        icon_button.clicked.connect(self.icon_btn_clicked)
        icon_button.resize(150, 50)
        icon_button.move(50, 130)

        # text 전용 버튼 (icon 없음)
        text_button = QPushButton("text button", self)
        text_button.clicked.connect(self.text_btn_clicked)
        text_button.resize(150, 50)
        text_button.move(50, 190)

    def it_btn_clicked(self):
        """icon + text 버튼 클릭 시 호출됨."""
        self.hello_label.setText("Icon and text Button")

    def icon_btn_clicked(self):
        """icon 전용 버튼 클릭 시 호출됨."""
        self.hello_label.setText("Icon Button")

    def text_btn_clicked(self):
        """text 전용 버튼 클릭 시 호출됨."""
        self.hello_label.setText("text Button")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MW()
    sys.exit(app.exec())
```