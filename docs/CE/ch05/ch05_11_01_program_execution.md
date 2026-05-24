---
title: Library, Shared Library, Dynamic Linking
description: 실행 파일 생성 과정에서 linker가 object file과 library를 결합하는 방식, runtime library의 역할, shared library와 dynamic linking의 차이를 정리한다.
tags:
  - linker
  - static linker
  - library
  - shared library
  - dynamic linking
  - runtime library
  - CRT
  - object file
  - ELF
  - executable file
  - entry point
  - relocation
  - symbol resolution
---

# Library, Shared Library, Dynamic Linking


## **0. Library**

다음을 참고하라:

[Library vs. Framework](https://dsaint31.tistory.com/452)

---

## **1. Linker**

Executable file을 만들기 위해 Linker는 다음의 여러 조각들을 하나로 연결함.

* 컴파일러가 생성한 개별 object file
* 프로그램이 사용하는 여러 `Library`
* 각 object file과 library에 정의된 symbols

이 과정에서 Linker는 다음 작업을 수행함.

* 심볼 결합(Symbol Resolution)
    * 함수, 변수 등의 symbol reference가 실제 어느 symbol definition을 가리키는지 결정함.
* 주소 재배치(Relocation)
    * object file 단위로 작성된 code와 data의 주소를 최종 배치에 맞게 수정함.
    * 모듈 간 함수 호출이나 데이터 참조가 올바른 주소를 가리키도록 조정함.
* 라이브러리 연결
    * 필요한 외부 library를 찾아 object file들과 연결함.
    * static library의 경우 필요한 code가 executable file에 포함될 수 있음.
    * shared library의 경우 실행 시 사용할 library reference가 executable file에 기록될 수 있음.

즉, Linker는 프로그램이 실행 가능한 형태가 되기 위해 필요한 object files와 libraries 사이의 의존 관계를 연결하는 도구임.

다음 URL 참고: [Compiler 언어가 실행파일 만드는 과정](../ch08/ce08_compiler_interpreter.md#compiler-language)

---

### **1-1. Executable and Linkable Format (ELF)**

**ELF(Executable and Linkable Format)** 는 Linux/Unix 계열에서 사용되는 binary file format임.

ELF는 다음과 같은 파일 형식에 사용됨.

* Object file
* Executable file
* Shared object file

즉, Linux 환경에서는 Linker가 입력으로 받는 object file과 출력으로 만드는 executable file, 그리고 shared library가 모두 ELF 형식일 수 있음.

> 엄밀히 말하면 ELF는 주로 Linux/Unix 계열에서 사용되는 형식임.  
> Windows에서는 Portable Executable(PE) 형식을 사용하고,  
> macOS에서는 Mach-O(Mach object) 형식을 사용함.

---

### **1-2. Object File**

Object file은 compiler가 source code를 번역한 중간 결과물(intermediate file)이며, 일반적으로 Linker의 입력 파일로 사용됨.

ELF 관점에서 object file 또는 관련 binary file은 다음과 같이 구분할 수 있음.

* Relocatable File
    * 다른 object file이나 library와 결합되기 위해 만들어진 파일.
    * 예: Linux의 `.o`, Windows의 `.obj`
    * symbol address가 아직 최종적으로 고정되지 않았으므로 symbol resolution과 relocation이 필요함.

* Executable File
    * 실행 가능한 형태로 완전히 링크된 파일.
    * 예: Linux의 `a.out`, 일반 executable file
    * Linker가 relocatable object files와 libraries를 결합하여 생성함.
    * machine code file이라고도 볼 수 있음.

* Shared Object File
    * runtime에 process address space로 mapping되어 사용될 수 있는 shared library.
    * 예: Linux의 `.so`
    * Windows의 `.dll`은 ELF shared object는 아니지만, 역할상 shared library에 해당함.

참고: [object code 관련 자료](../ch08/ce08_compiler_interpreter.md#byte-code-바이트코드)

---

## **2. Runtime Library**

Runtime Library는 OS와 programming language에 맞추어, 사용자 프로그램이 실행될 수 있도록 필요한 기본 실행 환경을 제공하는 library임.

주로 다음 기능을 제공함.

* runtime 초기화
* heap 관리 및 동적 메모리 할당 기능 제공
* 표준 입출력, 문자열 처리, 수학 함수 등 기본 library 기능 제공
* static/global data 초기화와 관련된 runtime 처리
* `main()` 호출 전후의 초기화 및 종료 처리

개발자는 보통 프로그램의 entry point로 `main()` 함수를 작성한다고 생각하지만, 실제 실행 흐름에서는 runtime startup code가 먼저 실행됨.

내부적으로는 `_start` 같은 실제 entry point에서 실행이 시작되고, runtime 초기화가 수행된 뒤 `main()` 함수가 호출됨. `main()`이 종료된 뒤에도 종료 처리, buffer flush, destructor 호출 등의 runtime 처리가 수행될 수 있음.

대표적으로 다음 작업들이 수행될 수 있음.

* process 실행 환경 준비
* command-line arguments와 environment variables 전달 준비
* C/C++ runtime 초기화
* global/static object 초기화
* `main()` 호출
* 프로그램 종료 처리

---

### **2-1. Example**

대표적인 runtime library 예시는 다음과 같음.

* Windows
    * MSVCRT(Microsoft Visual C Runtime Library)
    * `msvcrt.dll`, `ucrtbase.dll`

* Linux
    * glibc 등
    * `libc.so.6`

* macOS
    * libSystem
    * `libSystem.dylib`

Python의 경우에도 자체 runtime environment를 제공하며, 환경에 따라 다음과 같은 library가 사용될 수 있음.

* `libpython3.9.so`
* `python38.dll`
* `libpython3.9.dylib`

대부분의 현대 OS에서는 runtime library가 shared library 형태로 제공되는 경우가 많음. 다만 빌드 설정에 따라 runtime library를 executable file에 정적으로 포함할 수도 있음.

---

### **2-2. CRT(C Run Time)**

CRT는 C program을 위한 Runtime Library이며, 가장 기본적인 runtime library에 속함.

자세한 내용은 다음 글을 참고: [C Runtime(CRT)](https://ds31x.tistory.com/605)

---

## **3. Shared Library**

Shared Library는 여러 program이 공통으로 사용할 수 있도록 만들어진 library file임.

일반적으로 다음과 같은 형식으로 제공됨.

* Linux: `.so`
* Windows: `.dll`
* macOS: `.dylib`

Shared Library는 여러 program이 같은 library code를 사용할 수 있게 해줌. 이때 보통 Dynamic Linking을 통해 실행 시점에 해당 library가 process address space에 mapping됨.

예:

* `libc.so`
* `libm.so`
* `ucrtbase.dll`
* `libSystem.dylib`

Shared Library는 code를 각 executable file에 직접 복사하지 않고, 별도의 library file로 유지한다는 점이 핵심임.

---

## **4. Dynamic Linking**

Dynamic Linking은 program 실행 시점에 executable file이 필요로 하는 shared library를 찾아 process address space에 mapping하고, 필요한 symbols를 연결하는 방식임.

Static Linking과 Dynamic Linking은 다음과 같이 구분됨.

* Static Linking
    * build/link 단계에서 library code를 executable file에 포함시킴.
    * executable file의 크기가 커질 수 있음.
    * library를 수정해도 이미 만들어진 executable file에는 반영되지 않으므로 다시 link해야 함.
    * shared library를 정적으로 포함하는 경우, 다른 process와 해당 library code를 공유하기 어려움.

* Dynamic Linking
    * executable file에는 shared library에 대한 reference가 기록됨.
    * program 실행 시 dynamic linker 또는 loader가 필요한 shared library를 찾고 memory에 mapping함.
    * Linux에서는 대표적으로 `ld.so` 또는 `ld-linux.so`가 이 역할을 수행함.
    * shared library 검색 경로는 `/lib`, `/usr/lib` 같은 표준 경로, `LD_LIBRARY_PATH`, rpath/runpath 등의 설정에 의해 결정될 수 있음.
    * executable file의 크기를 줄일 수 있음.
    * 여러 process가 같은 shared library의 code page를 공유할 수 있어 memory 사용량을 줄일 수 있음.
    * library를 교체해도 executable file을 다시 build하지 않고 변경 사항을 반영할 수 있는 경우가 있음.
    * 단, ABI compatibility가 깨지면 실행 오류가 발생할 수 있음.

Dynamic Linking에서 dynamic loader는 shared library를 찾아 memory에 mapping하고, symbol reference가 실제 library symbol을 가리키도록 연결함.

일반적인 dynamic linking에서는 program 시작 시 필요한 shared library가 먼저 로드됨. 다만 symbol binding은 lazy binding 방식으로 실제 함수가 처음 호출될 때 수행될 수 있음.

또한 `dlopen()` 같은 API를 사용하면 program 실행 중 필요한 library를 명시적으로 로드할 수도 있음. 이는 dynamic loading이라고 구분해서 부르기도 함.

Shared Library code가 memory에 mapping되면, OS는 동일한 library의 code page를 여러 process가 공유하도록 할 수 있음. 단, process마다 독립적으로 가져야 하는 data 영역은 별도로 관리됨.

---

### **4-1. 정리하면**

* **Shared Library**
    * 여러 program이 공통으로 사용할 수 있도록 만들어진 library file.
    * Dynamic Linking이 가능하도록 설계된 library.

* **Dynamic Linking**
    * program 실행 시점에 shared library를 찾아 memory에 mapping하고 symbol을 연결하는 mechanism.
    * shared library라는 파일을 사용하는 방식 또는 절차에 해당함.

한 문장으로 정리하면, Shared Library는 공유 가능한 library file이고, Dynamic Linking은 실행 시점에 그 shared library를 연결하여 사용하는 mechanism임.
