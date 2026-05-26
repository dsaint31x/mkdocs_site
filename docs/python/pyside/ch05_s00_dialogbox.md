---
title: PySide6 Dialog 기본 코드
summary: PySide6에서 Dialog 또는 Dialog box를 다루기 위한 기본 stub code.
tags:
  - PySide6
  - Qt
  - QDialog
  - Dialog
  - Dialog Box
  - GUI
---

# PySide6에서 Dialog 사용하기

Dialog는 

* 사용자에게 정보를 보여주거나, 
* 사용자로부터 간단한 입력을 받기 위해 사용되는 GUI 구성 요소임.

> Dialog는 흔히 **Dialog box**라고도 부름.

PySide6에서는 Custom Dialog를 직접 만들 수도 있으나, Qt에서 미리 제공하는 built-in dialog를 사용하는 경우가 많음.

이 장에서는 PySide6에서 이들 built-in Dialog를 사용하는 방법을 살펴볼 예정임.

우선 이후 예제에서 공통으로 사용할 기본 stub code는 다음과 같음:

```python
import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
)


class MW(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main window의 title 설정.
        self.setWindowTitle("QDialog Example")

        # Dialog를 띄우기 위한 테스트용 button 생성.
        button = QPushButton("Press me for a dialog!", self)

        # button이 click되면 button_clicked method가 호출되도록 연결.
        button.clicked.connect(self.button_clicked)

        # button을 QMainWindow의 central widget으로 설정.
        self.setCentralWidget(button)

        # Main window를 화면에 표시.
        self.show()

    def button_clicked(self, s):
        # Dialog 관련 기능 테스트를 위한 method.
        print("click", s)

        # ----------------------
        # 이후 예제에서 이 위치에 
        # dialog 관련 코드가 작성될 예정임.


if __name__ == "__main__":
    # Qt application 객체 생성.
    app = QApplication(sys.argv)

    # Main window 객체 생성.
    wnd = MW()

    # Qt event loop 시작.
    app.exec()
```

다시 강조하지만, 위 코드는 특정 Dialog를 만드는 완성 예제가 아님.

* 이어지는 각각의 절에서 `button_clicked()` method 내부에 `QDialog`, `QMessageBox`, `QFileDialog` 등 Dialog 관련 코드를 추가될 예정임.
* 이를 통해 Dialog를 PySide에서 사용하기 위한 방법을 익실 수 있음.
