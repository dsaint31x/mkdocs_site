# Command Line Interface

키보드를 이용하여 terminal을 통해 computer와 대화하는 방식. 키보드로 command(명령)을 typing하여 입력하고, computer도 terminal 등에 문자를 출력하여 응답하는 방식임. (실제로 컴퓨터 초기에는 typewriter처럼 컴퓨터가 종이에 출력을 해줌.)

## Terminal

컴퓨터 초창기에는 HW로 컴퓨터에 연결된 I/O 장치였으나, 현재는 S/W로 사용자에게 CLI를 제공한다. 사용자의 명령을 기다리는 command prompt를 보여주고 사용자가 명령을 입력하면 그 결과를 문자로 출력하여 반응함.
Terminal은 키보드나 모니터의 장치 드라이버로부터 입력과 출력에 대한 처리를 위해 도움을 받아야 하고, 이는 OS를 통해 이루어짐. 즉, CLI를 채택한 user application들은 Terminal을 통해 입출력이 이루어지고 있으나 실제로는 중간에서 OS를 통하고 있음. 

Termianl : OS (including device drivers) : User Application (system call 사용)

## Terminal, Driver, and CLI based User Application.

현대의 OS는 대부분 Time Dividing Technique을 이용하여 마치 여러 Program이 동시에 실행되는 것처럼 보인다. 하지만, 실제로는 하나의 core당 하나의 program이 동작하는 것으로 실제 동작하는 program의 명령어들이 core의 regiser들에 저장되어 있다. 한 core에서 동작하는 단위를 process라고 부르며 이 process가 core에서  재실행되기 위해 필요한 데이터들을 process context라고 부름. 하나의 core에서 여러 process가 시분할(Time Dividing)으로 실행되는 경우, 실행되던 process의 context가 저장이되고 실행될 process의 context가 register등에 load되어야 하며, 이런 과정을 context switching이라고 부름.

CLI 를 사용하는 User application이 단일 process로 동작한다고 가정할 때, 이 역시 하나의 core에서 수행되기 위해서는 자신의 context가 cpu에 load되어야 한다. 사용자의 키보드로부터의 입력을 대기하는 순간에 core를 점거하고 있는 건 비효율적이므로 OS가 입출력을 대기하는 process들은 보통 context switching을 시켜서 sleep상태로 두는 경우가 일반적이다. 즉, User appliation이 입력을 받기 위해 OS에게 system call을 하는 순간, OS는 사용자가 키보드로부터 입력을 완료하기 전까지 해당 process를 sleep시킨다. (해당 system call이 buffered input을 지원하면서 요구한 경우이고, 사용자가 키보드를 누를 때마다 처리가 이루어지도록 지정도 가능하긴 함.)

사용자가 키보드로 입력할 때, 입력할 내용을 쓰는 동안에는 OS나 User application은 신경을 쓰지않으며 키보드의 driver가 자신의 buffer에 해당 내용을 쌓아두고 있을 뿐이다. (OS는 해당 User applicatoin을 sleep시키고, 다른 process를 수행중임) 이후 사용자가 Enter를 누르는 순간, 키보드로부터 OS는 버퍼에 쌓인 입력 내용을 읽어들여 해당 appliation을 깨워서 전달해 주며(interrupt이용), user appliation은 입력 내용을 처리를 core에서 수행한다.  

사실 context switching은 application이 무거울수록 부하가 많이 걸리는 작업이며, 이를 효과적으로 OS는 수행하기 위해 다양한 알고리즘을 사용한다. 

terminal은 단순히 computer가 사용자에게 보내는 텍스트만을 출력하지 않으며, 사용자가 키보드로 입력하고 있는 글자 하나 하나를 echo처리(화면에 그대로 출력해줌)한다. 

## Handle, File Pointer, and Standard I/O and Stream

Terminal과 User application의 통신, CLI는 키보드와 모니터의 드라이버와 OS, Terminal이 함께 하는 작업이며, 이들 사이에서 입출력을 원활하게 하기 위해 input buffer와 output buffer가 각 장치 드라이버 뿐 아니라 User application이 사용하는 system call 라이브러리에도 존재한다. 일반적으로 버퍼는 FIFO (First in First out)인 Queue 데이터 구조를 취함(물리적으로는 register와 memory이지만, SW적으로는 Queue임: 좀더 엄밀하게는 circular queue.) 

Standard I/O는 다양한 User application들이 CLI를 쉽게 구현할 수 있도록표준화된 라이브러리이며 C 언어에서 `stdio`임. 입출력은 terminal 이외에도 file에서도 이루어지는 경우가 많다. 

User application의 관점에서 장치 드라이버(file의 경우 storage 관련 드라이버)와 같은 OS가 관리하는 resource들에 접근하기 위한 수단은 system call이며 이들 system call을 통해 얻는 handle 또는 해당 리소스에 대한 descriptor (특히 file descriptor)등을 이용하여 user application은 리소스를 제어한다(정확히는 제어 요청을 OS에게 하는 것). 프로그래밍에서 handle을 얻어서 처리한 이후에는 다시 OS에 반환을 명시적으로 해줘야 하는게 일반적임. linux의 경우, 많은 device resource를 file로 추상화하여 마치 file을 이용하는 것처럼 serial port등을 사용한다.

즉, file에 입출력하는 것처럼 특정 resource에 입출력하게 되며, 많은 프로그밍 언어에서 stream을 다루는 부분이 이를 처리하는 방법을 설명한다.

linux에서는 User application에서 terminal과 데이터를 주고받기 위해 2개의 file handle을 열게 된다 (1개는 input으로 1개는 output으로). C언어의 경우 이 두 file handle에 대한 file pointer를 이용하는데 표준 입출력을 위해 제공하는  `stdio`에서 `stdin`과 `stdout`을 사용하여 terminal과 입출력을 수행하게 된다. 사실 `stderr`로 표준 에러를 출력하는 file pointer가 하나 더 있으며, User application에서 에러 관련 출력을 하는 경우에는 `stderr`를 사용한다. (차이는 `stderr`에서 user application이 제공하는 buffer가 없다는 점으로 user application이 sleep 등으로 중간에 서 있는 경우 `stdout`은 출력이 되지 않으나 `stderr`는 출력가능함) 


# Graphic User Interface

icon등이 그려진 button등을 통해 computer에게 지시를 내리는 방식. computer 전문가 들보다는 다른 업무를 위해 computer를 사용하는 이들에게 익숙한 방식. 자동화등의 측면에서는 효율이 떨어진다.
