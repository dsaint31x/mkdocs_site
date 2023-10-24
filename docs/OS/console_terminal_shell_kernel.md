# Console, Terminal, and Shell


## Console: 

> 컴퓨터(주로 서버)에 command를 작성하여 입력하고 그 결과를 확인할 수 있는 (물리적) 입출력 장치.  
> Terminal과 비슷한 의미를 가지고 있으나 보다 ^^물리적인 측면이 강조된 경우 사용^^ 된다.

A ^^physical device^^ that typically comprises 

* a monitor, 
* keyboard, and 
* mouse. 

It is used to ^^interact with a computer system^^ and can be found in server rooms or data centers where computers are managed remotely. 

The ***console*** allows system administrators to 

* monitor and 
* manage the computer system 

---

## Terminal

> 컴퓨터에 local 또는 remote로 접속할 수 있는 console을 SW로 구현한 것.  
> (보통 shell 이 수행되도록 해주는 wrapper라고 볼 수 있다.)
>
> 과거 terminal이나 console 모두 teletype(`tty`, 독립된 HW system)로 구성되었으나,  
> 기술의 발전으로 다른 컴퓨터의 OS에 접속하거나 한 컴퓨터에 다중 사용자가 접속하는 게 일반화 되면서 `tty`가 컴퓨터의 SW로 바뀌게 됨.  
> (때문에 virtual terminal, terminal emulator 라고도 불림).  
>
> 현재는 console이나 teletype(tty)보다는 terminal이라는 용어가 보다 많이 사용된다  
> (`tty`라는 용어는 linux등에서 많이 보임).  

Terminal은 Command Line Interface가 기본임.

A ***software application*** that allows users to ^^interact with a computer system^^ through a `command-line interface`. 

It provides users with a way to 

* enter ***text commands*** and 
* receive ***text-based output*** from the computer system. 

Some ^^popular terminal applications^^ include 

* Command Prompt (`cmd`) on Windows, 
* Terminal on macOS, and the many 
* terminal emulators available on Linux.

---

## Shell

> 사용자와 OS사이에 위치하고,  
> 사용자가 입력한 command들을 OS로 전달하여 실행시키고 
> 그 결과를 사용자에게 다시 보여주는 역할을 담당한다.  
> Terminal 에서 CLI 에서 보다 많이 언급되는 편임.  
> 
> OS의 구성요소 (OS를 아주 간단하게 `kernel`과 `shell`로 구성된다고 그리는 경우도 많음.)로서  
> shell은 `kernel`과 사용자 사이에 위치한다.  
>
> * 엄밀한 정의에서 OS는 `kernel`만을 가르킴.
> * 하지만, 많은 경우, `kernel` 외에 `shell`도 포함됨.

![](./img/os.png){width="600"}

* 위 그림에서 system call은 OS가 제공하는 서비스들에 User application이 접근하게 해주는 interface임.

A software program that provides users with access to the operating system's services and resources. 
 
It can be a `command-line interface` (CLI) or a `graphical user interface` (GUI). 
 
The `shell` allows users to ***interact with the computer system*** by 
 
* running commands, 
* launching applications, and 
* managing files and directories. 
 
 Some popular shells include 
 
 * `Bash` (Bourne Again Shell), 
 * `Zsh`, and 
 * `PowerShell`.

---

## 더 읽어보면 좋은 자료들.

* tty의 용어 유래 등의 역사를 살펴보려면 다음 URL을 참고하라: [Keyboard와 Terminal의 역사](https://dsaint31.me/mkdocs_site/CE/ch06/ce06_4_04_keyboard/#keyboard)

* [bash에 대한 간략한 소개](https://ds31x.tistory.com/48)