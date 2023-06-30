# Console, Terminal, and Shell


## Console: 

> 컴퓨터(주로 서버)에 command를 작성하여 입력하고 그 결과를 확인할 수 있는 입출력 장치. Terminal과 비슷한 의미를 가지고 있으나 보다 물리적인 측면이 강조된 경우 사용된다.

A ^^physical device^^ that typically comprises 

* a monitor, 
* keyboard, and 
* mouse. 

It is used to ^^interact with a computer system^^ and can be found in server rooms or data centers where computers are managed remotely. 

The console allows system administrators to 

* monitor and 
* manage the computer system 

## Terminal

> 컴퓨터에 local 또는 remote로 접속할 수 있는 console을 SW로 구현한 것. 보통 shell 이 수행되도록 해주는 wrapper라고 볼 수 있다. 과거 terminal이나 console 모두 teletype로 구성되었으나, 기술의 발전으로 다른 컴퓨터의 OS에 접속하거나 한 컴퓨터의 다중 사용자가 접속하는 게 일반적이 되면서 teletype가 컴퓨터의 SW로 바뀌게 됨. 현재는 console이나 teletype(tty)보다는 terminal이라는 용어가 보다 많이 사용된다.  

A ***software application*** that allows users to ^^interact with a computer system^^ through a `command-line interface`. 

It provides users with a way to 

* enter text commands and 
* receive text-based output from the computer system. 

Some ^^popular terminal applications^^ include 

* Command Prompt on Windows, 
* Terminal on macOS, and the many 
* terminal emulators available on Linux.

## Shell

> 사용자와 OS사이에 위치하고, 사용자가 입력한 command들을 OS로 전달하여 실행시키고 그 결과를 사용자에게 다시 보여주는 역할을 담당한다. CLI에서 보다 많이 언급되는 편임.  
> OS의 구성요소 (OS를 아주 간단하게 kernel과 shell로 구성된다고 그리는 경우도 있다. 이 둘이 가장 많이 사용자에게 이용된다는 측면이 반영된 듯)로서 kernel과 사용자 사이에 위치한다.  
>
> * 엄밀한 정의에서 OS는 kernel만을 가르킴.
> * 하지만, 많은 경우, Kernel외에 Shell도 포함됨.

![](./img/os.png){width="600"}

 A software program that provides users with access to the operating system's services and resources. 
 
 It can be a `command-line interface` or a `graphical user interface`. 
 
 The shell allows users to interact with the computer system by 
 
 * running commands, 
 * launching applications, and 
 * managing files and directories. 
 
 Some popular shells include 
 
 * `Bash` (Bourne Again Shell), 
 * `Zsh`, and 
 * `PowerShell`.