# Transistor (Transfer + Register)

오늘날 전자기기에서 주로 사용되는 소자이며, 전기회로와 전자회로를 구분짓는 active device의 대표격인 소자. 전류(BJT) 또는 전압(FET)에 의해 제어되는 switch, 가변저항, 증폭기로 사용된다.

대표적으로 Bi-Junction Transistor와 Field Effect Transisor를 교과서에서 다룬다. device 하나의 효율은 BJT가 보다 좋지만, FET는 크기가 매우 작아서 같은 크기에 60~80배의 집적도가 가능하여 BJT보다 FET가 보다 많이 사용되는 추세임. (원가의 측면등에서도 FET가 훨씬 유리).

FET에서도 Metal Oxide Silicon FET가 주로 많이 사용되고, N-channel MOSFET과 P-channel MOSFET 중에서도 carrier가 훨씬 빠른 electron을 사용하는 N-channel MOSFET이 N-channel MOSFET (N-MOS)가 가장 많이 사용됨.

워낙 작게 만들 수 있기 때문에 컴퓨터의 소형화에 큰 기여를 함. 너무 작게 만들 경우 발열이 커져 substrat인 silicon에 손상을 줄 수 있어 소형화에 한계가 있고, carrier의 속도에 의해 동작속도 한계가 있음. (차세대 반도체 소자는 carrier의 직접 이동이 아닌 방법이 고려되고 있음.)

Transistor는 물리적인 switching을 수행하는 Relay나 열을 가해야하는 Vacuum tube등에 비해서 가격, 속도, 크기, 수명 등의 모든 면에서 우수한 device임. (열전자 대신 semi-conductor를 이용한 Vacuum tube라고 보면 이해가 쉬움)

## N-MOS and P-MOS FET
N-MOSFET의 경우, Gate에 `1` (정확히는 $V_\text{GS} > V_\text{Th}$)인 경우 close가 되는데, output이 `0`에 해당하는 $V_\text{SS}$에서는 손실이 없지만, `1`에 해당하는 $V_\text{DD}$는 $V_\text{DD}-V_{Th}$가 되어 손실이 발생함.

N-MOS와 P-MOS는 각기 상보적인(complementary) 특징을 가지기 때문에 이 둘을 잘 조합한 CMOS (Complement Metal Oxide Silicon) FET이 낮은 전력 소모 등의 장점을 보임으로서 컴퓨터에서 많이 사용된다.

워낙 낮은 전력소모를 보이기 때문에, 컴퓨터의 BIOS(Basic Input/Output System)에서 필요로 하는 주변기기 정보를 저장하는데 사용되는 반도체기반 소자가 바로 CMOS이다. 때문에 CMOS와 BIOS가 엄연히 다른 것인데도 컴퓨터 사용자들 사이에서 마치 같은 용어인 것처럼 같이 사용하는 경우가 많다. BIOS는 말해서 program(엄밀하게는 nonvolatile firmware)으로 주변기기 사이의 정보전송을 관장하며 ROM에 저장되어 BIOS ROM이라고도 불리며, CMOS는 하드웨어(special memory chip)로 BIOS의 설정정보를 저장하는 역할을 한다. 즉, CMOS에 주변기기등의 하드웨어 관련 정보 및 BIOS 관련 정보가 CMOS에 저장하고 이 정보는 BIOS가 읽어들여 컴퓨터가 부팅될 때, 컴퓨터의 하드웨어들을 초기화한다.