# File System

File system은 ***OS가 HDD나 SSD 등의 저장장치에 데이터를 저장하고 접근하는 방법을 정의*** 하는 "file과 디렉터리의 구조적 조직"임. 

File system은 ***데이터를 관리*** 하고, ***저장공간을 효율적으로 사용*** 하며, ***사용자와 OS 사이의 인터페이스 역할을 수행*** 함.

> ***포맷(Formatting)***:  
>
> * 포맷은 저장 장치를 사용하기 위해 준비하는 과정을 말하며, 이 과정에서 파일 시스템을 생성함. 
>     * Windows에서는 partition을 formatting을 통해 volume으로 만듬.
>     * 즉, volume은 file system의 저장영역에 해당함.
> * 포맷을 할 때, 운영 체제는 디스크에 파일 시스템을 구축하여 데이터를 저장할 수 있는 구조를 생성.
> 이는 파일 시스템의 규칙에 따라 디렉토리, 파일 할당 테이블 등의 관리 정보를 설정하게 됨.

## 기본 구성요소.

file system을 구성하는 기본 요소는 다음과 같음:

1. **file**: ***데이터의 논리적 단위*** 로, 문서, 이미지, 프로그램 등 다양한 형태의 정보를 포함합니다.
2. **directory(또는 folder)**: file 을 그룹화하여 관리하는 논리적 단위.
3. **meta-data**: file의 크기, 생성 날짜, 수정 날짜 등 file에 관한 상세 정보를 포함.
4. **액세스 제어**: file과 directory에 대한 사용자의 접근 권한을 관리.

file system은 일반적으로 다음과 같은 작업을 지원합니다:

- file 생성, 삭제, 수정
- file과 디렉터리의 이름 변경 및 이동
- file에 대한 메타데이터 읽기 및 수정
- file과 디렉터리에 대한 보안 및 접근 권한 설정

## 대표적인 file system의 예:

1. **NTFS (New Technology File System)**
: Windows에서 주로 사용되며, 큰 file 크기와 복잡한 보안 옵션을 지원.

2. **FAT32 (File Allocation Table 32)**
: 호환성이 높아 많은 휴대용 장치와 게임 콘솔에서 사용됨. 그러나 4GB 이상의 file을 지원하지 않는 제한이 있음.

3. **ext4 (Fourth Extended Filesystem)**
: Linux에서 널리 사용되며, 높은 수준의 데이터 무결성과 대용량 저장소를 지원.

4. **APFS (Apple File System)**
: apple의 최신 운영 체제에서 사용되며, 최적화된 공간 할당과 빠른 성능을 제공.
