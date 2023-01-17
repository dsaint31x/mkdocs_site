# Network

## History of Data Communication

* 1844년 : Electrical Telegraphy (전신) 등장. Morse code를 이용하여 미국 볼티모어와 워싱턴 D.C. 사이에 연락이 이루어짐.
* 1876년 : 알렉산더 그레함 벨의 전화기 발명
* 1958년 : 냉전시대의 군사용 방어시스템의 일부. modem과 전화선 기반.
* 1960년대 : 중앙컴퓨터를 중심으로 ring형태의 다양한 LAN 들이 등장. modem과 전화선 기반으로 LAN이 구성됨.
* 1960년대 후반 : `packet-switched WAN`인 ARPANet (Advanced Research Project Agency Net) 등장. 이 ARPANet이 Internet으로 진화함.
* 1970년대 : ALOHA (Additive Links Online Hawaii Area) 시스템 (`packet-switched radio network`) 등장.
* 1973년 : Ethernet 개발됨 (ALOHA 시스템에서 영감을 받음)
* 1979년 : Bell연구소에서 `UNIX-to-UNIX copy (UUCP)` 가 등장하여 UNIX 기반 컴퓨터들이 데이터를 주고받고 프로그램을 원격으로 수행시킬 수 있게 됨. `UUCP`를 기반으로 일종의 Message system인 [USENet](http://commres.net/wiki/usenet)이 생성됨.
* 1990년대 : Internet (Inter+Net) 등장. WWW서비스 본격적으로 시작됨. Internet은 Network 의 Network를 가르키며, 기존의 WAN들을 전세계적으로 연결한 것이 Internet임.

> `Modem` (MOdulator/DEModulator)  
> 컴퓨터는 디지털 신호를 사용하기 때문에 아날로그 방식의 전화선(PSTN) 등을 이용하여 통신하기 위해서 변복조가 필요함. 이를 수행해주는 device가 바로 modem임.

<iframe width="560" height="315" src="https://www.youtube.com/embed/mi3RZh5Q8Xc?start=54" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

---

## 네트워크의 종류 (접속방식에 따른)

* [Circuit Switching Network and Packet Switching Networ](https://dsaint31.tistory.com/entry/CE-Circuit-Switching-and-Packet-Switching)

---

## LAN vs. WAN

> Local Area Network(LAN)은 작은 영역의 network를 가르키며, Wide Area Network (WAN)은 중대형 영역의 network를 가르킴. 

흔히, 집안이나 사무실 내의 네트워크 연결은 ‘LAN’, 지역 간/국가 간 네트워크 연결은 ‘WAN’이라 할 수 있다. 기관이나 기업들의 내부망을 가르키는 intranet은 보통 LAN이라고 보며, 여러 intranet이 연결되어 이루어진 WAN 중에서 전세계 규모로 연결된 network를 internet이라고 부름.

---

## Protocols

> set of rules. '약속', '규약', '협약' 등을 의미하는 단어로 상호간 원활한 교류, 소통, 통신을 위해  서로 동일하게 어떠한 설정/규칙을 정한 것을 가르킴.

* 통신을 원하는 두 개체 간에 무엇을, 어떻게, 언제 통신할 것인가를 서로 약속하여 통신상의 오류를 피하도록 하기 위한  통신 규약임. 
* protocol이 없다면, 정보를 보내는 컴퓨터는 16비트 패킷으로 데이터를 보내고, 정보를 받는 컴퓨터는 32비트 패킷의 데이터를 수신 기대하여 통신이 아예 안되는 상황 등이 벌어질 수도 있음. 
* 가장 유명한 프로토콜은 **개방형 상호 접속 시스템**(`Open Systems Interconnection/OSI`) 임.
* 사실 OSI는 컴퓨터들 사이의 네트워크 통신을 위한 일종의 가이드 라인이라고도 볼 수 있음. 
* 인터넷 프로토콜 가운데 가장 중요한 것으로 `TCP/IP`, `HTTP`, `FTP` 등이 있음.

---

## 통신 방식

`Simplex` : 단방향 통신.
 
 Data Terminal Equipment 2대가 연결되어 있는데, 한 DTE는 송신만을 다른 DTE는 수신만이 가능하도록 되어있어서 한 방향으로만 데이터가 전송되는 통신 방식을 가르킴. (과거의 TV,라디오 등이 취하는 방식)

 `Half Duplex` : 반이중 통신.

 DTE 2대가 시간적으로 교대로 데이터를 교환하는 방식으로 순간적으로는 데이터가 한 방향으로만 흐르지만, 해당 통신이 끝나면 다음번에는 송수신 방향이 바뀌어 데이터가 전송될 수 있는 통신 방식임. 워키토키 등에서 over로 자신의 말을 끝내면, 다른 이가 송신을 시작할 수 있는 형태가 Half duplex임.

 `Full Duplex` : 전이중 통신

연결된 2대의 DTE가 동시에 송수신을 다 할 수 있는 통신 방식 (전화가 가장 쉬운 예) 