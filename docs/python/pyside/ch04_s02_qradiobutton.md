---
title: QRadioButton Widget
description: 여러 option 중 하나만 선택하는 경우에 사용되는 Qt Widget. QButtonGroup을 이용한 그룹화 및 예제 코드 포함.
tags:
  - Qt
  - PySide6
  - PyQt6
  - QRadioButton
  - QButtonGroup
  - widget
  - GUI
  - signal
  - slot
date: 2025-04-12
---

# `QRadioButton` Widget

**module** : `QtWidgets`

여러 option(선택지) 중 하나를 선택하는 경우에 사용되는 Widget.

`QCheckBox`와 비슷한 기능과 모양을 가지지만, 아래와 같은 차이점이 있음.

* 외양 — 체크 부분이 **원 형태**임 (`QCheckBox`는 네모 모양)
* 기본 동작 — `autoExclusive`가 기본적으로 `True`로 설정되어 **하나만 선택** 가능
* `QCheckBox`는 여러 option을 동시에 선택하는 방식이 기본임

**`autoExclusive` 적용 범위 주의사항**

* `autoExclusive`는 동일한 parent widget 내의 `QRadioButton`끼리만 적용됨.
* 여러 그룹을 독립적으로 관리하려면 `QButtonGroup` instance를 이용하여 명시적으로 그룹화해야 함.
* 서로 다른 `QButtonGroup`에 속한 버튼들은 각각 독립적으로 exclusive가 적용됨.

---

## 주요 Signals

| Signal | 발생 조건 | Slot 전달 인자 |
|---|---|---|
| `toggled(checked)` | 버튼의 선택 상태가 변경될 때 | `bool` (`True`: 선택됨, `False`: 해제됨) |
| `clicked(checked)` | 버튼이 클릭될 때 | `bool` |

**`QButtonGroup` Signals**

* `QButtonGroup` 사용 시 개별 버튼 signal 대신 아래 signal을 주로 사용함.

| Signal | 발생 조건 | Slot 전달 인자 |
|---|---|---|
| `buttonClicked(button)` | 그룹 내 버튼이 클릭될 때 | `QAbstractButton` instance |
| `buttonToggled(button, checked)` | 그룹 내 버튼의 상태가 변경될 때 | `QAbstractButton` instance, `bool` |

공식 문서:

* Qt6 C++ : [https://doc.qt.io/qt-6/qradiobutton.html](https://doc.qt.io/qt-6/qradiobutton.html)
* PySide6 : [https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QRadioButton.html](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QRadioButton.html)

---

## 주요 Methods

| Method | 설명 |
|---|---|
| `isChecked()` | 현재 선택 여부를 `bool`로 반환 |
| `setChecked(bool)` | 선택 상태를 코드로 설정 |
| `text()` | 버튼에 표시된 문자열을 반환 |
| `setText(str)` | 버튼에 표시될 문자열 설정 |

---

## `QButtonGroup` 사용법

여러 `QRadioButton`을 하나의 그룹으로 묶어 독립적인 exclusive 동작을 구현할 때 사용함.

| Method | 설명 |
|---|---|
| `addButton(button)` | 그룹에 버튼 추가 |
| `addButton(button, id)` | 그룹에 버튼을 id와 함께 추가 |
| `removeButton(button)` | 그룹에서 버튼 제거 |
| `checkedButton()` | 현재 선택된 버튼 instance를 반환 |
| `checkedId()` | 현재 선택된 버튼의 id를 반환 (`-1`이면 미선택) |

**`id` 활용 팁**

* `addButton(button, id)` 로 정수 id를 부여하면, `checkedId()`로 어떤 버튼이 선택됐는지 분기 처리가 간편해짐.
* id를 지정하지 않으면 Qt가 자동으로 음수 id를 부여(-2부터)함.

---

## Example — `QButtonGroup`을 이용한 단일 선택

3개의 `QRadioButton` instance를 `QButtonGroup`으로 그룹화하여, 세 선택지 중 하나만 선택 가능하도록 구현한 예제.

* `buttonClicked` signal에 slot을 연결 → 클릭된 버튼의 text를 `dp_label`에 표시함.
* PySide6 우선으로 import하고, 없으면 PyQt6로 fallback 처리함.

```python
# ds_qradiobutton_ex0.py
import sys

try:
    from PySide6.QtWidgets import (
        QApplication, QWidget, QLabel,
        QVBoxLayout, QRadioButton, QButtonGroup,
    )
    qt_modules = 'PySide6'
except ImportError:
    try:
        from PyQt6.QtWidgets import (
            QApplication, QWidget, QLabel,
            QVBoxLayout, QRadioButton, QButtonGroup,
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
        self.setWindowTitle("Ex: QRadioButton")
        self.resize(400, 200)
        self.setup_main_wnd()
        self.show()

    def setup_main_wnd(self):
        # QRadioButton 3개 생성
        self.rb01 = QRadioButton('1. faith')
        self.rb02 = QRadioButton('2. hope')
        self.rb03 = QRadioButton('3. love')

        # 선택 결과 표시용 label 생성
        self.dp_label = QLabel("")

        # layout 설정
        lm = QVBoxLayout()
        lm.addWidget(QLabel('What is most important?'))
        lm.addWidget(self.rb01)
        lm.addWidget(self.rb02)
        lm.addWidget(self.rb03)
        lm.addWidget(self.dp_label)
        self.setLayout(lm)

        # QButtonGroup으로 3개의 버튼을 하나의 그룹으로 묶음
        # → 그룹 내에서 하나만 선택 가능하도록 exclusive 동작이 적용됨
        self.bg = QButtonGroup(self)
        self.bg.addButton(self.rb01)
        self.bg.addButton(self.rb02)
        self.bg.addButton(self.rb03)

        # 그룹 내 버튼 클릭 시 slot 연결
        self.bg.buttonClicked.connect(self.on_button_clicked)

    def on_button_clicked(self, button):
        """그룹 내 버튼 클릭 시 호출됨.
        클릭된 button instance가 인자로 전달되므로 text()로 내용을 가져옴.
        """
        self.dp_label.setText(button.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_wnd = MW()
    sys.exit(app.exec())
```