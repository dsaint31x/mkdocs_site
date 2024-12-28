---
title: Library, Shared Library, Dynamic Linking
tags: [linker, elf, object file, runtime library, entry point, shared library, library, static linker]
---

# Library, Shared Library, Dynamic Linking.

## **0. Library**

다음을 참고하라:

[Library vs. Framework](https://dsaint31.tistory.com/452)

---

---


## **1. Linker**

Executable 코드를 만들기 위해,  

* 해당 프로그램이 요구하는 다양한 `Library`  및  컴파일러가 생성한 개별 object 파일들을 
* 프로그램의 해당 symbols 와 연결시켜 결합시킴.
* 이 과정에서 Linker는 다음의 작업을 수행.
    * 심볼 결합(Symbol Resolution): 함수, 변수 등 심볼의 주소를 확인하고 참조를 결합.
    * 주소 재배치(Relocation): 모듈 간 호출이나 데이터 참조를 위해 각 코드와 데이터의 메모리 주소를 수정.
    * 라이브러리 병합: 필요한 외부 라이브러리(.lib, .so 등)를 결합.
* 프로그램이 실행코드가 되기 위해 필요한 모든 의존성 관계의 여러 조각(object files)들을 연결시킴.

다음 url 참고: [Compiler 언어가 실행파일 만드는 과정](../ch08/ce08_compiler_interpreter.md#compiler-language)

---

### 1-1. Executable and Linkable Format (ELF)

**ELF (Executable and Linkable Format)** 는 다음의 binary file 의 포맷을 의미함:

* Object 파일, 
* Executable 파일, 
* Dynamic Library (or Shared Library) 등 

즉, `linker`가 작업하는 **입력(오브젝트 파일)** 과 **출력(실행 파일)** 모두 ELF 형식으로 저장됨.

> 이는 엄밀하게 말하면 Linux에서의 이야기이며,  
> Windows에서는 Portable Executable (PE) 포맷을 사용하고,  
> macOS에서는 Mach-Object(Mach-O) 를 사용. 

---

### 1-2. Object File (ELF의 일종)

Object file은 Linker의 입력 파일로, Compiler 가 source code 를 번역한 중간 결과물(intermediate file).

다음 세 가지 유형으로 나누어짐:

* Relocatable File:
    * 다른 파일과 결합하기 위해 작성된 파일. (예: `.o`, `.obj`)
    * 심볼 주소가 고정되지 않고 resolve 및 relocation 필요.
* Executable File:
    * 실행 가능한 형태로 완전히 링크된 파일. (예: `.out`, `a.out`)
    * Linker 가 Relocatable File과 Library 를 결합하여 생성.
    * Machine code file 이라고도 불림.
* Shared Object File:
    * run-time 에 로드 가능한 동적 라이브러리. (예: `.so`, `.dll`)

참고: [object code 관련 자료](../ch08/ce08_compiler_interpreter.md#byte-code-바이트코드)

---

---

## **2. Runtime Library**

OS와 Program Language에 맞춰 하드웨어 독립적 실행 환경을 사용자 프로그램에게 제공하는 Library.

주로 다음의 기능을 제공

* 메모리 할당 및 설정
* stack 과 heap 구성.
* static data 의 초기값 설정: OS로부터 메모리 할당받고, executable에서 static data복사.

> 개발자가 프로그램을 만들 때, entry point로 `main()` 함수 등을 구현하나  
> Runtime Library가 항상 이보다 먼저 실행되어 프로그램이 실행될 수 있는 환경을 설정함.
> 내부적으로는 `_start` 등이 진짜 entry point이며 런타임 초기화 이후 `main()` 등이 호출됨.  
> 대표적으로 실행될 프로그램의 프로세스를 위한 메모리 할당 등이 수행됨.

### 2-1. Example

* Windows : `MSVCRT (Microsoft Visual C Runtime Library)`
    *  `msvcrt.dll`, `ucrtbase.dll`
* Linux: `glibc` 등
    * `libc.so.6` 
* macOS: `libSystem`
    * `libSystem.dylib` 

> Python의 경우 자체 런타임 환경을 제공:
>
> `libpython3.9.so`, `python38.dll`, `libpython3.9.dylib` 등.

대부분의 현대 시스템(특히 Linux, Windows, macOS)은 런타임 라이브러리를 공유 라이브러리로 제공하며, 런타임 중에 필요하면 로드되는 것이 일반적이나 개발자가 원할 경우 정적으로 실행파일에 포함 가능함.

## **3. Shared Library**

- Shard Library (공유 라이브러리)는 여러 프로그램이 공통으로 사용할 수 있는 라이브러리 파일.
- 보통 `.so` (Linux) 또는 `.dll` (Windows) 파일 형태로 제공.
- 같은 라이브러리를 여러 프로그램에서 동시에 사용할 수 있음: `Dynamic Linking` 을 통해

예: `libc.so`, `libm.so` 등.

---

---

## **4. Dynamic Linking** 

- 프로그램 실행 시점에서 Shared Library 를 메모리에 로드하고 연결하는 과정.
- `Static Linking`
    - 컴파일 시점에 라이브러리를 프로그램에 포함시킴
    - Shared Library도 Static Linking으로 포함 가능하나 이 경우 다른 프로그램과 공유 불가. 
- `Dynamic Linking` 
    - 실행 중에 필요할 때만 해당 라이브러리를 로드해.
    - Shared Library를 Dynamic Linking을 통해 여러 프로그램이 하나의 Shared Library를 공유.
    - 동적 링크를 통해 프로그램 크기를 줄일 수 있음.
    - 이는 라이브러리 업데이트 시 프로그램을 다시 컴파일할 필요가 없다는 장점도 제공.

Dynamic Loader (ld.so 등)가 Shared Library 를 찾아 적절히 메모리에 맵핑(mapping)하고, 필요한 기호(symbol)들을 연결시킴.

프로그램은 런타임 동안만 라이브러리에 의존하며, 라이브러리의 코드는 프로그램과 독립적으로 존재.

Dynamic Linking에서 Shared Library 코드가 메모리에 로드되면, 해당 영역은 Shared Memory 등을 통해 여러 프로세스에서 재사용.

---

### **4-1. 정리하면:**

- **Shared Library**
    - Dynamic Linking 이 가능하도록 설계된 파일(즉, 라이브러리).
- **Dynamic Linking** 
    - 실행 시점에 이러한 공유 라이브러리를 사용하는 메커니즘.

