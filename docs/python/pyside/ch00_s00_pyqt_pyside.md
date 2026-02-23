---
title: PyQt and PySide Overview
tags: [pyside6, pyqt6, qt, gui, python-binding]
---

## PyQt와 PySide란?

`PyQt`와 `PySide`는 "Qt Group"의 자회사인 "The Qt Company"가 개발한 강력한 **Cross-platform GUI Framework** 인 `Qt`를 Python 프로그래밍 언어에서 사용할 수 있게 해주는 **Python Binding** 라이브러리이다.


![](https://static.wikidocs.net/images/page/188088/pyqt_pyside.jpg)

---
### 참고 - (Language) Binding이란?

다음은 ***(Language) Binding*** 에 대한 정의이다 (from wikipedia)

> In programming and software design,  
> **Binding** is ***an application programming interface (API)***  
> that provides <u>glue code</u>  
> specifically made to allow ***a programming language***  
> to use <u>a foreign library</u> or <u>operating system service</u>  
> (one that is not native to that language).

즉, **Binding** 은 프로그래밍 언어가 외부 라이브러리나 운영 체제 서비스를 사용할 수 있도록 해주는 **API** 라고 보면 된다.

---

`PySide`와 `PyQt`는  

* C++ 기반의 ***Qt Framework*** 를  
* C++ 언어가 아닌 ***Python으로 사용*** 할 수 있도록 제공되는  
* ***Glue Code에 대한 API*** 이다.

간단히 말하면

* Python으로 코드를 작성하지만,
* 실제 동작할 때에는 대응되는 <u>C++로 구현된 Qt의 기계어 코드가 수행</u>된다.

> 참고로, NumPy 등도 실제로는 C나 C++로 구현된 실행 코드에 대한 Python (Language) Binding이라고 볼 수 있다. 

---

**참고 자료들**

* [API란](https://dsaint31.tistory.com/503)
* [Glue Code](https://ds31x.tistory.com/208)
* [Language Binding](https://ds31x.tistory.com/320)

---

## Qt란 무엇인가?

Qt는 The Qt Company에서 제공하는 **"UI 및 Application 개발을 위한 Framework"** 이다.
Qt는 단순한 라이브러리가 아니라, UI 개발부터 네트워크, 데이터베이스, 멀티미디어 등 애플리케이션 개발 전반을 지원하는 방대한 **Framework** 이다.

* 참고: [Framework란](https://dsaint31.tistory.com/entry/Programming-Library-vs-Framework)

Qt의 강점은 

* **Cross Platform** 으로 거의 모든 platform을 지원한다는 점으로 
* Windows, macOS, Linux, Android 등에서 동작 가능한 Application을 하나의 소스 코드로 개발할 수 있다. 

물론 "Write once, run anywhere"가 완벽하게 적용되는 것은 아니다. 모바일이나 임베디드 환경처럼 화면 크기나 하드웨어 특성이 다른 경우, 플랫폼에 맞는 UI 조정이나 기능 수정이 필요할 수 있다. 하지만 Qt는 이러한 플랫폼 간 차이를 최소화하여, 다른 프레임워크에 비해 훨씬 적은 노력으로 이식(Porting)이 가능하다.

> Desktop Application의 경우엔 거의 수정이 필요치 않으나, 모바일 쪽이나 Embedded System 쪽으로 타겟을 삼은 경우는 꽤 번거로운 수정이 동반되기 쉽다. 하지만 다른 Framework에 비하면 Qt는 수정해야 할 분량이 정말 적은 편에 속한다.


더욱이 매우 강력한 커뮤니티를 가지고 있으며 개발에 필요한 문서화가 잘 되어 있다는 점이 Qt의 최대 장점임.

Qt에 대한 보다 자세한 내용은 Qt의 [official site](https://www.qt.io)를 참고하라.

과거 국내의 경우, Qt는 대학교 연구실에서 시작품 개발 등에 사용되는 수준으로, 실제 상용 S/W 개발에서 그리 많이 사용되지 않았다. 하지만 최근 Python의 급격한 보급과 함께 `PySide`와 `PyQt`의 사용자가 증가하고 있는 추세이다.  


## Python을 통한 GUI Application 개발

Python으로 GUI 애플리케이션을 개발할 때, `PySide`와 `PyQt`는 가장 강력하고 널리 사용되는 도구 중 하나이다.

> Python에 기본 내장된 `Tkinter`가 있지만, 복잡한 UI를 구성하거나 전문적인 기능을 구현하기에는 Qt 기반의 라이브러리가 훨씬 유리하다.

`PySide`와 `PyQt`는 Qt에 대한 Python Binding이기 때문에, 

* Custom Widget 개발 등과 같은 고급 기능을 사용하기 위해서는 C++과 Qt에 대한 이해가 요구된다는 단점이 있으나, 
* Python은 주로 특정 알고리즘이나 특정 기술의 시작품을 빨리 개발하여 검토하는 데에 강점을 가지는 언어이고 
* 이 같은 시작품을 다루기 위한 GUI Application을 개발하는 경우에는 `PySide`나 `PyQt`의 ***Built-in Widget*** 들만으로도 충분하기 때문에 그 사용이 점점 확대되고 있다.

과거 C나 C++을 배운 개발자들이 Visual Programming을 배울 때는 MFC나 델파이 등이 사용되었으나, 컴공과 외에서는 교과과정에서 C나 C++보다 익히기 쉬운 Python으로의 대체가 많아지고 있는 상황도 `PySide`와 `PyQt`가 보다 많이 사용되는데 일조하고 있는 것도 사실이다. 

최근에는 하드웨어 성능의 향상으로 Python의 실행 속도 이슈가 상쇄되면서, 프로토타이핑뿐만 아니라 상용 소프트웨어 개발에도 Python과 Qt의 조합이 적극적으로 활용되고 있다.


이 책은 Python에 대한 기본적인 문법을 익힌 개발자 및 학생을 대상으로 하여, 간단한 GUI application을 `PyQt6` (혹은 `PySide6`)로 개발할 수 있는 역량을 갖추도록 하는 것을 목표로 한다.  

또한 `PySide6`와 `PyQt`를 이용하여 일반적인 GUI Application Programming에서 필요한 개념들을 소개한다.

> **GUI 개발의 어려움과 중요성**
>
> GUI를 만든다는 것은 단순히 기능을 구현하는 것을 넘어, **사용자 경험(UX)** 을 설계하는 일이다.
> 사용자가 직관적으로 기능을 이해하고, 오동작 없이 목표를 달성할 수 있도록 배려해야 한다. 이는 개발자의 논리적 사고뿐만 아니라, 사용자의 입장에서 생각하는 공감 능력과 디자인 감각을 필요로 한다.



## PyQt vs. PySide - 초보자를 위한 선택 기준 

현재 Qt의 Python 바인딩에는 두 가지 주요 선택지가 있다.

1.  **PyQt**: Riverbank Computing에서 개발. 역사가 길고 자료가 많음. (GPL/Commercial 라이선스)
2.  **PySide (Qt for Python)**: The Qt Company에서 공식 지원. Qt 프레임워크 개발사가 직접 제공하므로 안정성이 높고 라이선스가 좀 더 유연함. (LGPL/Commercial 라이선스)

초보자 입장에서는 두 라이브러리의 문법이 거의 99% 동일하므로 어느 것을 선택해도 무방하다. 다만, Qt6 이후로는 공식 지원인 `PySide6`가 표준으로 자리 잡아가고 있으므로, 본 문서에서는 `PySide6`를 기준으로 설명하되 `PyQt6`와의 호환성도 고려한다.

> **참고: 라이선스 (License)**
>
> 해당 주제에 대해서는 다음 blog의 글을 먼저 읽어보길 권한다. 
> 
> * *참고*: [E: overload의 [Python] PyQt와 PySide에 대한 잡설](https://dev-overload.tistory.com/44)


## 공식 URL

`PyQt`에 대한 보다 자세한 내용은 다음 URL을 참고하라.

* [Riverbank Computing의 PyQt 사이트](https://www.riverbankcomputing.com/news)


`PySide6`에 대한 보다 자세한 내용은 다음 URL을 참고하라.

* [Qt의 PySide 사이트](https://wiki.qt.io/Qt_for_Python)