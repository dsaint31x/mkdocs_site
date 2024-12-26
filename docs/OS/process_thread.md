# OS: Process and Thread

> 운영체제(OS)가 제공하는 추상화에서  
> **프로세스(Process)** 와 **스레드(Thread)** 는  
> OS가 CPU와 메모리 자원을 관리하고,  
> 사용자 프로그램이 하드웨어에 직접 접근하지 않아도 동작할 수 있도록 만들어진 ***추상화***

Process는 **실행 중인 프로그램의 instance** 에 대한 abstraction

* 실행중인 프로그램의 instance의 관련된 
* resource (CPU, Memory 등등)에 대한 추상화.

Thread 는 **Process 내부의 execution unit(실행 단위)** 를 abstraction

* OS의 Thread는 concurrency를 달성하게 해 줌.
* H/W Tread는 Parallelization을 달성하게 해 줌.


## Process vs Thread 

[Process vs Thread](https://ds31x.tistory.com/152)

## Process and (Logical) Memory.

[Logical Memory Structure for Process](https://dsaint31.tistory.com/421)

## Process Life Cycle

[Process Life Cycle](https://ds31x.tistory.com/261)

## Process Scheduling

[Process Scheduling](./process_sched.md)

## Inter-Process Communication

[IPC](./ipc.md)