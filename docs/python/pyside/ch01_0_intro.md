---
title: Chapter 01. Window and Dialog
tags: [pyside6, pyqt6, window, dialog, qmainwindow, qdialog, qapplication]
---

# Chapter 01. Window and Dialog

이 장에서는 **GUI application** 을 구성하는 핵심 요소인 **Main Window** (메인 윈도우)와 **Dialog Box** (대화상자)의 개념 및 차이점을 자세히 살펴보고, 이를 구현하기 위한 대표적인 클래스인 **QMainWindow** 와 **QDialog** 를 소개한다.

그리고 **QMainWindow** 의 초기화 설정부터 **Layout Manager** (레이아웃 매니저)를 활용한 **Central Widget** 구성 방법, **Modal** (모달)과 **Modeless** (모델리스) 대화상자의 동작 방식, 마지막으로 **QDialogButtonBox** 등을 활용하여 **Custom Dialog** (사용자 정의 대화상자)를 만들어보는 과정을 알아본다. 또한, 애플리케이션의 전반적인 제어 흐름을 담당하는 **QApplication** 과 **Event Loop** 의 개념도 함께 다룬다.

이 장에서 다루는 예제들은 **Main Window** 의 뼈대를 잡고 상황에 맞는 **Dialog** 를 띄우며 여러 **widget** 을 **container** 에 배치하는 기본적인 흐름을 익히기 위한 코드들이다.