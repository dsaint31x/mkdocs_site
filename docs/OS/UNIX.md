---
title: UNIX
tags: [OS, UNIX, LINUX, History]]

# UNIX

1969년 Bell연구소의 Ken Thompson등이 PDP-7 시스템(1964년 개발된 미니컴퓨터)의 OS로서 개발(Assembly Language로 개발)된 것이 최초의 UNIX임.

참고로, UNIX 라는 이름의 full name에 대해선 몇가지 의견만 있음: [참고자료](https://www.hanbit.co.kr/channel/category/category_view.html?cms_code=CMS7535176314) - 1970년 Brian Kernighan이 UNIX로 명명한 것으로 받아들여짐.

이후, 다양한 H/W platform에 이식되어 여러 기관에서 사용됨. 
(1972~1973년 개발된 C언어로 1973년 PDP-7 용 UNIX가 C로 포팅됨; 개발작업은 PDP-11에서 이루어짐)

현재는 Linux와 Windows에 밀려서 서버 포함하여 실제로 사용되는 점유율은 점점 낮아지고 있다.  
(슈퍼컴퓨터, 서버, PC 모두 분야에서 UNIX는 점점 보기 어려운게 현실임)

> UNIX도 Multics (Multiplexed Information and Computing Service)라는 시분할 운영체제에 기반을 두고 개발이 되었다.  
> Multics는 상업용으로는 성공을 거두지 못하였기 때문 현대적 OS의 시작이라는 타이틀을 UNIX에게 넘겨준 면은 있지만, UNIX는 Multics없이는 개발될 수 없다고 단언할 수 있을 정도로 그 기반을 제공해준 OS로 가치를 인정받고 있음.

---

---

## 발전사

다음의 URL을 참고.

* 참고: [System V, BSD, 그리고 LINUX 와 MacOS (ext)](http://ds31x.tistory.com/134)

---

---

## 특징

* 현재 UNIX는 다양한 영역에서 수많은 응용프로그램을 구동시키는 ***개방형 표준 운영체제*** 로 자리잡음.
* 대부분의 구현이 C언어 기반이며, 특정 HW시스템 종속적인 부분만을 수정할 경우 새로운 HW시스템에서 동작이 가능함.
    * 사실 C언어 자체가 UNIX를 만들기 위해 개발된 언어임.
    * Ken Thompson이 자신이 만든 B언어를 발전시켜 PDP-7용 UNIX를 만들기 위해 C언어를 개발.
* interactive system (~time sharing system)이면서 multi-processing 및 multi-user system임.
* 계층적인 Tree구조의 파일 시스템으로 구성됨.

---

---

## 다른 OS 들과의 관계.

1. **UNIX의 상용화 및 Linux의 등장**: 
    * 초기 UNIX는 여러 대학과 연구 기관에서 소스 코드 접근이 가능(모든 소스코드가 공개되어있었고 접근 가능했음)했고 사실상 무료로 이용가능한 매우 저가의 라이선스 형태로 배포되었으나, 
    * AT&T 사가 반독점법 등으로 인해 여러 회사로 분할(1984년)되면서 상용화가 강력하게 이루어지게 됨 (가격의 급상승 및 소스코드 접근이 제한되며 소스코드 자체가 공개되지 않게됨.). 
    * UNIX를 포함하여 많은 S/W 의 상용화가 가속화되면서 반작용으로 open source 운동이 일어났으며 
    * 이들의 결실 중 하나가 UNIX와 호환되는 자유로운 os인 Linux의 등장으로 이어짐.
2. **UNIX, Linux, MacOS의 관계와 POSIX**: 
    * UNIX는 많은 현대 운영체제의 기초를 제공하며, Linux와 MacOS, BSD는 UNIX의 설계 철학을 따르고 있음. 
    * Linux는 UNIX와 호환성을 유지하려는 목표를 가지고 있지만, **UNIX의 소스 코드를 기반으로 한 것은 아니기 때문에 UNIX like os라고 불림**.
    * 반면, BSD는 UNIX에서 파생되어 UNIX 소스 코드를 사용했으며, Genetic UNIX라고 불림.
    * macOS는 원래 UNIX 계열이 아니었으나, OS X (10을 의미)부터는 UNIX 기반의 NeXTSTEP에서 영향을 받아 BSD를 기반으로 하게 됨. 하지만 여러 차이로 인해 Genetic UNIX라고는 불리지 않는 편임.
    * 오늘날 Linux, BSD, macOS 모두 POSIX 표준을 따르고 있지만, 비용 등의 문제로 인해 공식 인증을 받은 것은 macOS 뿐임.
3. **Windows와 UNIX**: 
    * Windows는 **UNIX 기반 시스템이 아니면서 대중화에 성공한 거의 유일한 OS** 임.
    * POSIX 표준을 일부 지원하는 서브시스템을 제공. 
    * Windows 10부터는 Windows Subsystem for Linux (WSL)을 도입하여 Linux 커널을 실행할 수 있는 환경을 제공하고 있으며, 이는 Windows 10의 20H1 업데이트부터는 WSL2로 발전하여 진짜 Linux 커널이 실행되도록 지원하고 있음.

> 참고: [POSIX에 대하여.](../CE/ch15/ce15_2_4_portability.md#portable-operating-system-interface-posix)

결론적으로 LINUX와 macOS 등의 현대적 컴퓨터 OS의 기반이자 원형이 되어준 운영체제로 컴퓨터의 역사상 가장 중요한 위치를 차지하고 있는 것이 UNIX임.

Windows를 제외한 거의 모든 OS는 UNIX에 기반을 두고 있다고 볼 수 있고 이는 모바일 기기의 OS에서도 마찬가지로, android와 iOS, 타이젠 등도 다 UNIX-like OS 라고 볼 수 있다. 
