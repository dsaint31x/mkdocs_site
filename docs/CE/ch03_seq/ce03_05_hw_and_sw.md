# Hardware vs. Software (Firmware and FPGA관점에서 비교)

현재의 기술 trend는 convergence (융합)이다. 별개의 기술이라고 보이던 것들에서 각각의 장점을 가져와 더 나은 기술이 되는 경우가 많다. SW와 HW도 마찬가지이다. 

일반적으로 SW와 HW는 수행해야할 logic이 programming source code로 구현되느냐, 아니면 gate들로 구성된 chip으로 만들어지느냐의 차이로 구분이 된다. SW는 뭐든지 수행가능한 CPU (or MPU)에서 동작하거나 아니면 해당 SW를 수행할 수 있는 HW에서 수행되므로, 핵심 logic인 program (~bytes code)만 변경하면 다른 task를 수행하거나 좀 더 개선된 형태로 동작이 가능하다. 이에 비해 HW는 우선 제조가 되고 나면 설계된 task만 수행가능할 뿐 변경이 어렵다. 하지만, HW는 해당 task를 CPU 대비 매우 빠르게 수행하면서 개별 단가가 매우 낮다 (물론 large volumen production이 된 경우에 한함). SW는 뭐든지 수행할 수 있는 범용 CPU가 필요하므로 개별 단가가 낮아지기 어렵고, 실행속도 측면에서 HW (여기선 ASIC으로 생각하라)보다 낮은 성능을 보인다.

위에서 설명한 SW와 HW의 장단점을 개선하기 위한 여러 기술이 소개되었고, 예로서 firmware, FPGA 등이 있다.

## Firmware

이미 [ROM](./ce03_02_3_rom.md)에서 다루었듯이 초기의 ROM의 HW처럼 제조하고 나면 수정 및 변경이 불가했으나, 점점 ROM의 장점인 non-volatile은 유지하면서 자유롭게 수정가능하도록 만들어졌다는 것을 알 수 있다. 현재의 EEPROM과 Flash memory가 그 결과물이다. 이는 ROM에 저장된 SW를 가르키던 firmware의 정의를 확장시키는 결과로 이어졌다. 

`Firmware`
: 원래 firmware는 ROM에 저장된 software를 의미하였다. 전원이 나가도 유지가 되어야하는 logic을 programming code를 컴파일하여 만든 실행코드로 작성하고 이를 ROM에 저장시켰던 것이다. BIOS등이 대표적인 예라고 할 수 있다.

하지만 Flash memory가 ROM을 대체하면서, firmware도 제조된 이후 업데이트가 가능해졌고 이는 일반적인 software와 firmware의 구분을 굉장히 모호하게 만든다. 일반적으로 업데이트 빈도수가 보다 firmware가 적을 뿐이지 큰 차이가 없다.

## Field Programmable Gate Array (FPGA)

firmware 보다 더 강력한(?) 융합은 Filed Programmable Gate Array (FPGA) 라고 할 수 있다. 어찌되었든 firmware에서 ROM 또는 Flash memory는 logic을 실제 수행하진 않는다 (logic을 저장하고 있을 뿐이다). 즉, 앞서 설명한 logic의 수행의 관점에서보면 여전히 software라고 할 수 있다. 하지만, FPGA는 자체가 logic을 담고 있고 IC처럼 해당 logic을 수행하는 chip이다. 그러면서도 logic을 구현할 때, Hardware Description Language (HDL)과 같은 특별한 programming language로 구현하고 이를 FPGA에서 다운로드시킴으로 해당 logic을 수행하는 HW가 된다. 

IC가 gate들을 조합하여 구성되는 것을 이용하여, FPGA는 사용가능한 기본 component들을 block으로 지정하고 이를 array로 묶은 chip이다. 이를 어떻게 연결하느냐에 따라 logic이 구현되는데 이를 연결하는 것을 전용 programming language로 작성된 code가 결정한다. 즉, FPGA를 만드는 업체는 어떤 logic의 chip이 될 수 있는 일종의 만능칩을 제공하고, 이후 시스템이나 어플리케이션을 만드는 개발자가 여기에 logic을 구현하는 셈이다. 초기 FPGA는 PROM처럼 한번 다운로드하고 나면 수정이 안되었으나, 현재는 전기적으로 자유롭게 수정이 가능하다. 

FPGA는 firmware보다 한 발 더 나아간 ***수정이 가능한 Hardware*** 라고 할 수 있다. 

### ASIC vs. FPGA

반도체로 구현되는 다양한 IC들이 경우에는 대부분이 Application-Specific Integrated Circuit (ASIC)이라고 불리는 형태로 만들어진다.  
마치 ROM처럼 제조할 때, 사용되는 분야에 맞게 전용 logic을 탑재한 IC이다. 해당 task를 수행하는데 가장 빠르고 효율적인 IC를 만들 수 있으며 high-volume production application의 경우 가장 낮은 개별단가가 가능한 방법이다. 하지만, low-volume production application이 주가 되는 산업분야 (항공우주, 군수 및 방위, 의료 등등)에서는 개별단가를 낮추기가 어렵다. 일단 ASIC은 design 에 들어가는 비용과 manufature를 위한 초기 비용이 매우 높다. 한번 setup이 되고나서 생산을 하는데에는 비용이 낮지만 초기비용이 높고 이를 낮추기가 굉장히 어렵기 때문에 prototype application을 만들거나 low-volume production application에서 사용하기 쉽지 않다는 단점을 가진다.

* AP (Application Processor) : 대표적인 ASIC으로 휴대기기의 핵심 Processor임. 컴퓨터에서의 CPU와 같은 역할을 수행하면서 동시에 그래픽처리, 통신 등을 위한 기능도 수행함. 일종의 System on Chip 으로 작은 휴대기기의 공간에 많은 기능을 높은 집적도로 구현하기 위해 만들어진 ASIC임. 때문에 특정 용도(application)에 최적화된 Processor로 볼 수 있음.
* CPU (Cenral Processing Unit) : PC등에서는 주로 MPU (Micro Processor Unit)가 CPU로 사용됨. 연산과 제어만을 담당하고 그래픽처리, 통신등은 처리하지 않음 (Accelated Processing Unit의 경우, CPU+GPU로 최근 많은 CPU들이 그래픽처리도 포함하는 추세임). 대신 매우 높은 성능으로 연산 및 제어를 수행할 수 있게 만들어진다. 
* MCU (Micro Controller Unit) : MPU와 매우 흡사하지만, 연산 능력이 상대적으로 낮고 대신 저렴한 경우가 일반적이다. MPU가 컴퓨터 PC에서 사용된다면, MCU는 자판기나 전기밥솥, 오디오기기 등에서 제어등을 위해 사용된다. MPU에 memory나 i/o 등이 좀더 추가되어 하나의 ic로 패키징된 경우임.
* Micro-computer : IC 하나에 computer system을 집적시킨 SoC. AP (=보통 mobile AP를 가르킴)의 조상격으로 MCU에 시스템으로 필요한 기능 등을 추가하여 하나의 IC로 만든 것. 마이컴($\mu$-com or u-com)으로 표기되기도 함.

[MPU, micro controller 요약](https://dsaint31.tistory.com/entry/CE-Micro-Controller-Unit-MCU-and-Micro-computer)

> ASIC이 여러 사용처에서 공통적으로 사용되는 경우에는, 일종의 표준화된 제품으로 공급될 수 있으며 이를 Appliction-Sepecific Standard Product (ASSP) 라고도 부름. ASSP는 일종의 기성복(=유니폼처럼 특정 분야에서 입는)이고 ASIC은 완전맞춤복이라고 할 수 있음. 단 General purpose IC와 ASSP는 구별되는데 ASSP는 특정 용도나 분야에 한정되며, GPIC는 보다 다양한 용도, 기기, 분야에서 기성품(일반적인 기성복)으로 제공된다. 사실 ASSP와 ASIC은 기능적인 면과 기술적인 면에서 큰 차이가 없어서 ASIC으로 같이 불리며 비지니스 측면에서만 차이가 있다고 볼 수 있음.

FPGA는 ASIC과 반대되는 특성을 가진다. design과 manufature를 위한 초기 비용은 매우 낮지만, setup 이후의 생산 개별 단가는 ASIC보다 훨씬 높다. 하지만, 개별 제품이 고가이고 소량다품종이 요구되는 산업분야에선 ASIC보다 나은 선택이 된다. 실제 의료기기 및 항공우주 산업, 그리고 일부 방위산업 등에서는 FPGA가 빠르게 확산되고 있으며, 일부 ASIC의 분야마저 FPGA가 사용되고 있다.

### FPGA의 가능성

FPGA에서 가장 중요한 선두업체는 Xilinx와 Altera 인데, Altera는 Intel이 2015년 6월 인수를 했으며, AMD가 Xilinx를 2022년 2월 인수 완료했다. 실제로 FPGA의 개별단가도 기술의 발전으로 매우 낮아지고 있고 그 유연성이 CPU 업체들이 인수를 결정할 정도로 매우 중요하다는 반증이다. 요약하면 의료기기 및 지능형 컴퓨팅 등에서 FPGA의 중요성은 더욱 커질 것으로 보이며, 관련 시장 역시 더욱 넓어질 것이 분명하다. 

### FPGA를 위한 Programming Language (Hardware description language)

디지털 회로에 대한 지식을 기반으로 코드를 작성해야만 정상적인 동작이 되는 chip을 만들 수 있다. 이는 CPU 에 대한 지식이 풍부한 SW개발자가 좋은 프로그램을 만드는 것과 마찬가지이다. 일반 프로그래밍과 달리 동작 clock등에 대한 이해와 같은 HW적 지식이 필요하다. 

> 더욱이 SW개발에서 필요한 IDE (Integrated Development Environment)들이 상당수 무료 또는 저렴하게 사용할 수 있는 것과 달리, FPGA에서의 IDE에 해당하는 EDA (Electronic Design Automation)는 매우 고가임. 개개인이 공부하기에 사기는 어려움이 있다 (학교 등의 기관인증 아니면 ...). 2022.8 이후로는 미국의 동맹국이 아닌 150여개 국가는 사용에 특별허가까지 요구하는 경우가 발생...

`Verilog` and `VHDL`
: Verilog (system verilog포함)과 VHDL은 대표적인 HW description language임. FPGA를 설계하는데 사용되며, 실제 FPGA에 다운로드하기 전 시뮬레이션 등도 가능하다. 초창기에는 VHDL이 많이 사용되었으나 현재는 C와 비슷한 Verilog가 현재는 많이 사용된다. 

> Verilog HDL이 원래 이름이지만, 대부분 Verilog라고 부름. 

`SystemC`
: 앞서 두 언어와 마찬가지로 HW description language 중 하나이나, 좀 더 높은 수준의 abstraction을 제공하며 C++에 기본언어로 채택했다. 이는 좀더 개발자가 사용하기 쉽다는 뜻이며, 반대로는 HW 보다 사람에 친화적인 언어라고 볼 수 있다. 

## 다른 자료들

* 정보통신기술용어해설's [Verilog HDL](http://www.ktword.co.kr/test/view/view.php?m_temp1=6235)
* technologyreview's [미·중 반도체 전쟁 새로운 국면 진입…EDA 수출 금지의 파장은?](https://www.technologyreview.kr/eda-software-us-china-chip-war/)
* [디지털시스템 설계 및 실습](https://cms3.koreatech.ac.kr/sites/yjjang/down/dsys11/M01_VerilogHDL01.pdf)