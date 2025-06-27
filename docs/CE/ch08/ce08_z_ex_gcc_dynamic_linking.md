---
title: "gcc: Dynamic Linking"
tags:
    - gcc
    - so
    - Shared Object
    - LD_LIBRARY_PATH 
---

Dynamic Linking은 프로그램이 실행될 때 필요한 라이브러리 코드를 동적으로 로드하여 사용하는 방식을 가리킴.

좀더 자세한 건 다음을 참고: [Dynamic Linking](../ch05/ch05_11_01_program_execution.md#4-dynamic-linking)

이 문서는 `gcc`를 사용하여 간단하게 동적라이브러리 파일을 만들고 이를 동적으로 연결하여 사용하는 실행파일을 작성 및 동작시켜보는 예제를 소개함.

---


## 0. Pre-Requirements

### gcc (GNU Compiler Collection)

* C, C++, Objective-C, Fortran 등을 컴파일할 수 있는 컴파일러 모음.
* 여기서는 C 소스코드파일을 컴파일하고 Dynamic Linking을 사용하는 실행파일을 만드는데 사용됨.

> 단순한 예제이므로 `gcc` 만을 이용하나, 여러 파일들이 있는 실제 프로젝트의 경우 `CMake` 와 같은 빌더툴이 사용됨.

### Position Independent Code (PIC)

* 동적라이브러리의 경우, 생성되는 object code가 위치 독립적이어야 여러 프로그램에서 쉽게 사용할 수 있음.
    * 이를 고려하지 않을 경우, 고정된 메모리 주소에 의존할 수 있으며 이는 실행 프로그램에서 문제를 일으킬 수 있음.
* 때문에 컴파일러가 생성하는 object file(`.o`)이 메모리의 어느 위치에 로드되더라도 정상적으로 동작할 수 있도록 코드를 생성하도록 `-fPIC` 옵션을 추가해줌.

이는 shared object library 파일(`.so`)를 만들 때 사용됨.

### LD_LIBRARY_PATH

* 동적라이브러리 파일이 위치하는 path를 가지고 있는 Environment Variable 임. 
* 기본적으로 해당 경로들에서 동적라이브러리를 찾음.

> 이 문서에서는 단순한 예제이므로 **같은 디렉토리에서 동적라이브러리 파일** 을 놓고 진행함.

---


## 1. 실행파일 소스코드 컴파일.

```c linenums="1"
// main.c
#include <stdio.h>
void print_hello(void);

int main(void) {
    print_hello();
    return 0;
}
```

* `print_hello` 함수가 선언만 되어 있을 뿐 구현이 없음.
    * 동적으로 구현코드를 로드하여 사용할 예정임.

다음의 명령어로 컴파일.

```bash
gcc -c main.c -o main.o
```

* `-o` 옵션에 지정된 이름의 object code 파일이 생성됨.


---

## 2. 동적라이브러리 소스코드 컴파일.

```c linenums="1"
// mylib.c
#include <stdio.h>

void print_hello(void){
	printf("Hello, World from Shared Library!\n");
}
```

* Source code 상에서는 차이점이 없음.

다음의 명령어로 동적라이브러리 파일(`.so` 파일, Shared Object)로 컴파일.

```bash
gcc -shared -fPIC -o libmylib.so mylib.c
```

* `-shared` : 이 옵션은 컴파일러에게 공유라이브러리로 컴파일하도록 지시 (Shared Object 로 컴파일)
* `-fPIC` : 이 플래그는 생성되는 object code 가 위치 독립적이도록 지시함 (Shared Object에서 필요한 기능)

Linux 등의 경우, Shared Object 파일의 이름은 `lib`라는 접두사로 시작하고, `.so`라는 extension으로 끝나는게 관례임.


---

## 3. 동적라이브러리 사용하는 실행파일 빌드.

```bash
gcc main.o -o myexecutable -L. -lmylib
```

* `-o` : 빌드 결과 파일 이름 지정하는 옵션으로 `myexecutable`이라는 이름으로 실행파일 생성.
* `-L` : `-L/path/to/lib` 의 형태로 **동적라이브러리가 위치하는 경로를 지정** 해주는 옵션.
    * 경로를 복수개 지정가능함: 복수개의 `-L` 옵션을 사용하면 됨.
    * `-L/path/to/lib1:/path/to/lib2` 처럼 Colon `:`으로 구분하기도 하나 비추천.
    * 주어진 순서에 따라 라이브러리가 검색되며, 앞에 있는 라이브러리에 우선권이 있음. 
* `l` : `-ltargetlib` 의 형태로 **Dynamic Linking이 이루어지는 라이브러리 파일명을 지정** . 
    * 여기서 `lib`접두사와 `.so` 확장자는 빠짐.
    * 복수 개의 Shared Object 지정 가능함.
 
---

## 4. 실행하기.

```bash
❯ ./myexecutable
Hello, World from Shared Library!
```


---

## 5. 참고.

일반적으로 `.so`파일 하나당 하나의 소스코드가 존재함.

여러 object 파일들을 묶어서 하나의 `.so` 파일로 만들 수 있지만 일반적이진 않음.


---

## 참고자료

* [실습동영상](https://youtu.be/eA48Y59AvVo)