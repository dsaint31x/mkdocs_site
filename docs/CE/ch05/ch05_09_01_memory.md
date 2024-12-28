---
title: Memory Hierarchy and Cache
tags: [cache, cache hit, cache miss, dispatcher, write through, write back, cache coherence]
---

# Memory Hierarchy and Performance 

## 1. Memory Hierarchy

메모리 계층 구조는 다음 URL을 참고:

[Memory Hierarchy](../ch04/ce04_01_memory.md#4-memory-hierarchy-priceperformance-ratio-and-access-time)

* DRAM은 1/10 이상 CPU보다 느리다고 생각해도 됨.
* Disk의 경우 1/100만 이상 느림.
* 때문에 Cache가 존재.

---

---


## 2. Cache Memory 주요 개념 설명

### 2-1. Cache Miss와 Cache Hit

캐시 메모리 접근 시 발생할 수 있는 두 가지 상황:

- **Cache Hit**: 
    - CPU가 Cache Memory 에서 원하는 데이터를 찾은 경우. 
    - 이는 가장 이상적인 상황 
    - CPU는 별도의 Main Memory 접근 없이 빠르게 데이터를 얻을 수 있음.
- **Cache Miss**: 
    - CPU가 캐시 메모리에서 원하는 데이터를 찾지 못한 경우. 
    - 이때는 Main Memory에서 데이터를 가져와야 하므로, 추가적인 시간이 소요.

---

### 2-2. Dispatcher (디스패처)

Dispatcher 는 Cache Memory System 에서 다음의 역할을 수행:

- 데이터의 이동을 관리하고 제어하는 logic circuit.
- 서로 다른 크기의 데이터 블록들을 효율적으로 패킹하고 언패킹하는 작업을 수행.
- Cache와 Main Memory 사이의 데이터 전송을 조율.

---

### 2-3. Cache Coherency (캐시 일관성)

Multi-Processor 또는 Multi-Core 환경에서 발생하는 중요한 이슈:

- 여러 Processor 나 Core 가 동일한 데이터에 접근할 때, 데이터의 일관성을 유지해야함.
- 이는 한 Core가 데이터를 수정했을 때, 다른 코어들이 이 변경사항을 정확히 인식해야 함을 의미.
  
#### 2-3-1. `Write Through` 방식.:

- 데이터를 쓸 때 Cache 와 Main Memory 에 동시에 기록.
- 성능은 다소 저하되지만, Cache Coherency를 보장.

#### 2-3-2. `Write Back` 방식.:

- 캐시의 데이터가 수정될 때 즉시 메인 메모리에 기록하지 않고, 캐시에만 먼저 기록.
- 수정된 캐시 데이터는 나중에 캐시에서 방출(eviction)될 때 한꺼번에 메인 메모리에 기록
- 메모리 쓰기 횟수가 줄어들어 시스템 성능이 향상
- Cache Coherency 를 위한 복잡한 기술이 요구됨.
- 갑작스러운 시스템 장애 시 캐시의 수정된 데이터가 손실될 수 있음.