---
title: QLineEdit Widget
description: 한 줄(single line) text 입력에 사용되는 Qt Widget. Signals, 주요 Methods, 편집 기능(cut/copy/paste/undo/redo) 및 예제 코드 포함.
tags:
  - Qt
  - PySide6
  - PyQt6
  - QLineEdit
  - Widget
  - GUI
  - Signal
  - Slot
date: 2025-04-12
---

# `QLineEdit` Widget

**module** : `QtWidgets`

한 줄(single line)의 text 입력에 사용되는 Widget.

`QTextEdit`와 달리 single-line 입력에 특화되어 있으며, 다음 기능들을 기본 제공함.

* 일반적인 text 편집 기능
    * cut, copy, paste
    * redo, undo
* 암호 입력 등을 위한 입력 글자 숨기기 기능 (`EchoMode`)

---

## 편집 기능 (cut / copy / paste / undo / redo)

별도 코드 없이도 아래 세 가지 방법으로 사용 가능함.

### 1. Keyboard Shortcut - 자동 지원

`QLineEdit` instance가 focus를 가지고 있을 때 아래 단축키가 자동으로 동작함.

| 기능 | Windows / Linux | macOS |
|---|---|---|
| copy | `Ctrl+C` | `Cmd+C` |
| cut | `Ctrl+X` | `Cmd+X` |
| paste | `Ctrl+V` | `Cmd+V` |
| undo | `Ctrl+Z` | `Cmd+Z` |
| redo | `Ctrl+Y` / `Ctrl+Shift+Z` | `Cmd+Shift+Z` |
| 전체 선택 | `Ctrl+A` | `Cmd+A` |

### 2. Context Menu - 자동 지원

`QLineEdit` 위에서 우클릭하면 Qt가 자동으로 context menu를 표시함.

* cut / copy / paste / select all / undo / redo 항목이 기본으로 포함됨.
* 별도 구현 불필요.

### 3. Programmatic API - 메서드로 직접 호출

코드에서 직접 호출 가능한 method들도 제공됨.

| Method | 동작 |
|---|---|
| `cut()` | 선택된 text를 clipboard로 잘라냄 |
| `copy()` | 선택된 text를 clipboard로 복사 |
| `paste()` | clipboard 내용을 커서 위치에 붙여넣음 |
| `undo()` | 마지막 편집 작업을 취소 |
| `redo()` | 취소한 편집 작업을 다시 실행 |
| `isUndoAvailable()` | undo 가능 여부를 `bool`로 반환 |
| `isRedoAvailable()` | redo 가능 여부를 `bool`로 반환 |

**주의**

* `cut()`과 `copy()`는 text가 선택되어 있어야 동작함.
* 선택 없이 호출하면 아무 일도 일어나지 않음.

---

## Signals

Signal은 특정 이벤트 발생 시 Qt가 자동으로 emit하는 알림으로, Slot(처리 함수)에 연결하여 사용함.

| Signal | 발생 조건 | Slot 전달 인자 |
|---|---|---|
| `returnPressed` | Enter / Return 키 입력 시 | 없음 |
| `selectionChanged` | 선택된 text 범위 변경 시 | 없음 |
| `textChanged(text)` | text 변경 시 (프로그램 코드에 의한 변경 포함) | `str` |
| `textEdited(text)` | **사용자** 가 직접 키보드로 text 편집 시 | `str` |
| `editingFinished` | 편집 완료 시 (Enter 입력 또는 focus 이탈) | 없음 |

**`textChanged` vs `textEdited`**

* `textChanged`는 코드에서 `setText()`를 호출해도 emit되지만,
* `textEdited`는 사용자가 직접 키보드로 입력할 때만 emit됨.

**`editingFinished` 주의사항**

* 이 Signal은 인자를 전달하지 않음.
* Slot에서 text가 필요하면 `self.widget.text()`로 직접 가져와야 함.

공식 문서:

* Qt6 C++ : [https://doc.qt.io/qt-6/qlineedit.html](https://doc.qt.io/qt-6/qlineedit.html)
* PySide6 : [https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QLineEdit.html](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QLineEdit.html)

---

## 주요 Methods

| Method | 설명 |
|---|---|
| `setMaxLength(n)` | 입력 가능한 최대 글자 수를 `n`으로 제한 |
| `setPlaceholderText(str)` | 입력 전 표시될 안내 문자열 설정 |
| `setReadOnly(bool)` | `True`이면 읽기 전용으로 동작 |
| `setEchoMode(mode)` | 입력 표시 방식 설정 (예: 암호 입력 시 `Password` 모드) |
| `clear()` | 입력된 text를 모두 삭제 |
| `text()` | 현재 입력된 text를 `str`로 반환 |
| `selectedText()` | 선택된 text를 `str`로 반환 |
| `setInputMask(str)` | 입력 가능한 패턴(mask)을 지정 |
| `setStyleSheet(str)` | CSS 문자열로 스타일 변경 |

**`setEchoMode` 사용 예시**

* 암호 입력 필드로 만들려면 아래와 같이 사용함.

```python
from PySide6.QtWidgets import QLineEdit
self.pw_edit.setEchoMode(QLineEdit.EchoMode.Password)
```

---

## Example 0 - 편집 기능 동작 확인 (cut / copy / paste / undo / redo)

버튼으로 각 편집 기능을 직접 호출하여 동작을 확인하는 최소 예제.

* 텍스트 드래그 선택 후 `cut` / `copy` / `paste` 버튼을 눌러 동작 확인 가능.
* `undo` / `redo` 버튼으로 편집 이력 탐색 가능.
* `status_label`에서 `isUndoAvailable()` / `isRedoAvailable()` 상태가 실시간으로 반영됨.

**테스트 순서**

1. text 입력 → `undo` 버튼 반복 클릭 → 입력 내용이 하나씩 되돌아가는지 확인
2. `undo` 후 `redo` 버튼 클릭 → 되돌린 내용이 복구되는지 확인
3. text 드래그 선택 → `copy` → 커서를 다른 위치로 이동 → `paste`
4. text 드래그 선택 → `cut` → 내용이 사라진 것 확인 후 `paste`로 복구
5. `status_label`에서 `isUndoAvailable()` / `isRedoAvailable()` 상태 변화 확인

```python
import sys

try:
    from PySide6.QtWidgets import (
        QApplication, QWidget, QLineEdit,
        QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
    )
except ImportError:
    from PyQt6.QtWidgets import (
        QApplication, QWidget, QLineEdit,
        QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
    )


class MW(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("QLineEdit - Edit Operations Test")
        self.setup_main_wnd()
        self.show()

    def setup_main_wnd(self):
        lm = QVBoxLayout()

        lm.addWidget(QLabel("Input:"))
        self.le = QLineEdit()
        self.le.setPlaceholderText("텍스트를 입력하고 드래그로 선택 후 버튼을 눌러보세요.")
        lm.addWidget(self.le)

        # 각 버튼 → 해당 method 직접 연결
        btn_layout = QHBoxLayout()
        for label, slot in [
            ("cut",   self.le.cut),
            ("copy",  self.le.copy),
            ("paste", self.le.paste),
            ("undo",  self.le.undo),
            ("redo",  self.le.redo),
        ]:
            btn = QPushButton(label)
            btn.clicked.connect(slot)
            btn_layout.addWidget(btn)

        lm.addLayout(btn_layout)

        # undo / redo 가능 여부를 실시간으로 표시
        self.status_label = QLabel("undo: -, redo: -")
        lm.addWidget(self.status_label)
        self.le.textChanged.connect(self.update_status)

        self.setLayout(lm)

    def update_status(self):
        undo_ok = self.le.isUndoAvailable()
        redo_ok = self.le.isRedoAvailable()
        self.status_label.setText(
            f"undo available: {undo_ok}  |  redo available: {redo_ok}"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wnd = MW()
    sys.exit(app.exec())
```

---

## Example 1 - Signals 동작 확인

각 Signal이 언제 emit되고, 어떤 값을 전달하는지 확인할 수 있는 예제.

* `dp_label3`는 `QLabel.setText`를 직접 Slot으로 `textChanged`에 연결 → text 변경 시 label이 자동으로 갱신됨.
* `editingFinished`는 인자가 없으므로 Slot 내부에서 `self.le.text()`로 text를 직접 가져옴.
* PySide6 우선으로 import하고, 없으면 PyQt6로 fallback 처리함.

```python
import sys

try:
    from PySide6.QtWidgets import (
        QApplication, QWidget, QLabel,
        QVBoxLayout, QLineEdit,
    )
    qt_modules = 'PySide6'
except ImportError:
    try:
        from PyQt6.QtWidgets import (
            QApplication, QWidget, QLabel,
            QVBoxLayout, QLineEdit,
        )
        qt_modules = 'PyQt6'
    except ImportError:
        print("PySide6 또는 PyQt6가 설치되어 있지 않습니다.")
        sys.exit(1)


class MW(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("QLineEdit Signal Example")
        self.setup_main_wnd()
        self.show()

    def setup_main_wnd(self):
        lm = QVBoxLayout()

        lm.addWidget(QLabel('What is most important?'))

        self.le = QLineEdit()
        self.le.setMaxLength(10)                         # 최대 10자 제한
        self.le.setPlaceholderText("Type something...")  # placeholder text

        # 각 Signal을 Slot(메서드)에 연결
        self.le.returnPressed.connect(self.on_return_pressed)
        self.le.textChanged.connect(self.on_changed)
        self.le.textEdited.connect(self.on_edited)
        self.le.editingFinished.connect(self.on_editing_finished)

        lm.addWidget(self.le)

        # 결과 표시용 Label 4개 생성
        self.dp_label0 = QLabel("textChanged: (대기 중)")
        self.dp_label1 = QLabel("textEdited: (대기 중)")
        self.dp_label2 = QLabel("editingFinished: (대기 중)")
        self.dp_label3 = QLabel("textChanged (직접 연결): (대기 중)")

        for lbl in (self.dp_label0, self.dp_label1,
                    self.dp_label2, self.dp_label3):
            lm.addWidget(lbl)

        # textChanged Signal을 QLabel.setText에 직접 연결하는 방법
        self.le.textChanged.connect(self.dp_label3.setText)

        self.setLayout(lm)

    def on_return_pressed(self):
        """Enter/Return 키 입력 시 호출됨."""
        selected = self.le.selectedText()
        print(f"[returnPressed] selected text: '{selected}'")

    def on_changed(self, text: str):
        """textChanged Signal 처리.
        코드에 의한 setText() 호출 시에도 emit됨.
        """
        self.dp_label0.setText(f"textChanged: '{text}'")

    def on_edited(self, text: str):
        """textEdited Signal 처리.
        사용자가 직접 키보드로 입력할 때만 emit됨.
        """
        self.dp_label1.setText(f"textEdited: '{text}'")

    def on_editing_finished(self):
        """editingFinished Signal 처리.
        이 Signal은 인자를 전달하지 않으므로 text()로 직접 가져옴.
        """
        current_text = self.le.text()
        self.dp_label2.setText(f"editingFinished: '{current_text}'")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_wnd = MW()
    sys.exit(app.exec())
```

---

## Example 2 - 기본 입력 폼

`QPushButton` 2개를 이용해 Clear / OK 기능을 구현한 예제.

* **Clear 버튼**: `clear()`로 입력 내용 초기화
* **OK 버튼**: `text()`로 입력 내용을 console에 출력 후 창 닫기
* `setStyleSheet()`에 CSS 문자열을 전달하여 배경색·글자색 변경 가능

```python
import sys

try:
    from PySide6.QtWidgets import (
        QApplication, QWidget,
        QLabel, QLineEdit, QPushButton,
    )
    qt_modules = 'PySide6'
except ImportError:
    try:
        from PyQt6.QtWidgets import (
            QApplication, QWidget,
            QLabel, QLineEdit, QPushButton,
        )
        qt_modules = 'PyQt6'
    except ImportError:
        print("PySide6 또는 PyQt6가 설치되어 있지 않습니다.")
        sys.exit(1)


class MW(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(340, 120)   # 창 크기 고정
        self.setWindowTitle("QLineEdit Example")
        self.setup_main_wnd()
        self.show()

    def setup_main_wnd(self):
        QLabel("Please enter your name below.", self).move(50, 10)

        name_label = QLabel("Name:", self)
        name_label.move(10, 50)

        # QLineEdit 생성 및 설정
        self.name_edit = QLineEdit(self)
        self.name_edit.resize(210, 24)
        self.name_edit.move(80, 47)
        self.name_edit.setStyleSheet(
            "background-color: yellow; color: rgb(50, 150, 250);"
        )
        self.name_edit.setMaxLength(30)
        self.name_edit.setPlaceholderText("Enter your name")

        # Signal 연결
        self.name_edit.returnPressed.connect(self.on_return_pressed)
        self.name_edit.selectionChanged.connect(self.on_selection_changed)
        self.name_edit.textChanged.connect(self.on_text_changed)
        self.name_edit.textEdited.connect(self.on_text_edited)

        clear_button = QPushButton("Clear", self)
        clear_button.move(100, 85)
        clear_button.clicked.connect(self.clear_text)

        ok_button = QPushButton("OK", self)
        ok_button.move(200, 85)
        ok_button.clicked.connect(self.accept_text)

    def clear_text(self):
        """입력 필드를 초기화함."""
        self.name_edit.clear()

    def accept_text(self):
        """입력된 text를 console에 출력하고 창을 닫음."""
        print(f"입력된 이름: {self.name_edit.text()}")
        self.close()

    def on_return_pressed(self):
        print("[returnPressed] Enter 키가 눌렸습니다.")

    def on_selection_changed(self):
        print("[selectionChanged] 선택 범위가 변경됐습니다.")

    def on_text_changed(self, text: str):
        print(f"[textChanged] '{text}'")

    def on_text_edited(self, text: str):
        print(f"[textEdited] '{text}'")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MW()
    sys.exit(app.exec())
```

**`setFixedSize` vs `setMaximumSize`**

* `setMaximumSize(w, h)` : 최대 크기만 제한 → 사용자가 더 작게 줄일 수 있음.
* `setFixedSize(w, h)` : 크기를 완전히 고정 → 사용자가 resize 불가.