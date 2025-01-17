---
title: "gcc: Static Linking"
tags:
    - gcc
    - Object
    - Header
    - hdr 
---

# gcc: Static Linking

여러 개의 소스 파일을 사용하여 정적 링크를 통해 하나의 실행 파일을 만드는 방법을 보여주는 문서임.  

좀더 자세한 건 다음을 참고: [Dynamic Linking](../ch05/ch05_11_01_program_execution.md#4-dynamic-linking)

> `gcc` (GNU Compiler Collection), `C` 언어를 이용함.

---

## Step 1: 소스 파일 및 헤더 파일 작성

`main.c` 파일은 프로그램의 entry point를 구현하고, 여러 object 파일의 함수를 호출함. 

```c linenums="1"
// main.c
#include <stdio.h>
#include "lib1.h" // lib1.h 헤더 파일을 포함
#include "lib2.h" // lib2.h 헤더 파일을 포함

int main(void) {
    print_hello(); // lib1.c에서 정의된 함수 호출
    print_hi();    // lib2.c에서 정의된 함수 호출
    return 0;
}
```

`lib1.c` 파일은 `print_hello` 함수를 정의함.

```c linenums="1"
#include <stdio.h>
#include "lib1.h" // lib1.h 헤더 파일을 포함

void print_hello() {
    printf("Hello from lib1!\n");
}
```

`lib2.c` 파일은 `print_hi` 함수를 정의.

```c linenums="1"
#include <stdio.h>
#include "lib2.h" // lib2.h 헤더 파일을 포함

void print_hi() {
    printf("Hi from lib2!\n");
}
```

> ***헤더 파일***
> 
> * 함수나 변수의 선언을 포함하여, 이 프로그램의 다른 부분에서 해당 요소를 사용할 수 있게 함. 
> * 헤더 파일을 사용함으로써 코드의 재사용성과 유지 관리 편해짐.


`lib1.h` 는 `lib1.c`의 헤더파일로 `print_hello` 함수의 선언을 포함함. 

* 헤더 파일은 함수의 선언을 포함하여, 
* 이 함수를 사용하는 다른 C 파일에서 해당 함수가 무엇인지 알 수 있게 해주어 컴파일까지 가능하게 해 줌.
* 이후 Linking 을 통해 구현코드가 합쳐져서 executable 파일이 됨.

```c linenums="1"
#ifndef LIB1_H
#define LIB1_H

void print_hello(void);

#endif
```

`lib2.h`는 `lib2.c`의 헤더파일로 `print_world` 함수의 선언을 포함. 

* 헤더 파일은 중복 포함 방지를 위해 `#ifndef`, `#define`, `#endif`를 사용함. 
* 이를 ***Include Guard*** 라고 하며, 여러 번 include (포함)되는 문제를 방지.

```c linenums="1"
#ifndef LIB2_H
#define LIB2_H

void print_hi(void);

#endif
```

---


## Step 2: 각 소스 파일을 오브젝트 파일로 컴파일

```sh
gcc -c main.c -o main.o
gcc -c lib1.c -o lib1.o
gcc -c lib2.c -o lib2.o
```

* `-c`: Compile Option
    * 각 소스 파일을 개별적으로 오브젝트 파일로 변환. 
* `-o`: Output Option
    * 생성된 오브젝트 파일의 이름을 지정.

---


## Step 3: 오브젝트 파일을 하나의 실행 파일로 링크

다음의 명령어는 static linking을 통해 모든 필요한 코드를 실행 파일에 포함시킴.  
이를 통해 실행 파일이 독립적으로 동작할 수 있음.

```sh
gcc -o myexecutable main.o lib1.o lib2.o
```

* `main.o`, `lib1.o`, `lib2.o` 를 하나의 실행 파일 `myexecutable`으로 합침. 
* `-o` : 링크된 최종 실행 파일의 이름을 지정. 여기서는 `myexecutable`입니다.

---


## 실행:

```sh
./myexecutable
```
출력은 다음과 같음.

```
Hello from lib1!
Hi from lib2!
```

---


## 관련자료

* [Dynamic Linking](./ce08_z_ex_gcc_dynamic_linking.md)
* [Static Linking과 Dynamic Linking](../ch05/ch05_11_01_program_execution.md#4-dynamic-linking)
* [실습동영상](https://youtu.be/GlpY0b1P-pY)