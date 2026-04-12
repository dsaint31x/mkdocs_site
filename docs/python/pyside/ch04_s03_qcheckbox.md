---
title: QCheckBox Widget
description: 여러 option 중 복수 개를 선택할 수 있는 Qt Widget. QButtonGroup을 이용한 그룹화, tri-state, exclusive 동작 전환 예제 포함.
tags:
  - Qt
  - PySide6
  - PyQt6
  - QCheckBox
  - QButtonGroup
  - widget
  - GUI
  - signal
  - slot
date: 2025-04-12
---

# `QCheckBox` Widget

**module** : `QtWidgets`

여러 option 중 **복수 개** 를 선택할 수 있게 해주는 checkable box Widget.

* 체크 가능한 네모 박스와 그 옆의 text label로 구성됨.
* `toggled` 또는 `clicked` signal을 통해 slot과 연결하여 사용함.

---

## `QRadioButton`과의 차이점

| 항목 | `QCheckBox` | `QRadioButton` |
|---|---|---|
| 기본 선택 방식 | 복수 선택 가능 | 하나만 선택 (exclusive) |
| 외관 | 네모 박스 | 원형 버튼 |
| `autoExclusive` 기본값 | `False` | `True` |

---

## 그룹으로 묶기

여러 check box를 그룹화할 때 아래 두 가지 방법을 사용함.

* `QButtonGroup` — abstract container로, 외관 없이 논리적 그룹화만 담당함.
* `QGroupBox` — 외관(테두리, 제목)을 포함한 그룹화 widget.

**`QButtonGroup` 사용 시 주의사항**

* `QButtonGroup`은 layout을 제공하지 않음.
* check box를 화면에 배치하려면 별도로 layout manager 또는 `QGroupBox`에 추가해야 함.
* `QGroupBox`를 사용하는 경우가 실무에서 더 많은 편임.

---

## 세 가지 상태 (Tri-state)

기본적으로 `QCheckBox` instance는 **2개의 상태**를 가짐.

* `True` — checked
* `False` — unchecked

`setTristate(True)` 호출 시 **3개의 상태**로 확장됨.

| 상태 | 정수값 | `Qt.CheckState` enum |
|---|---|---|
| checked | `2` | `Qt.CheckState.Checked` |
| partially checked | `1` | `Qt.CheckState.PartiallyChecked` |
| unchecked | `0` | `Qt.CheckState.Unchecked` |

**`PartiallyChecked` 활용 예**

* 계층 구조의 check box에서 부모 check box가 자식들의 혼합 상태를 표현할 때 사용함.
* `setCheckState(Qt.CheckState.PartiallyChecked)`로 코드에서 직접 설정 가능.

---

## 주요 Methods

| Method | 설명 |
|---|---|
| `isChecked()` | 체크 여부를 `bool`로 반환 |
| `checkState()` | 현재 상태를 `Qt.CheckState`로 반환 (tri-state 모드에서 주로 사용) |
| `toggle()` | 체크 상태를 반전시킴 |
| `setChecked(bool)` | 체크 상태를 코드로 설정 |
| `setTristate(bool)` | `True`이면 tri-state 모드 활성화 |
| `setCheckState(Qt.CheckState)` | `Qt.CheckState` enum으로 상태 직접 설정 |
| `setText(str)` | label 문자열 설정 |
| `text()` | 현재 label 문자열 반환 |

---

## 주요 Signals

| Signal | 발생 조건 | Slot 전달 인자 |
|---|---|---|
| `toggled(checked)` | 상태가 변경될 때 | `bool` (`True`: checked, `False`: unchecked) |
| `clicked(checked)` | 클릭될 때 | `bool` |
| `stateChanged(state)` | tri-state 모드에서 상태가 변경될 때 | `int` (0 / 1 / 2) |

**`toggled` vs `stateChanged`**

* 2-state 모드에서는 `toggled`를 주로 사용함.
* tri-state 모드에서는 `stateChanged`를 사용해야 `PartiallyChecked` 상태까지 구분 가능함.

공식 문서:

* Qt6 C++ : [https://doc.qt.io/qt-6/qcheckbox.html](https://doc.qt.io/qt-6/qcheckbox.html)
* PySide6 : [https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QCheckBox.html](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QCheckBox.html)

---

## Example — exclusive 동작 전환

`QCheckBox` instance 3개를 `QButtonGroup`으로 그룹화하고,  
하단의 별도 check box로 exclusive / non-exclusive 모드를 전환하는 예제.

* `buttonClicked` signal → 클릭된 버튼의 text를 `dp_label`에 표시.
* `toggled` signal → exclusive 모드 전환 시 모든 check box를 unchecked 상태로 초기화.
* `reset_checkboxes()` 내부에서 `setExclusive(False)`로 잠시 해제 후 초기화 → 다시 원래 상태로 복원하는 방식을 사용함. (exclusive 모드에서는 모든 버튼을 동시에 uncheck 할 수 없기 때문)
* PySide6 우선으로 import하고, 없으면 PyQt6로 fallback 처리함.

```python
import sys

try:
    from PySide6.QtWidgets import (
        QApplication, QWidget, QLabel,
        QVBoxLayout, QCheckBox, QButtonGroup,
    )
    from PySide6.QtCore import Qt
    qt_modules = 'PySide6'
except ImportError:
    try:
        from PyQt6.QtWidgets import (
            QApplication, QWidget, QLabel,
            QVBoxLayout, QCheckBox, QButtonGroup,
        )
        from PyQt6.QtCore import Qt
        qt_modules = 'PyQt6'
    except ImportError:
        print("PySide6 또는 PyQt6가 설치되어 있지 않습니다.")
        sys.exit(1)

print(f"Using {qt_modules} binding.")


class MW(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ex: QCheckBox with Exclusive Toggle")
        self.resize(400, 250)
        self.init_ui()
        self.show()

    def init_ui(self):
        lm = QVBoxLayout()
        self.setLayout(lm)

        lm.addWidget(QLabel('What is most important?'))

        # QCheckBox 3개 생성 및 layout에 추가
        checkbox_texts = ['1. faith', '2. hope', '3. love']
        self.checkboxes = [QCheckBox(text) for text in checkbox_texts]
        for cb in self.checkboxes:
            lm.addWidget(cb)

        # 선택 결과 표시용 label
        self.dp_label = QLabel("")
        lm.addWidget(self.dp_label)

        # QButtonGroup으로 그룹화 → exclusive 모드로 시작
        self.bg = QButtonGroup(self)
        for cb in self.checkboxes:
            self.bg.addButton(cb)
        self.bg.setExclusive(True)
        self.bg.buttonClicked.connect(self.on_checkbox_clicked)

        # exclusive 모드 전환용 check box
        # exclusive=True → 복수 선택 불가이므로, 초기 체크 상태는 False
        self.cb_toggle_exclusive = QCheckBox("Check it for multiple selection.")
        self.cb_toggle_exclusive.setChecked(not self.bg.exclusive())
        self.cb_toggle_exclusive.toggled.connect(self.on_toggle_exclusive)
        lm.addWidget(self.cb_toggle_exclusive)

    def on_checkbox_clicked(self, button):
        """그룹 내 check box 클릭 시 호출됨.
        클릭된 button instance가 인자로 전달됨.
        """
        self.dp_label.setText(button.text())

    def on_toggle_exclusive(self, state: bool):
        """exclusive 모드 on/off 전환 처리.
        전환 전에 모든 check box를 unchecked 상태로 초기화함.
        """
        print(f"multiple selection mode: {state}")
        self.reset_checkboxes(False)
        self.bg.setExclusive(not state)

    def reset_checkboxes(self, state: bool):
        """모든 check box를 주어진 상태(state)로 설정함.

        exclusive 모드에서는 Qt가 "항상 하나는 checked 상태를 유지"하도록 강제함.
        따라서 현재 checked된 버튼에 setChecked(False)를 호출해도 Qt가 이를 무시함.
        결과적으로 exclusive 모드가 활성화된 상태에서는 모든 버튼을 unchecked로 만들 수 없음.
        이를 우회하기 위해 setExclusive(False)로 잠시 해제 후 초기화하고 원래 상태로 복원함.

        세 방식 모두 for문을 사용함. 차이는 어떤 컨테이너를 순회하느냐에 있음.

        approach 01 — self.checkboxes 순회, toggle() 이용:
            현재 checked 상태를 확인 후 반전시키는 방식.
            for cb in self.checkboxes:
                if cb.isChecked(): cb.toggle()

        approach 02 — self.checkboxes 순회, setChecked() 이용:
            목표 상태를 직접 지정하는 방식.
            for cb in self.checkboxes:
                cb.setChecked(state)

        approach 03 — bg.buttons() 순회 (현재 사용):
            QButtonGroup에서 직접 버튼 목록을 가져오므로
            self.checkboxes 같은 별도 attribute를 유지하지 않아도 됨.
        """
        old_exclusive = self.bg.exclusive()
        self.bg.setExclusive(False)

        for cb in self.bg.buttons():   # approach 03
            cb.setChecked(state)

        self.bg.setExclusive(old_exclusive)
        print("--------------")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_wnd = MW()
    sys.exit(app.exec())
```