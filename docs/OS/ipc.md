# Inter-Process Communication (IPC)

Process 는 서로 독립된 자원을 가지고 있으며 서로의 연산 수행이 영향을 끼치지 못함.

여러 Processes가 같이 resources를 공유하고 Data를 주고 받아 작업을 수행하려면, 
Process간에 통신이 필요함.

크게 다음의 방식으로 수행됨.

## Signal 이용.

Signal 은 ***Kernel을 통해 비동기적인 event를 처리하기 위한 방법*** 이나,  
**Process 간 통신에도 제한적으로 사용이 가능함.**

> Signal 은 Kernel을 경유하여  
> 특정 Process에서 다른 Process로 보내질 수 있음.

특정 Process에서 특정 Signal을 받을 경우,

현재 실행되고 있는 Process가 Signal을 받을 경우, 

1. Interrupt가 발생한 것처럼 현재의 실행을 멈추고, 
2. 해당 Signal을 처리하는 Signal Handler가 실행되며, 
3. 해당 Signal Handler가 종료하면 다시 이전의 실행을 재개하게 됨.

이를 이용하여, 

* 특정 Signal을 받을 경우 수행되는 Signal Handler를 
* 재정의해두고, 해당 Process에 해당 Signal을 보내는 방식으로 
* ***IPC를 제한적으로 구현*** 하게 됨.

Linux의 경우, System Call인 `sigaction` 과 `signal`을 통해  
특정 Signal에 대한 처리를 구현할 수 있음.

* 특정 Signal의 기본동작을 변경: `sigaction`
* 특정 Signal에 Signal Handler를 등록: `signal`

Python을 이용하여 Signal Handler를 등록하는 예제는 다음과 같음.

```Python linenums="1"
import signal
import os
import time

# 시그널 핸들러 함수 정의
def handle_signal(signum, frame):
    print(f"Received signal: {signum} in process {os.getpid()}")

# 시그널 핸들러 등록
signal.signal(signal.SIGINT, handle_signal)  # Ctrl+C (SIGINT) 처리
signal.signal(signal.SIGTERM, handle_signal) # 종료 요청 시 처리

print(f"Process ID: {os.getpid()}")
print("Waiting for signals... Press Ctrl+C to send SIGINT")

try:
    while True:
        time.sleep(1)  # 무한 대기
except KeyboardInterrupt:
    print("Exiting program.")
```

* 다른 터미널에서 `kill -SIGTERM <target_process_id>`를 수행해보거나,
* 위 프로그램이 실행 중인 Terminal 에서 `CTRL+c`로 interrupt를 발생시켜보면 
* 구현한 Signal Handler의 동작을 확인할 수 있음.
* 종료시키려면 `kill -9 <target_process_id>`를 수행.

참고: [Signal 요약](https://ds31x.tistory.com/132)

---

---

## Shared Memory (공유메모리)

OS 가 MMU (Memory Management Units)를 지원할 경우, 
다수의 Process의 page table 에서  
물리적으로 같은 RAM의 영역을 매핑할 경우,  
해당 영역을 복수의 해당 Processes가 접근함으로서  
효율적인 IPC가 가능해짐.

> 다른 이름으로 Shared Memory는 Shared Page라고도 불림.

Process 입장에서는 자신에게 할당된 Memory 영역을 읽고 쓰는 것과   
같은 방식으로 다른 Process와 커뮤니케이션을 하는 것이기 때문에   
매우 효율적인 커뮤니케이션이 됨: 가장 빠른 IPC 방법임.

* Kernel의 개입이 Signal을 이용하는 방식 등에 비해 거의 없음.
* 직접적으로 메시지를 주고 받는 방식인 socket등을 이용하는 방삭보다 속도가 빠름.
* race condition 으로 인해 data consistency 에 문제가 있을 수 있음.

이를 위해서 사용되는 세부 방식은 크게 다음과 같음.

1. 프로세스가 공유할 메모리 영역을 확보하는 system call을 사용.
2. 메모리 대신에 file 등의 공유 자원을 이용하는 방식도 넓게 보면 공유메모리라고 볼 수 있음.

Python 등에서는 `multiprocessing` 모듈의 `shared_memory` 서브 모듈을 활용하여  
프로세스 간에 메모리를 직접 공유할 수 있음.

```Python linenums="1"
from multiprocessing import shared_memory, Process
import numpy as np

# 공유 메모리에서 데이터를 생성하는 함수
def worker(name):
    # 이미 생성된 공유 메모리에 연결
    existing_shm = shared_memory.SharedMemory(name=name)
    # 공유 메모리를 numpy 배열로 변환
    shared_array = np.ndarray((10,), dtype=np.int32, buffer=existing_shm.buf)
    
    # 데이터 수정
    shared_array[0] += 1
    print(f"Worker updated array: {shared_array}")
    
    # 연결 해제
    existing_shm.close()

if __name__ == "__main__":
    # 공유 메모리 생성
    shm = shared_memory.SharedMemory(create=True, size=10 * 4)  # 10개 int32 크기
    array = np.ndarray((10,), dtype=np.int32, buffer=shm.buf)
    array[:] = np.arange(10)  # 초기 데이터 설정
    print(f"Initial array: {array}")
    
    # 프로세스 시작
    p = Process(target=worker, args=(shm.name,))
    p.start()
    p.join()
    
    # 메인 프로세스에서 수정 확인
    print(f"Array after worker: {array}")
    
    # 공유 메모리 닫기 및 해제
    shm.close()
    shm.unlink()
```

참고: [Memory Management Units](https://dsaint31.me/mkdocs_site/CE/ch05/ch05_06_01_mmu/)

---

---

## Message Passing (메시지 전달)

IPC를 위한 방법 중 하나로, Processes가 서로 message를 주고 받아서 커뮤니케이션을 수행.

가장 직접적인 의미에서의 IPC로서 다음의 특징을 가짐.

* Kernel에 의해 주도되기 때문에 Signal 의 경우 처럼 data consistency에 문제가 없음: Kernel의 영향이 적은 Shared Memory와 차이점.
* 주고 받는 데이터가 Kernel을 통해 전달되기 때문에 Shared Memory보다 속도가 느림.

이를 위해서 사용되는 세부 방식은 다음과 같음.

* socket 이용: 네트워크 통신의 socket을 사용하므로 remote host의 process와도 통신이 가능.  
    * 기본적으로 양방향.
    * 가장 복잡한 형태의 abstraction이 지원이 되어야 함.
    * data serialization 에 기반하며, 다중 client 가 제공됨.
    * 확장성이 가장 높은 편이나 다른 방식보다 속도가 느림.
* Remote Procedure Call (RPC): 
    * 원격지의 코드를 호출하는 기술로 대규모 트래픽이 요구되는 서버간 통신환경에서 많이 사용됨.
    * Google의 `gRPC` 등의 프레임워크를 이용
* Pipe 사용: 
    * 일반적으로 단방향이고 부모/자식 프로세스에서만 사용가능 (이는 `unnamed pipe`인 경우)
    * `named pipe`는 양방향이고 임의의 프로세스 간에 사용가능

개인적으로 Pipe가 가장 쉽게 사용가능한 방법이라고 생각되나,  
같은 host에서만 가능하고 보통 한 프로세스의 출력을 다른 프로세스의 입력으로 사용할 때 이용되는 것이라  
확장성이 적음.

Python으로 socket을 이용한 예제는 다음과 같음:

```Python linenums="1"
import socket

def server_program():
    host = '127.0.0.1'  # 로컬호스트
    port = 9000         # 포트 번호

    # 소켓 생성
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))  # 서버 주소와 포트 바인딩
    server_socket.listen(1)           # 하나의 클라이언트 연결 대기

    print("Server is waiting for a connection...")
    conn, address = server_socket.accept()  # 클라이언트 연결 수락
    print(f"Connection from {address} has been established.")

    while True:
        data = conn.recv(1024).decode()  # 클라이언트로부터 데이터 수신
        if not data:
            break
        print(f"Received from client: {data}")
        conn.send("Acknowledged".encode())  # 클라이언트로 응답 송신

    conn.close()  # 연결 종료
    
    
def client_program():
    host = '127.0.0.1'  # 서버 주소 (로컬호스트)
    port = 9000         # 서버 포트 번호

    # 소켓 생성
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))  # 서버에 연결

    message = input("Enter message to send: ")

    while message.lower().strip() != 'exit':
        client_socket.send(message.encode())  # 메시지 송신
        data = client_socket.recv(1024).decode()  # 서버로부터 응답 수신
        print(f"Server response: {data}")

        message = input("Enter message to send: ")

    client_socket.close()  # 연결 종료

import sys    
if __name__ == '__main__':
    if sys.argv[1].lower() == 's':
        server_program()
    else:
        client_program()
```