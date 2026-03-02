---
title: "Internet, WWW, TCP/IP 정리"
description: "Internet의 계층적 구조부터 WWW, Client/Server Model, TCP/IP, DNS, 주요 프로토콜 및 Firewall까지 정리"
tags:
  - Internet
  - TCP/IP
  - WWW
  - HTTP
  - DNS
  - Firewall
--- 

![](./img/IMG_3592.png){style="display: block; margin: 0 auto; width:400"}

# Internet

Internet은 Network 의 [Network](https://ds31x.github.io/wiki/network/)를 가리키며, 기존의 WAN들을 전세계적으로 연결한 것이 Internet임.

> Internet is not actually a physical network; it’s **a set of layered protocols**.

계층화된 프로토콜 집합이기 때문에,  

* 하위의 물리적 계층이 기술의 발전으로 바뀌더라도  
* 상위의 계층에 영향을 주지 않도록 설계됨. 

> 이같은 계층화와 추상화 덕분에
> 전화선에서 광케이블 등으로 물리적 계층은 바뀌었지만,  
> 상위의 계층들은 그로 인한 변경없이 동작이 가능함.

---

## World Wide Web (WWW)

World Wide Web은 인터넷 위에서 동작하는 ***하이퍼텍스트 기반 정보 시스템*** 임.

* WWW에서 문서들은 HTML(HyperText Markup Language)로 작성되며,
* 문서 간 연결은 hyperlink를 통해 이루어짐.
* WWW에서 제공되는 자원(문서 포함)은 URL(Uniform Resource Locator)로 식별됨.

> Web의 핵심은 “문서 간 연결 구조”임.  
> 사용자는 링크를 통해 문서를 탐색하며 정보를 획득함.

주의한 점은 

* Web은 인터넷 그 자체가 아니라,
* 인터넷 위에서 동작하는 하나의 응용 계층 서비스이라는 것임.

> 참고로 최초의 [웹브라우저](#Web-Browser) 이름도 World Wide Web 이었음: 1990년 Tim Berners-Lee가 개발.
> 이후 정보 시스템 과 이름이 겹치는 혼돈을 피하기 위해 Nexus로 이름이 변경됨.

---

## Client / Sever Model

Web은 Client / Server Model 위에서 동작함.

* **Client** 는 요청(request)을 보내는 주체이고,
* **Server** 는 요청을 처리하고 응답(response)을 반환하는 주체임.

동작 흐름은 다음과 같음.

1. Client가 특정 URL에 대한 요청을 보냄.
2. Server가 해당 자원을 처리함.
3. Server가 결과를 응답으로 반환함.

이때 사용되는 대표적 프로토콜은 HTTP 임.

> 여러 Client가 하나의 Server에 동시에 접속할 수 있으며,  
> Server는 다수의 요청을 일반적으로 병렬적으로 처리함.

---

## Web Browser

Web Browser는 Web Client에 해당하는 소프트웨어임.

대표적인 예로는
Google Chrome,
Mozilla Firefox 등이 있음.

Browser의 주요 기능은 다음과 같음.

* URL 입력을 통한 자원 요청
* HTTP 요청 전송
* HTML 문서 수신
* CSS 해석
* JavaScript 실행
* 화면 렌더링

> Browser 내부에는 Rendering Engine이 존재하며,  
> 이는 HTML을 DOM(Document Object Model) 구조로 변환하고  
> 화면에 시각적으로 표현함.
 
오늘날의 웹브라우저는 단순히 Web서비스에서의 클라이언트라기보다는 일종의 VM으로 여겨지기도 함: 

* 다음을 참고: [VM으로서의 Web Browser](../ch09/ce09_web_browser/)

---

## Transmission Control Protocol/Internet Protocol (TCP/IP)

***internet을 구성*** 하고 있는 the pair of protocols.

* Internet에 접속하기 위한 protocol.  
(internet은 TCP/IP를 이용하여 구성된 network임)
* TCP라는 프로토콜(Layer 4)과 IP라는 프로토콜(Layer 3)을 합쳐서 사용. 

  - IP protocol 위에 TCP protocol이 정의됨.
  - `192.168.31.34`과 같은 IP Address와 `datagram`으로 불리는 packet 을 사용 (IP 프로토콜의 특징), 
  - 신뢰성 높은 데이터 송수신(TCP 프로토콜의 특징)을 제공 (`TCP`는 packet의 수신을 보장함.)

> 전 세계의 모든 컴퓨터와 기기가 인터넷을 통해 상호 연결되기 위해서는  
> TCP/IP 라는 protocol pair 를 사용해야 하고,  
> 때문에 IP Address를 각각의 장비에 부여해야 함.  

---

## IP Address

Internet 상(or Network)에서 어떤 한 컴퓨터를 찾아낼 수 있는 **주소**.    
(= 인터넷상에서 데이터를 송수신할 목적으로 **컴퓨터에게 부여하는 값.**)

> Windows OS의 `네트워크 속성` 등에서 탭으로 보이는 `Internet Protocol Version 4(TCP/IPv4)`가 TCP/IP 설정을 하는 곳임.

* 실제로는 Ethernet card에 IP address가 할당된다.


  [IP Address 설명 URL](https://dsaint31.tistory.com/439)

---

## Domain Name System

Domain : 인터넷에 연결된 컴퓨터를 ***사람이 쉽게 기억하고 입력할 수 있도록 문자(영문, 한글 등)로 만든 인터넷 주소***.

* [Domain이란?](https://xn--3e0bx5euxnjje69i70af08bea817g.xn--3e0b707e/jsp/resources/domainInfo/domainInfo.jsp)

* [DNS란](https://dsaint31.tistory.com/440)

* [notion메모](https://www.notion.so/mmmil/Domain-Name-System-727bf668104a4dfaade9830fa743a96d)

---

## 기타용어 및 Protocol

`Hyper-Text`  
: 인터넷 웹 페이지 구성 하는 Text를 지칭

`Hyper-Link`  
: 특정 하이퍼 텍스트를 마우스로 클릭하여 다른 웹 페이지로 이동시키는 방식을 `하이퍼링크` 라고 함.

`HTTP`  
: Hyper-Text Transfer Protocol 의 abbreviation.  
하이퍼 텍스트를 전송 및 제어하는 응용계층 `protocol`이 HTTP이다.  
(TCP/IP 위에 정의)  

`HTML`  
: Hyper-Text Markup Language 의 abbreviation.  
웹 페이지(Hyper-Text)를 작성하는 언어가 ‘HTML’. 

`HTTPS`  
: http와 동일하지만 보안(secure) 기능을 추가한 것으로 http 프로토콜에 보안 기능을 제공하는 SSL (Secure Socket Layer) 프로토콜을 접목한 형태.  
SSL은 오늘날 [TLS (Transport Layer Security)](https://ds31x.tistory.com/613?category=717892#6.-tls-transport-layer-security) 로 계승된 상태임.

`SMTP`  
: Simple Mail Transfer Protocol 의 abbreviation.  
email 전송 protocol. 기본적으로 25번 포트 사용.

`FTP`
: * 파일 전송을 위해 사용하는 protocol. (TCP/IP 위에 정의)
:     - binary mode와 ASCII mode가 있음 (txt파일 다운로드 제외하곤 binary mode사용)
:     - Anonymous FTP의 경우, account없이 사용하는 경우이며 이 경우 ID는 `Anonymous`, 패스워드는 자신의 e-mail을 쓰는게 일반적.
: * 앞선 `http`를 사용하는 웹 페이지에서도 파일을 다운로드할 수 있지만, 대량의 파일을 다운로드하기에는 아무래도 불편하고 느리다. 
: * ftp 프로토콜은 원격의 컴퓨터에 접속하여 파일만 빠르게 업로드/다운로드할 수 있도록 한다.
: * 대표적 sw : [https://filezilla-project.org/](https://filezilla-project.org/)

---

## Firewall (방화벽)

컴퓨터 네트워크에서 해커나 크래커, 또는 바이러스 등이 네트워크 내부에 침입하지 못하도록 하는 보안 장비 또는 SW를 가리킴.

* 일반적으로 네트워크 구성에서 가장 윗단에 배치되어(컴퓨터-스위치-라우터-방화벽 순), 네트워크 내외에 걸쳐 데이터나 사용자의 이동 패턴을 분석한 후 사전에 지정한 보안 정책(rule)에 따라 처리

**윈도우 방화벽**

- 윈도우에 설치된 각종 프로그램 중에서 네트워크(혹은 인터넷)로 통신하는 프로그램의 통신 허용 여부를 설정
- 이미 널리 알려진 통신 프로그램은 통신을 허용하고 있지만, 불확실 프로그램에 대해서는 통신 차단 확인 창을 띄움.
- 특정 프로그램(온라인 게임 포함)이 통신 불가 또는 접속 불가 문제가 발생한다면, 윈도우 방화벽 설정을 확인해야 함. 
- 윈도우 방화벽은 통신 포트(네트워크에서 데이터가 이동하는 통로)에 따라 통신을 차단하기도 한다(방화벽의 기본적인 기능). 


