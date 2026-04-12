---
title: QGroupBox Widget
description: 외관을 가진 Qt container widget. QCheckBox/QRadioButton 그룹화, setCheckable을 이용한 일괄 enable/disable 예제 포함.
tags:
  - Qt
  - PySide6
  - PyQt6
  - QGroupBox
  - QButtonGroup
  - widget
  - GUI
  - signal
  - slot
date: 2025-04-12
---

# `QGroupBox` Widget

**module** : `QtWidgets`

외관(frame + title)을 가진 container widget.

* 포함된 child widget들을 **그룹 이름(title)** 과 **네모 frame** 으로 시각적으로 묶어 표시함.
* `QButtonGroup`과 달리 외관을 제공하며, layout manager를 통해 child widget의 배치를 제어할 수 있음.
* title 옆에 check box를 추가하여 child widget 전체를 한 번에 enable/disable하는 기능도 제공함.

---

## `QGroupBox` vs `QButtonGroup`

| 항목 | `QGroupBox` | `QButtonGroup` |
|---|---|---|
| 외관 (frame + title) | 있음 | 없음 (abstract container) |
| child widget 배치 | layout manager로 제어 | 없음 |
| 기능적 그룹화 (exclusive, signal 일괄 연결 등) | 지원 안 함 | 지원 |
| 사용 목적 | 시각적 그룹화 | 논리적 그룹화 |

**실무에서의 조합 패턴**

* `QGroupBox` 단독 - 시각적 그룹화만 필요한 경우.
* `QGroupBox` + `QButtonGroup` 조합 - 시각적 그룹화와 논리적 그룹화를 동시에 구현할 때 사용함.

---

## child widget 배치 방법

`QWidget`을 container로 사용하는 방식과 동일함.

1. layout manager instance를 생성
2. child widget들을 layout manager에 추가
3. `QGroupBox` instance의 `setLayout()`으로 layout manager를 설정

---

## 주요 Methods

| Method | 설명 |
|---|---|
| `setTitle(str)` | 그룹 이름(title) 설정 |
| `setCheckable(bool)` | `True`이면 title 옆에 check box 생성 - child widget 전체를 enable/disable 가능 |
| `setChecked(bool)` | `True`이면 child widget 전체 enable, `False`이면 전체 disable |
| `isChecked()` | 현재 enable 여부를 `bool`로 반환 |
| `setFlat(bool)` | `True`이면 border 없는 평평한 외관 - 기본값은 `False` |

---

## 주요 Signals

| Signal | 발생 조건 | Slot 전달 인자 |
|---|---|---|
| `clicked(checked)` | title 옆 check box 클릭 시 (`setCheckable(True)` 필요) | `bool` |
| `toggled(checked)` | checked 상태 변경 시 | `bool` |

공식 문서:

* Qt6 C++ : [https://doc.qt.io/qt-6/qgroupbox.html](https://doc.qt.io/qt-6/qgroupbox.html)
* PySide6 : [https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QGroupBox.html](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QGroupBox.html)

---

## Example - QGroupBox + QButtonGroup 조합

왼쪽 `QGroupBox`에는 `QCheckBox` 3개 (복수 선택 가능),  
오른쪽 `QGroupBox`에는 `QRadioButton` 3개 (하나만 선택 가능)를 배치한 예제.

* 왼쪽 `QGroupBox`는 `setCheckable(True)`로 설정 - title 옆 check box로 child widget 전체를 enable/disable 가능.
* `QCheckBox`와 `QRadioButton` 각각을 `QButtonGroup`으로 그룹화하여 signal을 일괄 연결함.
* 개별 button들을 `MW` instance의 attribute로 관리하지 않음 - `QButtonGroup.buttons()`로 순회하여 접근함.

**`checkedButton()` 동작 주의사항 (주석 해제 후 테스트 권장)**

* non-exclusive 모드에서 `checkedButton()`은 list가 아닌 **객체 하나** 만 반환함.
* check로 인해 호출된 경우 - 해당 checked button 객체를 반환.
* uncheck로 인해 호출된 경우 - checked 상태인 버튼 중 index가 가장 낮은 것을 반환.
* 아무것도 선택되지 않은 경우 - `None` 반환.

```python
# ds_qgroupbox_ex0.py

import sys

try:
    from PySide6.QtWidgets import (
        QApplication, QWidget,
        QRadioButton, QCheckBox, QButtonGroup,
        QHBoxLayout, QVBoxLayout,
        QGroupBox,
    )
    from PySide6.QtCore import Qt
    qt_modules = 'PySide6'
except ImportError:
    try:
        from PyQt6.QtWidgets import (
            QApplication, QWidget,
            QRadioButton, QCheckBox, QButtonGroup,
            QHBoxLayout, QVBoxLayout,
            QGroupBox,
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
        self.init_ui()

    def init_ui(self):
        self.setMinimumSize(400, 200)
        self.setWindowTitle("QGroupBox Ex")
        self.setup_main_wnd()
        self.show()

    def setup_main_wnd(self):
        lm = QHBoxLayout()

        # 왼쪽 - QCheckBox 그룹 (복수 선택 가능, enable/disable 토글 가능)
        self.grp_checks = QGroupBox("QCheckBox Grp")
        self.grp_checks.setCheckable(True)
        self.grp_checks.setChecked(False)   # 초기 상태 - disabled

        # 오른쪽 - QRadioButton 그룹 (하나만 선택 가능)
        self.grp_radios = QGroupBox("QRadioButton Grp")

        lm.addWidget(self.grp_checks)
        lm.addWidget(self.grp_radios)
        self.setLayout(lm)

        self.set_checks()
        self.set_radios()

    def set_checks(self):
        lm = QVBoxLayout()

        self.bg_checks = QButtonGroup()
        self.bg_checks.setExclusive(False)  # 복수 선택 허용
        for idx in range(3):
            cb = QCheckBox(f"check {idx}")
            self.bg_checks.addButton(cb)
            lm.addWidget(cb)
        self.grp_checks.setLayout(lm)

        self.bg_checks.buttonClicked.connect(self.on_check_clicked)
        self.grp_checks.clicked.connect(self.on_grp_checks_clicked)

    def set_radios(self):
        lm = QVBoxLayout()

        self.bg_radios = QButtonGroup()
        self.bg_radios.setExclusive(True)   # 하나만 선택 가능
        for idx in range(3):
            rb = QRadioButton(f"radio {idx}")
            self.bg_radios.addButton(rb)
            lm.addWidget(rb)
        self.grp_radios.setLayout(lm)

        self.bg_radios.buttonClicked.connect(self.on_radio_clicked)
        self.grp_radios.clicked.connect(self.on_grp_radios_clicked)

    def on_check_clicked(self, button):
        """QCheckBox 그룹 내 버튼 클릭 시 호출됨.
        현재 checked 상태인 모든 check box를 출력함.
        """
        print(f"sender: {self.sender()}, clicked: {button.text()}")

        for cb in self.bg_checks.buttons():
            if cb.isChecked():
                print(f"  checked: {cb.text()}")

        print("======================\n")

        # bg_checks.checkedButton() 동작 테스트 (주석 해제 후 확인 권장)
        # non-exclusive 모드에서는 list가 아닌 객체 하나만 반환됨.
        # - check 시 : 해당 checked button 반환
        # - uncheck 시 : checked 상태 중 index가 가장 낮은 버튼 반환
        # - 전체 uncheck 시 : None 반환
        # a = self.bg_checks.checkedButton()
        # print(a.text() if a is not None else 'not checked!')
        # print("======================")

    def on_radio_clicked(self, radio_btn):
        """QRadioButton 그룹 내 버튼 클릭 시 호출됨.
        현재 checked 상태인 radio button의 index와 text를 출력함.
        """
        print(f"sender: {self.sender()}, clicked: {radio_btn.text()}")

        for idx, rb in enumerate(self.bg_radios.buttons()):
            if rb.isChecked():
                print(f"  checked: [{idx}] {rb.text()}")

        print("======================\n")

        # bg_radios.checkedButton() 동작 테스트 (주석 해제 후 확인 권장)
        # a = self.bg_radios.checkedButton()
        # print(a.text() if a is not None else 'not checked!')
        # print("======================")

    def on_grp_checks_clicked(self, checked: bool):
        """QGroupBox title의 check box 클릭 시 호출됨.
        checked=True이면 child widget 전체 enable,
        checked=False이면 child widget 전체 disable.
        """
        print(f"checks group - checked: {checked}")

    def on_grp_radios_clicked(self, checked: bool):
        """QGroupBox title의 check box 클릭 시 호출됨 (setCheckable 설정 시).
        이 예제에서 grp_radios는 setCheckable을 설정하지 않았으므로 호출되지 않음.
        """
        print(f"radios group - checked: {checked}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wnd = MW()
    sys.exit(app.exec())
```