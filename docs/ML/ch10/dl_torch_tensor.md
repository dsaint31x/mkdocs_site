# PyTorch 기초

## Tensor 다루기

Tensor의 기본 개념과 data type, 주요 attributes, 생성 및 indexing 방법을 정리하고,  
vectorized operation과 in-place operation 등 tensor 연산의 기본 원리를 다룸.  
또한 GPU 기반 acceleration을 통해 tensor 연산을 효율적으로 수행하는 방법까지 함께 소개

* [Tensor 다루기 기초 - PyTorch 중심](https://ds31x.tistory.com/389)

## Autograd

Autograd는

* reverse mode automatic differentiation을 구현하여
* Back-propagation learning에서 필요한 backward pass,
* 즉 computational graph를 따라 gradient를 자동으로 계산하는 과정을 수행하는 도구임.

참고: [backpropagation](https://dsaint31.me/mkdocs_site/ML/ch08/back_propagation/)

* [PyTorch: Autograd](https://ds31x.tistory.com/227)
* [Autograd : In-place 연산](https://ds31x.tistory.com/690)
* [autograd 심화: grad_fn 과 custom operation 만들기](https://ds31x.tistory.com/408)
