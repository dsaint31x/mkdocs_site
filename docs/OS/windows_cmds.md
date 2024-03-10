# 명령어 (Windows)

이 문서는  Windows의 command.exe 에서 사용되는 기본적인 명령어를 소개함.

Command Prompt는 

* PowerShell과 함께 Windows에서 사용되는 CLI(Command Line Interface)임.
* Windows의 기본적인 명령어를 실행하고, 간단한 script (`.bat` 파일)를 실행하는데 사용됨.
* Windows의 가장 기본적인 Command Line Interpreter(CLI)이며, PowerShell에 비해 제한된 기능을 가짐.
    * `CLI` 는 Command Line Interface 또는 Command Line Interpreter를 가르킴.

---

`Window키+r`를 누르고 `cmd` 를 입력하고 엔터를 누르면, command prompt창이 뜸.

해당 창에서 다음과 같은 메시지가 보임.

```basic
Microsoft Windows [Version 10.0.22621.1555]
(c) Microsoft Corporation. All rights reserved.

C:\Users\MMMIL>
```

- `C:\Users\MMMIL>` 부분을 prompt라고 부르며, 현재 cwd를 나타냄.
- 기본적으로 사용자의 home 디렉토리를 cwd로 하여 시작함.
- `MMMIL`은 windows의 현재 사용자의 ID임.

command prompt에서 커서가 깜빡거리고 있으며 이 경우 명령어를 입력하고 엔터를 누르면 해당 명령어가 수행됨.

---

---

## 1. File 관련

### 1-1. File 목록 표시

```python
dir c:
```

- 디스크 드라이브 c에 있는 파일 목록을 보고 싶은 경우 사용.
- 해당 디스크 드라이브에 들어있는 모든 파일 이름, 크기, 생성일자 및 일시 등을 나타내는 리스트 출력

```python
dir *.txt
```

- 현재 경로(cwd)에서 `.txt` 확장명을 가진 파일 리스트를 보여줌

---

### 1-2. 파일 내용의 출력

```python
type 파일명
```

- 텍스트 파일의 내용을 보고 싶을 때 사용됨.
- 파일이 매우 클 경우, `more`를 이용하여 나누어 출력할 수 있음.

---

### 1-3. 파일의 복사

```basic
copy [옵션] source destination 
copy [옵션] source[+...] destination
```

- 파일 단위로 복사를 수행.
- **파일의 결합** 에도 사용 가능함
- 옵션
    - `/a`
        - 아스키 파일(텍스트 파일)을 의미
    - `/b`
        - binary 파일 의미

---        

### 1-4. 파일 지우기

```basic
del [옵션] 파일_이름
erase [옵션] 파일_이름
```

- 하나 이상의 파일 또는 디렉토리를 지움.
- `*` 문자 등을 이용하면 복수의 파일 삭제.
- 옵션
    - `/p`
        - 각 파일을 삭제하기 전에 물어봄.

---

### 1-5. 파일 이름 바꾸기

```basic
ren filename1 filename2
```

- filename1 파일의 이름을 filename2로 바꾼다.
- 예
    - 모든 텍스트파일이 doc파일로 변경
    `ren *.txt *.doc`
    - `1.txt`를 `4.txt`로 변경.
    `ren 1.txt 4.txt`

---

---

## 2. directory 관련

### 2-1. 디렉토리 이동 및 현재 디렉토리 출력.

```basic
cd target_dir_path
```

- `target_dir_path`로 이동한다.
- current working directory (cwd, or present working directory, pwd)를 `target_dir_path`로 바꿈.
- 예
    - 현재 cwd 밑의 lecture밑의 subdirectory인 ce로 이동.
    `cd ./lecture/ce`

```basic
cd 
```

- argument없이 `cd`만 입력할 경우, 현재 cwd의 경로를 출력해줌.

> `cd`는 chagne directory의 abbreviation임.

---

### 2-2. 디렉토리 생성.

```basic
mkdir new_dir_path
```

- `new_dir_path`에 해당하는 directory를 생성한다.
- 이미 있는 경우엔 에러 메시지를 보여줌.

---

### 2-3. 디렉토리 삭제.

```basic
rmdir target_dir_path
```

- `target_dir_path`에 해당하는 directory를 삭제한다.
- `rmdir`은 비어있는 디렉토리만 삭제가능함.
- `del` 혹은 `erase`로 디렉토리를 지정할 경우, 해당 디렉토리 밑의 모든 것을 지울지를 물어보며, y를 통해 다 삭제하고 나서 `rmdir`로 디렉토리 제거.

---

### 2-4. 드라이브 이동

```basic
d:
```

- `d`드라이브로 이동함.
- cwd는 이전에 `d`드라이브에서 작업하던 path로 놓이게 됨. (보통은 `d` 드라이브 최상단)
- `c:` 를 입력시 `c` 드라이브로 이동.

---

## 3. Etc

### 3-1. 화면 지우기

```basic
cls
```

- command prompt window에 출력된 내용이 너무 많을 경우 `cls`를 통해 화면을 지우면 깨끗해짐.

### 3-2. 문자열 출력하기

```basic
echo [option] [문자열]
```

- `[문자열]`을 stdout (보통 모니터)에 출력
- redirection `>` 과 `>>`를 통해 특정 파일에 문자열을 입력시킬 수 있음 (`>>`의 경우 추가)
- `echo %PATH%` 와 같이 환경변수 `PATH`의 내용을 출력하는 데에도 사용가능함.

batch파일등에서 입력된 명령어에 대한 echo출력을 막기 위해서도 사용됨.

```basic
echo off
```

다음과 같은 test.bat 파일을 만들고 `echo on`과 `echo off`의 차이점을 살펴볼 것.

```bat
echo off

echo "====================="
echo 테스트.
```

- 한글이 깨진다면, `chcp 65001`을 입력하여 terminal에서 utf-8 인코딩을 사용하도록 변경.
- 아니면, notepad등에서 해당 `test.bat`파일을 `ANSI` 인코딩으로 저장할 것.

> `chcp` 는 CHange Code Page를 의미함.


### 3-3. 날짜 및 시간

```basic
date
```

- 날짜를 보여주고 변경할 수 있음
- 변경을 원치 않으면 그냥 enter를 입력

```basic
time
```

- 시간을 보여주고 변경할 수 있음
- 변경을 원치 않으면 그냥 enter를 입력

### 3-4. 도움말

```basic
help 알고자하는_명령어
```

- 콘솔창에서 각 명령어에 대한 도움말을 살펴볼 수 있음.

```basic
help
```

- 콘솔창에서 지원하는 명령어를 보여줌.