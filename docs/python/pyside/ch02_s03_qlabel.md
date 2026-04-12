---
title: QLabel Widget
description: GUI에서 text 또는 image를 표시하는 Qt Widget. 정렬, 폰트, 이미지, 배경색 설정 방법 및 예제 코드 포함.
tags:
  - Qt
  - PySide6
  - PyQt6
  - QLabel
  - widget
  - GUI
date: 2025-04-12
---

# `QLabel` Widget

**module** : `QtWidgets`

GUI에서 고정된 text 문자열 또는 image를 표시하는 Widget.

* 사용자와 직접 상호작용하지 않음 (uneditable).
* GUI에서 정보를 표시하는 용도로 매우 많이 사용됨.
* textual content 정렬을 위해 `QtCore.Qt` class의 `AlignmentFlag` enum과 자주 함께 사용됨.
* image 표시를 위해 `QtGui.QPixmap`과 함께 사용됨.

공식 문서:

* Qt6 C++ : [https://doc.qt.io/qt-6/qlabel.html](https://doc.qt.io/qt-6/qlabel.html)
* PySide6 : [https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QLabel.html](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QLabel.html)

---

## 주요 Methods

| Method | 설명 |
|---|---|
| `__init__(text, parent)` | text와 parent widget을 인자로 받아 instance 생성. parent 지정 권장 |
| `setText(str)` | 표시할 문자열 설정 |
| `text()` | 현재 표시 중인 문자열 반환 |
| `setAlignment(flag)` | `Qt.AlignmentFlag` enum으로 content 정렬 방식 설정 |
| `setFont(QFont)` | `QtGui.QFont` instance로 폰트 설정 |
| `setPixmap(QPixmap)` | `QtGui.QPixmap` instance로 표시할 image 설정. 재호출 시 이전 image가 교체됨 |
| `setScaledContents(bool)` | `True`이면 pixmap을 `QLabel` instance의 크기에 맞게 scaling |
| `move(x, y)` | absolute positioning에서 widget의 위치를 지정 |
| `setStyleSheet(str)` | CSS 문자열로 스타일 변경 |

---

## 사용 예시

### Textual content 표시

```python
label0 = QLabel("text str to display")
label1 = QLabel("Hello, World and Qt!", self)  # parent widget 지정 권장
```

---

### 정렬 방식 지정

`setAlignment()` method에 `Qt.AlignmentFlag` enum을 인자로 전달하여 설정함.

```python
from PySide6.QtCore import Qt  # Qt class는 QtCore 모듈에서 제공됨

label_instance.setAlignment(Qt.AlignmentFlag.AlignCenter)  # PySide6 / PyQt6 모두 동작
# label_instance.setAlignment(Qt.AlignCenter)              # PySide6 전용 (하위 호환)
```

* `QLabel` instance의 영역 내에서의 정렬을 의미함.
* 자주 사용되는 `AlignmentFlag` 값은 아래와 같음.

| enum 값 | 설명 |
|---|---|
| `Qt.AlignmentFlag.AlignLeft` | 좌측 정렬 |
| `Qt.AlignmentFlag.AlignRight` | 우측 정렬 |
| `Qt.AlignmentFlag.AlignHCenter` | 수평 방향 중앙 정렬 |
| `Qt.AlignmentFlag.AlignTop` | 상단 정렬 |
| `Qt.AlignmentFlag.AlignBottom` | 하단 정렬 |
| `Qt.AlignmentFlag.AlignVCenter` | 수직 방향 중앙 정렬 |
| `Qt.AlignmentFlag.AlignCenter` | `AlignHCenter \| AlignVCenter` 와 동일 - 수평 + 수직 중앙 정렬 |

**`Qt.AlignCenter` vs `Qt.AlignmentFlag.AlignCenter`**

* `Qt.AlignmentFlag.AlignCenter` - PySide6 / PyQt6 모두 동작함. 권장 표기.
* `Qt.AlignCenter` - PySide6에서만 동작하는 하위 호환 표기. PyQt6에서는 동작하지 않음.

---

### Font 지정

`QtGui.QFont` instance를 `setFont()` method의 인자로 전달하여 설정함.

```python
from PySide6.QtGui import QFont

label_instance.setFont(QFont("Arial", 20))
```

* 폰트 종류 **Arial**, 크기 **20pt** 로 지정된 `QFont` instance를 생성하여 적용함.

---

### Image 표시

`QPixmap` instance를 `setPixmap()` method로 전달하여 image를 표시함.

```python
from PySide6.QtGui import QPixmap

image_label = QLabel()
pixmap = QPixmap("images/norwegian.jpg")
image_label.setPixmap(pixmap)
image_label.setScaledContents(True)
```

* `setPixmap()` - 표시할 image를 `QPixmap` instance로 설정함. `setPixmap()`을 다시 호출하면 이전 image가 **교체**됨 (중첩 표시되지 않음).
* `setScaledContents(True)` - pixmap을 `QLabel` instance의 현재 크기에 맞게 scaling하여 표시함. `QLabel` 자체의 크기는 별도로 설정해야 함.

**지원 image 포맷**

* Qt가 기본 지원하는 포맷: `jpg`, `png`, `bmp`, `gif`, `xpm` 등.
* 지원 포맷 전체 목록은 `QImageReader.supportedImageFormats()`로 확인 가능.

---

### 배경색 변경

`setStyleSheet()`에 CSS 문자열을 전달하여 설정함.

```python
label_instance.setStyleSheet("background-color: black;")
```

---

## Example - `QLabel`을 이용한 기본 GUI

`QWidget`을 상속한 main window에 `QLabel` instance 2개를 child로 배치하는 예제.

* 하나는 text, 하나는 image를 표시함.
* `move()`를 이용한 absolute positioning 방식을 사용함.
* image 파일 경로는 `os` 모듈로 현재 스크립트 위치를 기준으로 계산함.
* PySide6 우선으로 import하고, 없으면 PyQt6로 fallback 처리함.

**Absolute positioning 주의사항**

* `move()`로 위치를 직접 지정하는 absolute positioning은 main window를 resize할 경우 layout이 어색하게 보일 수 있음.
* Qt에서는 layout manager를 통한 widget 배치를 권장함.
* absolute positioning을 사용할 경우에는 `setFixedSize()`로 창 크기를 고정하는 것이 가장 간편한 우회 방법임.

참고: `os` 모듈 파일 관련 사용법 - [https://ds31x.tistory.com/25](https://ds31x.tistory.com/25)

```python
# labels.py
import sys
import os

try:
    from PySide6.QtWidgets import QApplication, QWidget, QLabel
    from PySide6.QtGui import QFont, QPixmap
    from PySide6.QtCore import Qt
    qt_modules = 'PySide6'
except ImportError:
    try:
        from PyQt6.QtWidgets import QApplication, QWidget, QLabel
        from PyQt6.QtGui import QFont, QPixmap
        from PyQt6.QtCore import Qt
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
        self.setGeometry(100, 100, 250, 200)  # 위치 (100, 100), 크기 250x200
        self.setFixedSize(250, 200)            # 창 크기 고정 - absolute positioning 사용 시 권장
        self.setWindowTitle('QLabel Example')
        self.setup_main_wnd()
        self.show()

    def setup_main_wnd(self):
        # text label 생성
        # 아래 한 줄로도 동일하게 생성 가능
        # hello_label = QLabel('Hello, World and Qt!', self)
        hello_label = QLabel(self)
        hello_label.setText('Hello, World and Qt!')
        hello_label.setFont(QFont('Arial', 15))
        hello_label.move(10, 10)

        # 아래 두 줄을 주석 해제하여 동작 확인 가능
        # hello_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # hello_label.setStyleSheet("background-color: yellow")

        # image label 생성
        # 스크립트 파일 위치를 기준으로 image 경로를 계산함
        path_py_file = os.path.dirname(os.path.realpath(__file__))
        img_path = os.path.join(path_py_file, 'img/world.png')

        if os.path.exists(img_path):
            world_label = QLabel(self)
            pixmap = QPixmap(img_path)
            # scaled()는 새로운 QPixmap을 반환함 - in-place 변환이 아님
            pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
            world_label.setPixmap(pixmap)
            world_label.move(25, 40)
        else:
            print(f'Image not found: {img_path}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MW()
    sys.exit(app.exec())
```

**`pixmap.scaled()` 주의사항**

* `scaled()`는 원본 pixmap을 수정하지 않고 **새로운 `QPixmap` instance를 반환**함.
* 반드시 반환값을 변수에 다시 할당해야 함. (`pixmap = pixmap.scaled(...)`)
* `Qt.AspectRatioMode.KeepAspectRatio` - 원본 비율을 유지하면서 지정한 크기 안에 맞게 축소/확대함.