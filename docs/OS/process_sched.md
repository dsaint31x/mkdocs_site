---
title: Process Scheduling
tags: [Queue, Dispatcher, Preemptive, Non-Preemptive, Round Robin, FCFS, CFS, vruntime]
---

# Process Scheduling (or CPU Scheduling, Short-term Scheduling): OS 의 핵심 역할

OS에서 Process Scheduling은 **여러 Process가 CPU를 효율적으로 사용할 수 있도록 실행 순서를 정해줌**.

이 문서에서는

* Process Scheduling의 기본 구조 (Queues, Dispatcher) 와 
* 주요 알고리즘, 그리고 
* Linux의 CFS 알고리즘과 `vruntime` 개념을 다룸.

H/W Resource에서 CPU가 가장 중요한 자원이라고 볼 수 있기 때문에, H/W Resource를 관리하는 OS의 입장에서 
가장 중요한 역할이라고 볼 수 있음.

> Process를 CPU에 할당을 관리하는 것을 ***Short-term Scheduling*** 이라고하고,  
> Process를 Memory에 load하는 관리하는 것을 ***Long-term Scheduling*** 이라고 함. 
> 둘 모두 OS에서 중요한 Scheduling임.

---

---

## 1. Process Scheduling의 기본 개념

### 1.1 Scheduling Queue

Process Scheduling은 다음 두 가지 주요 Queue를 중심으로 이루어짐:

- **Ready Queue**: 
    - CPU 실행을 기다리는 Process들의 Process Control Block(PCB) 참조가 저장된 자료구조. 
    - OS는 Ready Queue에서 Scheduling 알고리즘(아래에 설명)에 따라 실행할 Process를 선택.
- **I/O Wait Queue**: 
    - I/O 작업을 수행 중이거나 이를 기다리는 Process들이 대기하는 공간. 
    - I/O 작업이 완료되면 해당 Process는 Ready Queue로 이동.

---

### 1.2 Dispatcher 의 역할

Process Scheduler 가 Ready Queue에서 Process를 선택하면, Dispatcher 가 이를 CPU에 실제로 할당함. 

Dispatcher 는 다음 작업을 수행:

- 실행 중인 Process 상태 저장 (PCB에 Context 저장)
- Ready Queue에서 선택된 Process의 상태 복원
- 사용자 모드로 전환하여 Process 실행

Dispatcher 의 역할은 Scheduling 알고리즘이 결정한 선택을 실행으로 옮기는 데 필수적임. 

이 과정에서 **Context Switch(문맥 교환)** 이라는 오버헤드가 발생할 수 있음.

---

### 1.3 Scheduling 기준

OS는 다양한 기준을 고려하여 Scheduling을 수행합니다:

- **응답 시간(Response Time)**: 사용자 요청에 대한 빠른 응답을 제공.
- **대기 시간(Waiting Time)**: Ready Queue에서 대기하는 시간을 최소화.
- **처리량(Throughput)**: 단위 시간당 처리되는 Process 수를 최대화 (요구시간이 짧은 녀석부터 처리하는 이유).
- **공정성(Fairness)**: Process 간 자원 배분의 균형 유지.

---

---

## 2. Scheduling 알고리즘의 구분

Scheduling 알고리즘은 크게 Non-preemptive (비선점형)과 Preemptive (선점형)으로 나눌 수 있음.

- **비선점형 Scheduling**: 
    - 실행 중인 Process가 자발적으로 CPU를 반환 (I/O 대기를 위해서)하거나 
    - 작업을 완료할 때만 다른 Process에 CPU를 할당하는 방식.
- **선점형 Scheduling**: 
    - OS가 실행 중인 Process를 강제로 중단(Timer Interrupt등을 통해)하고 
    - 다른 Process에 CPU를 할당할 수 있는 방식.

이 두 가지 방식은 Process 실행 흐름과 시스템 자원 활용 방식에서 큰 차이를 보이며, 각각의 방식은 다음과 같이 여러 알고리즘으로 구현됨.

---

### 2-1. Non-Preemptive Scheduling

* Non-Preemptive(비선점형) Scheduling은 단순한 방법이기 때문에 
* 특정 상황에서는 비효율적일 수 있음: 
    * `Starvation`(아사, 기아) 문제 발생하기 쉬움: 특히 FCFS방식에서 매우 실행시간이 긴 process가 있을 경우 심각한 결과를 초래.
    * interactive task에 불리함.

#### 2-1-1. 주요 알고리즘

- **FCFS (First-Come, First-Served)**
    - Ready Queue에 도착한 순서대로 Process에 CPU를 할당.
    - 구현이 단순하지만 긴 Process가 짧은 Process를 지연시키는 **`Convoy Effect` (호위효과)** 가 발생할 수 있음.
- **SJF (Shortest Job First)**
    - Ready Queue에서 `CPU Bust Time` 이 가장 짧은 Process를 선택.
    - 평균 대기 시간을 줄이는 데 효과적 
    - CPU 이용시간이 긴 Process (`CPU bound Process`)가 기아 상태 (`Starvation`)에 빠질 위험이 존재.
- **Priority Based Non-Preemptive Scheduling**
    - 가장 높은 우선순위를 가진 Process를 선택.
    - 낮은 우선순위 Process는 무기한 대기 상태에 놓일 수 있음: `Starvation`.
- **Multi-Level Queue Scheduling** \*\*
    - **구조**: 
        - Process를 특성에 따라 여러 Queue로 분류하며, 
        - 각 Queue는 독립적인 Scheduling 알고리즘을 사용.
        - Queue 간의 이동은 없음.
    - **Queue 구성**:
        - Foreground Process Queue: 
            - 사용자가 보는 공간에서 상호작용하며 실행되므로 응답 시간 중시하여 
            - RoundRobin (아래 설명) 알고리즘을 도입.
        - Background Process Queue: 
            - 사용자가 인지하지 못하는 공간에서 사용자와 상호작용 없이 실행되므로 처리량 중시. 
            - FCFS 알고리즘을 적용하여 batch job의 효율 극대화.
        - System Process Queue: 
            - 높은 우선순위 부여. 
            - 중요한 시스템 작업의 빠른 실행을 위해 Preemptive Scheduling이 적용시켜 즉각적인 처리 보장.
    - **I/O와의 연계**: 
        - I/O 작업을 많이 수행하는 Process는 
        - 빠르게 I/O 대기 Queue와 준비 Queue를 오가며 효율적으로 Scheduling.

---

### 2-2. Preemptive Scheduling

Preemptive Scheduling은 Non-Preemptive Scheduling과 달리, 

* **실행 중인 프로세스를 OS가 강제로 중단** 하고 Ready Queue에 있는 다른 프로세스에 CPU를 할당할 수 있음. 
* 이는 Ready Queue에 새로운 프로세스가 도착하거나 Time Slice가 만료되는 상황에서 작동

#### 2-2-1. 주요 알고리즘

- **SRTF (Shortest Remaining Time First)**
    - Ready Queue에서 남은 CPU Bust Time이 가장 짧은 Process를 선택.
    - I/O 중심 Process는 짧은 실행 시간을 자주 가지므로 대기 시간이 최소화됨.
- **라운드 로빈 (Round Robin)** \*\*
    - 모든 Process에 동일한 Time Slice(or 타임 퀀텀)을 부여하며, 
    - Time Slice가 만료되면 Ready Queue의 맨 뒤로 이동.
    - Time Slice 설정이 시스템 성능에 중요한 영향을 미침.
- **Priority Based Preemptive Scheduling**
    - 더 높은 우선순위의 Process가 Ready Queue에 도착하면 
    - 실행 중인 Process를 중단하고 해당 새로운 Process를 선택.
- **Multi-Level Feedback Queue Scheduling** \*\*\*
    - **동작 방식**:
        - Process를 여러 단계의 Ready Queue로 나누어 관리.
        - 상위 Queue일수록 짧은 Time Slice을 부여하면서 우선 실행되는 구조임 
            - 주로 상호작용이 필요한 foreground process가 상위 Queue에 위치.
        - CPU 사용 시간이 긴 Process는 점차 하위 Queue로 이동 
            - 하위 Queue는 우선순위가 낮지만 할당된 time slice는 긴 편임. 
            - 하위 Queue에는 주로 백그라운드 프로세스가 위치하게 됨.
        - 처음에 상위 Queue에 들어가 실행되고 점차 하위 Queue에 push 되는 구조임.
    - **특징**:
        - I/O 중심 프로세스는 상위 큐에서 높은 우선순위를 부여받아 빠르게 처리됨.
        - 대화형 프로세스는 짧은 Time Slice을 통해 응답 시간을 단축하여 사용자 경험을 개선.
        
---

---

## 3. 실제 사용되는 Process Scheduling 구현물

앞서 살펴본 알고리즘들이 단독으로는 사용되지 않으며,  
다양한 우선순위과 알고리즘이 합쳐져서 OS에서 사용됨.

대표적인 예가 바로 Linux의 선점형 `CFS`(Completely Fair Scheduler)로서  
이는, **`vruntime`** 을 기반으로 공정한 Process Scheduling을 구현함. 

### 3-1 vruntime 개념

- `vruntime`은 일종의 **가상 실행 시간**: Process의 실제 실행 시간을 가중치로 보정한 값.
- **우선순위가 높은 Process** 는 
    - **낮은 가중치(`Nice value`)를 가져 `vruntime` 증가 속도가 느리며**, 
    - 실제 CPU 사용 시간에 비해 낮은 `vruntime` 값을 가짐.
    - 이를 통해 더 자주 CPU를 할당받을 수 있음.
- I/O 중심 Process는 
    - 그 자체로 CPU 사용 시간이 짧아 `vruntime` 이 덜 증가함.

---

### 3.2 CFS 동작 방식

- **레드-블랙 트리 (`RB Tree`)**: 
    - Ready Queue를 트리 구조로 구현하여 
    - `vruntime`이 가장 작은 Process를 빠르게 선택.
- **Context Switch(문맥 교환)**: 
    - 실행 중인 Process의 `vruntime`이 증가하면 
    - 자연스럽게 다른 Process로 전환됨.
- **nice 값 조정**: 
    - Process의 우선순위를 동적으로 제어. 
    - 시스템 성능을 최적화합니다.
    - 낮은 `nice` 값(예: `-20`)은 높은 우선순위를 나타내며 낮은 가중치를 가지며 느리게 `vruntime`이 증가.
    - 높은 `nice` 값(예: `+19`)은 낮은 우선순위를 나타내며 높은 가중치를 가지며 빠르게 `vruntime`이 증가.


