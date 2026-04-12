---
title: QtGui 모듈 - QFont, QPixmap
description: QtGui 모듈의 대표 클래스인 QFont와 QPixmap의 개념과 주요 사용법. QLabel과 함께 자주 사용됨.
tags:
  - Qt
  - PySide6
  - PyQt6
  - QtGui
  - QFont
  - QPixmap
  - widget
  - GUI
date: 2025-04-12
---

# `QtGui` 모듈 - `QFont`, `QPixmap`

**관련 module** : `QtGui`

`QFont`와 `QPixmap`은 `QtGui` 모듈에서 제공하는 대표적인 클래스들로,  
`QLabel` widget과 자주 함께 사용되는 **그래픽 요소들을 추상화** 하고 있음.

**주의사항**

* 이 둘은 widget이 아님 (`QWidget`의 subclass가 아님).
* 글자를 나타내는 폰트 (`QFont`) 와 이미지 (`QPixmap`) 를 `QLabel` widget에서 사용하는 용도로 매우 빈번하게 이용됨.

---

## `QtGui` 모듈 개요

GUI에서 사용되는 그래픽 요소들을 제공하는 모듈.

* `QFont`, `QPixmap` 외에도 `QPainter`, `QColor`, `QIcon` 등 그래픽 관련 클래스들을 제공함.
* 그림판과 같은 기능 구현에 필요한 클래스들도 포함되어 있음.

공식 문서:

* Qt6 C++ : [https://doc.qt.io/qt-6/qtgui-index.html](https://doc.qt.io/qt-6/qtgui-index.html)
* PySide6 : [https://doc.qt.io/qtforpython-6/PySide6/QtGui/index.html](https://doc.qt.io/qtforpython-6/PySide6/QtGui/index.html)

---

## `QFont` 클래스

GUI에서 textual content를 표시할 때 사용할 폰트를 추상화하는 클래스.

공식 문서:

* Qt6 C++ : [https://doc.qt.io/qt-6/qfont.html](https://doc.qt.io/qt-6/qfont.html)
* PySide6 : [https://doc.qt.io/qtforpython-6/PySide6/QtGui/QFont.html](https://doc.qt.io/qtforpython-6/PySide6/QtGui/QFont.html)

### 생성자

일반적으로 constructor의 인자로 폰트명(`str`)과 폰트 크기(`int`)를 전달하여 instance를 생성함.

```python
from PySide6.QtGui import QFont

QFont("Arial", 20)
```

* 폰트 종류: **Arial**
* 폰트 크기: **20pt**

---

## `QPixmap` 클래스

스크린에 image를 표시하는 데 사용되는 클래스.

* `QLabel` instance에서 image를 표시할 때 사용됨.
* `QPainter`와 함께 사용하면 선이나 도형 등을 직접 그리는 것도 가능함. (일종의 도화지 역할)

공식 문서:

* Qt6 C++ : [https://doc.qt.io/qt-6/qpixmap.html](https://doc.qt.io/qt-6/qpixmap.html)
* PySide6 : [https://doc.qt.io/qtforpython-6/PySide6/QtGui/QPixmap.html](https://doc.qt.io/qtforpython-6/PySide6/QtGui/QPixmap.html)

### 생성자

constructor의 인자로 읽어들일 image의 경로를 `str`로 전달함.

```python
from PySide6.QtGui import QPixmap

pixmap = QPixmap("img/world.png")   # image 경로를 str로 전달
img_label.setPixmap(pixmap)
```

### 주요 Methods

| Method | 설명 |
|---|---|
| `scaled(w, h, mode)` | 지정한 크기로 resize된 **새로운** `QPixmap` instance를 반환. <br/>원본을 수정하지 않음 |
| `fill(color)` | pixmap 전체를 지정한 색으로 채움 |

**`scaled()` 사용 예시**

```python
from PySide6.QtCore import Qt

pixmap = QPixmap("img/world.png")
# scaled()는 새로운 QPixmap을 반환하므로 반드시 재할당해야 함
pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
```

* `Qt.AspectRatioMode.KeepAspectRatio` - 원본 가로세로 비율을 유지하면서 지정한 크기 안에 맞게 scaling함.
* `scaled()`는 **in-place 변환이 아님**. 반환된 새 instance를 변수에 재할당해야 적용됨.

**`fill()` 사용 예시**

```python
from PySide6.QtCore import Qt

pixmap = QPixmap(200, 200)          # 빈 QPixmap 생성 (width, height)
pixmap.fill(Qt.GlobalColor.white)   # 흰색으로 채움
```

* `Qt.GlobalColor` enum으로 색상을 지정함.
* 빈 canvas를 만들고 `QPainter`로 그림을 그릴 때 주로 사용하는 패턴임.