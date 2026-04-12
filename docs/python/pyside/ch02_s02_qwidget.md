---
title: QWidget Class
description: Qt에서 모든 widget의 base class인 QWidget의 개념, 용도, 주요 Methods 설명.
tags:
  - Qt
  - PySide6
  - PyQt6
  - QWidget
  - widget
  - GUI
date: 2025-04-12
---

# `QWidget` Class

**module** : `QtWidgets`

Qt에서 GUI를 구성하는 모든 widget들이 공통으로 가져야 하는 기능을 추상화(abstraction)한 class.

즉, widget의 abstraction이 바로 `QWidget` class임.

공식 문서:

* Qt6 C++ : [https://doc.qt.io/qt-6/qwidget.html](https://doc.qt.io/qt-6/qwidget.html)
* PySide6 : [https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QWidget.html](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QWidget.html)

---

## 용도

`QWidget`은 직접 instantiate하기보다 아래와 같이 상속하여 사용하는 경우가 많음.

* **Main Window class의 base class** - `QWidget`을 상속하여 application의 main window를 구현함.
* **Container widget** - 관련 있는 여러 widget들을 묶어 담는 container 객체로 사용함.
* **Custom widget의 super class** - 새로운 widget을 직접 구현할 때 상속 대상으로 사용함.

---

## 주요 Methods

### 표시 및 창 제어

| Method | 설명 |
|---|---|
| `show()` | widget을 화면에 표시함 |
| `hide()` | widget을 화면에서 숨김 |
| `close()` | widget에 close event를 전달함. <br/>`WA_DeleteOnClose` attribute가 설정된 경우 메모리에서 삭제되며, 설정되지 않은 경우 기본 동작은 hide임 |
| `setWindowTitle(str)` | window의 title bar에 표시될 문자열 설정 |
| `setGeometry(x, y, w, h)` | widget의 위치 `(x, y)` 와 크기 `(w, h)` 를 한 번에 설정. <br/>`(x, y)` 는 parent widget 기준 상대 좌표이며, top-level window인 경우 스크린 기준 절대 좌표임 |

### 크기 조절

| Method | 설명 |
|---|---|
| `resize(w, h)` | widget의 현재 크기를 재설정 |
| `setFixedSize(w, h)` | widget 크기를 고정 - 사용자가 resize 불가 |
| `setMinimumSize(w, h)` | widget의 최소 크기 설정 |
| `setMaximumSize(w, h)` | widget의 최대 크기 설정 |
| `setMinimumWidth(w)` | widget의 최소 너비만 설정 |
| `setMinimumHeight(h)` | widget의 최소 높이만 설정 |
| `setMaximumWidth(w)` | widget의 최대 너비만 설정 |
| `setMaximumHeight(h)` | widget의 최대 높이만 설정 |

**크기 관련 method 선택 기준**

* 너비와 높이를 동시에 고정하려면 `setFixedSize()` 사용.
* 최소/최대 중 한 방향만 제한하려면 `setMinimumSize()` / `setMaximumSize()` 사용.
* 너비 또는 높이 중 하나만 제한하려면 개별 method (`setMinimumWidth()` 등) 사용.