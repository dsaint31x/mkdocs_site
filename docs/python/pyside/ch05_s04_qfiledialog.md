---
title: QFileDialog로 file과 directory 선택하기
tags:
  - Python
  - PySide6
  - Qt
  - QFileDialog
  - Dialog
  - GUI
---

# QFileDialog로 file과 directory 선택하기

> ***QFileDialog***  
> file이나 directory를 열거나 선택할 때 사용하는 built-in dialog.

`QFileDialog`는 Qt Framework에서 제공하는 Standard Dialog Box 중 하나임.

사용자가 file이나 directory를 선택하면, 해당 위치에 대한 path 문자열을 얻을 수 있는 interface를 제공함.

`QFileDialog`는 다음과 같은 경우에 사용됨.

* file을 열기 위해 path를 선택해야 하는 경우
* 여러 files를 한 번에 선택해야 하는 경우
* 저장할 file name과 directory를 선택해야 하는 경우
* 특정 directory를 선택해야 하는 경우
* OS의 native file dialog box style을 사용하여 자연스러운 사용자 경험을 제공해야 하는 경우

앞서 살펴본 `QMessageBox`, `QInputDialog`처럼 `QFileDialog`도 static method를 이용하면 간단히 사용할 수 있음.  
별도의 dialog class를 직접 만들지 않아도 file system과 사용자 사이의 기본적인 상호작용을 처리할 수 있음.

---

## QFileDialog의 주요 static methods

`QFileDialog`에서 자주 사용하는 static methods는 다음과 같음.

| Method | 용도 | 반환값 |
|---|---|---|
| `getOpenFileName()` | 단일 file 선택 | `(file_path, selected_filter)` |
| `getOpenFileNames()` | 복수 files 선택 | `(file_paths, selected_filter)` |
| `getSaveFileName()` | 저장할 file path 선택 | `(file_path, selected_filter)` |
| `getExistingDirectory()` | directory 선택 | `directory_path` |

주의할 점은 `getOpenFileName()`, `getOpenFileNames()`, `getSaveFileName()`의 두 번째 반환값이  
`is_ok` 같은 boolean 값이 아니라 **선택된 filter 문자열** 이라는 점임.

즉, 다음과 같은 형태임.

```python
file_name, selected_filter = QFileDialog.getOpenFileName(...)
```

사용자가 실제로 선택했는지는 반환된 path가 빈 문자열인지 확인하면 됨.

```python
if file_name:
    print("file selected")
else:
    print("cancelled")
```

---

## 단일 file 선택: getOpenFileName

`getOpenFileName()`은 사용자에게 단일 file을 선택하도록 요청함.

선택된 file의 path 문자열과 선택된 filter 문자열을 tuple로 반환함.

반환값은 다음과 같음.

* `file_name`: 사용자가 선택한 file의 path 문자열
* `selected_filter`: 사용자가 선택한 file filter 문자열

사용자가 `Cancel`을 누르면 `file_name`은 빈 문자열 `""`이 됨.

다음은 `getOpenFileName()`을 사용하는 독립 실행 가능한 예제임.

```python
import sys

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QPushButton,
)


class MW(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("QFileDialog.getOpenFileName Example")

        # button을 central widget으로 설정함.
        # button을 누르면 단일 file 선택 dialog가 표시됨.
        button = QPushButton("Open File", self)
        button.clicked.connect(self.open_file)

        self.setCentralWidget(button)
        self.show()

    def open_file(self):
        # 단일 file을 선택하는 dialog.
        # 반환값은 file path 문자열과 선택된 filter 문자열임.
        file_name, selected_filter = QFileDialog.getOpenFileName(
            self,                              # parent widget
            "Open file",                       # dialog title
            "",                                # start directory
            "Text files (*.txt *.html *.py);;All files (*.*)",
        )

        # 사용자가 Cancel을 누르면 file_name은 빈 문자열임.
        if file_name:
            QMessageBox.information(
                self,
                "Selected File",
                f"File: {file_name}\nFilter: {selected_filter}",
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MW()

    sys.exit(app.exec())
```

위 코드에서는 extension이 `.txt`, `.html`, `.py`인 file을 선택할 수 있음.
`All files (*.*)` filter를 선택하면 모든 file을 선택할 수 있음.

---

## 복수 files 선택: getOpenFileNames

`getOpenFileNames()`는 사용자에게 여러 files를 선택하도록 요청함.

`getOpenFileName()`과 거의 같지만, 반환되는 첫 번째 값이 문자열 하나가 아니라 list임.

반환값은 다음과 같음.

* `file_names`: 선택된 file path 문자열들의 list
* `selected_filter`: 사용자가 선택한 file filter 문자열

다음은 `getOpenFileNames()`를 사용하는 독립 실행 가능한 예제임.

```python
import sys

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QPushButton,
)


class MW(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("QFileDialog.getOpenFileNames Example")

        # button을 누르면 복수 file 선택 dialog가 표시됨.
        button = QPushButton("Open Files", self)
        button.clicked.connect(self.open_files)

        self.setCentralWidget(button)
        self.show()

    def open_files(self):
        # 복수 file을 선택하는 dialog.
        # 첫 번째 반환값은 file path 문자열들의 list임.
        file_names, selected_filter = QFileDialog.getOpenFileNames(
            self,
            "Open files",
            "",
            "Images (*.png *.jpg *.jpeg);;Text files (*.txt);;All files (*.*)",
        )

        # 사용자가 하나 이상의 file을 선택한 경우 list가 비어 있지 않음.
        if file_names:
            QMessageBox.information(
                self,
                "Selected Files",
                "\n".join(file_names) + f"\n\nFilter: {selected_filter}",
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MW()

    sys.exit(app.exec())
```

여러 files를 선택해야 하므로, dialog에서 `Ctrl` 또는 `Shift`를 이용하여 여러 항목을 선택할 수 있음.

---

## 저장할 file path 선택: getSaveFileName

`getSaveFileName()`은 사용자에게 저장할 file name과 directory를 선택하도록 요청함.

주의할 점은 `getSaveFileName()`이 실제 file을 저장해주는 method가 아니라는 점임.

이 method는 저장할 위치와 file name만 선택하게 해줌.
실제 저장 작업은 반환된 path를 이용하여 직접 처리해야 함.

다음은 `getSaveFileName()`을 사용하는 독립 실행 가능한 예제임.

```python
import sys

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QPushButton,
)


class MW(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("QFileDialog.getSaveFileName Example")

        # button을 누르면 저장할 file path를 선택하는 dialog가 표시됨.
        button = QPushButton("Save File", self)
        button.clicked.connect(self.save_file)

        self.setCentralWidget(button)
        self.show()

    def save_file(self):
        # 저장할 file path를 선택하는 dialog.
        # 이 method는 실제 저장을 수행하지 않고, 저장할 path만 반환함.
        file_name, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Save file",
            "",
            "Text files (*.txt);;Python files (*.py);;All files (*.*)",
        )

        # 사용자가 Cancel을 누르면 file_name은 빈 문자열임.
        if file_name:
            # 실제 file 저장은 반환된 path를 이용하여 직접 수행해야 함.
            with open(file_name, "w", encoding="utf-8") as f:
                f.write("Hello QFileDialog\n")
                f.write(f"Selected filter: {selected_filter}\n")

            QMessageBox.information(
                self,
                "Saved",
                f"File saved to:\n{file_name}",
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MW()

    sys.exit(app.exec())
```

이 예제에서는 사용자가 선택한 path에 실제로 text file을 저장함.

다만 기존 file을 선택하면 overwrite될 수 있으므로, 실제 application에서는 overwrite 여부를 더 명확히 처리하는 것이 좋음.

---

## directory 선택: getExistingDirectory

`getExistingDirectory()`는 사용자에게 directory를 선택하도록 요청함.

file 대신 directory가 대상이라는 점을 제외하면 `getOpenFileName()`과 유사함.

`getExistingDirectory()`는 file path가 아니라 directory path를 반환함.

사용자가 취소한 경우 빈 문자열 `""`이 반환되므로, 다음과 같이 선택 여부를 확인할 수 있음.

```python
if directory_path:
    print("directory selected")
```

다음은 `getExistingDirectory()`를 사용하는 독립 실행 가능한 예제임.

```python
import sys

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QPushButton,
)


class MW(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("QFileDialog.getExistingDirectory Example")

        # button을 누르면 directory 선택 dialog가 표시됨.
        button = QPushButton("Open Directory", self)
        button.clicked.connect(self.open_directory)

        self.setCentralWidget(button)
        self.show()

    def open_directory(self):
        # directory를 선택하는 dialog.
        directory_path = QFileDialog.getExistingDirectory(
            self,
            "Select a Directory",
            "",
            QFileDialog.Option.ShowDirsOnly,
        )

        # 사용자가 directory를 선택한 경우 directory_path는 빈 문자열이 아님.
        if directory_path:
            QMessageBox.information(
                self,
                "Selected Directory",
                f"Directory: {directory_path}",
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MW()

    sys.exit(app.exec())
```

`QFileDialog.Option.ShowDirsOnly`를 사용하면 directory 선택에 집중된 dialog로 동작함.

---

## file filter 사용하기

`QFileDialog`에서는 file filter를 사용하여 dialog에 표시하거나 선택할 수 있는 file 종류를 제한할 수 있음.

```python
file_name, selected_filter = QFileDialog.getOpenFileName(
    self,
    "Open file",
    "",
    "HTML Files (*.html);;Text Files (*.txt)"
)
```

4번째 positional argument가 file filter에 해당함.

여러 filter를 제공하려면 `;;`을 구분자로 사용함.

```python
"HTML Files (*.html);;Text Files (*.txt);;Python Files (*.py)"
```

여러 extension을 하나의 filter에 포함시키려면 공백으로 구분함.

```python
"Source Files (*.py *.cpp *.h)"
```

따라서 다음과 같이 작성하는 것이 일반적임.

```python
"Text files (*.txt *.html *.py)"
```

`*.txt, *.html, *.py`처럼 comma로 구분하지 않는 것이 일반적임.

다음은 file filter를 확인하기 위한 독립 실행 가능한 예제임.

```python
import sys

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QPushButton,
)


class MW(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("QFileDialog File Filter Example")

        # button을 누르면 여러 file filter를 가진 dialog가 표시됨.
        button = QPushButton("Open File with Filter", self)
        button.clicked.connect(self.open_file_with_filter)

        self.setCentralWidget(button)
        self.show()

    def open_file_with_filter(self):
        # 여러 filter를 제공할 때는 ';;'로 구분함.
        file_name, selected_filter = QFileDialog.getOpenFileName(
            self,
            "Open file",
            "",
            "HTML Files (*.html);;Text Files (*.txt);;Python Files (*.py);;All files (*.*)",
        )

        if file_name:
            QMessageBox.information(
                self,
                "Selected File",
                f"File: {file_name}\nFilter: {selected_filter}",
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MW()

    sys.exit(app.exec())
```

이 예제에서는 사용자가 어떤 filter를 선택했는지도 함께 확인할 수 있음.

---

## QFileDialog.Option enum

`enum`은 미리 정해진 이름 있는 상수들의 집합으로, code에서 option이나 상태값을 의미 있는 이름으로 표현하기 위해 사용됨.

`QFileDialog`는 `QFileDialog.Option` enum을 통해 다양한 추가 options를 제공함.

이를 통해 file dialog box의 동작과 appearance를 좀 더 세밀하게 제어할 수 있음.

static method에서는 `options` parameter를 통해 설정함.

여러 option을 함께 사용할 때는 다른 flag enum과 마찬가지로 bitwise OR 연산자 `|`를 사용함.

```python
options = (
    QFileDialog.Option.ShowDirsOnly
    | QFileDialog.Option.DontResolveSymlinks
)
```

---

## 자주 사용하는 QFileDialog options

### DontUseNativeDialog

시스템이 제공하는 native dialog style을 사용하지 않도록 설정함.

이 option을 사용하면 OS native dialog 대신 Qt가 제공하는 standard dialog가 사용됨.

특정 OS의 native dialog에서 문제가 발생하거나, Qt dialog의 동작을 직접 제어해야 할 때 사용할 수 있음.

```python
QFileDialog.Option.DontUseNativeDialog
```

---

### ShowDirsOnly

directory만 표시하도록 설정함.

주로 `getExistingDirectory()`에서 사용됨.

```python
QFileDialog.Option.ShowDirsOnly
```

---

### DontConfirmOverwrite

`getSaveFileName()`에서 사용자가 기존 file을 선택했을 때, overwrite 여부를 확인하는 추가 dialog를 띄우지 않도록 설정함.

```python
QFileDialog.Option.DontConfirmOverwrite
```

---

### ReadOnly

dialog를 read-only mode로 설정함.

```python
QFileDialog.Option.ReadOnly
```

---

### HideNameFilterDetails

file filter에서 extension 세부사항을 숨김.

예를 들어 기본적으로 다음과 같이 보이는 filter가

```text
Images (*.tif *.png)
```

다음과 같이 표시될 수 있음.

```text
Images
```

```python
QFileDialog.Option.HideNameFilterDetails
```

---

### DontResolveSymlinks

symbolic link를 실제 대상 path로 해석하지 않고, link 자체로 처리함.

symbolic link의 원래 path를 유지해야 할 때 사용할 수 있음.

```python
QFileDialog.Option.DontResolveSymlinks
```

---

### DontUseSheet

macOS에서 dialog가 sheet 형태로 표시되지 않도록 설정함.

sheet는 macOS에서 특정 parent window에 붙어서 내려오는 modal dialog 형태를 가리킴.

이 option을 사용하면 dialog가 sheet가 아니라 독립적인 dialog box처럼 표시됨.

```python
QFileDialog.Option.DontUseSheet
```

---

## option을 함께 사용하는 예제

다음은 `QFileDialog.Option`을 함께 사용하는 독립 실행 가능한 예제임.

```python
import sys

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QPushButton,
)


class MW(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("QFileDialog.Option Example")

        # button을 누르면 options가 적용된 directory 선택 dialog가 표시됨.
        button = QPushButton("Open Directory with Options", self)
        button.clicked.connect(self.open_directory_with_options)

        self.setCentralWidget(button)
        self.show()

    def open_directory_with_options(self):
        # 여러 option은 bitwise OR 연산자 | 로 함께 지정할 수 있음.
        options = (
            QFileDialog.Option.ShowDirsOnly
            | QFileDialog.Option.DontResolveSymlinks
        )

        directory_path = QFileDialog.getExistingDirectory(
            self,
            "Select a Directory",
            "",
            options,
        )

        if directory_path:
            QMessageBox.information(
                self,
                "Selected Directory",
                f"Directory: {directory_path}",
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MW()

    sys.exit(app.exec())
```

이 예제에서는 directory만 선택하도록 하고, symbolic link를 실제 대상 path로 해석하지 않도록 설정함.

---

## 정리

`QFileDialog`는 file이나 directory를 선택하기 위한 built-in dialog임.

* 단일 file 선택: `getOpenFileName()`
* 복수 file 선택: `getOpenFileNames()`
* 저장할 file path 선택: `getSaveFileName()`
* directory 선택: `getExistingDirectory()`

file 선택 관련 static methods는 대체로 다음과 같은 반환값을 가짐.

```python
file_path, selected_filter = QFileDialog.getOpenFileName(...)
```

여기서 두 번째 반환값은 boolean이 아니라 선택된 filter 문자열임.

따라서 사용자가 실제로 file을 선택했는지는 첫 번째 반환값이 빈 문자열인지 여부로 확인하는 것이 일반적임.

```python
if file_path:
    # 사용자가 file을 선택한 경우
    pass
```

`getSaveFileName()`도 마찬가지로 실제 저장을 수행하지 않음.
저장할 path만 선택하게 해주므로, 실제 file write는 별도로 구현해야 함.
