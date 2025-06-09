# Portability (이식성)

처음 개발된 H/W 및 S/W 환경 외에서 실행이 가능한지를 나타내는 특성.

* **100% 동작을 보장한다** 라기보다는, **어느 정도의 수정 이 이루어져야 실행이 가능한지** 를 나타낸다고 보는 게 정확하다.
* 아주 ^^약간의 수정을 가해서 동작^^ 하도록 만들 수 있다면 ***portability가 우수하다*** 고 할 수 있음.
* 다른 환경(S/W 환경에서는 주로 다른 os를 지칭)에서 수행하도록 수정하는 작업을 `PORTING`이라고도 부름 (java로 만들어진 프로그램을 C언어로 바꾸는 작업 처럼 다른 프로그래밍 언어로 바꾸는 것도 porting이라 부른다.)

Python과 같은 interpreter 언어나, Java와 같이 virtual machine에서 동작하는 언어들이 유행한 이유는 사실 `porting` 없이도 이기종 장비에서 수행가능하다는 장점이 있기 때문이다.

* 실제로는 해당 interpreter나 virtual machine이 설치된 장비여야 하지만, 프로그래머 입장에서는 본인이 사용할 환경에 해당 언어의 interpreter나 virtual machine만 설치하면 되는 터라... (물론 타켓 환경에 필요한 virtual machine이 없다면 아예 포기해야 한다.)
* 컴파일 언어 중에서는 `C` 언어가 **portability가 우수한 언어로 분류** 되는데 이는 다양한 이기종 장비에서 사용가능한 GNU build tool들이 지원되고 있으며, 실제 많은 OS들이 `C`로 개발되었고 무엇보다 다음 설명할 `POSIX`라는 API에 대한 구현물을 거의 모든 OS가 제공하기 때문임 (사실 `POSIX`의 경우 법으로 강제한 부분도 큼). 

---

## Portable Operating System Interface (`POSIX`)

> Operation System (실제로는 UNIX 및 UNIX-like OS)이 제공해야하는 Service Interface를 정의하고 있는 [IEEE (Institute of Electrical and Electronic Engineers)](https://www.ieee.org/) 표준. 

컴퓨터 역사 초기에는 vender가 거의 없어서 portability는 큰 문제가 아니었으나,  
1980년대 UNIX의 보급과 함께, EDA 보급이 대중화되기 시작하면서 여러 컴퓨터 vender가 생겨났고,  
더 나아가 PC가 대중화되면서 S/W의 portability를 매우 중요시되게 됨.

여러 컴퓨터 Vender들의 OS의 구현물 사이의 portability를 확보하기 위해 IEEE가 제정한 OS용 service들을 위한 공통(or 표준) API가 바로 `POSIX`임.

* ^^kernel에 대한 `C` language interface^^ 인 ***system call 등을 정의*** 하고 있음.  
* `POSIX` 가 만들어지던 당시 거의 모든 OS가 `UNIX`를 기반으로하고 있었기 때문에 ^^`POSIX`는 UNIX based OS간의 portability를 위한 것^^ 으로도 볼 수 있음.
* `POSIX` 자체는 `UNIX` 기반이라고 봐도 무방함.

`POSIX`는 일종의 표준 API로 ***Portability가 높은 UNIX application S/W*** 를 만들기 위한 것임.  
하지만 Windows OS도 내부에서 POSIX를 일부 지원하고 있음.  
Windows를 제외한 OS들은 대부분이 `UNIX` 기반인 터라 ^^`POSIX` 인증을 받거나 받지 않더라도 대부분이 `POSIX` 를 지키고 있다^^ . (심지어 Android도...)

* `POSIX` 를 지킬 경우, `UNIX-like OS`라고 불림.

> 정말 `C` 언어로 개발할 때, `POSIX`라는 용어를 많이 보게 된다.

---

## 참고하면 좋은 자료들.

* [POSIX Abstractions in Modern Operating Systems: The Old, the New, and the Missing](https://roxanageambasu.github.io/publications/eurosys2016posix.pdf)
* [POSIX.1-2017 관련 URL](https://pubs.opengroup.org/onlinepubs/9699919799/)
