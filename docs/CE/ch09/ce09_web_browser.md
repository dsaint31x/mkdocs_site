---
title: Web Browser
tags:
    - web browser
    - engine
----
 
# Web Browser

웹브라우저는 

* 가장 널리 사용되는 복잡한 SW 중 하나이면서, 
* 매우 다양한 instruction set을 지원하며 이들을 조합하여 새로운 기능을 추가할 수 있는 일종의 Virtual Machine 
* 또는 Software로만 구현된 Abstract Computer 라고 할 수 있다.

> Calculator와 Computer의 정의의 차이를 한 번 다시 생각해봐라.

일반적으로 애기한다면,

* 인터넷 망에서 정보를 검색하는데 사용되는 응용 프로그램.
* 인터넷에서 문자, 영상, 음향 등 다양한 형태로 저장되어 있는 정보를 찾아 접근, 열람할 수 있도록 해 주는 SW

> HTML5 등의 지원 등에 따라 기존의 OS에서 수행되던 많은 응용 프로그램이 웹 브라우저를 통해 수행되는 형태의 발전을 보이고 있음. → 웹 오피스 (Google Workspace 등등) 및 웹 OS
, 구글 포토 : 사진 관리 설치형 어플리케이션을 대체, 구글 맵 : 지도 기반 설치형 어플리케이션 보다 우수. 

---

---

## Interpreter 또는 VM으로서의 Web browser

달리 애기하면, web browser는 일종의 `interpreter` 라고 생각할 수 있다. 

Web browser는 매우 다양한 instruction set을 지원하며, 이들 사용하여 프로그래밍할 수 있는 다양한 프로그래밍언어를 지원한다. Web browser는 이들 다양한 프로그래밍언어(interpreter language)의 source code를 원격지 등에서 읽어들여서 이들을 해석하고 대응하는 instruction들의 집합을 수행하는 interpreter라고 볼 수 있다.  
대부분의 Web browser는 해당 수행이 어떻게 이루어지는지를 developer console을 통해 확인할 수 있다.

Web browser you use every day is

* a ***`virtual machine`*** -- an abstract computer with an incredibly complicated instruction set implemented entirely in software.
* one of ***`interpreters`***.

---

### Engine (or Layout Engine, Rendering Engine)

* HTML과 CSS, XML등으로 작성된 웹페이지를 읽어들여서 사람이 읽을 수 있는 문서로 표시해주는 웹 브라우저의 핵심기능을 담당하는 component를 지칭함.
* Markup language등에 대한 일종의 interpreter라고 볼 수 있음.
* 최근의 web browser에는 프로그램 같이 사용자의 입력에 대한 반응 등을 하기 위해 JavaScript Engine(자바스크립트 엔진) 이 추가되어 있음.

---

### JavaScript Engine

JavaScript 엔진은 오늘날 웹 브라우저의 핵심 구성 요소로, 

* HTML과 CSS를 담당하는 Layout Engine과 함께 현대 웹 브라우저의 기반을 형성. 
* JavaScript 코드를 해석하고 실행하는 이 시스템은 단순한 인터프리터를 넘어선 정교한 실행 환경임.

[JavaScript Engine의 동작방식 등에 대한 참고 자료](https://ds31x.tistory.com/434)

#### 주요 브라우저와 JavaScript 엔진

각 주요 브라우저는 고유한 JavaScript Engine을 사용하거나 기존 Engine을 채택:

* Chrome: Google의 **V8 엔진** 을 사용. 이 엔진은 뛰어난 성능으로 유명하며, Node.js에서도 사용됨.
* Firefox: Mozilla의 **SpiderMonkey 엔진** 을 사용. 이는 최초의 JavaScript 엔진 중 하나로 계속 발전해옴.
* Safari: Apple의 JavaScriptCore(별칭 **Nitro**) 엔진을 사용. 이 엔진은 ***WebKit 프레임워크의 일부로 iOS와 macOS 기기에서도 사용***.
* Edge(현재 버전): 2020년 이후 Microsoft는 Edge 브라우저를 Chromium 기반으로 재구축했으며, 현재는 Google의 V8 엔진을 사용.
    * Edge(레거시): 초기 버전의 Microsoft Edge는 **Chakra** 엔진을 사용했음.
    * Internet Explorer: Microsoft의 **Chakra(JScript)** 엔진을 사용(현재는 지원 종료).
* Opera: 2013년 이후 Chromium 기반으로 전환하여 V8 엔진을 사용.
* Chromium: Google의 오픈소스 브라우저 프로젝트로, V8 JavaScript 엔진을 사용. 
    * 많은 현대 브라우저(Chrome, Edge, Opera, Brave 등)가 Chromium을 기반으로 개발됨.

---

### Web Browser를 VM 관점으로 볼 때 JavaScript Engine의 역할.

브라우저를 하나의 가상머신으로 볼 때, JavaScript 엔진은 다음과 같은 역할을 수행함:

* 실행 환경: 브라우저 가상머신의 "프로세서" 역할을 담당하며 웹 애플리케이션 코드를 처리.
    * 런타임 시스템: 코드 실행, 메모리 관리, 가비지 컬렉션을 총괄.
* Bytecode Interpreter: 중간 표현인 bytecode를 실행하는 핵심 컴포넌트.
* 최적화 컴파일러: 자주 사용되는 코드 패턴을 감지하고 최적화 (JIT 컴파일러 기술 포함)
* 샌드박스 메커니즘: 보안 경계를 형성해 웹 코드가 시스템의 다른 부분에 접근하지 못하도록 제한.

---

---

## Web browser의 중요성.

웹 브라우저의 점유 → 인터넷의 점유 (혹은 지배)

> ex) 1990년대의 Netscape, 2000년 중반의 IE 등, 2020년대 초반의 Chrome.

* 다양한 정보와 문서의 집합체인 internet에서 data를 열람하기 위해서는 web browser는 사실상 필수적인 SW임.
* 특정 web browser 의 독주시 인터넷 전체 표준 마저도 흔들릴 수 있음.

## 참고

* [virtual machine](../ch15/ce15_2_6_container.md#container-and-virtual-machine) 
* [Interpreter](../ch08/ce08_compiler_interpreter.md#interpreter-language)