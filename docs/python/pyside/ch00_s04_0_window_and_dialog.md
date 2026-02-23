---
title: Window and Dialog
tags: [pyside6, pyqt6, window, dialog, qmainwindow, qdialog, modal, modeless]
---

# Window and Dialog

일반적으로 **GUI application**은 다음과 같은 요소들로 구성된다.

* 1개의 **Main Window**
* 0개 이상의 보조 **Window**들
* 0개 이상의 **Dialog Box**들

> 각 window는 여러 자식 **widget**을 가질 수 있다.

앞서 살펴본 `empty_window_ps.py` 예제는 ***1개의 main window로만 구성***된 가장 단순한 형태라고 할 수 있다.

결국, PyQt나 PySide로 GUI application을 개발한다는 것은 **Main Window**를 포함한 다양한 **Window**와 **Dialog Box**를 설계하고 구현하는 것을 의미한다.

> **Window**는 GUI 프로그램에서 사용자가 보는 ***창***을 가리킨다.  
> Qt 프레임워크에서는 ***부모(parent)가 없는 widget을 바로 Window라고 부른다***.

이 장에서는 GUI의 핵심 구성 요소인 Main Window와 Dialog Box의 개념과 차이점에 대해 알아본다.

---

---

# Main Window

대부분의 GUI application에서 사용자가 가장 오랜 시간 동안 상호작용하며 머무르는 곳이 바로 ***Main Window***이다.

* 각 GUI application은 통상적으로 하나의 main window를 가지며, 
* application의 시작과 종료가 이 main window와 생명주기를 같이 하는 경우가 많다.

***Main window***는 GUI application의 **Main Interface** 역할을 수행한다.

일반적으로 main window는 다음과 같은 표준적인 구조를 가진다.

![ref. : https://doc.qt.io/qt-6/qmainwindow.html](https://static.wikidocs.net/images/page/189215/MainWindowLayout.png){style="display: block; margin:0 auto; width="400px"}

* **Menu Bar**: Window의 *상단에 고정*되며, 파일, 편집, 도움말 등의 메뉴를 포함한다. (Main window당 1개)
* **Tool Bar**: 자주 사용하는 명령을 아이콘 버튼 등으로 제공하며, 이동이 가능하거나 고정될 수 있다. (여러 개 가능)
* **Dock Widget**: 메인 영역 주변에 도킹되거나 분리되어 떠다닐 수 있는 보조 윈도우이다. (여러 개 가능)
* **Central Widget**: Main window의 중심에 위치하며, 실제 작업이 이루어지는 주요 영역이다. (Main window당 1개)
* **Status Bar**: Window의 *하단에 고정*되어 상태 정보를 표시한다. (Main window당 1개)

> **참고**: `QMainWindow` 클래스를 사용할 때, **Central Widget**은 반드시 설정되어야 한다. 일반적으로 여러 widget들을 배치한 container 성격의 `QWidget` 인스턴스를 생성하여 `setCentralWidget()`으로 지정한다.

PyQt나 PySide에서 **Main Window**를 구현하는 방법은 크게 두 가지이다.

1.  **`QMainWindow` 상속**: 
    *   위 그림과 같은 전형적인 데스크톱 애플리케이션 구조(메뉴바, 툴바, 상태바 등)가 필요한 경우 사용한다.
    *   대부분의 본격적인 애플리케이션 개발에 적합하다.
2.  **`QWidget` 상속**: 
    *   `empty_window_ps.py` 예제처럼 매우 간단한 구조이거나, 표준적인 레이아웃을 따르지 않는 비전형적인 GUI를 만들 때 사용한다.
    *   부모 widget(`parent`) 없이 생성하면 그 자체로 window가 된다.

요약하면, **전형적인 GUI application**을 만들 경우 `QMainWindow`를 이용하고, **간단한 형태나 특수한 목적의 GUI**를 구현할 경우엔 `QWidget`을 이용하는 것이 일반적이다.

---

---

# Dialog Box

**Dialog Box(대화 상자)**는 사용자에게 정보를 보여주거나 입력을 받기 위해 일시적으로 나타나는 ***간단한 창***을 의미한다. 줄여서 **Dialog**라고도 부른다.

Main window가 application의 주 무대라면, dialog box는 다음과 같은 보조적인 역할을 수행한다.

- **정보 알림 및 경고**: 오류 메시지, 작업 완료 알림 등을 사용자에게 전달.
- **사용자 입력 요청**: 파일 열기/저장, 설정 변경, 간단한 데이터 입력 등.

대부분의 dialog box는 **부모 window(parent)**를 가지며, 사용자로부터 받은 입력을 부모에게 전달하여 application의 상태를 변경하는 데 사용된다.

---

## Dialog Box의 종류 (Modality)

Dialog box는 동작 방식(Modality)에 따라 크게 두 가지로 나뉜다.

### 1. Modal Dialogs
*   **특징**: Dialog가 떠 있는 동안 **사용자는 해당 dialog와만 상호작용**할 수 있다. Application의 다른 window(예: Main window)는 비활성화되어 입력을 받지 않는다.
*   **용도**: 사용자의 즉각적인 응답이 필요하거나, 작업이 완료되기 전에는 다른 일을 진행할 수 없는 경우(예: '저장하지 않고 종료하시겠습니까?', 파일 열기 등).
*   **구현**: 주로 `QDialog`를 상속받아 구현하며, `exec()` 메서드로 실행한다.

### 2. Modeless Dialogs
*   **특징**: Dialog가 떠 있어도 **다른 window와 자유롭게 상호작용**할 수 있다.
*   **용도**: 작업 흐름을 끊지 않고 정보를 참조하거나 도구를 사용하는 경우(예: 찾기/바꾸기 창, 팔레트 등).
*   **구현**: `QDialog`를 상속받아 `show()` 메서드로 실행하며, 필요에 따라 `setWindowModality(Qt.NonModal)` 등을 설정한다.

## Built-in Dialogs

PySide(PyQt)는 파일 선택, 색상 선택, 폰트 선택, 메시지 표시 등 자주 사용되는 기능들을 위해 **표준 Dialog 클래스**들을 이미 제공하고 있다.

*   `QFileDialog`: 파일 열기/저장
*   `QColorDialog`: 색상 선택
*   `QFontDialog`: 폰트 선택
*   `QMessageBox`: 알림, 경고, 질문 메시지 표시

따라서, 특별한 레이아웃이나 기능이 필요한 경우가 아니라면 **기본 제공되는 클래스들을 활용**하는 것이 개발 효율성과 사용자 경험(UX) 측면에서 유리하다. 커스텀 dialog가 필요한 경우에만 `QDialog`를 상속하여 직접 구현하면 된다.