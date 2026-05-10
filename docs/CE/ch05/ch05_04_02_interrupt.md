# Interrupt and Polling

`Interrupt`와 `Polling`은 `CPU`에게 어떤 event들이 발생했음을 알리고 이들을 처리하기 위해 제안된 두가지 방법임.

event가 발생했을 때, `CPU`는 대개의 경우 어떤 process를 처리하고 있을 경우가 많음. 즉, `CPU`는 어떤 process를 처리하고 있는 도중이라도 특정 event들이 발생했는지 여부를 알 수 있어야 하고 이를 처리할 수 있어야 함.

예를 들어, 키보드에서 입력이 된 event가 발생했으나 `CPU`가 특정 process를 처리하느라 이를 인식하지 못할 경우 사용자는 해당 process가 종료되기 전까지는 키보드를 통한 어떤 입력도 수행되지 못하는 것을 보게될 것이고 이는 컴퓨터가 죽은 게 아닌가 생각하게 될 것임. 때문에 interrupt나 polling을 통해 event를 확인하고 처리할 수 있어야 함.

---

## Polling

`Polling` 방식의 경우, ^^CPU는 일정시간 간격으로 현재 수행 중인 process를 잠시 멈추고, event들이 발생했는지를 점검^^ 하게 된다.  

***점검해야할 모든 event들을 주기적으로 체크하는 방식*** 이기 때문에 점검해야 하는 event의 수가 많아질수록 CPU에 걸리는 부하가 커진다. 

때문에 현재는 `interrupt` 방식이 `polling` 보다 많이 사용되며, 실제로 ^^HW적으로 구현된 interrupt system이 사용^^ 된다. 

오늘날 `Polling`은 일종의 protocol이며  SW적으로 구현하여 특정 처리 등을 할 때 사용된다.

---

## Interrupt

`Interrupt`는 ^^CPU가 주도적으로 체크하는 `polling`^^ 과 달리, event가 발생된 경우 ***해당 event와 관련된 device가 CPU에게 event가 발생*** 되었다고 알려준다.

주변기기에서 발생한 `interrupt`의 처리과정을 예를 들어 살펴보면 다음과 같다.

1. 주변기기에서 CPU가 attention해야만 하는 event가 발생시, `Interrupt ReQuest` (`IRQ`)을 생성하여 CPU(or processor)에게 보내게 됨
2. 이를 받은 processor는 현재 작업 수행(execution)의 상태를 저장하고 수행을 멈춘다. 
3. 그리고 해당 `interrupt`의 `interrupt vector`를 참고하여 처리를 수행할 `interrupt handler` (or `interrupt service routine`)를 호출하게된다.
4. `interrupt handler`는 해당 interrupt를 처리하는 작업을 수행하게 된다. interrupt handler는 ***특정 interrupt에 해당하는 event시 처리되어야할 작업을 구현한 function*** 이라고 생각하면 됨.
5. `interrupt handler`가 처리를 끝내면, processor는 중단시킨 작업(process)를 다시 재개한다.

---

### Stack 과 interrupt

현재 실행 중이었던 process의 상태를 저장하고, interrupt handler가 종료되고 나면 돌아올 주소 등이 저장하기 위해 사용되는 자료구조가 `stack`으로, 오늘날 processor들은 이를 위한 stack을 hardware로 구현하고 있다.

이같은 상태 저장 등은 `interrupt handler`가 책임지고 수행한다.

---

### Interrupt vector

`Interrupt handler`가 위치하고 있는 memory address등을 가지고 있음.

발생한 interrupt의 종류와 이를 처리할 interrupt handler의 memory address등을 가지고 있음.

---

### (Interrupt) Mask, Priority and Timer

***특정 `interrupt`를 켜고 끌 수 있으며 이에 대한 정보를 가지고 있는 `mask`*** 가 존재함.

또한 interrupt들은 `priority`(우선순위)를 가지며 ***높은 우선순위의 interrupt*** 가 우선적으로 처리된다.

지나치게 interrupt처리에 많은 시간을 줄 수 없으며, 이같은 시간제한을 위한 `timer interrupt`도 존재함.

---

---

##- OS와 signal (or event) handler system.

SW적 관점에서 OS는 마치 hardware interrupt를 모방한 ***virtual or software interrupt system*** 을 가지고 있다.


User application에서 

1. system call을 통해 Kernel mode로 동작을 요청할 때
2. software interrupt (=trap)가 발생하며,
3. 이후로 kernel mode가 되어 해당 처리가 완료된 이후,
4. 원래의 User application의 user mode로 돌아와 작업이 재개된다.

UNIX에서는 이러한 software interrupt 개념에 착안하여, 

* 프로세스에게 **비동기적** 으로 event 발생을 통보하기 위한 signal mechanism을 제공.
* Signal은 **software interrupt와 유사하게 현재 실행 흐름을 중단하고 등록된 handler를 호출** 한다.
* 하지만, CPU 명령어에 의해 **동기적으로 발생하는 software interrupt(trap)** 와 달리
* kernel이 프로세스 단위로 전달하는 **비동기적/동기적 통보 메커니즘** 이라는 점에서 구별됨:
    * `CTRL+C`에 의한 `SIGINT`도 대표적인 signal의 예임
    * CPU Exception에 의해 만들어지는 SIGNAl은 동기적이나
    * 다른 SIGNAL은 모두 비동기적임.
    * S/W Interrupt는 CPU 에서 발생하나,
    * SIGNAL은 항상 Kernel이 생성하고 전달함 (발생원인은 CPU일수도 그외의 H/W일수도 있음).

[SIGNAL 요약](https://ds31x.tistory.com/132)

하지만 최근에는 `signal`이라는 용어보다 `event`라는 용어가 더 많이 사용된다.

보다 자세한 건 다음 url을 참고할 것 : [Interrupt 요약](https://dsaint31.tistory.com/447)

--

### 참고: H/W Interrupt vs. S/W Interrupt vs. Signal

* H/W Interrupt는 **외부 장치가 CPU에게** 알리는 것(External, Asynchronous)이고,
* S/W Interrupt는 **프로그램이 CPU를 통해 Kernel에게** 요청(CPU의 명령어 execute 통해)하는 것(Internal, Synchronous) 이며,
* Signal은 **Kernel이 프로세스에게** 통보하는 것 (Kernel, Asynchronous/Synchronous).

| | H/W Interrupt | S/W Interrupt | Signal |
|---|---|---|---|
| **발생 원인** | CPU 외부 장치 (키보드, 타이머 등) | CPU가 명령어 실행 (`INT n`, `SVC`, `SYSCALL`) | Kernel이 생성 |
| **발생 위치** | CPU 외부 | CPU 내부 | Kernel |
| **동기/비동기** | 항상 비동기 | 항상 동기 | 주로 비동기, CPU Exception에 의한 경우 동기 |
| **전달 대상** | CPU → Kernel(ISR) | CPU → Kernel(ISR) | Kernel → Process |
| **전달 방향** | H/W → CPU → Kernel | 프로그램 → CPU → Kernel | Kernel → 프로세스 |
| **처리 방식** | ISR 실행 | ISR 실행 | Signal handler 실행 |
| **handler 등록** | Kernel이 관리 | Kernel이 관리 | 프로세스가 등록 가능 |
| **목적** | H/W 이벤트 처리 | OS 서비스 요청 (system call) | 프로세스에 이벤트 통보 |
| **예시** | 키보드 입력, 타이머 | `SYSCALL`, `SVC`, `INT 0x80` | `SIGINT`, `SIGFPE`, `SIGKILL` |

