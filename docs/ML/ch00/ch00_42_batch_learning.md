# Batch Learning

* Batch Learning은 가용한 데이터를 모두 사용(test data 등을 직접 본다는 의미는 아님)하여 훈련.
* Offline Learning으로 불림.

일반적으로 정해진 주기마다 훈련시켜, 새 모델로 교체하는 형태를 취함.


서비스로 사용되는 ML들의 경우, Incremental Learning 을 취하는 경우가 많아지고 있으나, quality 보장이 쉽지 않은 측면이 있어서 여전히 batch learning 이 선호되는 경우가 많음.

> 개인적으로 공부할 때 사용하는 ML은 모두 batch learning이라고 보면 된다.
