# History of Computer

여기서는 컴퓨터의 발전사를 다룬다. 쉽게 따라가기 위해서 세대별로 나누어서 정리했으나....

모든 역사가 그렇듯이 칼로 딱 잘라지지도 않고, 사람마다 견해가 다르기 때문에 흐름을 따라가기 위한 일종의 도구로서 generation을 이해하자. 기억과 이해를 돕기 위해 도입한 것으로 만고불변의 진리가 아니다. 특히 현대에 가까워질수록 사람마다 의견이 다르다.

> 특히, 최초 논쟁은 의미가 없다. ==;; 많이 알려진 최초의 ~~ 은 깊게 파보면 다른 관점이 수도 없이 나온다. (하늘 아래 새 것이 없다. 모든 것이 과거의 기술과 개념들이 조합되고 개선되면서 나오는 것인지라...)

## 조상님들...

`Atanasoff Berry Computer (ABC)`
: 세계최초의 `전자식 컴퓨터`로 알려짐 (`ENIAC`은 최초의 전자디지털 컴퓨터). 1937~1942년에 아이오와 주립대의 존 빈센트 아타나소프와 클리포드 베리가 개발한 컴퓨터로 복잡한 수학계산등에 사용된 것으로 알려짐.

`Colossus`
: Alan Turing이 만든 bombe (에니그마를 해독하기 위한 전기기계식 컴퓨터?)와 그의 확률론적 방식에 영향을 받아, 1943~1945년 개발된 컴퓨터.
이미테이션 게임이라는 영화를 보면 관련 이야기들이 나옴. 
2차세계대전(1939~1945) 중 독일군의 암호전신기인 Lorenz Chiper를 해독하기 위해 개발된 세계최초의 `프로그래밍(외장형)이 가능한 전자디지털 computer`였음.  
^^군사기밀이었기 때문에 한참 후에 존재가 공개(1970년대)^^ 된 컴퓨터(Vacuum tube를 사용했고, 스위치 및 플러그를 이용한 프로그래밍을 지원) 

`(Havard) Mark I`
: 세계최초의 `전기기계식 computer`로 알려짐. 1944년 IBM사에 개발한 것으로 Automatic Sequence Control Calculator (ASCC)라고 불린 일종의 자동계산기 (Havard에 납품되어서 Havard가 붙는데, 그냥 Mark I이 이름). 
3,000개의 `Relay(전기기계식 switch)`와 4마력의 motor 72개로 구성됨. 
15.3m의 길이에 2.4m의 높이에 걸맞는 31.5톤의 무게로 알려짐(기계식의 위엄?).  
`톱니바퀴로 가감산이 가능한 계산기를 치차식 계산기`라고 부르는데, 이 것의 극한으로 간 것이 Mark I임 (motor가 필요한 이유.).  
원폭 개발 등에 사용됨. 

## 1st Generation

1951 ~ 1959 : Vacuum tube의 시대.

* 1951년 1세대의 대표적인 computer인 `UNIVAC I`이 상용화됨.
    * 1945년 (ENIAC의 등장) 부터라고 보는 이들도 많음.
* Vacuum tube 가 주 구성요소임.
    * 많은 전력소모와 발열 과 함께 잦은 고장의 원인.
* 주기억장치
    * 수은지연회로 (mercury acoustic delay lines), William 관 및 Magnetic drum 등..
* 입력이 종이테이프(paper tabpe) 및 천공카드(punched cards)
    * Vacuum tube의 열로 인해 종이테이프가 탈 정도 였다고 함.    
* millisecond 단위의 연산속도.

과학 계산, 통계처리, 미사일 탄도 계산 등에 이용되었음. SW라는 개념이 없다고 봐도 되는 세대이다. 컴퓨터가 수행할 동작을 배선을 통해 만든 회로를 교체해야하는 형태이다.

> H/W : 컴퓨터를 구성하는 물리적 기계장치.  
> S/W : H/W를 운영하고 이용하기 위한 프로그램.

### ENIAC (Electronic Numerical Integrator and Cacluator)

1946년 개발된 일반적으로 알려진 최초의 전자 디지털 컴퓨터 로 알려진 컴퓨터.

* 미사일 탄도 계산을 위한 미분방정식을 풀기 위해서...
* 100여명의 수학자들이 모여 한 달동안 계산 을 대체하기 위해.
* decimal (십진수 체계) 를 사용. 

![](./img/Classic_shot_of_the_ENIAC.jpg){width="300" align="center"}

* By Unidentified U.S. Army photographer - Image from [2], Public Domain, https://commons.wikimedia.org/w/index.php?curid=978770

18,000 여개의 진공관과 1,500 개의 relay로 구성되었고, 150kW의 전력소모 및 $24 \times 6.974 \times 0.945 m^3, 30t$의 정말 큰 컴퓨터.

* 존 모클리 : 물리학자.
* 프레스퍼 에커트 : 전기공학자.

펜실베니아 대학 (Mauchly and Eckert)에서 가동할 경우, 펜실베니아의 가로등이 희미해질 정도였다고함.

* 배선과 스위칭으로 컴퓨터를 제어. (~프로그래밍?)
* paper tape, punched card가 입력수단.

### EDVAC (Electronic Discrete Variable Automatic Computer)

1952년 von Neumann이 제안한 stored program computer (프로그램 내장형 컴퓨터) architecture를 채택하여 개발된 컴퓨터.

* ENIAC은 programm이 내장되어 있지 않음. (수동 전화 교환기 와 같은 외양. 배선 변경으로 컴퓨터 동작을 지시.)
* EDVAC은 현재 디지털 컴퓨터들이 채택하고 있는 `stored program computer` 개념과 이진법 (binary) 을 실제 구현한 컴퓨터임.
* 그 유명한 `John von Neumann`이 컨설팅을 담당.

### The von Neumann Architecture

Stored program computer의 구조로서 현대 컴퓨터들이 대부분 채택하고 있음.
다음과 같은 세 부분으로 구성됨.

![von Neumann Architecture](./img/von_Neumann_arch.png){ width="300" }

* data를 외부로부터 입력받고, 처리 결과를 외부에 표시하는 I/O Device (키보드, 모니터, 프린터 등등)
* data의 저장을 담당하는 memory (storage를 포함)
* data의 처리를 담당하는 CPU (Control Unit과 ALU등으로 구성됨.)

Neumann은 memory(기억장치)에 컴퓨터의 instruction들과 data들을 함께 저장하는 stored programm 방식을 1946년에 제안했고, EDVAC이 이를 구현했음. EDVAC 이후, 이를 기점으로 `Software`라는 개념이 등장함!

> 1949년의 `EDSAC`(윌킨스)이 최초의 stored program computer이긴 하지만, 대부분의 최초에 대한 부분은 논쟁이 많다. 가장 유명한 것이 `EDVAC`인지라...

### UNIVAC (Universal Automatic Computer)

1951년 개발된 최초의 `상업용 컴퓨터`.

![](./img/Univac_I_Census_dedication.jpg){width="300"}

* By U.S. Census Bureau employees - https://www.census.gov/history/, Public Domain, https://commons.wikimedia.org/w/index.php?curid=61118833

약 95만 달러의 고가였고, 관공서 및 대형 연구소 등에서 사용됨. 참고로 당시 대학민국 1인당 GDP는 50불 수준)

> UNIVAC이 유명해진 이유는, 1952년 대통령선거에서 개표가 5% 정도 진행된 시점에서 매우 적은 sample만으로 정확히 당선자로 아이젠하워를 예측 (CBS TV)하는데 사용되었기 때문임. 컴퓨터의 효용성을 대중에 크게 알린 사건임.

## 2nd Generation

1950년대 후반 ~ 1960년대 중반 정도

* `Transistor` (1948년 개발됨) 가 주 구성요소임.
    * Vacuum tube를 사용했던 컴퓨터들 보다 1/100 수준의 크기로 소형화.
    * 동시에 생산단가가 낮아지면서 상업용 컴퓨터 보급이 보다 원활해짐.
* 기억장치
    * magnetic core(자기코어, primary memory)
    * secondary memory : magnetic tape(자기테이프), magnetic disc(자기디스크) 등.
* micro-second 단위의 연산속도.
* Operating System (OS)가 IBM204 등에서 등장하기 시작.
* bacth processing(1950년대)이 주로 사용되었으나 multiprogramming(1960년대)의 개념도 등장.
    * `Multiprogramming`이란 I/O 처리로 인해 CPU연산이 필요하지 않은 경우, 다른 프로그램에게 CPU를 사용할 수 있도록 해줌. (이를 위해 여러 프로그램이 main memory에서 동시에 상주함.)
        * 이전의 방식(한 프로그램이 끝날 때까지 점유)은 Uni-programming (단일 프로그램)이라고 불림.
        * 고가의 컴퓨터를 효율적으로 사용하기 위한 기술이었고 이는 time-sharing system으로 이어짐.
    * `Batch processing`이란
        * 특정 시간에 대량의 데이터를 일괄적으로 처리하는 것을 의미.
        * 컴퓨터가 어떤 작업이 주어지면, 끝날 때가지 해당 작업만 수행하게 되며, processor scheduling이라는 개념이 도입되기 전에는 거의 모든 작업이 batch processing이었음.
        * 한 프로그램의 수행이 끝나면, 사람이 이를 확인하고 다음 수행할 프로그램을 전달해주는 형태임.
* `machine language`와 `assembler`가 이용됨.

> mutliprogramming과 비슷한 개념이 multitasking임. 
> 하나의 장비에서 여러 프로그램이 동시에 수행을 목표로 하기보다는 CPU의 idle time을 줄이기 위해 도입된 multiprogrmming과 달리, multitasking은 하나의 resource를 여러 process들이 공유하는 개념으로 동시에 수행되는 것을 목표로 하고 있어서 multiprogramming의 논리적인 확장이라고 볼 수 있다.  
사실 resource에서 가장 중요한 것이 CPU이고, 어찌 보면 유사한 개념이지만, multitasking은 round-robin sheduling algorithm과 같은 스케쥴링 알고리즘이 multiprogramming에 보다 추가된 것이며 여러 task를 동시에 수행시키기 위한 기술(사실은 그렇게 느껴지게 하기 위한 기술)이다. 반면, multiprogramming이 오직 단일 CPU의 idle time을 줄이기 위한 context changing에만 초점을 둔 것으로 여러 작업이 동시에 실행되는 것을 보장하지 않는다.  
결국, multitasking은 multi-programming에 multi-processing과 time-sharing 등의 개념 등이 보다 추가된 것이다.  
> 보다 자세한 건 다음 url을 참고하라. [Difference Between Multiprogramming and Multitasking](https://www.tutorialspoint.com/difference-between-multiprogramming-and-multitasking)

TRADIC, TX-0 등등이 유명한 2세대 컴퓨터임.

> `ENIAC`이 17,000개의 vacuum tube를 사용한 것에 비교하여 `TRADIC`은 800개의 transistor를 사용하면서 1/15,000 수준의 전력을 소비했음.

1960년 초반에 등장한 `키보드`와 `모니터`의 등장으로 기존의 batch processing에서 `interative system`(1960년대)으로의 변화가 가능해짐.   키보드와 모니터 등을 통해 사용자에게 작업이 진행되는 중간에 입력과 출력이 가능해졌다. 

#### TRADIC (TRAnsistorized Airborne DIgital Computer)

1955년 AT&T Bell 연구소의 J. H. Felker가 만든 ^^transistor기반 컴퓨터^^ .  
800여개의 transistor와 10,000여개의 게르마늄 수정정류기를 사용한 것으로 알려짐.

![](./img/TRADIC_computer.jpg){width="300" align="center"}

* By Unknown author - Retrieved January 24, 2015 from Radio-Electronic Engineering magazine, Ziff-Davis Publishing Co., New York, Vol. 24, No. 5, May 1955 , cover on http://www.americanradiohistory.com, Public Domain, https://commons.wikimedia.org/w/index.php?curid=38024210

#### TX-0 (Transistorized eXperimental computer 0)

1956년 MIT Lincoln 연구소의 Ken Olson과 Stan Olson (형제임), Harlan Anderson이 미 해군의 후원으로 개발한 범용 transistor 기반 컴퓨터.

#### LARC (Livermore Atomic Research Computer)

2차 세계대전 이후 ^^핵무기 개발 경쟁^^ 으로 인해 탄생한 초기 `슈퍼컴퓨터`. 버클리 대학 부설 로렌스 연구소와 스페릴랜드사가 미 해군 연구개발센터에 1960년 개발 설치한 슈퍼컴퓨터 (들인 비용에 비해 만족스러운 성능은 아니었다고 함.) 

## 3rd Generation

1964년대 ~ 1971년대

* Integrated Circuit (IC)가 주요 구성요소.
    * IC 사용은 보다 높은 신뢰성과 처리속도와 용량을 보유한 컴퓨터를 보다 작게 만들 수 있도록 해줌.
* `UNIX` 의 등장(1960년대 후반)으로 오늘날 OS의 개념이 명확해짐.
    * Time sharing system (시분할 시스템)을 채택하여 여러 terminal을 지원하게 됨.
    * 최초로 다중작업(Multi-tasking) 및 다중사용자가 가능한 OS.
    * UNIX는 현대 OS의 기본 개념을 수립한 OS로 가치가 있음.
* nano-second의 연산속도
* 컴퓨터에 family (계열) 개념이 일반화되면서 기종간 호환성이 커짐.

IBM 360 (1964), CDC 7600, UNIVAC1108(이 컴퓨터는 일부 문헌에서 2세대로도 기재되지만 IC의 개념으로 보면 3세대라 보는게 맞다고 생각됨) 등이 유명한 3세대 컴퓨터임.
또한 1964년의 BASIC을 기점으로 컴퓨터와 함께 bundle로 제공되던 SW가 아닌 SW만으로 공급되기 시작했음.

### BASIC (Beginner's All-purpose Symbolic Instruction Code)

1964년 다트머스 대학의 John Kemeny(존 케메니)와 Thomas Kurtz(토마스 커츠)가 개발.

* 교육용으로 시작됨.
* imperative language
* interpreter 방식으로 시작되었으나, 이후 compiler도 도입됨.
* Bundle로 제공되지 않은 최초의 SW에 해당.

### IBM 360

1964년 IBM이 내놓은 ^^범용대형컴퓨터^^ (Mainframe).

360은 360도를 의미하여, 해당 컴퓨터가 어느 특정한 분야가 아닌 모든 연구 및 산업 분야에서 사용가능한 범용을 강조하기 위해 붙여진 이름을 가짐.

* 8bit에 해당하는 byte라는 개념과 byte단위의 memory adress, word의 개념과 같이 오늘날 컴퓨터 기술에서 표준적으로 사용되는 여러 기술이 적용된 컴퓨터임.
* ^^다중 사용자 접속^^ 을 제공했으며 많은 대학교와 연구소등에서 사용된 기념비적인 컴퓨터임.

### CDC (Control Data Corporation) 7600

1968년 CDC가 개발한 슈퍼컴퓨터. 
진정한 슈퍼컴퓨터로 인정받은 컴퓨터로서 기존의 시스템보다 10배 이상 빠른 속도 (1MFLOPS)와 6배 이상의 메모리 등을 가진 컴퓨터로 알려짐. 이를 개발한 Seymour Cray는 오늘날 슈퍼컴퓨터의 아버지로 불림. 

#### 정보처리 속도 단위

`FLOPS (Floating-point Operation Per Second)`는 정보처리 속도 단위로 초당 부동소수점 연산 횟수를 의미함. Mega-, Giga 등의 prefix가 사용된다. 다른 단위로는 IPS (Instruction Per Second)로 초당 명령어 횟수도 있음.

> 인간의 경우 LIPS (Logical Inference Per Second)로 초당 논리적추론 횟수 를 적용할 수 있는데, 보통 인간이 2 LIPS 정도가 가능하다. 참고로 1LIPS는 대략 100~1,000 개의 instruction으로 구성된다고 알려짐.

## 4th Generation

1970년대 ~ 현대

* `LSI` (Large Scaled Integrated circuit)과 `VLSI` (Very Large Scaled Integrated circuit)이 사용된 컴퓨터
* ^^오늘날의 컴퓨터가 4세대^^ 에 속한다. (혹자들은 5세대를 애기하기도 하지만...)
* 오늘날 CPU로 불리는 `Micro-processor`가 드디어 등장한 세대이며, 이를 통해 Personal Computer (PC)가 보급되기 시작한 세대이기도 함.
    * `Intel4004` (1981년. 최초의 Mirco-processor, 4bit CPU)는 2,300개의 transistor로 구성되었고 초당 60,000개의 연산이 가능.
* Internet의 등장으로 Network가 일반화된 세대이기도 하며, 휴대용 컴퓨터가 등장한 세대이기도 함.

> 일부 문헌에서는 VLSI를 이용하는 컴퓨터를 5세대라고 부르기도 하지만, VLSI의 개념 자체가 1980년대 개발된 이후로 급격한 성능향상이 이루어져 VLSI와 ULSI (Ultra LSI)구분 자체가 무의미해지고 있다. 오늘날 개발되고 있는 IC들도 그냥 VLSI로 부르고 있다 (과거 개념에보면 Ultra Super ... 등의 수식어가 붙어야할 수준 임에도... PC에 사용되는 i7 cpu가 100억 수준의 소자가 집적되어 있다).  
> [IC 관련 자세한 것은 이 링크를 참고](../ch02_co/ce02_03_4_IC.md)  
> 때문에 지적 능력을 가진 컴퓨터의 등장을 가르켜 5세대라고 불러야 한다는 의견이 대두되고 있다. 즉, 컴퓨터 자신이 학습을 하고 학습한 내용을 토대로 자신의 성능을 향상시키는 것이 가능해지는 컴퓨터가 대중화되는 시대를 5세대라고 해야한다는 의견인데... 기계학습 (특히, 딥러닝)의 발전으로 일부 분야에서는 사람 이상의 성능을 스스로 학습하여 달성하는 컴퓨팅이 가능해지고 있는터라...  
앞서 애기한대로, 지나치게 엄격하고 세대를 나누는 건 의미가 없다. ^^발전사를 기억하기 쉽게 하기위해 도입한 개념^^ 으로만 생각하자.

### Personal Computer

1976년 PC Apple의 등장으로 개인이 computer를 가지는 시대가 열림.

![](./img/PC_apple1.png)

Apple2가 1977년 나오면서 PC가 본격적으로 보급되기 시작함. 상당수 문헌에서는 Apple2를 3세대 컴퓨터로 분류하기도 하며 이후 등장한 IBM 5150과 Macintosh를 4세대로 분류한다.


## References

* My Computer Notes's [What are the Generations of Computer](https://mycomputernotes.com/generations-of-computer/)
* [History of Computer Development](https://prezi.com/868wjfuzufee/presentation/?token=8d632e494ae6ccbd5097afc5eca19b7cee1de821c024dce1e4fa45af0d473d95&utm_campaign=share&utm_medium=copy)
* smart.science.go.kr's [컴퓨터](https://smart.science.go.kr/scienceSubject/computer/timeView.action) : 강추함. 재미도 있음.






