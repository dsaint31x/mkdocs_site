---
title: QInputDialog
tags:
  - Python
  - PySide6
  - Qt
  - GUI
  - Dialog
---

# QInputDialog

***`QInputDialog`***
: 사용자로부터 문자열, 숫자, item 선택값 등을 입력받기 위한 built-in dialog임.  
하나의 입력값을 간단히 입력받을 때 사용함.

`QInputDialog`는 별도의 custom dialog class를 직접 만들지 않고도 사용할 수 있는 입력용 dialog임.  
입력받고자 하는 값의 type에 따라 적절한 static method를 호출하면 됨.

Dialog는 dialog box라고도 부르며, 사용자에게 정보를 요구하거나 선택을 받기 위해 일시적으로 표시되는 GUI 요소임.

---

## 기본 사용 구조

`QInputDialog`의 static method들은 대체로 다음과 같이 두 개의 값을 반환함.

```python
ret_value, is_ok = QInputDialog.someMethod(...)
```

* `ret_value` : 사용자가 입력하거나 선택한 값.
* `is_ok` : 사용자가 `OK` 버튼을 눌렀는지 여부.

즉, `ret_value`만 바로 사용하는 것이 아니라, 사용자가 입력을 확정했는지를 `is_ok`로 확인하는 것이 일반적임.

```python
if is_ok:
    print(ret_value)
```

사용자가 `Cancel`을 누르거나 dialog를 닫은 경우에는 `is_ok`가 `False`가 됨.

---

## 주요 static methods

`QInputDialog`는 입력받고자 하는 값의 type에 따라 다음 static method를 제공함.

| static method        | 입력 대상     | 내부 widget        |
| -------------------- | --------- | ---------------- |
| `getText()`          | 한 줄 text  | `QLineEdit`      |
| `getMultiLineText()` | 여러 줄 text | `QTextEdit`      |
| `getInt()`           | integer   | `QSpinBox`       |
| `getDouble()`        | double    | `QDoubleSpinBox` |
| `getItem()`          | item 선택   | `QComboBox`      |

---

## QInputDialog.getText()

`getText()`는 사용자로부터 한 줄의 text를 입력받기 위한 static method임.

* 내부적으로 `QLineEdit` widget이 있는 modal dialog를 생성하고 실행하여, 사용자로부터 한 줄의 문자열을 입력받아 반환함.
* 짧은 이름, 검색어, ID, password처럼 한 줄 입력이면 충분한 경우에 사용함.

다음이 전형적인 사용법을 나타내는 code snippet임:

```python
ret_text, is_ok = QInputDialog.getText(
    parent,       # 부모 widget
    title,        # dialog title
    label_text,   # input field 위의 label text
    echo_mode,    # 사용자 입력에 대한 echo mode
    default_text, # 기본 text 값
)
```

`echo_mode`는 사용자에게 text가 어떻게 표시될지를 결정함.
`QLineEdit` widget과 동일한 echo mode를 지원함.

* `QLineEdit.Normal`
  : 기본 설정. 입력한 text가 그대로 input field에 표시됨.

* `QLineEdit.NoEcho`
  : 입력해도 text가 표시되지 않음.

* `QLineEdit.Password`
  : password 입력창처럼 입력한 글자가 대체 기호로 표시됨.

* `QLineEdit.PasswordEchoOnEdit`
  : 입력 중에는 text가 보이고, focus를 잃으면 password처럼 대체 기호로 표시됨.

### Example

```python
import sys

from PySide6.QtWidgets import (
        QApplication, QMainWindow,
        QWidget, QPushButton, QLabel, QVBoxLayout,
        QLineEdit, QInputDialog,
        )

class MW (QMainWindow):

    def __init__(self):
        super(MW, self).__init__()

        # UI 구성을 별도의 method로 분리.
        self.init_ui()

        # main window를 화면에 표시.
        self.show()

    def init_ui(self):
        
        # QInputDialog.getText()를 실행하기 위한 button.
        self.button0 = QPushButton('Test.')

        # button이 clicked signal을 발생시키면 slot00()이 호출됨.
        self.button0.clicked.connect(self.slot00)

        # 사용자가 입력한 text를 표시할 label.
        self.ret_label = QLabel()

        # button과 label을 위에서 아래로 배치하기 위한 layout.
        layout = QVBoxLayout()
        layout.addWidget(self.button0)
        layout.addWidget(self.ret_label)
        
        # QMainWindow에는 layout을 직접 설정하지 않음.
        # QWidget을 하나 만들고, 해당 widget에 layout을 설정한 뒤
        # QMainWindow의 central widget으로 지정함.
        tmp = QWidget()
        tmp.setLayout(layout)

        self.setCentralWidget(tmp)

    def slot00(self):
        # 현재 slot을 호출한 sender object를 확인.
        print(self.sender())

        sender = self.sender()

        # 여러 widget이 같은 slot에 연결될 수 있으므로,
        # 어떤 widget에서 signal이 발생했는지 확인함.
        if sender == self.button0:

            # 한 줄 text 입력을 위한 dialog를 실행.
            ret_text, is_ok = QInputDialog.getText(
                    self,                         # parent widget
                    "Input Text",                 # dialog title
                    "Enter Your Text!",           # input field 위의 label text
                    QLineEdit.PasswordEchoOnEdit, # echo mode
                    "default text!",              # 기본 text 값
                    )

            # 사용자가 OK를 누른 경우에만 입력값을 사용함.
            if is_ok:
                # 입력받은 text를 label에 표시.
                self.ret_label.setText(f'{ret_text}')

if __name__ == "__main__":
    # Qt application 객체 생성.
    app = QApplication(sys.argv)

    # main window 생성.
    mw = MW()

    # Qt event loop 실행.
    sys.exit(app.exec())
```

---

## QInputDialog.getMultiLineText()

`getMultiLineText()`는 사용자로부터 여러 줄의 text를 입력받기 위한 static method임.

`getText()`가 `QLineEdit` 기반의 한 줄 입력 dialog를 제공한다면,
`getMultiLineText()`는 `QTextEdit` 기반의 여러 줄 입력 dialog를 제공함.

설명문, memo, comment처럼 줄바꿈이 필요한 text 입력에 사용함.

```python
ret_text, is_ok = QInputDialog.getMultiLineText(
    parent,       # 부모 widget
    title,        # dialog title
    label_text,   # input field 위의 label text
    default_text, # 기본 text 값
)
```

`getText()`와 달리 `echo_mode` 인자는 없음.
즉, password 입력처럼 문자를 숨겨서 표시하는 용도가 아니라, 여러 줄의 일반 text 입력을 받는 용도임.

### Example

```python
import sys

from PySide6.QtWidgets import (
        QApplication, QMainWindow,
        QWidget, QPushButton, QLabel, QVBoxLayout,
        QInputDialog)

class MW (QMainWindow):

    def __init__(self):
        super(MW, self).__init__()

        # UI 구성을 별도의 method로 분리.
        self.init_ui()

        # main window를 화면에 표시.
        self.show()

    def init_ui(self):
        
        # QInputDialog.getMultiLineText()를 실행하기 위한 button.
        self.button0 = QPushButton('Test.')

        # button이 clicked signal을 발생시키면 slot01()이 호출됨.
        self.button0.clicked.connect(self.slot01)

        # 사용자가 입력한 여러 줄 text를 표시할 label.
        self.ret_label = QLabel()

        # button과 label을 위에서 아래로 배치하기 위한 layout.
        layout = QVBoxLayout()
        layout.addWidget(self.button0)
        layout.addWidget(self.ret_label)
        
        # layout을 담을 QWidget을 만들고,
        # 이를 QMainWindow의 central widget으로 사용함.
        tmp = QWidget()
        tmp.setLayout(layout)

        self.setCentralWidget(tmp)

    def slot01(self):
        # 현재 slot을 호출한 sender object를 확인.
        print(self.sender())

        sender = self.sender()

        if sender == self.button0:

            # 여러 줄 text 입력을 위한 dialog를 실행.
            ret_text, is_ok = QInputDialog.getMultiLineText(
                    self,              # parent widget
                    "Input Text",      # dialog title
                    "Enter Your Text!",# input field 위의 label text
                    "default text!",   # 기본 text 값
                    )

            # 사용자가 OK를 누른 경우에만 입력값을 사용함.
            if is_ok:
                # ret_text에는 줄바꿈 문자가 포함될 수 있음.
                self.ret_label.setText(f'{ret_text}')

if __name__ == "__main__":
    # Qt application 객체 생성.
    app = QApplication(sys.argv)

    # main window 생성.
    mw = MW()

    # Qt event loop 실행.
    sys.exit(app.exec())
```

---

## QInputDialog.getInt()

`getInt()`는 사용자로부터 integer(정수)를 입력받기 위한 static method임.

내부적으로 `QSpinBox` widget이 있는 modal dialog를 생성하고 실행하여, 사용자로부터 정숫값을 입력받아 반환함.
직접 숫자를 입력할 수도 있고, spin button을 이용해 값을 증가 또는 감소시킬 수도 있음.

```python
ret_int, is_ok = QInputDialog.getInt(
    parent,        # 부모 widget
    title,         # dialog title
    label_text,    # input field 위의 label text
    value=0,       # 기본값
    minValue=0,    # 입력 가능한 최솟값
    maxValue=100,  # 입력 가능한 최댓값
    step=1,        # 증가/감소 단위
)
```

`getInt()`에서 중요한 인자는 다음과 같음.

* `value` : dialog가 처음 열렸을 때 표시되는 기본 정숫값.
* `minValue` : 사용자가 입력할 수 있는 최솟값.
* `maxValue` : 사용자가 입력할 수 있는 최댓값.
* `step` : spin button을 눌렀을 때 값이 증가하거나 감소하는 단위.

### Example

```python
import sys

from PySide6.QtWidgets import (
        QApplication, QMainWindow,
        QWidget, QPushButton, QLabel, QVBoxLayout,
        QInputDialog)

class MW (QMainWindow):

    def __init__(self):
        super(MW, self).__init__()

        # UI 구성을 별도의 method로 분리.
        self.init_ui()

        # main window를 화면에 표시.
        self.show()

    def init_ui(self):
        
        # QInputDialog.getInt()를 실행하기 위한 button.
        self.button0 = QPushButton('Test.')

        # button이 clicked signal을 발생시키면 slot00()이 호출됨.
        self.button0.clicked.connect(self.slot00)

        # 사용자가 입력한 정숫값을 표시할 label.
        self.ret_label = QLabel()

        # button과 label을 위에서 아래로 배치하기 위한 layout.
        layout = QVBoxLayout()
        layout.addWidget(self.button0)
        layout.addWidget(self.ret_label)
        
        # layout을 담을 QWidget을 만들고,
        # 이를 QMainWindow의 central widget으로 사용함.
        tmp = QWidget()
        tmp.setLayout(layout)

        self.setCentralWidget(tmp)

    def slot00(self):
        # 현재 slot을 호출한 sender object를 확인.
        print(self.sender())

        sender = self.sender()

        if sender == self.button0:

            # 정수 입력을 위한 dialog를 실행.
            ret_int, is_ok = QInputDialog.getInt(
                    self,                    # parent widget
                    "Input Integer",         # dialog title
                    "Enter Your Int Value!", # input field 위의 label text
                    0,                       # 기본값
                    0, 100,                  # 입력 가능한 최솟값, 최댓값
                    3,                       # 증가/감소 단위
                    )

            # 사용자가 OK를 누른 경우에만 입력값을 사용함.
            if is_ok:
                # 입력받은 integer를 label에 표시.
                self.ret_label.setText(f'{ret_int}')

if __name__ == "__main__":
    # Qt application 객체 생성.
    app = QApplication(sys.argv)

    # main window 생성.
    mw = MW()

    # Qt event loop 실행.
    sys.exit(app.exec())
```

---

## QInputDialog.getDouble()

`getDouble()`은 사용자로부터 double(실수, floating point value)을 입력받기 위한 static method임.

내부적으로 `QDoubleSpinBox` 계열의 widget이 있는 modal dialog를 생성하고 실행하여, 사용자로부터 실숫값을 입력받아 반환함.
`getInt()`와 마찬가지로 입력 가능한 범위를 제한할 수 있으며, 소수점 이하 자리수를 지정할 수 있음.

```python
ret_double, is_ok = QInputDialog.getDouble(
    parent,         # 부모 widget
    title,          # dialog title
    label_text,     # input field 위의 label text
    value=0.0,      # 기본값
    minValue=0.0,   # 입력 가능한 최솟값
    maxValue=100.0, # 입력 가능한 최댓값
    decimals=4,     # 표시할 소수점 이하 자리수
)
```

`getDouble()`에서 중요한 인자는 다음과 같음.

* `value` : dialog가 처음 열렸을 때 표시되는 기본 실숫값.
* `minValue` : 사용자가 입력할 수 있는 최솟값.
* `maxValue` : 사용자가 입력할 수 있는 최댓값.
* `decimals` : 표시할 소수점 이하 자리수.

### Example

```python
import sys

from PySide6.QtWidgets import (
        QApplication, QMainWindow,
        QWidget, QPushButton, QLabel, QVBoxLayout,
        QInputDialog)

class MW (QMainWindow):

    def __init__(self):
        super(MW, self).__init__()

        # UI 구성을 별도의 method로 분리.
        self.init_ui()

        # main window를 화면에 표시.
        self.show()

    def init_ui(self):
        
        # QInputDialog.getDouble()을 실행하기 위한 button.
        self.button0 = QPushButton('Test.')

        # button이 clicked signal을 발생시키면 slot00()이 호출됨.
        self.button0.clicked.connect(self.slot00)

        # 사용자가 입력한 실숫값을 표시할 label.
        self.ret_label = QLabel()

        # button과 label을 위에서 아래로 배치하기 위한 layout.
        layout = QVBoxLayout()
        layout.addWidget(self.button0)
        layout.addWidget(self.ret_label)
        
        # layout을 담을 QWidget을 만들고,
        # 이를 QMainWindow의 central widget으로 사용함.
        tmp = QWidget()
        tmp.setLayout(layout)

        self.setCentralWidget(tmp)

    def slot00(self):
        # 현재 slot을 호출한 sender object를 확인.
        print(self.sender())

        sender = self.sender()

        if sender == self.button0:

            # 실수 입력을 위한 dialog를 실행.
            ret_double, is_ok = QInputDialog.getDouble(
                    self,                        # parent widget
                    "Input Double",              # dialog title
                    "Enter Your Double Value!",  # input field 위의 label text
                    0,                           # 기본값
                    0.0, 100.0,                  # 입력 가능한 최솟값, 최댓값
                    4,                           # 표시할 소수점 이하 자리수
                    )

            # 사용자가 OK를 누른 경우에만 입력값을 사용함.
            if is_ok:
                # 입력받은 double 값을 label에 표시.
                self.ret_label.setText(f'{ret_double}')

if __name__ == "__main__":
    # Qt application 객체 생성.
    app = QApplication(sys.argv)

    # main window 생성.
    mw = MW()

    # Qt event loop 실행.
    sys.exit(app.exec())
```

---

## QInputDialog.getItem()

`getItem()`은 사용자에게 item list를 제시하고, 그 중 하나를 선택하도록 하는 static method임.

직접 text를 입력받기보다, 미리 정해진 후보 중 하나를 고르게 하고 싶을 때 사용함.
예를 들어 category, option, mode, preset 등을 선택하게 할 때 적합함.

내부적으로는 `QComboBox` 기반의 widget을 사용함.
따라서 dropdown list 형태로 item들을 보여주고, 사용자는 그 중 하나를 선택할 수 있음.

```python
ret_item, is_ok = QInputDialog.getItem(
    parent,        # 부모 widget
    title,         # dialog title
    label_text,    # input field 위의 label text
    items,         # item list
    current=0,     # 처음 선택되어 있을 item의 index
    editable=True, # text 직접 입력 가능 여부
)
```

`getItem()`에서 중요한 인자는 다음과 같음.

* `items` : 사용자에게 보여줄 item list.
* `current` : dialog가 처음 열렸을 때 선택되어 있을 item의 index.
* `editable` : `True`이면 list에 없는 text도 직접 입력할 수 있고, `False`이면 주어진 item 중에서만 선택할 수 있음.

### Example

```python
import sys

from PySide6.QtWidgets import (
        QApplication, QMainWindow,
        QWidget, QPushButton, QLabel, QVBoxLayout,
        QInputDialog)

class MW (QMainWindow):

    def __init__(self):
        super(MW, self).__init__()

        # UI 구성을 별도의 method로 분리.
        self.init_ui()

        # main window를 화면에 표시.
        self.show()

    def init_ui(self):
        
        # QInputDialog.getItem()을 실행하기 위한 button.
        self.button0 = QPushButton('Test.')

        # button이 clicked signal을 발생시키면 slot00()이 호출됨.
        self.button0.clicked.connect(self.slot00)

        # 사용자가 선택한 item을 표시할 label.
        self.ret_label = QLabel()

        # button과 label을 위에서 아래로 배치하기 위한 layout.
        layout = QVBoxLayout()
        layout.addWidget(self.button0)
        layout.addWidget(self.ret_label)
        
        # layout을 담을 QWidget을 만들고,
        # 이를 QMainWindow의 central widget으로 사용함.
        tmp = QWidget()
        tmp.setLayout(layout)

        self.setCentralWidget(tmp)

    def slot00(self):
        # 현재 slot을 호출한 sender object를 확인.
        print(self.sender())

        sender = self.sender()

        if sender == self.button0:

            # item list 중 하나를 선택하기 위한 dialog를 실행.
            ret_item, is_ok = QInputDialog.getItem(
                    self,                       # parent widget
                    "Input Item",               # dialog title
                    "Select Your Value!",       # input field 위의 label text
                    ["faith", "hope", "love"], # item list
                    0,                          # 처음 선택되어 있을 item의 index
                    )

            # 사용자가 OK를 누른 경우에만 선택값을 사용함.
            if is_ok:
                # 선택된 item을 label에 표시.
                self.ret_label.setText(f'{ret_item}')

if __name__ == "__main__":
    # Qt application 객체 생성.
    app = QApplication(sys.argv)

    # main window 생성.
    mw = MW()

    # Qt event loop 실행.
    sys.exit(app.exec())
```

`getItem()`에서 `editable`을 생략하면 기본값은 `True`임.
따라서 사용자가 list에 없는 text도 직접 입력할 수 있음.
주어진 item 중에서만 선택하도록 제한하려면 `editable=False`를 명시하면 됨.

