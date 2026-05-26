---
title: QMessageBox 기본 사용법
summary: QMessageBox의 역할, modal dialog 동작 방식, 주요 static methods의 용도를 정리함.
tags:
    - python
    - pyside6
    - pyqt
    - qmessagebox
    - dialog
---

# QMessageBox 기본 사용법

`QMessageBox`는 사용자에게 message를 전달하거나, 사용자의 간단한 선택을 입력받기 위해 사용하는 dialog임.

주로 다음과 같은 용도로 사용됨.

- 일반 정보 안내
- 경고 표시
- 오류 또는 치명적 문제 표시
- 사용자에게 `Yes` / `No` 같은 간단한 질문 제시
- application의 이름, 버전, 제작자, 로고, 저작권, 법적 정보 등을 보여주는 About dialog 표시

즉, `QMessageBox`는 사용자에게 전달할 message의 성격에 따라 `information`, `warning`, `critical`, `question`, `about` 등의 형태로 사용됨.

일반적으로 `QMessageBox`는 modal dialog로 사용됨.  

* 즉, 사용자가 dialog에 응답하기 전까지 현재 작업 흐름이 대기함.
* modeless 또는 비동기 방식으로 사용하려면 `QMessageBox` 객체를 직접 생성한 뒤 `exec()`가 아니라 `open()`을 사용할 수 있음.  
    * 하지만 이 경우 사용자의 선택 결과를 반환값으로 바로 받는 것이 아니라, signal-slot을 통해 처리해야 함. 
* 일반적인 간단한 message box에서는 주로 modal dialog가 사용됨.

## 사용법

PyQt와 PySide가 제공하는 `QMessageBox`는 자주 사용되는 message dialog를 간단히 생성하고 표시하기 위한 static methods를 제공함.

대표적인 static methods는 다음과 같음.

```python
QMessageBox.information(parent, title, message)
QMessageBox.warning(parent, title, message)
QMessageBox.critical(parent, title, message)
QMessageBox.question(parent, title, message)
QMessageBox.about(parent, title, message)
```

각 method의 용도는 다음과 같음.

| Method          | 용도                                         |
| --------------- | ------------------------------------------ |
| `information()` | 일반적인 정보 message 표시                         |
| `warning()`     | 주의나 경고 message 표시                          |
| `critical()`    | 심각한 오류 message 표시                          |
| `question()`    | 사용자에게 질문을 제시하고 선택을 받음                      |
| `about()`       | application 정보, 제작자, 버전, 저작권 등의 message 표시 |

* 이들 static method는 dialog를 생성하고 화면에 표시한 뒤, 사용자의 선택 결과를 반환함.

> 참고로, `about()`은 보통 application 정보를 보여주는 용도로 사용되므로, 사용자의 선택을 세밀하게 처리하는 용도보다는 정보 표시 목적이 강함.  
> 일부 문헌에선 Message Dialog로 분류하지 않기도 함.

===

## 주요 static methods 사용 예제

앞서 살펴본 `QMessageBox`의 static methods는 사용 방식이 서로 비슷함.

기본적으로 다음과 같은 형태로 사용됨.

```python
QMessageBox.method_name(
    parent,
    title,
    message,
    buttons,
)
```

---

### `information()`

`information()`은 사용자에게 일반적인 정보 message를 보여주기 위해 사용됨.

```python
QMessageBox.information(
    self,                           # parent
    "info title",                   # title
    "info content",                 # message
    QMessageBox.StandardButton.Ok,  # button
)
```

`information()`은 작업 완료, 상태 안내, 단순 공지처럼 사용자에게 일반적인 정보를 전달할 때 사용됨.

---

### `warning()`

`warning()`은 사용자에게 주의가 필요한 message를 보여주기 위해 사용됨.

```python
QMessageBox.warning(
    self,                           # parent
    "warning title",                # title
    "warning content",              # message
    QMessageBox.StandardButton.Ok,  # button
)
```

`warning()`은 작업을 계속할 수는 있지만, 사용자가 주의해야 할 상황을 알릴 때 사용됨.

예를 들어 저장되지 않은 내용이 있거나, 설정값이 부적절하거나, 이후 작업에 문제가 생길 수 있음을 알릴 때 사용할 수 있음.

---

### `critical()`

`critical()`은 사용자에게 심각한 오류 message를 보여주기 위해 사용됨.

```python
QMessageBox.critical(
    self,                           # parent
    "critical title",               # title
    "critical content",             # message
    QMessageBox.StandardButton.Ok,  # button
)
```

`critical()`은 프로그램 실행에 문제가 있거나, 사용자의 작업을 계속 진행하기 어려운 오류를 알릴 때 사용됨.

> `information()`, `warning()`, `critical()`은  
> 사용 방식은 거의 같지만,  
> 표시되는 icon과 message의 의미적 중요도가 다름.

---

### `question()`

`question()`은 사용자에게 질문을 제시하고, 사용자의 응답을 받기 위해 사용됨.

```python
ans = QMessageBox.question(
    self,                              # parent
    "title of question",              # title
    "content of question",            # message
    QMessageBox.StandardButton.No |
    QMessageBox.StandardButton.Yes,    # buttons
    QMessageBox.StandardButton.Yes,    # default button
)
```

* 4번째 argument는 질문에 대한 답으로 제공할 button들을 지정하는 부분임.
* 위 예제에서는 `QMessageBox.StandardButton` enum의 `No`와 `Yes`가 dialog에 표시됨.
* 5번째 argument는 dialog가 처음 표시될 때 기본으로 선택되어 있는 button임.
* 반환값은 사용자가 선택한 button임.

다음과 같이 반환값을 받아 적절한 처리를 하도록 구현됨:

```python
if ans == QMessageBox.StandardButton.Yes:
    print("User selected Yes.")
else:
    print("User selected No.")
```

---

### `about()`

`about()`은 S/W의 정보 등을 보여주는 **About Dialog**를 생성하는 데 사용됨.

`about()`도 `QMessageBox`에서 제공하는 static method임.  
즉, application에 대한 정보를 사용자에게 전달하는 message dialog를 간단히 만들 때 사용됨.

```python
QMessageBox.about(
    self,                # parent
    "About This SW",     # title of about dialog
    """<p>The example of QMessageBox</p>
    <p>version 0.1</p>"""
)
```

* Dialog에 표시되는 문자열은 plain text뿐 아니라, 일부 HTML tag를 지원하는 rich text도 가능함.

`QMessageBox`의 icon을 직접 지정해야 하는 경우에는 static method가 아니라 `QMessageBox` 객체를 직접 생성한 뒤 `setIcon()` 또는 `setIconPixmap()`을 사용하는 방식이 적절함.

다음의 예제 코드를 참고:

```python
msg_box = QMessageBox(self)
msg_box.setWindowTitle("About This SW")
msg_box.setText(
    """<p>The example of QMessageBox</p>
    <p>version 0.1</p>"""
)
msg_box.setIconPixmap(QPixmap("app_icon.png"))
msg_box.exec()
```

* 단순한 About Dialog는 `QMessageBox.about()`을 사용하고,
* icon이나 세부 속성을 직접 제어해야 하면 `QMessageBox` instance를 만들어 사용하는 것이 적절함.
* 이때 표시되는 icon은 application에서 사용하는 `QApplication` instance의 `setWindowIcon()`에 설정된 `QIcon` instance 를 통해 변경가능함.

---

## `QMessageBox`에서 지원하는 Buttons

위 예제에서는 `QMessageBox.StandardButton`의 button들을 사용했음.

`QMessageBox`에서는 상황에 따라 다음과 같은 standard button들을 선택해서 사용할 수 있음.

- `QMessageBox.StandardButton.Ok`
- `QMessageBox.StandardButton.Cancel`
- `QMessageBox.StandardButton.Open`
- `QMessageBox.StandardButton.Close`
- `QMessageBox.StandardButton.Save`
- `QMessageBox.StandardButton.SaveAll`
- `QMessageBox.StandardButton.Discard`
- `QMessageBox.StandardButton.Apply`
- `QMessageBox.StandardButton.Reset`
- `QMessageBox.StandardButton.RestoreDefaults`
- `QMessageBox.StandardButton.Help`
- `QMessageBox.StandardButton.Yes`
- `QMessageBox.StandardButton.YesToAll`
- `QMessageBox.StandardButton.No`
- `QMessageBox.StandardButton.NoToAll`
- `QMessageBox.StandardButton.Abort`
- `QMessageBox.StandardButton.Ignore`
- `QMessageBox.StandardButton.Retry`
- `QMessageBox.StandardButton.NoButton`

* PySide6에서는 `QMessageBox.Ok`처럼 간단한 축양형으로 사용하는 방식보다  
* `QMessageBox.StandardButton.Ok`처럼 enum 을 사용하는 방식이 더 명확함.

> 참고로, `QMessageBox.StandardButton.NoButton`은 실제로 표시할 button이 아니라, “button 없음”을 의미하는 값임.

여러 button을 동시에 표시하려면 bitwise OR 연산자 `|`를 사용함.

```python
buttons = (
    QMessageBox.StandardButton.Yes |
    QMessageBox.StandardButton.No |
    QMessageBox.StandardButton.Cancel
)
```

이렇게 지정하면 dialog에 `Yes`, `No`, `Cancel` button이 함께 표시됨.

다음은 위의 버튼들을 확인할 수 있는 코드임

```python
import sys

from PySide6.QtWidgets import QApplication, QMessageBox


def show_all_buttons_dialog():
    buttons = (
        QMessageBox.StandardButton.Ok
        | QMessageBox.StandardButton.Cancel
        | QMessageBox.StandardButton.Open
        | QMessageBox.StandardButton.Close
        | QMessageBox.StandardButton.Save
        | QMessageBox.StandardButton.SaveAll
        | QMessageBox.StandardButton.Discard
        | QMessageBox.StandardButton.Apply
        | QMessageBox.StandardButton.Reset
        | QMessageBox.StandardButton.RestoreDefaults
        | QMessageBox.StandardButton.Help
        | QMessageBox.StandardButton.Yes
        | QMessageBox.StandardButton.YesToAll
        | QMessageBox.StandardButton.No
        | QMessageBox.StandardButton.NoToAll
        | QMessageBox.StandardButton.Abort
        | QMessageBox.StandardButton.Ignore
        | QMessageBox.StandardButton.Retry
    )

    ans = QMessageBox.information(
        None,
        "All Standard Buttons",
        "This dialog shows most QMessageBox standard buttons.",
        buttons,
        QMessageBox.StandardButton.Ok,
    )

    print("Selected button:", ans)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    show_all_buttons_dialog()

    sys.exit(app.exec())
```


