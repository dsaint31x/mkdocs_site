# Nesterove-accelerated Adaptive Momentum Adam (NADAM)

> NAG와 Adam의 개념을 합친 형태.
> 

NAG에서 사용했던 방식대로 현재 위치에서 다음 위치로 이동할 기울기와 모멘텀 값을 구하는 것이 아닌 모멘텀 값으로 이동한 뒤에 기울기를 구하는 방식.

Adam과 Nag의 장점을 합쳐서 Adam보다 좀 더 빠르고 정확하게 global minimum을 찾아낼 수 있음.

> 일반적으로 `NADAM`이 `Adam`보다 보다 나은 것으로 알려져있으나 일부 dataset에 따라서는 `Adam` 또는 `RMSProp`가 나은 경우도 있음.  
> `RMSProp`, `Adam`, `Nadam` 등이 잘 동작하지 않을 경우 `NAG`도 좋은 대안이 될 수 있음.

## Reference

* [Incorporating Nesterov Momentum into Adam](http://cs229.stanford.edu/proj2015/054_report.pdf)
* [An overview of gradient descent optimization algorithms](https://arxiv.org/abs/1609.04747)