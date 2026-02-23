---
title: QtWidgets Module Overview
tags: [pyside6, pyqt6, qtwidgets, qwidget, qapplication, qlabel]
---

# QtWidgets Module Overview

## 0. `QtWidgets` module 이란

Desktop-style의 GUI를 위한 다양한 **widget class** 들을 제공하는 ***module(모듈)*** 이다.

`QtGui`와 `QtCore`와 함께 가장 많이 사용되는 3대 module임.

해당 모듈에서 가장 많이 이용되는 **classes** 로는 다음이 있음.

### 0-0. `QWidget` : Qt 에서 비어있는 기본 widget 을 위한 Class. 

  * 일반적으로 관련있는 Widgets를 포함하여 묶어주는 **container** 로 많이 사용됨.
  * GUI Components (=widgets) 이 공유하는 기본 기능들을 가지고 있음.

GUI의 기본 구성요소인 [Widget](https://wikidocs.net/189238)을 추상화하고 있는 Class.

> 참고 : [추상화(abstraction) 란](https://dsaint31.me/mkdocs_site/python/oop/oop_1_01_abstraction/#abstraction-class-and-instance)

### 0-1. `QApplication` : Qt 의 GUI application을 추상화하고 있는 class

  * 이 class의 **instance** 가 GUI application에 해당함.
  * 해당 application의 **interaction** 을 처리하는 **event loop** 를 유지함.

제공되는 대표적인 widgets 중 다음 3가지가 `empty_window_ps.py` 예제에 사용되었다.

```Python
from PySide6.QtWidgets import QApplication, QWidget, QLabel
# from PyQt6.QtWidgets import QApplication, QWidget, QLabel
```

---

## 1. 예제에서 사용된 Class들

### 1-0. `QWidget` Class

앞서 `QtWidgets` 모듈에서 언급했듯이, <u>GUI의 다양한 component</u>를 PySide와 PyQt에서는 ***widget*** 이라고 부른다.

* Widgets가 공통적으로 가져야 하는 기능을 `QWidget` class에 **abstraction(추상화)** 시켜 놓았다.
* 즉, widget의 **abstraction** 이라고 생각하면 된다.

`QWidget`은 widget에게 요구되는 다양한 기능들을 구현하고 있으며, 앞서 `empty_window_ps.py` 예제에서 사용된 것들은 다음과 같다.

- `show()` :  
	해당 widget의 **instance** 를 화면에 보이게 하는 **method**.
- `setGeometry(left_x, left_y, width, height)` :  
	해당 widget의 **instance** 의 위치와 크기를 설정하는 **method**.
- `setWindowTitle("title_str")` :  
	해당 widget의 윈도우의 **title bar** text(문자열)를 설정하는 **method**.
- `close()` :  
	해당 widget의 윈도우를 닫음.

> PyQt에서 `xxx`라는 이름의 **attribute**에 대해  
>  
>  * 설정하는 ***setter*** method들은 `setXxx(...)`라는 이름(`set` 다음에 **upper case**) 을 가지고, 
>  * ***getter*** 들은 **lower case** 그대로 사용하여 `xxx()`의 이름을 가진다.
>    
> `QWidget`의 `geometry`는 **setter** 가 `setGeometry`, **getter** 가 `geometry`라는 이름으로 주어져 있다.
> 

Setter와 Getter개념이 생소하다면 다음 문서를 참고하라 : [OOP: Setter and Getter](https://dsaint31.me/mkdocs_site/python/oop/ds_setter_and_getter/)

---

### 1-1. `QApplication` Class

Qt 의 GUI application을 추상화하고 있는 class.  

PySide 또는 PyQt로 GUI 프로그램을 만들 때, 

* 오직 하나의 `QApplication` **instance** 만 생성되어야 하며, 
* 해당 **instance** 의 `exec()` **method** 호출을 통해 해당 GUI application의 오직 하나뿐인 `Qt (Main) Event Loop`가 수행된다. 

즉, `QApplication` class는 

* ***사용자와 OS와의 interaction(상호작용)을 위한 처리(=event loop)*** 를 구현하고 있고, 
* 대응하는 GUI application 에 속한 widgets의 ***초기화*** 및 ***해제*** 등을 담당함.
* 일종의 Qt application handler라고 생각할 수 있음.

---

### 참고: Qt (Main) Event Loop

Qt GUI application의 GUI 창에서 이루어지는 ***OS와 사용자와의 interaction(상호작용)이 처리되는 event loop***.

* 사용자의 버튼 클릭 등의 **interaction** 은 해당하는 **event** 를 생성시키고 
* 이 **event** 는 ***event queue*** 에 집어넣어지는데,
* 해당 Qt GUI application에 대응하는 `QApplication` **instance** 에 <u>오직 하나 존재하는 ***event loop***</u>가 
    * 해당 Queue에서 이를 하나씩 꺼내어 
    * 해당 **event** 의 **type** 을 인식하고 이에 따라 처리함.

***Qt event loop*** 는 

* `QApplication`의 **instance** 에서 `exec` **method** 호출을 통해 시작되고, 
* ***main window가 종료될 때 종료됨***.

---

### 1-2. `QLabel` Class

Qt GUI application에서 

* <u>내용이 변하지 않는 text 문자열</u> (주로 single line)을 보여주거나, 
* <u>내용이 변하지 않는(=고정된) image</u>를 보여주는 widget.  

`QLabel`의 **instance** 들은

- 사용자와 상호작용을 하지 않지만, GUI를 구성하는 데 매우 많이 사용됨.
- 생성자에서 부모 widget의 **instance** 를 넘겨주어 사용되거나, 
- **Argument** 없이 생성자를 호출하고 이후에 **container** 나 **layout manager** 등에 추가되는 방식으로 사용된다.

---

이 후에도 수많은 widget Class들이 나오지만 위에서 다룬 class들은 기본 중의 기본으로 정말 많이 사용된다. 다음의 PyQt 또는 PySide에서 제공하는 API등을 한번 읽어보길 권한다.

* [PyQt Reference Guide](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
* [PySide API](https://doc.qt.io/qtforpython/api.html)
  
다음으로 일반적인 GUI Application의 개념적 구성단위 중 대표적인 Main Window와 Dialog box에 대해 살펴보겠다.