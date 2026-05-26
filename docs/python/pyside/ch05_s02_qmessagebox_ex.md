---
title: QMessageBox 예제 코드
summary: PySide6에서 QMessageBox의 information, warning, critical, question dialog를 사용하는 예제 코드를 정리함.
tags:
    - python
    - pyside6
    - pyqt
    - qt
    - qmessagebox
    - dialog
    - gui
---

# QMessageBox 예제 코드

`QMessageBox`의 static method를 사용하면 사용자에게 message dialog를 간단히 표시할 수 있음.  
아래 예제들은 버튼을 클릭했을 때 각각 `information()`, `warning()`, `critical()`, `question()` dialog를 띄우는 코드임.

---

## information

`information()`은 사용자에게 일반적인 정보 message를 보여줄 때 사용됨.  
작업 완료, 상태 안내, 단순 공지처럼 심각하지 않은 내용을 전달하는 데 적합함.

```python
import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QMessageBox,
)


class MW(QMainWindow):
    def __init__(self):
        super().__init__()

        # main window의 title 설정.
        self.setWindowTitle("QMessageBox.information Example")

        # dialog를 띄우기 위한 button 생성.
        button = QPushButton("Press me for a dialog!", self)

        # button 클릭 시 button_clicked method가 호출되도록 signal-slot 연결.
        button.clicked.connect(self.button_clicked)

        # button을 main window의 central widget으로 지정.
        self.setCentralWidget(button)

        # main window 표시.
        self.show()

    def button_clicked(self, checked):
        # button click signal에서 전달된 checked 상태 출력.
        print("click", checked)

        # information dialog 표시.
        # Ok와 Cancel button을 표시하고, 기본 선택 button은 Ok로 지정함.
        result = QMessageBox.information(
            self,
            "Message",
            "This is an information message.",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Ok,
        )

        # 사용자가 누른 button 값 출력.
        print("Dialog result:", result)


if __name__ == "__main__":
    # Qt application instance 생성.
    app = QApplication(sys.argv)

    # main window instance 생성.
    wnd = MW()

    # Qt event loop 실행.
    app.exec()
```

---

## warning

`warning()`은 사용자에게 주의가 필요한 message를 보여줄 때 사용됨.  
작업을 계속할 수는 있지만, 사용자가 확인해야 할 조건이나 위험 가능성이 있을 때 적합함.

```python
import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QMessageBox,
)


class MW(QMainWindow):
    def __init__(self):
        super().__init__()

        # main window의 title 설정.
        self.setWindowTitle("QMessageBox.warning Example")

        # dialog를 띄우기 위한 button 생성.
        button = QPushButton("Press me for a dialog!", self)

        # button 클릭 시 button_clicked method가 호출되도록 signal-slot 연결.
        button.clicked.connect(self.button_clicked)

        # button을 main window의 central widget으로 지정.
        self.setCentralWidget(button)

        # main window 표시.
        self.show()

    def button_clicked(self, checked):
        # button click signal에서 전달된 checked 상태 출력.
        print("click", checked)

        # warning dialog 표시.
        # Ok와 Cancel button을 표시하고, 기본 선택 button은 Ok로 지정함.
        result = QMessageBox.warning(
            self,
            "Warning",
            "This is a warning message.",
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Ok,
        )

        # 사용자가 누른 button 값 출력.
        print("Dialog result:", result)


if __name__ == "__main__":
    # Qt application instance 생성.
    app = QApplication(sys.argv)

    # main window instance 생성.
    wnd = MW()

    # Qt event loop 실행.
    app.exec()
```

---

## critical

`critical()`은 사용자에게 심각한 오류 message를 보여줄 때 사용됨.  
프로그램 실행을 계속하기 어렵거나, 즉시 확인이 필요한 오류 상황을 알릴 때 적합함.

```python
import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QMessageBox,
)


class MW(QMainWindow):
    def __init__(self):
        super().__init__()

        # main window의 title 설정.
        self.setWindowTitle("QMessageBox.critical Example")

        # dialog를 띄우기 위한 button 생성.
        button = QPushButton("Press me for a dialog!", self)

        # button 클릭 시 button_clicked method가 호출되도록 signal-slot 연결.
        button.clicked.connect(self.button_clicked)

        # button을 main window의 central widget으로 지정.
        self.setCentralWidget(button)

        # main window 표시.
        self.show()

    def button_clicked(self, checked):
        # button click signal에서 전달된 checked 상태 출력.
        print("click", checked)

        # critical dialog 표시.
        # 심각한 오류 message를 사용자에게 보여줄 때 사용함.
        result = QMessageBox.critical(
            self,
            "Critical",
            "This is a critical error message.",
            QMessageBox.StandardButton.Ok,
            QMessageBox.StandardButton.Ok,
        )

        # 사용자가 누른 button 값 출력.
        print("Dialog result:", result)


if __name__ == "__main__":
    # Qt application instance 생성.
    app = QApplication(sys.argv)

    # main window instance 생성.
    wnd = MW()

    # Qt event loop 실행.
    app.exec()
```

---

## question

`question()`은 사용자에게 질문을 제시하고, 사용자의 응답을 반환값으로 받을 때 사용됨.  
반환된 button 값을 비교하면 사용자의 선택에 따라 이후 동작을 분기할 수 있음.

```python
import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QMessageBox,
)


class MW(QMainWindow):
    def __init__(self):
        super().__init__()

        # main window의 title 설정.
        self.setWindowTitle("QMessageBox.question Example")

        # dialog를 띄우기 위한 button 생성.
        button = QPushButton("Press me for a dialog!", self)

        # button 클릭 시 button_clicked method가 호출되도록 signal-slot 연결.
        button.clicked.connect(self.button_clicked)

        # button을 main window의 central widget으로 지정.
        self.setCentralWidget(button)

        # main window 표시.
        self.show()

    def button_clicked(self, checked):
        # button click signal에서 전달된 checked 상태 출력.
        print("click", checked)

        # question dialog 표시.
        # Yes와 No button을 제공하고, 기본 선택 button은 Yes로 지정함.
        response = QMessageBox.question(
            self,
            "Question Message",
            "Do you like PySide6?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes,
        )

        # 사용자가 선택한 button에 따라 분기.
        if response == QMessageBox.StandardButton.Yes:
            print("User likes PySide6!")
        else:
            print("User does not like PySide6!")

        # 사용자가 누른 button 값 출력.
        print("Dialog result:", response)


if __name__ == "__main__":
    # Qt application instance 생성.
    app = QApplication(sys.argv)

    # main window instance 생성.
    wnd = MW()

    # Qt event loop 실행.
    app.exec()
```
