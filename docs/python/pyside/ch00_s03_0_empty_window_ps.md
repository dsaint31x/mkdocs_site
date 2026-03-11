---
title: Empty Window Example
tags: [pyside6, pyqt6, QWidget, QApplication, QLabel, basic-structure]
---

간단한 예제 코드를 라인별로 살펴봄으로써  
`PySide` 또는 `PyQt`에서 프로그래밍을 어떻게 하는지 전체적인 순서를 파악해보자.

우선 다음과 같이 단순한 **window(창)** 하나로 구성된 **GUI application** 이다.

![empty_window_ps.py 동작화면](https://static.wikidocs.net/images/page/189191/fig_c01_01.png){style="display: block; margin:0 auto; width="400px"}

* 위의 그림에서 화살표와 붉은색, 푸른색은 설명을 위해 추가된 것이다.

일반적으로 `PySide6` 또는 `PyQt6`의 프로그램은 다음과 같은 구현 순서를 따른다.

1. 필요한 **libraries** 및 **modules** 을 import하기.
2. 만들고자 하는 GUI 프로그램의 **class** 를 구현.
3. **Main script** 로 동작(main scope에서 동작)하는 루틴 구현.

> **Main scope에서 동작** 한다는 것은  
> **script** 또는 **interactive shell** 등에서 해당 모듈이 실행된 경우에만 실행되고, 
> `import` 등을 통해 다른 모듈에 import될 때는 실행되지 않음을 의미함.

해당 순서로 위의 화면이 나오게 하는 코드는 다음과 같다.

```python
# -*- coding: utf-8 -*-
#
# empty_window_ps.py
#
# Description: 
#       이 스크립트는 PySide6/PyQt6 애플리케이션의 기본적인 구조를 보여주는
#       아주 간단한 빈 Qt 창을 생성하는 예제.
# Author: dsaint31
# Date: 2024-02-23
#

# 1. 필요한 library 및 module을 import 하기
import sys

# PySide6/PyQt6 사용을 확인하기 위한 flag
PYSIDE = False
PYQT = False

# PySide6를 우선적으로 import 하도록 시도
try:
    import PySide6.QtCore
    from PySide6.QtWidgets import (QApplication, QWidget, QLabel)
    PYSIDE = True
except ImportError: # ImportError만 처리하여 예외 처리 명확성 증가
    pass # 실패 시, 특별한 처리 없이 넘어감

# PySide6 import에 실패했을 경우, PyQt6를 import 하도록 시도
if not PYSIDE:
    try:
        import PyQt6.QtCore
        from PyQt6.QtWidgets import (QApplication, QWidget, QLabel)
        PYQT = True
    except ImportError: # ImportError만 처리하여 예외 처리 명확성 증가
        pass # 실패 시, 특별한 처리 없이 넘어감

# 2. 만들고자 하는 GUI 프로그램의 class를 구현
# QWidget을 상속받아 새로운 class MW를 정의
class MW(QWidget):
    def __init__(self):
        """ 생성자(Constructor) """
        # 부모 class인 QWidget의 생성자를 호출하여 초기화
        super().__init__()
        # UI 초기화를 담당하는 method 호출
        self.initialize_ui()

    def initialize_ui(self):
        """Application의 UI 설정을 담당"""
        # Window의 위치와 크기를 설정. 
        # setGeometry(x position, y position, width, height)
        self.setGeometry(200, 100, 400, 200)
        
        # Window의 title bar에 보일 text를 설정
        self.setWindowTitle("Main Window in PyQt or PySide. 한글.")
        
        # Window에 포함될 widget들을 설정하는 method 호출
        self.setup_main_wnd()
        
        # 설정된 Window를 화면에 표시 
        # (부모가 없는 widget은 show() 호출 필요)
        self.show()
        
    def setup_main_wnd(self):
        """메인 Window에 포함될 widget들을 생성 및 설정"""
        # QLabel widget을 생성. 
        # 생성자의 인자로 'self'를 넘겨주어, 이 widget의 parent를 MW instance로 지정.
        hello_label = QLabel(self)
        
        # Label에 표시될 text를 'Hello, World and Qt!'로 설정
        hello_label.setText('Hello, World and Qt!')
        
        # Label의 위치를 
        # parent widget의 좌상단으로부터 x=150, y=90 위치로 이동 
        # (절대 위치 지정 방식)
        hello_label.move(150,90)

# 3. Main script로 동작하는 루틴 구현
if __name__ == '__main__':
    # PySide 사용 시 PySide6 버전 정보 출력
    if PYSIDE:
        print(PySide6.__version__)
        print(PySide6.QtCore.__version__)
    # PyQt 사용 시 PyQt6(Qt) 버전 정보 출력
    elif PYQT:
        print(PyQt6.QtCore.qVersion())
    # PySide6나 PyQt6 모두 사용 불가능할 경우 메시지 출력 후 종료
    else: 
        print("Neither PySide6 nor PyQt6 is available. Please install one.")
        sys.exit(1)

    # 모든 PyQt/PySide GUI application은 
    # 하나의 QApplication instance를 필요로 함
    # sys.argv를 통해 command line arguments를 application에 전달
    app = QApplication(sys.argv)
    
    # Main window(MW)의 instance를 생성
    window = MW()
    
    # application의 event loop를 시작
    # app.exec()가 반환하는 종료 코드를 
    # sys.exit()에 전달하여 script를 안전하게 종료
    sys.exit(app.exec())
```

위 소스 코드를 순서대로 설명한다.

## Import 부분

* `import` statement를 통해, 필요한 **library** 들과 **module** 들을 가져온다. 
* `PySide6`를 우선적으로 사용하도록 되어있고, 없을 경우엔 `PyQt6`를 사용함. 
* 위의 예제처럼 <u>가급적 특정 모듈에서 가져올 것들을 명시적으로 지정</u>하여 가져오는 게 좋은 습관이다. 
* `from PyQt6.QtWidgets import *`와 같이 특정 모듈에서 모두 가져오는 방식(*Global Import* 이라고 불림)은 피하는 게 좋다.

**참고:** [**global import** 관련 자료](https://ds31x.tistory.com/425)

## Class 구현 부분

* `MW` class는 `QWidget`를 상속한 **subclass** 이며, 위 예제의 ***main window*** (main window에 대한 정확한 개념은 QMainWindow에서 다룬다)에 해당한다.  
    * 이 class의 **instance** 인 `window`는 *사용자가 GUI program에서 보게 되는 <u>window(창)</u>* 에 해당한다. 
    * 이는 위의 예제 코드로 만드는 GUI 프로그램에서 **최상위 instance** (해당 instance를 포함하고 있는 instance가 없음)이며, **GUI에서 사용되는 다른 모든 components를 직/간접적으로 포함** 하고 있다.
    * <u>`QWidget`의 초기화 루틴 수행</u>을 위해 **생성자(constructor) `__init__()`에서 `super().__init__()`를 수행** 한다.
    * `super()`는 부모 클래스(=super class)의 ***proxy object를 반환*** 해 줌: 이 예제에서는 `MW` class의 부모 클래스인 `QWidget`에 대한 객체를 반환해준다.
    * 이후, 해당 GUI application을 초기화하는 **method** `initialize_ui()`를 호출한다.
* 이 예제에서 사용자가 보는 window에 포함되어 있는 **GUI component** (=widget)는 `QLabel`이다.
    * ***PyQt에서 GUI component를 widget이라고 지칭*** 하므로 이후로는 ***widget*** 이라는 용어를 사용한다.  
    * `QLabel` instance가 `setup_main_wnd()` method에서 생성되며,
      * 생성될 때 인자로 넘겨진 `self`가 <u>해당 instance를 포함하는 부모 instance</u>가 된다. 
      * <u>이 때의 `self`는 `MW` class에서 사용된 것</u>이므로 `MW` class의 instance인 `window`를 가리킨다. 

* PyQt에서 모든 widget은 ***부모-자식 관계*** 를 가지게 된다. 
    * 이 예제에서, *유일하게 부모가 없는 widget은 main window* 이며, 이 window를 제외한 모든 widget은 각각 부모 widget을 가지고 있다: 부모가 없는 widget을 Qt에서는 **window** 라고 부름. 
    * 만약 부모 widget 객체가 application 동작 중에 제거되면, 해당 widget 객체의 자식 widget들도 제거된다. 그리고 자식 widget들은 부모 widget의 영역 내에서 배치되어 보이게 된다.
    * 위의 예제에서 `MW` class의 `window`가 제거되어 화면에서 사라지게 처리되면, 자식인 `QLabel`의 instance도 화면에서 사라진다.

> * `QWidget`을 상속한 class는 다른 widget들을 포함할 수 있는 ***일종의 container*** 로 사용되고, main window로도 동작 가능하다.  
>   뒤에 좀 더 자세히 다루겠지만, 앞서 말한 대로 ***window는 부모 객체가 없는 최상위 instance*** 를 가리키며, 이 window 중에서도 main window의 life cycle은 해당 GUI application과 같다.
> * `QLabel`은 text나 image를 표시하는 widget으로 사용자에게 고정된 어떤 정보를 보여주는 역할을 한다. 여기선 text인 `'Hello, World and Qt!'`를 보여준다.

### initialize_ui 메서드 부분 

**생성자** (`__init__` method)에서 호출되며, GUI application의 초기화를 담당하고 있다.

* `MW` class의 `initialize_ui()` method에서 호출된 `self.setGeometry(200, 100, 400, 200)`은 ***일종의 setter*** 로 main window인 `MW` class의 instance인 `window`의 창(window)이 모니터 화면의 어디에 어느 정도 크기로 보여질지를 설정한다. 
    * `x position, y position, width, height` 순으로 **arguments** 가 넘겨진다.
* `MW` class의 `initialize_ui()` method에서 호출된 `self.setWindowTitle("Main Window in PyQt")`은 ***일종의 setter*** 로 main window의 **title bar(타이틀 바)**  에 보여질 text를 설정한다.
* `MW` class의 `initialize_ui()` method에서 호출된 `self.show()`를 통해 해당 `initialize_ui()`를 호출한 instance가 화면에 보여지게 된다. 
    * GUI를 다 그리고 나서 호출되며, 실제 화면을 사용자가 보게 해준다.
    * 일반적으로 **부모가 없는 widget** 은 `show()` method가 호출되지 않으면 보이지 않음(invisible).
    * 참고로 부모가 없는 위 예제의 widget을 `show()` method 호출 없이 수행시킬 경우, 종료시킬 수 없음.
* `self.show()` 전에 main window의 자식 widget들을 생성 및 추가, 배치하는데, 이를 위 예제에서는 `setup_main_wnd()` method가 담당하고 있다.
    * `self.show()` 호출되기 전에 화면에 GUI application이 보여줄 부분들이 모두 생성 및 추가 처리되어야 한다. 
    * 이를 위의 예제에서는 `setup_main_wnd()` method가 구현하고 있음.
    

### setup_main_wnd() 메서드 부분

* `MW` class의 `setup_main_wnd()`에서 실행된 `hello_label = QLabel(self)` statement는 `hello_label`이라는 이름의 `QLabel` instance를 생성한다. 
    * 이때 생성자의 인자로 넘겨진 `self`가 바로 부모 객체의 instance를 가리킴. 
    * 위의 예제에서는 해당 `self`는 `MW` class의 instance인 `window`를 의미함.
* `QLabel` instance인 `hello_label`의 method `setText()`를 호출하여 `QLabel` widget이 보여줄 text를 설정한다. 
    * 이 예제에서는 `'Hello, World and Qt!'`가 설정되었다.
* `QLabel` instance인 `hello_label`의 method `move()`를 통해 부모 객체(또는 container)에서 해당 `hello_label` 라벨이 어디에 위치할지를 정한다.
    * Container에서 해당 `QLabel` instance가 어디에 놓일지를 좌표로 지정하는 것으로 ***absolute alignment*** 라고 불리는 방식이다(이후 자세히 다룸). 
    * 이 예에서는 x 좌표 150, y 좌표 90에 위치하게 한다.

## Main Scope 코드부

앞서 얘기한 순서의 script로 동작(**main scope** 에서만 동작)하는 루틴으로 `__name__`의 값이 `'__main__'`인 경우에만 동작하도록 if-statement로 싸여 있다.


참고: [Special Variable: `__name__` 에 대해](https://ds31x.tistory.com/129)


* `PyQt6.QtCore.qVersion()`을 통해, 현재 설치된 PyQt의 버전을 확인할 수 있다. 
    * 이 예제에서 꼭 필요한 부분은 아니다.
* `PySide6`에서 버전을 확인하는 것은 `PySide6.__version__`을 이용한다.

모든 PyQt application은 **main scope** 로 동작하는 부분에서 `QApplication`의 **instance** 를 **하나 생성** 해야 하며, 생성할 때 `sys.argv`를 통해 사용자가 지정한 인자들을 넘겨주는 방식이 권장된다.

* `app = QApplication(sys.argv)`를 호출하여, `QApplication`의 **instance** 인 `app`를 생성하였다.

> `sys.argv`에는 CLI에서 파이썬 프로그램을 실행시 추가된 **command line arguments** 가 `list` 형태로 저장되어 있기 때문에, Qt와 관련 있는 argument들을 `QApplication`의 **instance** 에 전달하여 해당 argument에 맞게 동작하도록 구현하는데 도움이 됨.

* `app`의 method `exec()`를 수행하면, PyQt의 ***event loop가 시작*** 되어 OS나 사용자가 발생시키는 event들을 처리하기 시작한다. 
    * 따라서 이를 호출하기 전 **main window** 의 **instance** 를 생성하고 해당 **instance** 의 `show()` method를 호출시켜 사용자가 **main window** 를 보고, 해당 **main window** 에서 버튼을 누르는 등의 상호작용을 할 수 있도록 하는 것이 일반적이다.
    * 위의 예제에서는 `window = MW()`를 `sys.exit(app.exec())`보다 먼저 호출하여 이를 처리했다.
    * **Main window** 의 **instance** 의 `show()` method가 호출되지 않으면 해당 window가 보이지 않는다.
    * **Event loop** 는 이후 event 처리에서 자세히 다룸.
* `app.exec()`가 반환값을 반환하는 시점은 PyQt GUI application을 사용자가 종료시킨 경우로 프로그램이 끝났음을 의미한다. 
    * 반환값은 해당 종료가 정상 종료인지 비정상 종료인지를 나타내는 코드이기 때문에 
    * **Script** 로서 동작한 Python 프로그램을 종료시키는 `sys.exit()`의 **argument** 로 넘겨주는 형태로 구현하는게 좋다.
    * 위의 예제에서는 `sys.exit(app.exec())`로 이를 구현했다.
