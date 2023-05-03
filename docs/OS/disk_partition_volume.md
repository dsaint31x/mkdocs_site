# Disk, Partition, and Volume

## Disk

> 💡 시스템에 장착되어 있는 저장 장치

- 윈도우에선 시스템에 장착된 storage(저장 장치)를 의미
- 파티션(혹은 볼륨)으로 나뉘어 사용되는 저장장치

### **참고**
    
`Disk`

- 자기 디스크로(Magnetic Disk) 둥근 원반에 자성을 가진 물체를 입히고 그 표면에 자력을 이용하여 데이터를 기록하고 자기장의 변화를 통해 데이터를 읽는 방식의 자기 기록 매체를 의미.
- 플로피 디스크 드라이브, ZIP 드라이브, 하드 디스크 드라이브 등
    
`Disc`    
- 광 디스크로(Optical Disc) 둥근 원반에 얇은 반사체를 입힌 후 레이저를 이용하여 홈을 파서 데이터를 기록하고 레이저 반사의 변화를 통해 데이터를 읽는 방식의 광학 기록 매체를 의미.
- 대표적으로 CD, DVD, 블루레이 등

### Disk 종류(1)

- Fixed Disk (고정 디스크)
    - 시스템에 장착되어 이동불가인 디스
    - SSD,SATA,IDE 등
- Removable Disk (이동식 디스크)
    - USB,e-SATA 등
- Virtual Disk (가상 디스크)
    - Daemon이나 ISO 툴 등
- Raid Disk
    - 여러 물리적 디스크가 하나의 디스크로 인식되도록 array로 묶임.
        
### Disk 종류(2) : Window OS
    
**기본 디스크**

- Primary Partition, Extended Partition, Logical Drive를 사용하여 데이터 구성.
- ***포맷된 파티션*** 은 ***볼륨*** 이라고 함.
- 기본 디스크 상에서 **볼륨과 파티션은 동의어**

**동적 디스크**

- **기본 디스크** 의 Primary Partition처럼 동작하는 동적 볼륨을 포함.
- 소프트웨어 기반 레이드

## Partition ← Windows7 이상에서는 사용치 않는 용어

>💡 디스크의 공간을 논리적으로 분할하여 별도의 데이터 영역으로 분할한 공간

**별도의 디스크처럼 동작하는 컴퓨터 하드 디스크의 일부**.

### 참고
    
**Primary Patition**

- `MBR`(마스터부트)
    - 기본 디스크에 최대 4개까지 만들 수 있으며, OS를 설치할 수 있음.
- `GPT`(Globally Unique Identifire)
    - 기본디스크에 최대 128개까지 만들수 있음.(일반 bios가 아닌 EFI가 지원)

**Extended Partition**

- 주파티션과 달리 갯수 제한이 없음.
- MBR은 4개의 파티션 중에 하나를 Extended Partition으로 명기하고, 이 안에 EBR를 추가 생성하여 다시 Extended Partition내에 논리드라이브라는 파티션을 생성.

**Logical Drive**

- MBR
    - 기본디스크 내의 확장 파티션 내에 만들 수 있는 파티션

## Volume

>💡 파일 시스템으로 **포맷된 디스크 상의 저장 영역**.

- 일반적으로 **드라이브 문자를 지정** 받아 ***드라이브*** 가 됨.
- 기본 디스크에선 하나의 파티션이 하나의 볼륨.
    - 단일 하드 디스크에서 여러 개의 볼륨 (기본디스크)
    - 여러 하드 디스크로 된 하나의 볼륨 (동적디스크)

엄밀하게는 좀 다르나, 거의 Partition으로 생각해도 됨.

## Drive

파일 시스템에서 포맷하여 ^^드라이브 문자가 지정된 볼륨^^.

>💡 드라이브 문자가 지정된 저장영역

## References

* [참고 : 시스템 예약 파티션](https://www.notion.so/e22501de011f43ca88c418cdddbbe929)