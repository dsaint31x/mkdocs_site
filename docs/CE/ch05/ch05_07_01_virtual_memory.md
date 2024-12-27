---
title: Virtual Memory
tags: [MMU, Virtual Memory, Physical Memory, Demand Paging, Swapping, Page Fault, Page Replacement, LRU]
---

# Virtual Memory

## **1. Virtual Memory란?**

`MMU` 는 

* 프로그램(or process)의 virtual memory를 
* 실제 physical memory에 매핑(mapping)하는 역할을 수행함.  
`MMU` can map a program’s virtual addresses to physical memory. 

더나아가 Virtual Memory는

* Memory Management Method로서, 
    * physical memory를 abstraction 하여,
    * 실제 physical memory와 사용자 관점의 logical memory를 분리하고, 
* `MMU`를 통해 이들간의 매핑을 함으로서
    * 실제 physical memory 의 크기 제한을 넘어
    * 다수의 프로그램들이 동시에 실행가능하도록 해 주는 메모리 관리 기술.

![](./img/virtual_memory.png){style="display: block; margin: 0 auto; width:400px"}

---

---

## **2. Demand Paging (요구페이징)**

Virtual Memory Management를 위한 Method로서,

* 프로세스를 memory에 load할 때, 
* 전체 모든 page를 적재하지 않고, 필요한 page들만 메모리에 load하고
* 나머지는 disk에 저장하는 방식을 사용하여
* 메모리를 절약하는 기법임.

`Demand Paging`은 필요한 pages만 RAM에 올리면서,  
동시에 최대한 page fault의 발생빈도를 줄이는 것이 목표로 함.

> 한 Process의 전체 영역이 swap-in, swap-out하는 `Swapping` 과 달리,  
> 보다 쪼개어 이루어지는 것이 `demand paging` 임.

Demand Paging을 통해 Virtual memory에서는  
**모든 프로세스에서 요청된 전체 메모리 양**이 물리적으로 사용 가능한 양을 초과할 수 있게 됨.

* 이는 OS에서 `Demand Paging` 을 통해 
* 현재 필요하지 않은 메모리 페이지의 내용을 더 크지만 느린 대용량 저장 장치인 디스크로 이동 (swap out) 시키고 
* 프로그램이 스왑 아웃된 메모리에 액세스하려고 하면, 운영 체제는 필요한 공간을 만들기 위해 필요한 작업을 수행한 후 요청된 페이지를 RAM으로 복사(swap in)를 수행함.

![](./img/virtual_memory2.png){style="display: block; maring:0 auto;width:400px"}

---

---

## **3. Page Fault**

Process가 실행하는 도중 필요한 page가 physical memory에 존재하지 않아,  
disk로부터 해당 page를 swap-in 해야 하는 경우를 가르킴.

* `Page Fault`는 `Fault` interrupt를 발생시켜서 
* 필요한 page를 swap-in 시키는 작업을 시작시킴.
* 메모리에 빈 공간이 존재하면 그대로 읽어들여 swap-in이 이루어지지만,
* 빈 공간이 부족하면, ***Page Replacement 알고리즘*** 에 따라 메모리의 page 중 일부를 disk로 swap out시키는 작업이 선행됨.


Page Fault를 최소화해야 성능이 올라가며,  
Page Replacement 알고리즘은 흔히 `LRU (Least Recently Used) 알고리즘`을 사용함.

---

---

## **4. LRU (Least Recently Used) algorithm**

LRU 알고리즘은

* page들에 대한 access를 추적하여,
* 가장 최근에 빈번하게 사용되는 pages는 physical memory에 남기고,
* 최근에 가장 덜 사용된 page를 swap-out 시키는
* page replacement 방법임. 
