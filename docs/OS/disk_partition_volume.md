# Disk, Partition, and Volume

## Disk

> 시스템에 장착되어 있는 저장 장치

- 윈도우에선 시스템에 장착된 storage(저장 장치)를 의미
- partition(혹은 volume)으로 나뉘어 사용되는 저장장치

***

### **참고** : Disk and Disc
    
`Disk`

- 자기 디스크로(Magnetic Disk) 둥근 원반에 자성을 가진 물체를 입히고 그 표면에 자력을 이용하여 데이터를 기록하고 자기장의 변화를 통해 데이터를 읽는 방식의 자기 기록 매체를 의미.
- 플로피 디스크 드라이브, ZIP 드라이브, 하드 디스크 드라이브 등
    
`Disc`    
- 광 디스크로(Optical Disc) 둥근 원반에 얇은 반사체를 입힌 후 레이저를 이용하여 홈을 파서 데이터를 기록하고 레이저 반사의 변화를 통해 데이터를 읽는 방식의 광학 기록 매체를 의미.
- 대표적으로 CD, DVD, 블루레이 등

***

### Disk 종류(1)

- Fixed Disk (고정 디스크)
    - 시스템에 장착되어 이동불가인 디스크.
    - SSD, SATA, IDE 등
- Removable Disk (이동식 디스크)
    - USB,e-SATA 등
- Virtual Disk (가상 디스크)
    - Daemon이나 ISO 툴 등
- Raid Disk
    - 여러 물리적 디스크가 하나의 디스크로 인식되도록 array로 묶임.

***

### Disk 종류(2) : Window OS
    
**primary disk(기본 디스크)**

- Primary Partition, Extended Partition, Logical Partition를 사용하여 데이터 스토리지를 구성.
- ***포맷된 파티션*** 은 ***볼륨*** 이라고 함.
- MBR 또는 GPT 스키마를 사용하며, 하나의 partition이 하나의 volume에 해당함.
- partition 중심으로 관리됨.

**dynamic disk(동적 디스크)**

- **기본 디스크** 의 Primary Partition 처럼 동작하는 ***동적 볼륨*** 을 포함.
- 소프트웨어 기반 RAID(레이드)를 통해 volume 생성이 가능.
    - 여러 partition이 모여 하나의 volume을 생성.
    - mirrored volume: 복구 가능.
    - striped volume: 보다 빠른 속도 지원.
    - RAID-5 volume: 복구와 속도를 둘 다 추구.
- volume 중심으로 관리됨.

***

***

## Partition 

> disk(디스크)의 공간을 논리적으로 분할하여 별도의 데이터 영역으로 분할한 공간

**별도의 디스크처럼 동작하는 컴퓨터 하드 디스크의 일부**.

format을 통해, os에서 사용가능한 volume이 됨.

### 참고: `MBR` Scheme, `GPT` Scheme

> `MBR` 스키마는 HDD나 다른 storage에서 data를 분할하고 부팅정보를 저장하는 방법을 정의하는 partition table 구조임.  
> 2TB 이상의 disk를 지원하지 못함(32bit address 기반).  
> 이를 개선한 `GPT` 스키마가 개발됨.

***

### 참고: Scheme

Scheme는 특정 목적을 달성하기 위한 조직적인 방법이나 체계 등을 가르킴. 컴퓨터 공학에서는 종종 

* 데이터의 구성
* 프로토콜
* 형식 또는 방법론

을 가르키거나 설명하는데 사용됨.

Partition Scheme라고 하면, HDD나 storage를 조직화하는 방법으로 이는 컴퓨터에서 데이터를 저장하고 관리하기 위해 사용되는 구조적인 체계를 가르킴.

**Primary Partition**

- `MBR`(Master Boot Record) 스키마.
    - 기본 디스크에 최대 4개의 primary partition까지 만들 수 있으며, 이 primary partition에 OS를 설치할 수 있음.
- `GPT`(Globally Unique Identifier Partition Table, GUID Partition Table) 스키마.
    - 기본디스크에 최대 128개까지 partition을 만들 수 있음.
    - 주의할 점은 `GPT`에선 extended partition의 개념이 없음.
    - 일반 BIOS가 아닌 Extensible Firmware Interface(EFI)가 지원하는 스키마.

**Extended Partition**

- `MBR` 스키마에서 HDD를 논리적으로 나누는 데 사용되는 특별한 partition으로 `MBR`스키마에서 primary partition을 4개만 가지는 단점을 보완하기 위해 도입됨.
- MBR은 4개의 파티션 중에 하나를 Extended Partition으로 명기하고, 
- Extended Partition 내의 각 logical partition은 EBR(Extended Boot REcord)로 시작되며 EBR을 통해 해당 logical partition의 위치, 크기 및 다음 EBR로의 link 정보를 포함하고 있음.
- 즉, 하나의 Extended Partition 내부에 여러 개의 logical partition을 가질 수 있음. 

**Logical Partition**

- MBR 스키마에서 사용됨.
- 기본디스크 내의 extended partition 내에 만들 수 있는 partition.
- EBR 로 시작되며, 각 logical partition들이 이 EBR을 통해 서로 순차적으로 연결되어 있기 때문에 logical partition에서 데이터를 찾기 위해서는 여러 EBR을 거쳐야 하는 성능저하가 있음.

***

***

## Volume

> "파일 시스템"으로 **포맷된 디스크 상의 저장 영역**.
> 
> * 하나 이상의 partition에 파일 시스템이 포맷되고 
> * os에서 데이터를 접근할 수 있도록 만들어진 논리적인 저장 단위임.

Volume은 partition에 format을 통해 file system이 구성된 것을 가르킴.

- 일반적으로 volume은 **드라이브 문자를 지정** 받아 ***드라이브*** 가 됨.
- 기본 디스크에선 하나의 파티션이 하나의 볼륨이 되는게 일반적임.
    - 단일 하드 디스크에서 여러 개의 볼륨 (기본디스크)
        - 이 경우, 하나의 partition이 하나의 volume.
    - 여러 하드 디스크로 된 하나의 볼륨 (동적디스크)
        - 이 경우, 여러 partition이 하나의 volume
        - 동적 디스크외에 RAID 구성도 여기에 포함됨.

엄밀하게는 좀 다르나, 기본디스크에서는 volume은 Partition으로 생각해도 큰 문제 없음.

***

***

## Drive

파일 시스템에서 포맷하여 ^^드라이브 문자가 지정된 볼륨^^.

> 드라이브 문자가 지정된 저장영역

---

---

## References

* [참고 : 시스템 예약 파티션](https://www.notion.so/e22501de011f43ca88c418cdddbbe929)