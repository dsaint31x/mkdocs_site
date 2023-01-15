# Container

`Container`는 On-premise 나 cloud 등의 다양한 환경에서 linux 및 windows application을 패키징하고 실행하기 위한 기술.

`Container`는 applicatoin을 보다 쉽게 개발, 배포 및 관리할 수 있도록 ***격리된 경량의 환경*** 을 제공함.
  - applicatoin이 요구하는 library들과 다른 sw를 하나의 패키지로 제공해줌.
  - 제공해주는 sw에 OS까지 포함되기 때문에 사실상 `container`를 수행시킬 수 있는 SW만이 Host OS (=Docker)에 있으면 된다.

* `Container`는 target application이 실행되기 위해 필요한 최소한의 경량 환경을 host OS에 격리되어 제공함.
* Host OS의 kernel 을 공유하지만, 이에 대해 제한된 access만이 가능(application을 수행하는데 필요한)하도록 system에 대한 격리된 view를 제공함.
* `Container`는 Host OS와 Kernel을 공유하므로 해당 Kernel 상에서 빌드되지만, OS가 제공하지만 공유된 kernel이 제공하지 않는 운영체제서비스 (target application이 요구하는 간단한 OS API및 서비스) 및 application에 필요한 시스템 파일(라이브러리 등)을 따로 제공하여, Host OS의 사용자 모드 환경과 격리된 환경을 제공함.
* `Container`에서의 파일 변경이나 설정 변경은 오직 `container`에만 영향을 준다(host OS와 일부 storage를 공유할 수도 있으며 이 경우엔 host OS도 변경 내용에 영향을 받을 수 있음).
* `Container`는 host OS와 공유하는 kernel을 제외한 격리된 환경을 제공하기 위해 image로 패키징 됨. 해당 image에는 공유하지 않는 OS의 서비스 및 시스템파일 및 가상 storage, 그리고 타켓 application이 포함되며 host OS입장에서는 일종의 파일로 보임.

> Virtual Machine의 경우, container와 달리 자체 kernel을 포함한 완전한 OS를 실행시키기 때문에 해당 OS가 인식할 가상 Hardware까지 제공해야하며, 이는 보안적인 측면에서 보다 강력한 격리를 제공하나 Container보다 훨씬 무거운 환경임 (`Container`에 비해 더 많은 시스템 리소스가 필요).

> Cloud Computing의 경우, 물리적 시스템 위에 Virtual Machine들이 존재하고, 해당 VM들 위에서 Container들이 동작하는 방식이 일반적임. EC2등의 서비스는 사용자가 VM을 임대하는 것으로 생각할 수 있음.

# Virtual Machine

> Virtual Machine이 동작하는 Host System을 Hypervisor라고 칭하기도 하는데, VM은 Host System의 OS와 완전히 격리되어 동작함. VM내에서는 완전한 OS가 수행되므로 VM내에서 동작하는 OS가 기대하는 가상의 하드웨어들을 제공해야하며 이는 container보다 많은 리소스를 필요로 하게 함.

HW의 발전으로 가능해진 것으로 마치 여러 application처럼 시분할 기술을 통해 단일 OS에서 실행하는 것처럼, 여러 OS를 단일 물리적 시스템에서 시분할로 실행하는 방법이 Virtual machine임.

하지만 application과 달리 OS는 HW에서 수행되는 instruction set이 있고 HW와 상호작용을 하기 때문에, "실제 물리적 시스템의 HW에서 해당 작업을 담당하는 Host OS"와 "VM 내의 OS"사이에서 ***VM내 OS의 요청을 Host OS가 수행할 수 있는 요청으로 변환해주는 중간자*** 가 필요하다. 이는 일종의 interpreter라고 볼 수 있는데, OS는 machine에 설치된다는 종래의 개념에서 virtual machine이라는 이름이 붙었다고 생각하면 쉽게 이해가 될 것이다.

VM으로 유명한 SW들은 MS사의 Hiper-V와 Oracel의 Virtual Box등이 있다.

복잡한 연산 등을 VM으로 수행하기에는 High-end PC에서도 다소 무리가 있다. 하지만 간단한 워드 수준의 작업은 VM으로 충분하기 때문에 일반 사용자도 관공서나 특정 기관에서 사용해야하는 웹 어플리케이션 또는 SW가 이전 버전의 OS 나 웹브라우저 등을 요구하는 경우 (내 장비에 설치하기엔 너무 구식인 경우도 있을 수 있다)에 VM은 좋은 대안이 된다.









# References

* [Container vs. Docker](https://hazel-developer.tistory.com/m/242)