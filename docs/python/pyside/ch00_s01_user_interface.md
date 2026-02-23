---
title: User Interface
tags: [interface, user-interface, gui, cli, pyside6, pyqt6]
---

## Interface

Interface는 2개 이상의 hardware device나 software 사이에 위치하는 **연결 매개체** 로서, 서로 간의 data나 signal을 주고받으며 **상호 작용** 할 수 있도록 해주는 것을 의미한다. 이는 물리적인 hardware일 수도, 논리적인 software일 수도 있으며, 단순한 **규약(protocol)** 일 수도 있다.

> 쉽게 말해,  
> 두 개 이상의 객체가 서로 대화하는 방법이라고 생각하면 된다. 

## Machine Interface

Machine Interface는 **인간의 직접적인 개입 없이** 기계(machine)와 기계, 또는 시스템과 시스템 간의 상호 작용을 매개하는 인터페이스를 의미한다. 이는 주로 자동화된 시스템이나 데이터 통신에서 중요하게 다루어진다.

User interface가 사용자의 편의성과 직관성을 최우선으로 고려한다면, machine interface는 기계 간 통신의 **정확성**, **효율성**, 그리고 **표준화**를 핵심으로 한다.
User interface가 사용자의 편의성과 직관성을 최우선으로 고려한다면, machine interface는 기계 간 통신의 **정확성**, **효율성**, 그리고 **표준화** 를 핵심으로 한다.

대표적인 예는 다음과 같다.

*   **Hardware Interface**: USB, HDMI, GPIO와 같이 물리적인 장치들을 연결하는 규격.
*   **Software Interface**: 서로 다른 소프트웨어 간의 데이터 교환을 위한 **Application Programming Interface (API)** 나 통신 프로토콜(protocol).

> 즉, 기계들끼리 서로 데이터를 주고받기 위해 약속된 언어나 연결 방식이라고 볼 수 있다.

## User Interface

User Interface (UI)는 interface의 한 종류로, 한 쪽이 **인간(사용자)** 이고 다른 한 쪽은 **기기나 시스템** (hardware 또는 software)인 경우를 의미한다. Wikipedia의 정의에 따르면 다음과 같다.

> 사람(사용자)과 사물 또는 시스템, 기계, 컴퓨터 프로그램 등 사이에서 의사소통을 할 수 있도록 일시적 또는 영구적인 접근을 목적으로 만들어진 물리적, 가상적 매개체.

흔히 접하는 예로 키보드와 마우스처럼 사람의 손과 눈을 이용하는 방식이 있지만, user interface가 반드시 시각과 촉각에만 국한되는 것은 아니다.

좋은 UI가 제공될 경우, 사용자는 시스템에게 원하는 작업을 **직관적이고 쉽게 지시** 할 수 있으며, 그 **결과(feedback)** 또한 명확하게 확인할 수 있다. 예를 들어, 좋은 게임은 스토리도 중요하지만, 조작이 직관적이고 효율적인 제어가 가능한 interface를 제공해야 한다. 이는 다른 software나 device들도 마찬가지이다. 

좋은 UI는 특정 동작을 수행하는 데 필요한 **입력 횟수를 최소화** 하면서도 **직관적으로 이해** 될 수 있도록 설계되어야 한다. 또한, 시스템의 상태나 결과를 사용자가 쉽게 파악할 수 있어야 하며, **잘못된 입력이나 오류** 에 대해서도 쉽게 인지하고 수정할 수 있어야 한다.

컴퓨터 분야의 user interface 중에서는 **Command Line Interface (CLI)** 와 **Graphical User Interface (GUI)** 가 가장 대표적이다. 시스템 관리나 개발 등 전문가 영역에서는 여전히 CLI가 중요하게 사용되지만, 일반적인 사용자 환경에서는 GUI가 사실상 표준 user interface로 자리 잡았다. 최근 가상 및 증강현실(VR/AR) 기술의 발전으로 새로운 형태의 UI가 등장하고 있지만, 여전히 GUI는 가장 보편적이고 중요한 UI이다.

> Command Line Interface 등에 대한 좀 더 자세한 내용은 다음 URL의 앞부분을 참고할 것.  
> 
> * [Command Line Interface](https://dsaint31.me/mkdocs_site/CE/ch10/ce10_2_01_cli_terminal/)

## Graphical User Interface

이 책에서 다루는 `PySide6`와 `PyQt6`는 바로 desktop 컴퓨터(노트북 포함) 환경에서 **Graphical User Interface (GUI)** 기반의 애플리케이션을 개발하는 도구이다. 

현대의 GUI는 키보드 명령어보다는 마우스나 터치스크린을 주로 사용하여, **화면에 표시되는 그래픽 요소**(아이콘, 버튼, 창 등)를 **직접 조작** 하는 방식으로 상호 작용한다. 이는 컴퓨터 전문가가 아닌 일반 사용자도 쉽게 시스템을 사용할 수 있도록 해주며, CLI에 비해 **직관적이고 배우기 쉽다** 는 장점이 있다. 다만, 숙련된 전문가가 수행하는 반복적이고 복잡한 작업을 **자동화** 하는 데에는 CLI보다 불리할 수 있다.