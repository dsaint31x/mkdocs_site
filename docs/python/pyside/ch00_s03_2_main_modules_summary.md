---
title: Main Modules Summary
tags: [pyside6, pyqt6, QtCore, QtGui, QtWidgets, module]
---

# PySide6/PyQt6 Main Modules

PySide6와 PyQt6는 방대한 기능을 효율적으로 제공하기 위해 여러 개의 **module**로 나뉘어 있다. 
이 중에서 GUI 프로그래밍을 위해 가장 빈번하게 사용되는 핵심 3대 **module**인 `QtCore`, `QtGui`, `QtWidgets`의 역할과 특징을 요약한다.

## 1. QtCore

**Non-GUI** 기능들을 포함하며, Qt 프레임워크의 가장 **기반(foundation)**이 되는 module이다. GUI가 없는 애플리케이션에서도 사용된다.

**주요 특징:**

* **Core functionality**: **Memory management**, **thread management**, **file system access** 등 운영체제와 밀접한 핵심 기능을 제공한다.
* **Event System**: Qt의 강력한 **Signal and Slot** 메커니즘과 **Event loop** 처리를 담당한다.
* **Data Types**: `QString`, `QList` 등 Qt 전반에서 사용되는 기본 데이터 타입과 **container class**를 제공한다.
* **System Integration**: **Timer**, **date/time** 처리, **system information** 접근 등을 지원한다.

## 2. QtGui

**Graphical User Interface (GUI)**를 구성하는 데 필요한 기본적인 **graphic** 기능과 **base class**들을 제공한다. 

**주요 특징:**

* **Graphic Primitives**: **Pixel**, **color**, **brush**, **pen**, **font** 등 화면에 무언가를 그리기 위한 기본적인 **graphic element**를 다룬다.
* **2D Graphics & Imaging**: **2D vector graphics**, **image processing**, **OpenGL integration** 등을 지원한다.
* **Windowing System Integration**: 운영체제의 윈도우 시스템과 통신하여 **window**를 생성하고 관리하는 저수준 기능을 제공한다. (단, 버튼 같은 구체적인 위젯은 포함하지 않음)

## 3. QtWidgets

Desktop 환경에서 사용되는 전통적인 **User Interface (UI) element**인 **widget**들을 제공한다. `QtGui`와 `QtCore`를 기반으로 구축되어 있다.

**주요 특징:**

* **Ready-made Widgets**: **Button**, **label**, **text editor**, **scrollbar**, **dialog** 등 즉시 사용 가능한 다양한 **UI component**를 제공한다.
* **Layout Management**: **Widget**들을 화면에 배치하고 정렬하는 **layout manager**를 제공한다.
* **Classic Desktop UI**: 사용자가 친숙하게 느끼는 **desktop-style**의 애플리케이션을 구축하는 데 사용된다.

---

이 외에도 `QtNetwork` (네트워크 통신), `QtSql` (데이터베이스), `QtMultimedia` (오디오/비디오), `QtQuick`/`QtQml` (터치 친화적 UI) 등 다양한 모듈이 존재한다.