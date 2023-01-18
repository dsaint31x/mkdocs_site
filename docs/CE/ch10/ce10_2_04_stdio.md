# Standard I/O Library

## Standard I/O Library란?

다양한 OS에서 Input/Output(입출력)을 수행할 수 있도록 구현된 라이브러리.

- 프로그래머는 프로그래밍 과정에서 **직접 입출력을 수행하는 코드를 작성하지 않는다.**
- 보통 **입출력을 수행하는 Standard I/O 라이브러리의 함수들을 호출** 하여 입출력을 수행함.
- link 단계에서 코드에서 사용된 이들 라이브러리 함수들이 연결되거나(static link), runtime에 shared library로 있는 이들 라이브러리 함수들을 실행(Dynamic link)하는 방식을 취함.

* [Library에 대한 정의](https://dsaint31.tistory.com/entry/Programming-Library-vs-Framework)

## Low Level I/O : System Call

모든 I/O 처리에서는 `File Descriptor`가 필요하다 (즉, `system call`로 이루어진다는 애기임). UNIX의 경우, 모든 입출력 디바이스(소켓 포함)을 file처럼 abstraction (추상화, 또는 가상화라고도 함)시켜 ^^file과 같은 방식으로 처리^^ 하므로 해당 디바이스에 해당하는 File Descriptor (해당 resource에 대한 handler)를 open시켜 해당 디바이스를 사용하고 사용에 관련된 처리가 끝난 후 close시켜 OS에게 해당 자원을 돌려주는 방식으로 프로그래밍이 이루어지게 된다.

- 이는 결국 `system call`을 이용하는 방식으로 `open`, `write`, `read`, `close` 등은 Kernel이 제공하는 system call임.
- 이를 ***저수준 입출력*** 이라 부르며 ^^byte 단위의 입출력^^ 을 수행한다.

## High Level I/O : Standrad I/O Library

Standard I/O Library에서 제공하는 function들은 **고수준 입출력**으로 버퍼를 이용하여 한번에 file에서 읽어들이거나 쓸 수 있으며, 저수준의 system call함수들이 쓰는 file descriptor가 아닌 ***file 구조체에 대한 pointer***를 제공(C의 경우)한다.  

> 해당 구조체들(`handle`이라고 불림)은 저수준의 file descriptor 외에도 버퍼의 크기 등에 대한 정보도 가지고 있다. 


일반적인 프로그래밍 언어에서 각자의 문법으로 제공하는 입출력함수들은 대부분 고수준의 입출력함수 (user level buffering를 제공)로 생각해도 된다. 물론 이들도 결국에는 저수준 입출력함수 (kernel이 제공하는 입출력함수)를 사용한다.

- 높은 수준의 system programming을 하지 않은 터라… 이 둘의 차이점을 정말 살려서 개발해본 적은 없었던 거 같다.
    - library를 이용하는 경우를 library call이라고도 부르기도 하며, API (Application Programming Interface)라고 지칭하기도 함.
    - 일반적으로 library의 buffering은 system call 횟수를 지나치게 빈번하게 하지 않기 위한 용도로 제공된다.
    - 엄밀하게 애기하면 kernel도 내부적으로는 kernel buffering이 된다. 명쾌한 설명의 특징은 뭐든지 깊이 들어가면 틀렸다 (정확히는 약간의 차이가 있다).
- AI관련 모델 개발이나 영상처리 등의 수준에선 그냥 그런 게 있다 정도만 알고 있어도 큰 문제는 없을 듯…
- 당연히 저수준 입출력이 고수준 입출력보다 빠르다(내부적으로 편의 기능이 없으니…). 하지만 리소스가 어찌 보면 넘쳐나는 환경에 있는 AI개발자들에게는 그리 와닿지 않는 장점일 수도 있다.

## 표준입출력: `stdin`,`stdotu`, and `stderr`

모든 user application (혹은 사용자 프로그램)들은 입출력이 필요한데, 특별히 입력과 출력을 위의 file descriptor (C언어에선 file pointer로 생각하면 편함)등으로 지정하지 않은 경우에는 모니터가 표준출력(`stdout`)으로 지정되고 키보드가 표준입력(`stdin`)으로 지정됨.

> Python의 경우, `sys` 모듈의 `stdin` 과 `stdout`으로 지정되어 있고, C의 경우엔 `stdio` 라이브러리의 `stdin` 과 `stdout` 으로 접근가능함.
> 

하나 더 있는 게, 표준에러인 `stderr` 임. 이는 프로그램에서의 에러 출력을 담당하며, `stdout`과 마찬가지로 모니터로 지정되어 있다. 차이는 내부에서 buffer를 사용하느냐 인데 `stderr`는 버퍼를 사용하지 않는다.

표준 입출력은 워낙 많이 사용하므로 이를 open하고 close하는 것이 프로그래밍에서 명시적으로 하는 경우는 거의 없다고 봐도 된다. 실제로 버퍼를 flush하는 정도까지 필요한 경우는 있지만…

때문에 실제로 open으로 해당 리소스를 얻어오고 close로 닫는 과정은 file 입출력을 통해 접하는게 일반적이다. Python에서 간단한 text를 파일로 저장하는 과정에서 이를 확인할 수 있다.

```python
fd = open("test.txt", "w") # fd는 파일핸들러임.
fd.write("txt for test!\n")
fd.close()
```

open과 close가 항상 짝을 이루어져 수행되어야하는데, 생각보다 귀찮고 자주 잊어버리기 때문에, Python의 경우 `with`구문을 통한 처리가 일반적이다. (`with` 블록에서 제어가 나가는 순간 자동으로 file이 close됨)

```python
with open("test.txt","w") as fd:
  fd.write("txt for test!\n")
```

## Stream (or IO Stream)

`stream`은 흐름을 애기하며, ^^입출력을 일종의 bit들의 흐름 (bit stream, byte stream, byte flow)으로 생각^^ 할 수 있기 때문에 프로그래밍에서 ***I/O 가 이루어지는 대상 (or 매체, 장치, 파일, socket 등)을 가르키는데 사용되는 용어*** 임. 

즉, standard stream이라고 하면, 입력은 키보드이고 출력은 모니터가 될 것이다.

I/O와 함께 자주 나오는 용어이니 잊지 않는게 좋다. 실제로 Python의 `sys.stdin`을 표준 입력 스트림이라고 지칭한다.

Python에서 `sys.stdin`의 활용은 다음 코드를 보면 쉽게 이해가 될 거 같아 첨부한다.

```python
import sys
data = []
n = int(sys.stdin.readline())
for i in range(n):
    data.append(list(map(int,sys.stdin.readline().split())))
```

첫번째 라인에 행의 수를 입력받고, 이후 공백문자로 구분된 integer들을 가지는 행을 입력해주면 2차원의 list가 만들어진다.
