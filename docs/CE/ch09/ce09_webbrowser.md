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


## Interpreter 또는 VM으로서의 Web browser

달리 애기하면, web browser는 일종의 `interpreter` 라고 생각할 수 있다. 

Web browser는 매우 다양한 instruction set을 지원하며, 이들 사용하여 프로그래밍할 수 있는 다양한 프로그래밍언어를 지원한다. Web browser는 이들 다양한 프로그래밍언어(interpreter language)의 source code를 원격지 등에서 읽어들여서 이들을 해석하고 대응하는 instruction들의 집합을 수행하는 interpreter라고 볼 수 있다.  
대부분의 Web browser는 해당 수행이 어떻게 이루어지는지를 developer console을 통해 확인할 수 있다.

Web browser you use every day is

* a ***`virtual machine`*** -- an abstract computer with an incredibly complicated instruciton set implemented entirely in software.
* one of ***`interpreters`***.

### Engine (or Layout Engine, Randering Engine)

* HTML과 CSS, XML등으로 작성된 웹페이지를 읽어들여서 사람이 읽을 수 있는 문서로 표시해주는 웹 브라우저의 핵심기능을 담당하는 component를 지칭함.
* Markup language등에 대한 일종의 interpreter라고 볼 수 잇음.
* 최근의 web browser에는 프로그램 같이 사용자의 입력에 대한 반응 등을 하기 위해  자바스크립트 엔진 등이 추가되어 있음.

## Web browser의 중요성.

웹 브라우저의 점유 → 인터넷의 점유 (혹은 지배)

> ex) 1990년대의 Netscape, 2000년 중반의 IE 등, 2020년대 초반의 Chrome.

* 다양한 정보와 문서의 집합체인 internet에서 data를 열람하기 위해서는 web browser는 사실상 필수적인 SW임.
* 특정 web browser 의 독주시 인터넷 전체 표준 마저도 흔들릴 수 있음.

## 참고

* [virtual machine](/mkdocs_site/CE/ch15/ce15_2_6_container/#virtual-machine)
* [Interpreter](/mkdocs_site/CE/ch08/ce08_compiler_interpreter/#interpreter-language)