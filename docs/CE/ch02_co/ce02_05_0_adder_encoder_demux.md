# Gate들을 이용한 보다 복잡한 회로들.

Small-scale integration (`SSI`)을 이용하여 여러 `gate`들로 구성된 좀더 복잡한 회로들을 만드는 건 디지털 회로 또는 실습 시간에 많이 다루게 됨.

* Adder
* Encoder and Decoder
* Mux and Demux

이 장에서는 단순한 여럿 `AND`, `OR` gate들을 통해 구성되는 위의 component들 (책에서는 building block이라 표현)들이 구성되는 것을 다룸.

Programming에서는 단순한 statement와 expression들을 조합하여 function이라는 building block을 만들어내는데 이에 대한 hardware version이라고 생각할 수 있음.

## 구성.

* [Half Adder and Full Adder](./ce02_05_1_adder.md)
* [Decoder and Encoder](https://dsaint31.tistory.com/entry/CI-Binary-Decoder)
  
    * One-hot code 를 입력받아 binary code(이진수)로 변환하는 `priority encoder`
    * 이를 반대로 수행하는 `binary decoder`를 간단히 살펴봄.

* [Demux and Mux](https://dsaint31.tistory.com/entry/CI-Demultiplexer-and-Multiplexer)
    * Demux (single input, multiple outputs) : 하나의 입력을 여러 출력 중 하나로 연결해줌.
    * Mux (multiple inputs, single outputs) = selector : 여러 입력 중 하나를 하나의 출력에 연결해줌.