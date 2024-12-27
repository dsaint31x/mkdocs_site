# Dual Mode: System Mode vs. User Mode

OS는 다음의 두 가지 실행 모드 (Dual Mode)를 가짐: 

* System Mode (or Kernel Mode)
* User Mode

OS는 컴퓨터 시스템의 안정성과 보안을 유지하기 위해 System Mode와 User Mode라는 두 가지 실행 모드(Dual Mode)를 제공함. 

* 이 두 모드는 각기 다른 작업을 수행하며, 
* 시스템의 효율성과 안전성을 유지하는 데 핵심적인 역할을 함.

> CPU가 실행하는 코드는 무조건 main memory에 적재되어야 하는데 (von Neumann Arch.)  
> OS의 코드가 적재되는 영역은 `Kernel Space` (or `System Space`) 이고  
> 사용자 프로그램의 코드는 `User Space` 에 적재됨.  
> 모드에 따라 해당 영역의 코드를 실행을 시킬 수 있는지가 결정됨:  User Mode로는 System Space의 코드 실행이 불가함.


---

---

## **1. User Mode: 사용자 작업의 안전한 환경 (User Space)**

### 1-1. 정의

User Mode는 사용자 애플리케이션이 실행되는 제한된 환경임.  
이 모드에서는 시스템 자원(System Resources)에 직접 접근할 수 없으며, OS가 제공하는 인터페이스(=`system call`를 통해서만  해당 자원을 사용할 수 있음

---

### 1-2. 특징
	
1. 제한된 권한 (Restricted Access):
    * 시스템 자원에 대한 직접 접근은 불가능하며, OS가 허용한 범위 내에서만 동작.
    * CPU의 Flag Register 의 Supervisor Flag는 이 모드에서 비활성화(Unset, `0`) 상태
2. 안전성 보장 (Fault Isolation):
    * User Mode에서 실행되는 프로그램은 OS의 중요한 부분에 영향을 미치지 않도록 설계됨.
    * 따라서, 프로그램에 오류가 발생하더라도 시스템 전체가 중단되지 않음.
    * User Space에 적재된 코드가 실행됨.
3. 사용자 중심 작업 (User-Centric Tasks):
    * 애플리케이션 실행, 사용자 인터페이스 제공 등 주로 사용자가 직접적으로 실행하는 작업이 수행되는 모드임.

---

### 1-3. 예시

* 웹 브라우저(Web Browser), 텍스트 편집기(Text Editor), 게임(Game), Word-Processor 등등의
* 사용자 애플리케이션이 User Mode에서 실행됨.

---

---

## **2. System Mode: OS의 핵심 기능 (Kernel Space)**

### 2-1. 정의

System Mode는 OS의 핵심 기능 `Kernel`이 실행되는 모드.

이 모드는 H/W를 직접 제어하거나 시스템 자원에 접근할 수 있는 **최고 수준의 권한(Privileged Access)** 을 가짐.  
이 모드에서는 CPU의 Flag Register 의 Supervisor Flag가 활성화(Set, ‘1‘) 되어 있음.

---

### 2-2. 특징

1. 높은 권한 (Full Access):
    * H/W와 직접 상호작용하며, 
    * 시스템 자원을 완전히 제어할 수 있음.
2. 중요한 작업 수행 (Critical Tasks):
    * 메모리 관리(Memory Management), 
    * 프로세스 스케줄링(Process Scheduling), 
    * 장치 드라이버와의 상호작용(Device Driver Interaction) 등의 
    * 시스템의 핵심 작업이 System Mode에서 이루어짐.
3. 커널 코드 적재 영역 (Kernel Code Location = Kernel Space):
    * OS의 Kernel 코드는 RAM의 상위 주소 영역에 적재됨. 
    * 이 영역은 Kernel Space로 분리되어 있으며, 
    * User Mode에서 직접 접근할 수 없음: 사용자 프로그램의 코드는 User Space (하위주소부분)에 로드됨.
    * 이는 보안과 안정성을 보장하기 위한 구조로, 커널 코드와 데이터가 무결하게 유지될 수 있도록 합니다.
4. Page Table과 Segment Table의 위치:
    * Page Table:
        * 가상 메모리(Virtual Memory) 주소를 물리적 메모리 주소로 변환하는 데 사용 
        * Kernel Space에 위치.
        * 이는 OS가 메모리 매핑을 안전하게 관리할 수 있게 보장함.
    * Segment Table:
        * 세그먼트 기반 메모리 관리에서 사용하는 구조
        * 각 세그먼트의 위치와 크기를 저장
        * Kernel Space에 위치.
        * OS가 프로세스의 메모리 접근을 제어하기 위해 사용합니다.
5. PCB의 위치 (Location of Process Control Block, PCB):
    * 각 프로세스의 상태와 정보를 저장하는 **Process Control Block (PCB)** 은 Kernel Space에 위치
    * 이는 시스템 자원을 안전하고 효율적으로 관리하기 위해서임.
6. ISR의 위치 (Location of Interrupt Service Routine, ISR):
    * 하드웨어 이벤트를 처리하는 **Interrupt Service Routine (ISR)** 도 System Mode에서 실행.
    * 이로써 키보드 입력(Keyboard Input), 디스크 읽기/쓰기(Disk I/O) 같은 이벤트 처리도 Kernel Mode에서 이루어짐.

---

### 예시

* OS의 커널(Kernel), 
* 장치 드라이버(Device Driver), 
* 시스템 호출(System Call) 등이 System Mode에서 동작.

---

---

## **3. User Mode와 System Mode의 전환 (Transition Between Modes)**

Trap: User Mode에서 System Mode로 전환 

### 3-1.	 정의:

`Trap` 은 User Mode에서 System Mode로 전환하기 위한 메커니즘.

주로 "애플리케이션이 OS의 기능을 요청(system call)"하거나 "예외(Exception)가 발생(CPU가 인식)“ 했을 때 사용됨.

---

### 3-2. 작동 방식 (How It Works)

1. System Call 발생 (System Call Initiation):
    * 애플리케이션이 파일 열기(Open File), 네트워크 연결(Network Request)과 같은 작업을 요청하면, 
    * System Call을 통해 Trap이 발생.
    * Trap은 CPU가 system call을 받아들이고 kernel mode로 전환하게 함.
2. CPU 전환 (CPU Transition):
    * Trap 발생 시 CPU는 현재 프로그램 상태를 저장하고, 
    * Kernel Space에서 해당하는 작업을 수행.
3. User Mode 복귀 (Returning to User Mode):
    * Kernel Mode에서의 작업이 완료되면 
    * CPU는 아까 저장된 상태를 복원하여 User Mode로 돌아감.

---

---

## 참고: Trap과 Software Interrupt의 차이 (Trap vs. Software Interrupt)

| 특징  | Trap | Software Interrupt |
|:---:|:---:|:---:|
|발생 원인 | CPU 명령어 실행 또는 CPU의 예외 검출 | 특정 명령어 실행 또는 소프트웨어 이벤트(`SIGINT`) |
| 동기화(Synchronous) | 항상 Synchronous | 대부분 Synchronous 이나 일부 Asynchronous |
| System Call 관련 | 오늘날 OS에서 System Call을 위한 메커니즘으로 사용 | 초기 System Call을 구현. ARM 에서는 SVC로 system call 구현에 사용됨. |
| 발생 위치 | CPU 내부| CPU 또는 소프트웨어에 의해 발생 |

* Trap은 CPU 명령어에 의해 동기적으로 발생하며, 오늘날 대부분의 System Call이 Trap을 통해 처리됨.
* Software Interrupt는 더 넓은 범위를 포함하며 비동기적으로도 발생할 수 있음.

---

---

## **4. 예외(Exception) 처리: 시스템의 안정성 유지**

### 4-1. Hardware Exception

1. 정의 (Definition):
    * H/W에서 발생하는 Exception이나 Event로, CPU가 즉시 처리해야 하는 상황.
2. 종류 (Types):
    * Fault: 수정 가능한 오류로, 해당 명령어를 재실행할 수 있음 (발생시킨 명령어가 재실행됨).
    * Abort: 치명적인 오류로, 명령어를 재실행할 수 없으며 프로세스를 종료.
3. 작동 방식 (Mechanism):
    * CPU는 현재 상태를 저장한 후 
    * Kernel Space에서 Exception를 처리.

---

### 4-2. Page Fault

1. 정의 (Definition):
    * 프로세스가 필요로 하는 메모리 페이지가 RAM에 없을 때 발생하는 Exceptoin.
    * `Fault`의 대표적인 경우.
2. 작동 방식 (How It Works):
    * OS는 Page Fault 핸들러 (Kernel Space에 코드 존재)를 통해 
    * 필요한 데이터를 디스크에서 가져와 RAM에 로드한 후 프로세스를 재개.

---

---

## **5. 결론 (Conclusion)**

OS는 User Mode와 System Mode라는 Dual Modes를 통해 안정성과 효율성을 보장.

* User Mode는 사용자 애플리케이션 실행 환경을 제공하며, 안전하고 독립된 작업을 보장.
* System Mode는 OS의 핵심 기능 Kernel을 수행하며, 하드웨어와 시스템 자원을 관리.
* Trap은 두 모드 간의 전환을 가능하게 하여 프로세스가 OS의 기능을 안전하게 사용할 수 있도록 지원.

**Kernel Space는**

* OS의 커널 코드 위치
* RAM의 상위 주소에 위치 (아주 초기에는 address 0 부터 시작하는 구조였으나 오늘날에는 상위주소 영역에 위치함.)
* Page Table, Segment Table, PCB 등 중요한 구조는 Kernel Space에 위치
* 이를 통해 시스템 자원의 안전성과 효율성을 보장.