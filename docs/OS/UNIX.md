# UNIX

1969년 Bell연구소의 Ken Thompson등이 PDP-7 시스템의 OS로서 개발된 것이 최초의 UNIX임.

이후, 다양한 H/W platform에 이식되어 여러 기관에서 사용됨. 

현재는 Linux와 Windows에 밀려서 서버 포함하여 실제로 사용되는 점유율은 점점 낮아지고 있다. (슈퍼컴퓨터, 서버, PC 모두 분야에서 UNIX는 점점 보기 어려운게 현실임)

> UNIX도 Multics (Multiplexed Information and Computing Service)라는 시분할 운영체제에 기반을 두고 개발이 되었다. Multics는 상업용으로는 성공을 거두지 못하였기 때문 현대적 OS의 시작이라는 타이틀을 UNIX에게 넘겨준 면은 있지만, UNIX는 Multics없이는 개발될 수 없다고 단언할 수 있을 정도로 그 기반을 제공해준 OS임.

## 특징

* 현재 UNIX는 다양한 영역에서 수많은 응용프로그램을 구동시키는 ***개방형 표준 운영체제*** 로 자리잡음.
* 대부분의 구현이 C언어 기반이며, 특정 HW시스템 종속적인 부분만을 수정할 경우 새로운 HW시스템에서 동작이 가능함.
    * 사실 C언어 자체가 UNIX를 만들기 위해 개발된 언어라고 볼 수 있을 정도임.
* interactive system (~time sharing system)이면서 multi-procssing 및 multi-user system임.
* 계층적인 Tree구조의 파일 시스템으로 구성됨.

## ...

초기 UNIX의 경우, Open Source였으나 기업에서 사용이 활발히 이루어지면서 오프소스 정책이 폐기되었고, 이에 대한 반발로 Linux가 등작하게 됨.

LINUX와 Mac OS 등의 현대적 컴퓨터 OS의 기반이자 원형이 되어준 운영체제로 컴퓨터의 역사상 가장 중요한 위치를 차지하고 있는 것이 UNIX임.

* Linux는 기능적 측면에서 UNIX-like OS임. (source측면에서 Linux는 Unix의 소스와 상관없음.)
* BSD family 들이 UNIX의 소스코드에 기반한 OS임. (BSD family의 OS는 UNIX의 후손이라고 볼 수 있어서 Genetic UNIX라고도 불린다)
* 초기 MacOS (9.x버전 이전)은 UNIX 계열이 아니었으나, NeXTSTEP기반으로 만들어진 OS X부터는 BSD를 기반으로 개발이 이루어진터라 현재의 Mac OS도 UNIX-like임.

> 현재의 Linux와 Mac OS, BSD family들은 모두 POSIX를 따르는 UNIX-like OS임. 물론 비용적 문제로 공식 인증을 받은 경우는 Mac OS등으로 한정되지만 windows를 제외한 거의 모든 OS는 UNIX에 기반을 두고 있다고 봐도 된다. 이는 모바일 기기의 OS에서도 마찬가지로, android와 iOS, 타이젠 등도 다 UNIX-like라고 볼 수 있다.  
> 재미있는 건 Windows의 경우, 거의 유일한 UNIX에 기반을 두지 않은 OS임에도 POSIX 공식인증을 받은 서브시스템을 제공한다. Windows 10부터는 Windows Subsystem for Linux (WSL)이라는 Linux sub-system을 제공하며 Windows 10 20H1부터는 아예 Linux 커널이 수행되는 WSL2까지 제공하고 있다.
