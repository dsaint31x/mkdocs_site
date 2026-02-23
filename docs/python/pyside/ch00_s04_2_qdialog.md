---
title: QDialog
tags: [pyside6, pyqt6, qdialog, dialog, modal, modeless, custom-dialog]
---

## Module

* `PySide6.QtWidgets`
* `PyQt6.QtWidgets`

***`QDialog`***  
: PySide와 PyQt에서 사용되는 ***대화상자(Dialog Box)를 추상화*** 하여 <u>dialog에 필요한 표준 기능들을 미리 구현하고 있는 클래스</u>이다.

* **Modal**과 **Modeless** (or Non-modal) Dialog를 만드는 데 사용된다.
    * **Modal Dialog**: `exec()` 메서드를 사용하여 실행한다. 사용자가 창을 닫기 전까지 다른 창과 상호작용할 수 없다.
    * **Modeless Dialog**: `show()` 메서드를 사용하여 실행한다. (`open()` 메서드는 Window-modal로 동작). 창이 열려 있어도 다른 창과 상호작용할 수 있다.
* 사실 `QDialog`를 직접 인스턴스화하여 사용하는 경우는 드물며, 주로 **Subclassing** 하여 다양한 button, text, field, label을 추가한 **Custom Dialog**를 만드는 데 이용된다.
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
* "QDialog Title"이라는 제목을 가진 빈 대화상자가 모달(Modal)로 열린다.

```Python
import sys
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QVBoxLayout, QLabel,
    QMainWindow,
    QPushButton,
)

class MW(QMainWindow): 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QDialog Ex.")

        button = QPushButton("Press it for a Dialog")
        button.clicked.connect(self.button_clicked)

        self.setCentralWidget(button)

    def button_clicked(self, s):
        print("click", s)
        dlg = QDialog(self) 
        dlg.setWindowTitle("QDialog Title") 
        dlg.exec()
        
        # -------------
        # for custom dlg
        # dlg = CustomDlg(self)
        # if dlg.exec(): # Modal Dialog
        #     print('ok')
        # else:
        #     print("cancel")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    window.show()
    app.exec()
```

* Modal dialog에 대한 예제이므로,
* Dialog를 위한 Event Loop가 동작하도록 `dlg.exec()`를 호출해줘야 함.

위의 예는 Dialog Box를 만드는 가장 간단한 경우로, `QDialog`를 위의 경우처럼 사용하는 경우는 사실 없음.

다음 예제와 같이  

* `QDialog`는 
* Custom Dialog를 만들기 위해 
* **부모 클래스**로 사용되는 경우가 일반적임.

---

## 예제2: Custom Dialog

다음은 `QDialog`를 상속하여 Custom Dialog를 만드는 예제임.

해당 예제에서 `CustomDlg`는

* 고유의 title과 : `'Hello, QDialog'` 문자열 
* 특정 질문의 Label과 : `'Is something ok?'`
* **ok** 와 **cancel** 버튼을 가짐.

```Python
class CustomDlg(QDialog): 
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle('Hello, QDialog')
        
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        # buttons에 해당하는 button 객체
        self.button_box = QDialogButtonBox(buttons) 
        
        # QDialog의 메서드를 slot으로
        self.button_box.accepted.connect(self.accept) 
        # QDialog의 메서드를 slot으로
        self.button_box.rejected.connect(self.reject)    
                
        self.layout = QVBoxLayout()
        message = QLabel('Is something ok?')
        self.layout.addWidget(message)
        # QDialogButtonBox 객체 추가.
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