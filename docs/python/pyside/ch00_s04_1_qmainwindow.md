---
title: QMainWindow
tags: [pyside6, pyqt6, QMainWindow, central-widget, layout, gui]
---

## module

* `PySide6.QtWidgets`
* `PyQt6.QtWidgets`

***`QMainWindow`***
: GUI Application에서 핵심이 되는 창인 ***Main Window에서 필요한 표준 기능들을 미리 구현*** 하고 있는 Class.

* Title bar, Menu bar, Status bar, Dock Widget 들을 쉽게 추가할 수 있음.
* 때문에 Main Window를 위한 ***Custom Class*** 를 만들 때 부모 클래스로 사용됨.


## 초기화 설정 

size, title, icon 등을 <u> 초기화 루틴(보통 method를 의미)에서 설정</u> 함.

* `__init__(self)` 와 같은 생성자.
* Qt 가 `QMainWindow` 에 구현된 초기화 설정을 수행할 수 있도록 `super().__init__()`를 호출해야 함.

```python
def __init__(self):
    """ 생성자(Constructor) """
    # 부모 class인 QMainWindow의 생성자를 호출
    super().__init__()
    # UI 초기화를 위해 user-defined method 호출
    self.initialize_ui()
    
def initialize_ui(self):
    """Application의 UI 설정을 담당"""

    # 윈도우의 최소 크기를 400x500으로 설정
    self.setMinimumSize(400, 500) #width, height
    # 윈도우의 title bar에 보일 text를 설정
    self.setWindowTitle("Title of Main Window")
    
    # 아이콘 이미지 경로 설정
    # os.path.join을 사용하여 OS에 맞는 경로 구분자로 경로를 조합
    # __file__은 현재 스크립트의 절대 경로를 나타냄
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img/pyqt_logo.png')
    # QIcon을 사용하여 윈도우 아이콘을 설정
    if os.path.exists(icon_path):
        self.setWindowIcon(QIcon(icon_path))
    
    # 메인 윈도우의 central widget을 설정하는 method 호출
    self.setup_main_wnd()

    # 설정된 윈도우를 화면에 표시
    self.show()
    # self.showFullScreen()
    # self.showNormal()
```

* Main Window의 instance `self`의 메서드 `setMinimumSize(400,500)`를 통해 최소 size를 설정함.
    * `setFixedSize(QSize(400,500))` 을 통해, 창의 크기를 고정시킬 수도 있음 : 
        * Windows와 Linux에서는 고정되지만, 
        * MacOS에서는 전체 크기로 만드는 기능까지 막을 수는 없음.
	  * `QSize` 는 `width` 와 `height` parameter 순으로 생성되며 ***크기를 추상화하고 있는 class임***. 
        * 기본으로 pixel 수로 지정되며, 
        * `QtCore` 모듈에 속함.
	  * `setMaximuSize(400,500)` 를 통해 Main Window instance(창)의 ***최대 크기를 설정*** 할 수 있음.
	  * 사실 이 세가지의 size 관련 메서드들은 모든 widget에서 제공한다.  
* Main window의 instance `self`의 메서드 `setWindowTitle(“Title of Main Window”)`를 통해, 창의 title을 설정할 수 있음. 
* Main window의 instance `self`의 메서드 `setWindowIcon()`를 통해 application icon이 설정된 경우, main window의 상단 왼쪽에 할당된 icon이 보임.
     * `QIcon`은 `QtGui` 모듈에서 제공하는 Class임. 
     * Linux나 MacOS에선 보이지 않음.


## Central Widget 설정.

`QMainWindow` 의 가장 ***중앙에 위치하는 Widget*** 으로 <u>실제 어플리케이션에서 핵심적인 역할을 담당</u>한다. 

* 개념상으로는 <u>여러 widget으로 구성되어지는게 일반적</u>이지만, 
* 프로그래밍 관점에서는 <u>central widget으로 하나의 **container** 
  (일반적으로 `QWidget`instance)가 설정</u>되며,
    * 해당 container의 ***Layout Manager*** 를 통해 
    * <u>여러 개의 Widget들이 추가되도록 구현</u>한다.

이를 간단히 순서대로 설명하면 다음과 같다.

1. Main Window에 놓일 ***여러 Widgets를 설정*** 한다.
2. ***Layout Manager를 생성*** 하고, 
3. 1번에서 만든 ***여러 widget들을 해당 Layout Manager에 추가*** 한다. : 
	  * Layout Manager instance의 `addWidget()`메서드에 
	  * 추가할 Widgets의 instances를 <u>argument</u>로 넘겨줌.
4. ***Container를 생성*** 하고, 
5. 해당 Container의 Layout Manager를 <u>2번에서 만든 ***Layout Manager*** Instance로 설정</u>한다. :
	  * Container 의 instance의 `setLayout()`메서드에 
	  * 설정할 ***Layout Manager*** Instance를 argument로 넘겨줌.
6. 4번에서 생성한 ***Container*** 를 ***Main Window의 <u>Central Widget</u>*** 으로 설정한다.: 
	  * ***Main Window*** instance (보통 `self`)의 `setCentralWidget()`메서드에 
	  * 4번에서 생성한 ***Container*** 를 argument로 넘겨줌.

> Container로는 많은 경우 `QWidget` 객체가 사용됨.  

```python
"""메인 윈도우의 Central Widget을 생성 및 설정"""

# 1번 과정: Central Widget에 포함될 자식 widget들을 생성
label0 = QLabel("test0")
label1 = QLabel("test1")

# 2번 과정: 자식 widget들을 배치할 Layout Manager를 생성 
#          (QVBoxLayout: 수직 정렬)
vbox = QVBoxLayout()

# 3번 과정: Layout Manager에 자식 widget들을 추가
vbox.addWidget(label0)
vbox.addWidget(label1)

# 4번 과정: 자식 widget들과 layout을 담을 
#          container widget(QWidget)을 생성
container = QWidget()

# 5번 과정: container widget의 layout을 2번 과정에서 만든 vbox로 설정
container.setLayout(vbox)

# 6번 과정: 메인 윈도우의 Central Widget으로 container widget을 설정
self.setCentralWidget(container)
```
  
* `QMainWindow` 를 상속받은 class에서 사용된 코드 조각이며,  
* `self`가 main window (상속받아 구현된)의 instance에 해당함.
* `QtWidgets.QVBoxLayout`의 instance를 
* Layout Manager로 사용하기 때문에 위에서 아래 순으로 widget이 추가됨.
* `QWidget` instance를 Container로 사용함.
 
 
### 기타 기능
 
 전체 화면 모드(`Full Screen Mode`)로 동작.
 
 * `showFullScreen()` 메서드 사용.

일반 창 모드로 동작.

* `showNormal()` 메서드 사용.

## Example: ex_qmain_window.py

```python
# -*- coding: utf-8 -*-
#
# ex_qmain_window.py
#
# Description: QMainWindow를 상속받아 메인 윈도우를 생성하고,
#              Central Widget을 설정하는 방법을 보여주는 예제입니다.
# Author: [작성자 이름 또는 조직명]
# Date: 2026-02-23
#

# 1. 필요한 library 및 module을 import 하기
import sys
import os

# PySide6/PyQt6 사용을 확인하기 위한 flag
PYSIDE = False
PYQT = False

# PySide6를 우선적으로 import 하도록 시도
try:
    from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                                   QLabel, QVBoxLayout)
    from PySide6.QtGui import QIcon
    PYSIDE = True
except ImportError:
    pass

# PySide6 import에 실패했을 경우, PyQt6를 import 하도록 시도
if not PYSIDE:
    try:
        from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                                     QLabel, QVBoxLayout)
        from PySide6.QtGui import QIcon
        PYQT = True
    except ImportError:
        pass

# QMainWindow를 상속받아 메인 윈도우 class를 정의
class MW(QMainWindow):
    def __init__(self):
        """ 생성자(Constructor) """
        # 부모 class인 QMainWindow의 생성자를 호출
        super().__init__()
        # UI 초기화를 위해 user-defined method 호출
        self.initialize_ui()
        
    def initialize_ui(self):
        """Application의 UI 설정을 담당"""

        # 윈도우의 최소 크기를 400x500으로 설정
        self.setMinimumSize(400, 500) #width, height
        # 윈도우의 title bar에 보일 text를 설정
        self.setWindowTitle("Title of Main Window")
        
        # 아이콘 이미지 경로 설정
        # os.path.join을 사용하여 OS에 맞는 경로 구분자로 경로를 조합
        # __file__은 현재 스크립트의 절대 경로를 나타냄
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img/pyqt_logo.png')
        # QIcon을 사용하여 윈도우 아이콘을 설정
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # 메인 윈도우의 central widget을 설정하는 method 호출
        self.setup_main_wnd()

        # 설정된 윈도우를 화면에 표시
        self.show()
        
    def setup_main_wnd(self):
        """메인 윈도우의 Central Widget을 생성 및 설정"""
        
        # 1번 과정: Central Widget에 포함될 자식 widget들을 생성
        label0 = QLabel("test0")
        label1 = QLabel("test1")
        
        # 2번 과정: 자식 widget들을 배치할 Layout Manager를 생성 (QVBoxLayout: 수직 정렬)
        vbox = QVBoxLayout()
        
        # 3번 과정: Layout Manager에 자식 widget들을 추가
        vbox.addWidget(label0)
        vbox.addWidget(label1)
        
        # 4번 과정: 자식 widget들과 layout을 담을 container widget(QWidget)을 생성
        container = QWidget()
        
        # 5번 과정: container widget의 layout을 2번 과정에서 만든 vbox로 설정
        container.setLayout(vbox)
        
        # 6번 과정: 메인 윈도우의 Central Widget으로 container widget을 설정
        self.setCentralWidget(container)
        
# 3. Main script로 동작하는 루틴 구현
if __name__ == '__main__':
    # PySide6나 PyQt6 모두 사용 불가능할 경우 메시지 출력 후 종료
    if not PYSIDE and not PYQT:
        print("Neither PySide6 nor PyQt6 is available. Please install one.")
        sys.exit(1)

    # 모든 GUI app은 하나의 QApplication instance를 필요로 함
    app = QApplication(sys.argv)
    # Main window(MW)의 instance를 생성
    window = MW()
    # application의 event loop를 시작
    sys.exit(app.exec())

```