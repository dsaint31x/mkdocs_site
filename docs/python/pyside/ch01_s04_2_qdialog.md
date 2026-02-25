---
title: QDialog
tags: [pyside6, pyqt6, qdialog, dialog, modal, modeless, custom-dialog]
---

## Module

* `PySide6.QtWidgets`
* `PyQt6.QtWidgets`

***`QDialog`***  
: PySide와 PyQt에서 사용되는 ***대화상자(Dialog Box)를 추상화*** 하여 <u>dialog에 필요한 표준 기능들을 미리 구현하고 있는 클래스</u>이다.

* **Modal** 과 **Modeless** (or Non-modal) Dialog를 만드는 데 사용된다.
    * **Modal Dialog**: `exec()` 메서드를 사용하여 실행한다. 사용자가 창을 닫기 전까지 다른 창과 상호작용할 수 없다.
    * **Modeless Dialog**: `show()` 메서드를 사용하여 실행한다. (`open()` 메서드는 Window-modal로 동작). 창이 열려 있어도 다른 창과 상호작용할 수 있다.
* 사실 `QDialog`를 직접 인스턴스화하여 사용하는 경우는 드물며, 주로 **Subclassing** 하여 다양한 button, text, field, label을 추가한 **Custom Dialog** 를 만드는 데 이용된다.
* GUI 프로그램에서 흔히 사용되는 파일 열기, 메시지 표시 등의 기능은 Qt에서 이미 **Built-in Dialog Classes** (`QMessageBox`, `QFileDialog` 등)로 제공하고 있다.
    * 이러한 Built-in Dialog들은 `QDialog`를 상속받아 구현된 클래스들이다.
    * 대부분 static method를 제공하므로, 인스턴스 생성 없이 간편하게 사용할 수 있다.

> **Dialog (대화상자)의 주요 용도**
> 
> * 사용자에게 특정 정보(Message)나 경고를 알릴 때
> * 사용자로부터 입력을 받아야 하는 경우 (예: 설정 변경, 이름 입력)
> * 파일 열기/저장, 폴더 선택 등을 수행할 때
> * Main Window의 흐름을 잠시 멈추고 사용자의 확인이 필요한 경우

---

## 예제 1: QDialog 간단 사용

다음 예제 코드는 `QDialog`를 직접 생성하여 사용하는 가장 기본적인 형태를 보여준다.

* 메인 윈도우의 버튼을 누르면,
* `"QDialog Title"`이라는 제목을 가진 빈 대화상자가 모달(Modal)로 열린다.

```Python
# -*- coding: utf-8 -*-
#
# first_dlg.py
#
# Description: QDialog를 생성하고 실행하는 가장 기본적인 방법을 보여주는 예제.
#              특히 'modeless' 방식인 open() 메서드 사용법을 다룸.
# Author: dsaint31
# Date: 2024-02-23
#

import sys

# Qt 바인딩 선택 로직 (PySide6/PyQt6 호환성)
try:
    from PySide6.QtWidgets import (QApplication, QDialog, QMainWindow, QPushButton)
except ImportError:
    try:
        from PyQt6.QtWidgets import (QApplication, QDialog, QMainWindow, QPushButton)
    except ImportError:
        print("Python을 위한 Qt 바인딩 라이브러리가 없습니다.")
        sys.exit(1)

# 메인 윈도우 class 정의
class MW(QMainWindow):
    def __init__(self):
        """ 생성자(Constructor) """
        super().__init__()
        self.setWindowTitle("QDialog Ex.")

        # 버튼을 누르면 대화상자를 열도록 설정
        button = QPushButton("Press it for a Dialog")
        button.clicked.connect(self.button_clicked)
        self.setCentralWidget(button)

    def button_clicked(self, s):
        """ 버튼 클릭 시 호출되는 슬롯 """
        print("click", s)
        
        # QDialog의 기본 인스턴스를 생성. 부모를 self(MW)로 지정.
        dlg = QDialog(self)
        dlg.setWindowTitle("QDialog Title")
        
        
        # Modal 방식 대화상자 코드 (이 예제에서는 사용되지 않음)
        dlg.exec()
        
        # 다음은 open()을 사용하여 대화상자를 'Modeless' 형태로 실행
        # Modeless: 이 대화상자가 열려 있어도 부모 윈도우(MW)를 계속 사용할 수 있음
        #           코드 실행을 멈추지 않음.
        # dlg.open()

# Main script로 동작하는 루틴 구현
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    window.show()
    # sys.exit()를 사용하여 application을 안전하게 종료
    sys.exit(app.exec())
```

* Modal dialog에 대한 예제이므로,
* Dialog를 위한 Event Loop가 동작하도록 `dlg.exec()`를 호출해줘야 함.

위의 예는 Dialog Box를 만드는 가장 간단한 경우로, `QDialog`를 위의 경우처럼 사용하는 경우는 사실 없음.

다음 예제와 같이  

* `QDialog`는 
* Custom Dialog를 만들기 위해 
* **부모 클래스** 로 사용되는 경우가 일반적임.

---

## 예제2: Custom Dialog

다음은 `QDialog`를 상속하여 Custom Dialog를 만드는 예제임.

해당 예제에서 `CustomDlg`는

* 고유의 title과 : `'Hello, QDialog'` 문자열 
* 특정 질문의 Label과 : `'Is something ok?'`
* **ok** 와 **cancel** 버튼을 가짐.

```Python
# QDialog를 상속받아 사용자 정의 대화상자 class를 정의
class CustomDlg(QDialog):
    def __init__(self, parent=None):
        """ 생성자(Constructor) """
        super().__init__(parent)

        self.setWindowTitle('Hello, QDialog')

        # QDialogButtonBox를 사용하여 표준 버튼 (OK, Cancel)을 생성
        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.button_box = QDialogButtonBox(buttons)
        # button_box의 accepted 시그널을 QDialog의 내장 슬롯인 accept에 연결
        self.button_box.accepted.connect(self.accept)
        # button_box의 rejected 시그널을 QDialog의 내장 슬롯인 reject에 연결
        self.button_box.rejected.connect(self.reject)

        # 대화상자 내부 레이아웃 설정
        self.layout = QVBoxLayout()
        message = QLabel('Is something ok?')
        self.layout.addWidget(message)
        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)
```

* Dialog의 경우, 부모 Widget의 근처에서 해당 Dialog가 열리는 게 일반적이기 때문에, 부모 Widget의 정보를 넘겨줘야 함.
    * 생성자 `def __init__(self, parent=None):`로 구현하여, 
    * `QDialog` instance가 생성될 때, 부모 widget의 instance를 넘겨주는 게 일반적임.
* 일반적인 `QButton` instance를 Dialog에 추가할 수도 있으나 위의 예처럼 `QDialogButtonBox`를 이용하여 버튼을 추가하는 게 일반적임.
    * Dialog Box에서 사용되는 ***Push button은 거의 정형화*** 되어 있기 때문에,
    * `QDialogButtonBox`를 통해 지원되는 버튼들을 사용하는 게 좋음.
* Layout manager를 사용하여 `QLabel` instance와 2개의 push buttons (ok 및 cancel)의 instances가 배치됨.
