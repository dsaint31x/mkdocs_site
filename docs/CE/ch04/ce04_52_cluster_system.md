# Cluster System 

> Cluster System 은 ***여러 대의 컴퓨터를 하나의 시스템처럼 동작*** 하게 하여 높은 성능과 가용성을 제공하는 parallel computing architecture임.

Cluster System 은 

* 여러 대의 같은 OS가 설치된 독립적인 컴퓨터(노드)들과
* 동일한 파일 시스템을 
* ***고속의 LAN (Local Area Network)으로 연결*** 하여 
* 하나의 통합된 컴퓨팅 환경을 만드는 것을 가르킴.

참고: [LAN vs. WAN](../ch06/ce06_2_01_history.md#lan-vs-wan)

---

## 특징

특징은 다음과 같음.

* 병렬 처리를 통한 고성능: 각 노드는 독립적으로 작업을 수행하여 병렬 처리를 구현.
* ***밀접한 통합*** : 노드들은 동일한 환경(OS등)을 공유하며, 긴밀하게 상호 작용.
* 공유 저장소: 모든 노드가 동일한 파일 시스템에 접근(NFS)하여 데이터 일관성을 유지.
* 높은 신뢰성 (=고가용성)): 하나의 노드가 실패해도 다른 노드가 이를 대신하여 작업을 계속할 수 있음.
* 작업 스케줄링: 중앙 집중식 스케줄러가 있어 작업을 효율적으로 분배하여 효과적인 부하 분산이 가능함.

---

## 장단점

장단점은 다음과 같음.

***장점:***

* 높은 성능과 신뢰성.
* 중앙 관리와 제어 용이.
* 일관된 환경 제공.

***단점:***

* 확장성의 한계: 물리적으로 동일한 위치에 있어야 하며, 네트워크 대역폭과 하드웨어 제약이 있음.
* 고비용: 고성능 네트워크와 일관된 하드웨어 요구.

---

## 결론

Cluster System은 

* 높은 성능, 가용성, 확장성을 제공할 수 있음. 
* 과학 연구, 데이터베이스 관리, 웹 서비스, 인공지능 및 머신러닝 등 다양한 분야에서 활용됨.
* 특히 오늘날 클라우드 서비스의 기반은 대규모의 cluster system이라고도 할 수 있음.