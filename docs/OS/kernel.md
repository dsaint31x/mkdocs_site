# Kernel

운영체제 중 항상 메모리에 올라가 있는 **운영체제의 핵심 부분**

* 하드웨어와 User program (or application) 사이에서 
* User program (or application) 수행에 필요한 여러 서비스를 제공하기 위한 **인터페이스를 제공**
* **컴퓨터 H/W (CPU, Memory)의 resource(자원)들을 관리**

![](./img/kernel_shell.png)

> The kernel is the core of an operating system that manages system resources and provides services to applications and user processes. It is responsible for managing the computer's memory, input/output operations, and scheduling of processes. The kernel also serves as a bridge between the hardware and software components of the computer system. Without the kernel, the computer system would not be able to function properly.

## 컴퓨터 H/W resource에 대한 interface 제공.

Kernel은 ***User program과 H/W resource 사이에서 이들을 연결*** 해주는 역할을 수행함.

* User program은 `system call`을 통해 kernel에 필요한 H/W resource의 사용을 요청하며, 
* Kernel은 이를 받아 해당 `H/W resource`에게 해당하는 명령을 전달하여 작업을 수행하고, 그 결과를 user program에 반환해줌.

> User program은 ***Kernel이 제공하는 system call interface을 통해 computer의 physical resource를 사용*** 하게 됨.

## H/W Resource Management

Kernel은 컴퓨터 HW의 physical resource를 관리하며, 이들의 abstraction(or virtualization)인 virtual resource를 생성 및 관리함.

**`virtual resource`는 physical resource를 abstraction(추상화)한 것** 으로 각각의 User program들에서는 해당 virtual resource가 보이며, 이를 통해 user program들은 현재 자신이 특정 HW를 혼자서 쓰는 것처럼 느끼게 됨.

| Physical H/W | Virtual H/W |
| --- | --- |
| CPU | Task or Processor |
| Memory (or RAM) | Page or Segment |
| Disk (or HDD, SDD) | File |
| Network | Socket |

Kernel이 수행하는 H/W resource관리는 다음으로 구성됨.

`Task(Process) Management` 
: Physical resource인 CPU를 추상적 자원인 Task (or Processor)로 제공

`Memory Management` 
: Physical resource인 메모리를 추상적 자원인 Page (or Segement)로 제공

`File System` 
: Physical resource인 디스크를 추상적 자원인 File로 제공

`Network Management` 
: Physical resource인 네트워크 장치를 추상적 자원인 Socket으로 제공

`Device Driver Management` 
: 기타 외부 Device들 (Peripheral devices)과 user program 사이에서 중재자/인터프리터 로서 동작하면서 해당 Device들의 driver들을 관리함.

`Interrupt Handling` 
: 인터럽트 핸들러

`I/O Communication`
: 입출력 통신 관리


<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3232161401562757"
     crossorigin="anonymous"></script>
<ins class="adsbygoogle"
     style="display:block; text-align:center;"
     data-ad-layout="in-article"
     data-ad-format="fluid"
     data-ad-client="ca-pub-3232161401562757"
     data-ad-slot="5759309749"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>

## OS에서의 역할.

- OS는 `kernel`에 `system program (shell 및 여러 s/w)`들이 더해져서 구성된다.
- 추가되는 system program들은 file system utility, windowing systems 등등으로 User 또는 User program들이 컴퓨터를 보다 편리하게 사용할 수 있도록 해줌.
- 사실 kernel은 컴퓨터 사용자와 직접적으로 interaction은 하지 않고, ***shell이 중간에 위치하여 이를 담당함*** .

> kernel은 shell을 통하거나 다른 User program (or Application)을 통해 사용자와 interaction을 수행함.
>
