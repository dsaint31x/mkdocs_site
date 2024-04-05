# Gate들을 이용한 보다 복잡한 회로들.

Small-scale integration (`SSI`)을 이용하여 여러 `gate`들로 구성된 좀더 복잡한 회로들을 만드는 건 디지털 회로 또는 실습 시간에 많이 다루게 됨.

* Adder
* Encoder and Decoder
* Mux and Demux

이 장에서는 단순한 여럿 `AND`, `OR` gate들을 통해 구성되는 위의 component들 (책에서는 building block이라 표현)들이 구성되는 것을 다룸.

Programming에서는 단순한 statement와 expression들을 조합하여 function이라는 building block을 만들어내는데 이에 대한 hardware version이라고 생각할 수 있음.

## 구성.

* [Half Adder and Full Adder (notion)](https://dsaint31.notion.site/2-5-1-Building-an-Adder-8d766ecdc59d4241bdd70309f9651e12)
* [Decoder and Encoder](https://dsaint31.tistory.com/entry/CI-Binary-Decoder)
  
    * One-hot code 에서 binary code로 변환하는 binary encoder
    * 이를 반대로 수행하는 binary decoder를 간단히 살펴봄.

* [Demux and Mux](https://dsaint31.tistory.com/entry/CI-Demultiplexer-and-Multiplexer)
    * Demux (single input, multiple outputs)
    * Mux (multiple inputs, single outputs) = selector