---
title: Widget (위젯) 개요
description: GUI를 구성하는 기본 단위인 Widget의 개념과 Qt에서의 역할 및 parent-child 계층 관계 설명.
tags:
  - Qt
  - PySide6
  - PyQt6
  - widget
  - GUI
  - control
date: 2025-04-12
---

# Widget (위젯) 개요

컴퓨터 프로그래밍에서 **widget** (위젯) 또는 **control** (컨트롤)은  
***컴퓨터 사용자와 상호 작용하는 interface를 이루는 요소 (= GUI 구성 요소)*** 를 가리킴.

즉, ***GUI를 구성하는 기본적인 GUI component*** 가 바로 widget임.

---

## Qt에서의 Widget

Qt에서는 control이라는 용어보다 **widget** 이라는 용어를 주로 사용함.

**Qt 용어로 GUI를 만드는 것의 의미**

* 여러 종류의 widget들을 window에 배치하는 것을 의미함.

Widget은 다음을 정의하는 GUI component임.

* 화면에서 어떻게 표시될지 (외관)
* 컴퓨터 사용자와 어떤 상호 작용을 할지 (동작)

간략히 요약하면, widget은 ***GUI를 구성하는 가장 기본적인 control unit*** 임.

---

## Parent-Child 계층 관계 (Hierarchy)

Qt에서 모든 widget은 ***parent-child 계층 관계*** 를 가짐.

* parent widget은 여러 child widget을 가질 수 있음.
* child widget은 parent widget의 영역 안에 배치됨.
    * 좀 더 정확히 말하면, child widget은 parent widget의 좌표계를 기준으로 배치됨.
    * 단, parent widget의 visible area(가시영역)을 벗어나는 경우 clipping되어 화면에 보이지 않음.
* parent widget이 소멸되면 child widget도 함께 소멸됨.

**Window란?**

* parent widget이 없는 widget을 특별히 **window** 라고 부름.