# Virtual Memory


`MMU` can map a program’s virtual addresses to physical memory. 

![](./img/virtual_memory.png)


## Demand paging

Virtual memory에서는 모든 프로세스에서 요청된 메모리 양이 사용 가능한 양을 초과할 수도 있음.

이 경우, 운영 체제는 현재 필요하지 않은 메모리 페이지의 내용을 더 크지만 느린 대용량 저장 장치인 디스크로 이동시킵니다 (swap out).

프로그램이 스왑 아웃된 메모리에 액세스하려고 하면, 운영 체제는 필요한 공간을 만들기 위해 필요한 작업을 수행한 후 요청된 페이지를 다시 복사합니다(swap in).

![](./img/virtual_memory2.png)

## LRU algorithm

A least recently used (LRU) algorithm that tracks accesses to pages. The most frequently used pages are kept in physical memory; the least recently used are swapped out.