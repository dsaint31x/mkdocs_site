# Linux : 명령어 

### 현재 디렉토리 확인

현재 디렉터리를 확인하는 명령어는 `pwd`(print working directory)이다.

```bash
pwd
```

- 현재 위치를 확인한다. 즉, 현재 디렉터리의 절대 경로를 출력한다.

### 디렉토리 이동

다른 사용자의 접근을 막아 놓은 디렉터리를 제외하고는 어느 디렉터리로든 이동 가능.

```bash
cd target_directory_path
```

- 현재 디렉토리를 변경

### 디렉토리 내용 보기

디렉터리에 있는 파일이나 서브 디렉터리 등 디렉터리의 내용을 보는 명령은 ls(list)이다.

```bash
ls [option] file_or_dir_path
```

- 디렉토리의 내용 출력
- Option
    
    `-a` : 숨김 파일을 포함 모든 파일 목록 출력.
    
    `-d` : 지정한 디렉터리 자체의 정보를 출력.
    
    `-i`  :  첫 번째 행에 inode 번호를 출력한다.
    
    `-l`  : 파일의 상세 정보를 출력
    
    `-A` : `.`(마침표)와 `..`(마침표 두 개)를 제외한 모든 파일 목록을 출력
    
    `-F` : 파일의 종류를 표시한다(`*` : 실행파일, `/`: 디렉터리, `@`: 심벌릭 링크)
    
    `-L` : 심벌릭 링크 파일의 경우 원본 파일의 정보를 출력.
    
    `-R` : 하위 디렉터리 목록까지 출력.
    

### 디렉토리 만들기

```bash
mkdir [option] directory_path
```

- 디렉토리를 생성.
- Option
    
    `-p` : 하위 디렉터리를 계층적으로 생성할 때 중간 단계의 디렉터리가 없으면 자동으로 중간 단계 디렉터리를 생성하면서 전체 디렉터리를 생산한다.
    

### 디렉토리 삭제하기

```bash
rmdir [option] directory_path
```

- 디렉토리를 삭제
- Option
    
    `-p` : `--parent`로도 쓰임. 지정한 데릭터리를 삭제한 뒤, 그 디렉터리의 부모 디렉터리가 빈 디렉터리일 경우 부모 디렉터리도 자동으로 삭제.

### 파일이나 디렉토리 삭제.

```bash
rm [option] target_path
```

- 파일이나 디렉토리를 삭제함.
- Option

    `-r` : `--recursive`로도 쓰임. 디렉토리가 target인 경우 사용되며, target 밑의 하위 디렉토리 및 파일을 모두 제거함.

    `-i` : 삭제할 때마다 삭제여부등을 물어봄.

    `-f` : `--force`로도 쓰임. 삭제여부를 물어보지 않고 강제로 지움. 존재하지 않는 파일인 경우에도 명령어가 수행됨. (없는 파일을 지울 때는 없다는 메시지가 뜨는데 이런 메시지가 뜨지 않음)

### 복사

```bash
cp [option] src_path target_path
```

- 파일이나 디렉토리를 복사함.

### 이름변경 또는 이동

```bash
mv [option] src_path target_path
```

- 파일이나 디렉토를 이동하거나 이름을 변경함.

### (Text) 출력

```bash
cat target
```

- 파일의 내용 또는 환경변수의 내용을 출력 (text 출력에 사용됨)

### 특정 패턴 검색

```bash
grep pattern
```

- 입력에서의 특정 문자열 패턴을 검색.

### 파일 권한 변경

```bash
chmod mode target
```

- 파일 또는 디렉토리의 소유자, 그룹, 그외 사용자 등의 권한을 변경.
- 권한은 rwx 를 나타내는 이진수 (ex: b`100`은 읽기만 가능)를 팔진수로 바꾸어 표시 (읽기는 이진수로 b`100`이니 `4`로 표시).
- 소유자(`u`), 그룹(`g`), 그외 사용자(`o`) 순으로 지정함.

```bash
chmod 777 target_path
```

- target_path에 대해, 모든 사용자(`a`)가 읽기(r),쓰기(w),실행(x)가 가능.

```bash
chmod g+x target_path
```

- `target_path`에 대해, ***그룹*** 들에 실행 권한을 줌.

```bash
chmod a=r target_path
```

- `target_path`에 대해 모든 사용자가 읽기가 가능해짐.

```bash
chmod go-rwx target_path
```

- `target_path`에 대해 그룹과 그외 사용자 들의 모든 권한을 제거.

보다 자세한 건 다음 url참고 : [chmod 사용법](https://recipes4dev.tistory.com/175)

### 소유자 변경

```bash
chown [option] [user][:group] target_path
```

- 파일의 소유자, 그룹을 변경

### 프로세스 및 리소스 모니터링

```bash
top
```

- 시스템의 현재 작동 중인 프로세스 목록과 시스템 리소스 사용량을 표시

### 네트워크 인터페이스 정보 확인

```bash
ifconfig
```

- 네트워크 인터페이스의 정보를 표시