---
title: QComboBox Widget
description: 사전에 정의된 항목 중 하나를 dropdown list로 선택하는 Qt Widget. 주요 methods, signals 및 예제 코드 포함.
tags:
  - Qt
  - PySide6
  - PyQt6
  - QComboBox
  - widget
  - GUI
  - signal
  - slot
date: 2025-04-12
---

# `QComboBox` Widget

**module** : `QtWidgets`

사전에 정의된 항목 중 하나를 dropdown list로 선택하게 하는 Widget.

* 많은 수의 항목 중에서 입력받아야 하는 경우에 유용함.
* item들은 내부적으로 `str`로 관리됨.

---

## 주요 Methods

| Method | 설명 |
|---|---|
| `addItem(str)` | item을 하나씩 추가 |
| `addItems(list)` | item 목록을 한 번에 추가 |
| `setCurrentIndex(idx)` | 기본으로 선택될 item을 index로 지정 |
| `currentIndex()` | 현재 선택된 item의 index를 반환 |
| `currentText()` | 현재 선택된 item의 text를 반환 |
| `itemText(idx)` | 지정한 index의 item text를 반환 |
| `count()` | 전체 item 수를 반환 |
| `clear()` | 모든 item을 삭제 |

---

## 주요 Signals

| Signal | 발생 조건 | Slot 전달 인자 |
|---|---|---|
| `activated(idx)` | 사용자가 item을 선택(클릭)할 때 | `int` (선택된 item의 index) |
| `currentIndexChanged(idx)` | 현재 선택된 item이 변경될 때 | `int` (변경된 item의 index) |
| `currentTextChanged(text)` | 현재 선택된 item이 변경될 때 | `str` (변경된 item의 text) |

**`activated` vs `currentIndexChanged`**

* `activated` - 사용자가 직접 클릭하여 선택한 경우에만 emit됨. 이미 선택된 item을 다시 클릭해도 emit됨.
* `currentIndexChanged` - 코드에서 `setCurrentIndex()`를 호출해도 emit됨. 동일 item 재선택 시에는 emit되지 않음.

공식 문서:

* Qt6 C++ : [https://doc.qt.io/qt-6/qcombobox.html](https://doc.qt.io/qt-6/qcombobox.html)
* PySide6 : [https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QComboBox.html](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QComboBox.html)

---

## Example - 기본 선택 폼

`activated`와 `currentIndexChanged` signal의 동작 차이를 확인할 수 있는 예제.

* `on_selected` - 사용자가 item을 클릭할 때마다 호출됨. 동일 item 재선택 시에도 호출됨.
* `on_current_idx_changed` - 선택된 index가 실제로 변경된 경우에만 호출됨.
* PySide6 우선으로 import하고, 없으면 PyQt6로 fallback 처리함.

```python
import sys

try:
    from PySide6.QtWidgets import (
        QApplication, QWidget, QLabel,
        QVBoxLayout, QComboBox,
    )
    qt_modules = 'PySide6'
except ImportError:
    try:
        from PyQt6.QtWidgets import (
            QApplication, QWidget, QLabel,
            QVBoxLayout, QComboBox,
        )
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
        self.setWindowTitle("Ex: QComboBox")
        self.resize(400, 200)
        self.setup_main_wnd()
        self.show()

    def setup_main_wnd(self):
        lm = QVBoxLayout()
        lm.addWidget(QLabel('What is most important?'))

        self.items = ['faith', 'hope', 'love']

        self.cb = QComboBox()
        self.cb.addItems(self.items)

        # signal 연결
        self.cb.activated.connect(self.on_selected)
        self.cb.currentIndexChanged.connect(self.on_current_idx_changed)

        lm.addWidget(self.cb)

        self.dp_label = QLabel("")
        lm.addWidget(self.dp_label)

        self.setLayout(lm)

    def on_selected(self, idx: int):
        """activated signal 처리.
        사용자가 item을 클릭할 때마다 호출됨.
        동일 item을 다시 클릭해도 emit됨.
        """
        tmp = f"you selected: {self.items[idx]}"
        print(tmp)
        self.dp_label.setText(tmp)

    def on_current_idx_changed(self, idx: int):
        """currentIndexChanged signal 처리.
        선택된 index가 실제로 변경된 경우에만 호출됨.
        코드에서 setCurrentIndex() 호출 시에도 emit됨.
        """
        print(f"currentIndexChanged: {idx}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_wnd = MW()
    sys.exit(app.exec())
```