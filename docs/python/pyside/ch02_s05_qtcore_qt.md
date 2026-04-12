---
title: QtCore 모듈 - Qt Class
description: QtCore 모듈의 개요와 대표 클래스인 Qt namespace의 주요 enum 설명. Qt.AlignmentFlag, Qt.AspectRatioMode 포함.
tags:
  - Qt
  - PySide6
  - PyQt6
  - QtCore
  - widget
  - GUI
  - enum
date: 2025-04-12
---

# `QtCore` 모듈 - `Qt` Class

**module** : `QtCore`

`QtCore` 모듈은 Qt의 핵심 non-GUI 기능들을 제공하는 모듈임.

* Event Loop 및 signals / slots 메커니즘과 관련된 core class 제공
* 애니메이션, 상태 시스템, 스레드, 정규 표현식 관련 기능 포함
* 매핑된 파일, 공유 메모리 관련 기능 포함
* 사용자 및 application 설정을 위한 플랫폼 독립적인 abstraction 포함

간단히 말하면, ***버튼이나 라벨처럼 눈에 보이는 GUI가 아닌 것들과 관련된 class들이 모여 있는 모듈*** 임.

공식 문서:

* Qt6 C++ : [https://doc.qt.io/qt-6/qtcore-index.html](https://doc.qt.io/qt-6/qtcore-index.html)
* PySide6 : [https://doc.qt.io/qtforpython-6/PySide6/QtCore/index.html](https://doc.qt.io/qtforpython-6/PySide6/QtCore/index.html)

---

## `Qt` Class

widget이나 다른 class들의 **설정** 에 관련된 ***식별자(identifier)들***을 모아둔 일종의 namespace class.

* 정렬 방식 (`AlignmentFlag`), 가로세로 비율 (`AspectRatioMode`) 등 다양한 enum이 정의되어 있음.
* `QtCore` 모듈에서 import하여 사용함.

공식 문서:

* Qt6 C++ : [https://doc.qt.io/qt-6/qt.html](https://doc.qt.io/qt-6/qt.html)
* PySide6 : [https://doc.qt.io/qtforpython-6/PySide6/QtCore/Qt.html](https://doc.qt.io/qtforpython-6/PySide6/QtCore/Qt.html)

**사용 예시**

```python
from PySide6.QtCore import Qt

# 가로세로 비율을 유지하면서 resize
pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)

# QLabel의 text 정렬을 중앙으로 설정
hello_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
```

---

## `Qt.AlignmentFlag` enum

content의 정렬 방식을 지정하는 `enum` type.

| enum 값 | 설명 |
|---|---|
| `AlignLeft` | 좌측 끝으로 정렬 |
| `AlignRight` | 우측 끝으로 정렬 |
| `AlignHCenter` | 수평 방향 가운데 정렬 |
| `AlignTop` | 상단으로 정렬 |
| `AlignBottom` | 하단으로 정렬 |
| `AlignVCenter` | 수직 방향 가운데 정렬 |
| `AlignCenter` | `AlignHCenter | AlignVCenter` 와 동일 - 수평 + 수직 중앙 정렬 |
| `AlignJustify` | 가용한 공간에 맞춰 양쪽 정렬 (multi-line text에서만 효과 있음) |

### 사용법

`setAlignment()` method에 enum 값을 인자로 전달하여 설정함.

```python
label_instance.setAlignment(Qt.AlignmentFlag.AlignCenter)
```

수평과 수직 관련 값을 `|` (bitwise OR) 연산자로 조합하여 사용 가능함.

```python
label_instance.setAlignment(
    Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom
)
```

**`|` 연산자를 사용하는 이유**

* `AlignmentFlag`는 bitmask 기반의 flag enum임.
* 각 값이 서로 다른 bit를 차지하고 있어, `|` (bitwise OR) 연산으로 여러 flag를 동시에 적용할 수 있음.

**`AlignCenter` 주의사항**

* `AlignCenter`는 `AlignHCenter | AlignVCenter`의 조합으로, 수평 + 수직 모두 중앙 정렬함.
* 수평만 가운데로 정렬하려면 `AlignHCenter`를 단독으로 사용해야 함.