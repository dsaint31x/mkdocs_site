# I/O Stream 과  Standard I/O Library

## 1. Stream 이란?

**스트림(stream)** 이라는 개념은 데이터의 흐름을 의미하며, 이를 bit(비트) 또는 byte(바이트)의 연속으로 생각할 수 있음.

* 종종 bit stream 또는 byte stream 이라고도 불림.

***Programming*** 에서 Stream은 

* 입출력(I/O) 대상(장치, 파일, 소켓 등)으로 데이터를 주고받는 과정을 나타내는 용어. 
  
Stream 은 I/O 작업에서 데이터가 어떻게 흐르는지를 이해하는 데 중요한 역할을 하며, 
다양한 프로그래밍 언어에서 흔히 사용되는 개념임.

* [stream에 대한 다른 글](https://ds31x.tistory.com/341)

예를 들면, standard stream 으로 입력은 키보드, 출력은 모니터 장치에 데이터를 전달됨.

<figure markdown>
![standard stream](./img/standard_stream.png){width="400"}
<figcaption>standard stream from wikipedia (default configuration)</figcaption>
</figure markdown>  

> pipe 또는 redirection 등을 통해 키보드나 모니터가 아닌 다른 process의 stdin과 stdout으로 연결지어질 수도 있음.

Python에서 이는 `sys` 모듈의 `stdin`과 `stdout`으로 추상화되어 있음.

다음 code snippet은 키보드로부터 입력을 `sys.stdin`으로부터 읽어내어 stream으로 처리하는 것을 보여줌:

```python
import sys
data = []
n = int(sys.stdin.readline()) # 1줄을 읽어들여서 이후 입력받을 row수를 설정.
for i in range(n):
    data.append(list(map(int,sys.stdin.readline().split())))
```

* 첫번째 라인에 행의 수를 keyboard로부터 입력받아 변수 `n`에 할당하고, 
* 이후 공백문자로 구분된 integer들을 가지는 여러 행들을 앞서 입력한 숫자 `n` 만큼 입력해주면 
* 최종적으로 2차원의 list인 `data` 가 만들어진다.

> Python의 경우 일반적으로 보다 high level I/O인 `input`함수를 이용하지만,  
> 위의 예에서는 low level I/O 인 file descriptor의 wrapper인 `sys.stdin` 을  
> 이용한 stream 처리를 사용함.

---

---

## 2. Standard I/O Library란?

다양한 OS에서 일관되게 Input/Output(입출력)을 수행할 수 있도록 구현된 High Level I/O 라이브러리.

이 라이브러리는 프로그래머가 하드웨어와 직접 상호작용할 필요 없이 I/O 작업을 수행할 수 있도록 여러 함수를 제공함.  
이러한 라이브러리 함수들은 ***여러 장치와 상호작용하는 복잡성을 추상화*** 하여 I/O 작업을 더 효율적이고 쉽게 구현할 수 있도록 해 줌.

- 프로그래머는 프로그래밍 과정에서 **직접 입출력을 수행하는 코드를 작성하지 않는다.**
- 보통 **입출력을 수행하는 Standard I/O 라이브러리의 함수들을 호출** 하여 입출력을 수행함.
    - link 단계에서 코드에서 사용된 이들 라이브러리 함수들이 연결되거나(static link), 
    - runtime에 shared library로 있는 이들 라이브러리 함수들을 이용(Dynamic link)하는 방식을 취함.

* [Library에 대한 정의](https://dsaint31.tistory.com/entry/Programming-Library-vs-Framework)

> Standard I/O Library는 High Level I/O 로써,  
> 내부적으로는 OS의 Kernel에서 제공하는 Low Level I/O 를 사용함.

---

---

## 3. Low Level I/O: System Call

**Low Level I/O** 는 file descriptor(파일 디스크립터)를 직접 사용하여 입력과 출력을 관리하는 **system call** 을 의미함.

UNIX와 같은 시스템에서는 모든 I/O 장치(소켓 포함)가 file로 추상화되어, 다양한 유형의 I/O를 일관되게 처리할 수 있음.

각 I/O 장치는 

* file descriptor (resource를 식별하는 고유한 identifier)를 얻기 위해 열리고( **open** ),
* 이 file descriptor 를 통해 장치를 사용하며,
* 작업이 끝난 후에는 **닫기(close)** 를 통해 OS에 해당 리소스를 반환.

> 여기서 `resource` 는 OS가 관리하는 file(파일), memory(메모리), network connection(네트워크 연결) 등과 같은 **시스템 자원** 을 의미합니다.

일반적으로 사용되는 `system call`에는 `open`, `write`, `read`, `close` 등이 있음.

* 이들은 Kernel 에 의해 직접 관리되는 system call임.
- 이를 사용하는 I/O 방식을 ***Low Level I/O (저수준 입출력)*** 이라 부름.
- **byte 단위** 로 동작하며, 
- 높은 수준의 제어를 제공하지만, 
- 이는 모든 세부 사항을 프로그래머가 직접 관리해야 함.

> 높은 제어 수준을 제공하는 경우,  
> 프로그래머가 구현 및 관리해야하는 내용이 많아지는 단점이 존재함.

---

---

## 4. High Level I/O: Standard I/O Library

고레벨 I/O인 **Standard I/O Library** 에서 제공하는 functions는 다음의 특징을 가짐:

* **High Level I/O (고수준 입출력)** 을 제공함. 
* buffered I/O 를 사용하여 한번에 file에서 읽어들이거나 쓸 수 있음. 
* 저수준의 system call 함수로 file을 한번에 읽거나 쓸 수 있도록 buffer를 사용하여 효율성이 향상됨.
    * System Call 함수를 통한 Low Level I/O는 실행될 때마다 매번 Kernel mode로 전환되어야 하므로 비용이 큼.
    * Standard I/O Library는 내부적으로 버퍼를 사용하여 여러 작은 크기의 I/O 요청을 모아서 한번의 System Call 함수로 처리할 수 있음.
    * 내부적으로 최적의 Block Size로 I/O를 수행하도록 최적화되어 있음.
* file descriptor 를 직접 다루는 대신, 이를 내부적으로 사용하는 고수준의 파일 객체 (or 이에 대한 포인터: C의 경우 `FILE*`)를 사용함.
    * OS 마다 System Call의 구현이 다를 수도 있지만, 
    * Standard I/O Library는 모든 Platform에서 동일하게 동작하는 functions를 제공.  

> 해당 고수준의 객체(`handle`이라고 불림)들은  
> 
> * 저수준의 file descriptor 을 내부에 가지고 있는 일종의 Wrapper로서 
> * I/O를 위한 버퍼의 크기 등과 같은 추가 정보를 가짐. 
>
> 작은 크기의 데이터를 자주 읽거나 쓰는 경우에 High Level I/O가 효율적임.

예로 C언어를 들면, `fread()`, `fwrite()`, `fprintf()`, `fscanf` 같은 Standard I/O Library의 함수들은 내부적으로 `read()`, `write()` 와 같은 Low Level I/O 인 System Call 을 사용함. 

---

### 4-1. High Level I/O 와 Programming Language

대부분의 프로그래밍 언어에서  

* 각자의 문법으로 제공하는 입출력 함수들은 **대부분 고수준의 입출력함수** 로서, 
* **user level buffering** 을 추가 제공한다.    

**참고 사항**

* high level I/O도 내부적으로는 저수준 입출력함수 (kernel이 제공하는 입출력함수)를 사용함.
* high level I/O는 Library Call 또는 API (Application Programming Interface) 로 제공됨.
* 일반적으로 library call 등의 high level I/O에서는 앞서 살펴본대로buffering을 통해 system call 의 빈번한 실행을 방지하여 효율성을 높임.
    - 엄밀하게 애기하면 kernel 에서 system call 도 내부적으로는 kernel buffering 을 사용함. 

버퍼링의 관점에서 다음과 같이 구분됨.

- High Level I/O는 user level buffering 을 지원하고,
- Low Level I/O는 kernel level buffering 을 지원. 

**대부분의 개발자에게는 고수준 I/O가 더 사용하기 편리하고 효율적임.**  
Buffering은 일반적으로 High Level I/O의 특징으로 생각해도 됨(user level buffing 이 흔히 애기하는 buffering에 해당.)

> Low Level I/O가 High Level I/O 보다 속도가 빠름.
> 이는 편의 기능이 없다는 점에 대한 trade-off 라고 볼 수 있음.

### 4-2. Python에서 Standard I/O Library

Python에서 **표준 I/O 라이브러리** 는 `sys` 모듈과 `io` 모듈로 구성됨.  

* 이 모듈들은 파일과 스트림을 다루기 위한 다양한 함수와 클래스들을 제공 
* `sys` 모듈:
    * 표준 입출력(`stdin`, `stdout`, `stderr`)을 다룰 때 사용됨. 
* `io` 모듈:  
    * `io` 모듈은 파일 객체의 상위 수준 접근을 가능하게 해 줌.
    * 다양한 버퍼링 옵션을 제공하여 고수준의 I/O 처리를 가능하게 해 줌.

---

---

## 5. 표준 입력,출력,오류 스트림: `stdin`,`stdout`, and `stderr`

모든 user application (혹은 사용자 프로그램)들은 입출력이 필요한데,  
개발자가 파일 디스크립터를 명시적으로 정의하지 않은 경우, 기본적으로 다음과 같이 지정됨:

* `stdout` (표준 출력): 일반적으로 모니터.
* `stdin` (표준 입력): 일반적으로 키보드.
* `stderr` (표준 오류): 마찬가지로 모니터에 설정되지만, 버퍼링 측면에서 `stdout`과 차이가 있음. 
    * `stderr`는 버퍼링이 되지 않아 즉시 출력해야 하는 오류 메시지에 적합함.

예를 들어, 

* Python 에서는 이러한 스트림을 `sys` 모듈 (`sys.stdin`, `sys.stdout`, `sys.stderr`)을 통해 사용할 수 있고, 
* C 에서는 `stdio` 라이브러리를 사용하여 접근할 수 있습니다.


> `stdin`, `stdout`, `stderr` 는  
> OS의 관점에서는 ***file descriptor*** 에 해당하며 `int`형 숫자로 구분됨:  
> (`0:stdin`, `1:stdout`, `2:stderr`)
> 
> 하지만, Python과 같은 high level programming language에서는  
> file object (or file handle) 로 제공됨: (이는 file descriptor를 래핑하고 있는 wrapper임.)

표준 입출력 스트림은 워낙 많이 사용되기 때문에 `stdin`, `stdout` 을 명시적으로 프로그래머 직접 open하고 close하는 경우는 거의 없다고 봐도 된다 (일반적인 file에 접근하기 위해서는 open과 close를 직접 프로그래머가 호출하여 처리하는 것과 비교됨). 실제로 버퍼를 flush하는 정도까지 필요한 경우는 가끔 있긴 하다.

---

---

## 6. open and close.

일반적인 file descriptor (or file handle)을 통한 I/O(입출력)는 

* open으로 해당 file 리소스를 얻어오고, 
* 이후 입출력을 수행한 후, close로 닫는 과정을 거침. 

> 예외적인 경우는 `stdin`, `stdout`, `stderr` 와 같은 표준입출력 스트림로  
> 이들은 따로 열고 닫는 과정이 없음: User Application이 시작할 때 자동으로 open되고, 종료되면 자동으로 close 됨.

Python에서 간단한 문자열을 txt 파일로 저장하는 과정에서 이를 확인할 수 있다.

```python
fd = open("test.txt", "w") # fd는 파일핸들임.
fd.write("txt for test!\n")
fd.close()
```

open과 close가 항상 짝을 이루어져 수행되어야하는데, 생각보다 귀찮고 자주 잊어버리기 때문에, Python의 경우 `with`구문을 통한 context manager 를 이용한 처리가 권장된다.    
(`with` 블록에서 제어가 나가는 순간 자동으로 file이 close됨)

```python
with open("test.txt","w") as fd:
  fd.write("txt for test!\n")
```

보다 자세한 File Handling은 다음을 참고할 것:  

* [[Python] File Handling](https://ds31x.tistory.com/139)

---

---

# 7. 요약: Low Level I/O와 High Level I/O

**Low Level I/O:**

* System Call(시스템 호출)을 사용하며 
* 바이트 수준에서 동작하여 
* I/O에 대한 직접적인 제어를 제공 
* 더 많은 량의 코드가 필요.

**High Level I/O:** 

* 라이브러리 함수를 사용하고 
* 버퍼링된 I/O를 제공하여 
* 효율성을 유지하면서도 개발 과정을 단순화.

> 저수준 I/O는 추상화가 없기 때문에 더 빠르지만, 오늘날 대부분의 애플리케이션에서는 사용의 편리성과 리소스 관리가 더 중요함.  
> 일반적으로 Low Level I/O를 사용하여 얻어지는 속도에서의 장점은 대부분의 개발에서 그리 중요하지 않은 편임.

