---
title: 리눅스 (GNU/Linux)
tags: [OS, Linux, GNU, Kernel, Distributions, Ubuntu, Debian, RedHat, CentOS]
---
# GNU/Linux 

![](./img/linux_dist.png){style="display:block; margin:0 auto;width:500px"}

> 간단하게는 Linux라고도 불림 (사실 더 자주 쓰이는 건 Linux).

1991년 당시 University of Helsinki 학생(학부생, 복학생)이었던 Linus Torvalds가 개발한 Linux커널을 사용하는 UNIX-like OS임.

* 역시 UNIX-like OS이면서 교육용 OS인 [MINIX](https://namu.wiki/w/Minix) 을 사용(개발환경으로 이용했으며, MINIX의 코드를 사용한 건 아님) 하여
* Linux의 소스코드가 개발된 것으로 알려져 있다.

> 엄밀히 말하면 Linux는 "GNU/Linux" OS가 사용하는 Kernel의 이름이라고 봐야 하고,  
> 그 외의 "GNU/Linux" OS의 구성요소는 GNU project (`G`NU is `N`ot `U`nix의 앞글자를 딴 약어)에 의해 만들어졌다.  
> 때문에 GNU/Linux OS 가 정식 명칭이다.

참고로, 핀란드는 병역이 의무였으며 제대하고 2-3학년 시절에 Torvalds가 개발.

---

1983년 Richard Stallman 이 설립한 Free Software Foundation(FSF)에서 GNU project (Gnu is Not Unix project)를 시작(Linux 가 나오기 전)하면서 shell, gcc(컴파일러), utilities 등의 동작가능한 다양한 software들의 개발을 하고 있었음. Linux가 등장한 1991년 당시 OS에서 kernel 만이 부족한 상태였으며 이 공백을 Linux가 메꾸면서 UNIX-Like OS인 GNU/Linux가 탄생하게 됨.

Linux의 역사는 다음 URL을 참고.

* 참고: [System V, BSD, 그리고 Linux 와 macOS](http://ds31x.tistory.com/134)

Linux는 GNU의 [General Public License (GPL)](https://ds31x.tistory.com/544#3.-gnu-general-public-license---gpl-1989%EB%85%84)을 따르며, GNU의 다양한 S/W의 지원을 받기 때문에 GNU/Linux라고 불리는 게 보다 정확한 표현이라고 볼 수 있다. 하지만 실제로 Linux라는 용어로 Linus Torvalds의 Linux kernel과 GNU의 다양한 SW들로 구성된 OS를 가리키는 경우가 더 많다.

Linux는 다양한 배포판을 가지고 있으며 이들 배포판들은 각각의 장단점을 가짐.

---

---

## 특징

* 개방형 (Open Source) 임 : Source가 완전 공개가 되어 있기 때문에 이를 기반으로 다양한 파생 OS개발이 가능함.
    * 배포판들의 대부분 Linux kernel을 공유하고 그 외의 SW가 각 배포하는 주체들에 의해 차이점을 가진다.
* interactive system (~time sharing system)이면서 multi-processing 및 multi-user system임.
* 다중 작업 및 다중 사용자를 지원 : Linux는 Unix 못지 않게 서버를 위한 OS로 강력한 지지를 받고 있음. 
* 매우 높은 신뢰성과 함께 다양하고 강력한 네트워크 기능을 제공 : 서버로 동작하는 장비의 거의 대다수가 Linux인 이유임.

---

---

## 다양한 배포판과 중요성.

다양한 distributions(배포판, distros)을 가진다.

Debian 계열(Debian, Mint, Ubuntu 등)과 Redhat (Redhat, Fedora, CentOS)계열 등으로 나누어짐.

매우 다양한 distribution 이 존재하기 때문에 한번 정도 정리 해보는 걸 권함.

> 개인적으로 Debian계열을 선호하지만, 상업용으로는 보다 Redhat 계열 (특히 CentOS)이 좀 더 많이 사용되는 것으로 보인다.  
> 참고로, 기계학습이나 데이터 사이언스 계열에서는 Ubuntu 가 가장 많이 사용되는 추세임.

* [Distribution과 Kernel의 요약자료](http://ds31x.tistory.com/131)

---

### 1. Debian 계열.

***Debian***
: Debian은 1993년 Ian Murdock이 만든 배포판으로 `.deb` 패키지 포맷과 `apt` 패키지 관리 시스템을 사용 하는 특징을 가지며, Debian 계열의 여러 distros의 기반이 됨.

***Ubuntu***
: Ubuntu는 많은 논란을 일으키기도 하지만, 가장 사용자 층이 넓은 distro임이 분명함. 5년간 지원을 보장하는 LTS Version(Long Term Support Version)을 일반적으로 2년마다 발표하고, 그 사이 6개월마다 새로운 버전을 발표할 정도로 매우 활발한 움직임을 보인다. 뛰어난 사용자 친화성과 넓은 hardware 지원으로 유명하며, Kubuntu, Xubuntu와 같은 자체적인 variations 도 많음.

> Ubuntu는 2004년 마크 셔틀워스에 의해 출시된 이래 영국의 Canonical Ltd.가 주도하고 있는 distro로 ML 및 DL, Data Science 분야에서 가장 많이 이용되는 OS임.

***Linux Mint***
: Ubuntu를 기반으로 초보자에게 쉬운 접근성을 자랑하는 Desktop환경 제공으로 유명함. 2006년 초기버전 Ada로 공개된 이후, 다른 distro들이 주로 서버 장비를 대상으로 하는 것과 달리 desktop에 집중을 한 배포판으로 Windows에서 Linux로 넘어오는 초보자들을 대상으로 함.

---

### 2. Red Hat 계열.

Linux 비지니스 및 엔터프라이즈 시장에서 매우 큰 위치를 차지하고 있음.

***Fedora***
: 2003년 최초 공개 이후 지속되고 있는 Red Hat의 커뮤니티 기반 프로젝트로, `rpm`패키지 시스템(Red hat Package Manager)을 사용하며, 최신기술을 실험 및 적용하는 데 중점을 둠. 다음에 다루는 RHEL 의 테스트배드 역할도 겸하며 매우 짧은 릴리스 주기가 특징.

***Red Hat Enterprise Linux (RHEL)***
: 2002년 최초 출시(RHEL2.1) 이후 가장 상업적으로 성공한 Linux distro라고 할 수 있음. RHEL은 LTS (5년의 full support phase + 5년의 maintenance support = 10년 지원)를 제공하며 유료구독을 통해 기술지원과 보안업데이트를 지원함.

***CentOS***
: RHEL 의 무료버전으로 RHEL과 100% binary compatibility를 목표로 한 distro. 보통 RHEL이 나온 후 시간을 두고 배포되어 안정화된 버전으로 유명했음. 하지만 2020년 12월 Red Hat이 개발 중단을 선언하고 CentOS Stream으로 전환하면서 REPL의 다음 버전을 미리 경험하는 distro로 성격이 바뀜 (엄청난 논란이 있었던 사건.).

> CentOS의 종료는 다른 무료 서버 OS에 대한 필요성을 크게 부각시켰고, Rocky Linux나 AlmaLinux 등이 강력한 대안으로 떠오름.

---

### 3. SUSE 계열.

유럽 엔터프라이즈 시장에서의 강자임.
1994년 Software und System-Entwicklung (S.u.S.E GmbH) 사에서 slackware Linux를 기반으로 출발하여 오늘날 자체적인 독립 distribution 이 됨.

***openSUSE***
: YaST(Yet Another Setup Tool) 설정도구(관리툴)와 RPM 패키지 관리 시스템을 이용. SLE에서 파생된 코드를 사용하여 보다 안정성을 강조한 openSUSE Leap과 SLE의 롤링릴리스 모델을 따르는 openSUSE Tumbleweed로 나뉨.

***SUSE Linux Enterprise (SLE)***
: RHEL 과 함께 엔터프라이즈 시장에서 중요한 distro임.

> <u>rolling release는 지속적으로 업데이트가 가능하여 개별 버전으로 주기적인 업데이트 없이 최신 상태를 유지하도록 하는 방식</u> 으로 일반적인 "point release(static release)"와 구분됨.  
> Arch Linux, openSUSE Tumbleweed, Gentoo Linux, Manjaro 등이 채택하고 있으나, 최신 기술이 신속하게 배포된다는 점은 동시에 안정성을 떨어뜨리기 때문에 엔터프라이즈 환경에선 적절치 못함.

---

### 4. Arch 계열.

***Arch Linux***
: 최소주의와 사용자 맞춤형에 중점을 둔 distro. `pacman` 패키지 관리자를 사용함. 사용자 맞춤형에 중점을 두고 있어서 매우 유연한 구성이 가능하지만 반대급부로 설치와 설정이 다소 복잡한 편임.

***Manjaro***
: Arch Linux를 기반으로 하면서도 상대적으로 보다 쉬운 설치와 설정 및 사용성을 제공하는 distro.

---

### 5. 기타.

Gentoo, Slackware 와 같은 독립(?)적인 distributions도 많음.

---

---

## 사용분야

현재 server(super computer포함) 와 Embedded system, mobile에서 Linux 기반의 OS가 모두 1위를 차지하고 있다. 유일하게 1위가 아닌 분야가 desktop 시장임.