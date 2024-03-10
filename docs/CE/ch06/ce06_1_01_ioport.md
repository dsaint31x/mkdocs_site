# I/O Port

***I/O interface*** 라고도 불리며, 

* CPU 나 Processor에서는 외부 회로 등과 입출력(I/O)을 하기 위한 pin (or channel)으로 생각하면 된다. 
* 해당 pin의 전송 속도(bps)나 전송 레벨(voltage) 등등의 H/W적 specification을 지켜야 한다. (최악의 경우 소자가 망가질 수 있음).

일반적으로 processor에서 제공되는 pin들에 

* I/O device들이 연결되어 I/O가 이루어지며, 
* 해당 입출력을 위해 ***특정 register가 할당*** 된다. 
* 각 Port (or Pin) 에 대응하는 register에 해당 port의 ***pin 마다 1bit*** 가 할당된다. 
  * 즉, 8개의 pin으로 구성된 port의 경우 8bit의 register가 할당되고, 
  * 이 register의 값을 읽어들이거나 특정 값을 쓰는 방식으로 해당 pin들로부터 I/O가 수행된다.

> 저수준 언어(어셈블리)를 사용하는 경우, 보통 I/O 관련 register들의 주소(address)를 알고 있어야 했지만, 최근에 `C`를 이용하여 predefined된 변수 및 함수를 활용하여 읽고 쓰는 동작이 이루어진다.  
> 그래도 각 register의 이름과 대응되는 port를 익히는 것이 해당 microprocessor system에 대한 공부에서 매우 큰 부분을 차지한다 (외워야 하는 부분이기도 하고...)

---

I/O을 둘 다 수행하는 pin들에는 

* 보통 pin의 값이 저장되는 ***input register*** 와 
* pin의 출력값을 지정할 수 있는 ***output register*** , 
* 그리고 해당 pin을 입력으로 사용할지 출력으로 사용할지를 결정하는 ***pin mode register***

와 같이 3개의 대응되는 register가 지원되는 경우가 일반적이다.

예를 들어, 8-bit port B가 있다고 가정하면, 많이 사용되는 naming은 다음과 같다.

* `DDRB` : `Data Direction Register B` (= pin mode register or data direction register), ***pin mode를 결정*** 한다. `0`이면 입력, `1`이면 출력 을 의미하는 방식으로 port의 pin 이 입력으로 사용될지 출력으로 사용될지를 사용하기 전 설정해야 한다.
* `PORTB` : `output register`. latch, flip-flop으로 구성된 register로 pin에 출력할 값들을 가짐. 사용자는 이 register에 값을 기재함으로서 출력을 시킨다.
* `PINB` : `input register`. `PORTB`와 방향이 다른 입력용 register이다. pin의 값들을 읽어서 보관하고 있음. 

---

`C`언어로 접근할 경우, 

* 초보적 프로그래밍에서는 pin 하나 하나를 제어하는 함수들을 공부하는데, 
* 이보다는 register 전체를 읽어들여 ***bit operator*** 로 처리하는 방법이 보다 빠른 처리가 가능하다. 

때문에 C 프로그래밍의 경우 bitwise operator 등의 처리를 가장 많이 하는 분야가 embedding system programming임.  
해당 분야에 관심이 있다면, bitwise operators 와 hexadecimal 표현 등의 기초를 다지길 권한다.  
고성능 컴퓨터, cloud등의 플랫폼에서 개발하는 경우, bitwise operators 는 상대적으로 그리 많이 다루지는 않는 편이다 (가독성이 더 중요...).

> 하지만 어느 분야나 ***flag 처리*** 등에서 bitwise operation을 쓰므로 기본적인 내용은 알아야 한다.