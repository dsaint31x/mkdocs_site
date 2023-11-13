# Hyper-Parameters in DL

일반적으로 Deep Learning에서 Hyper-parameters는 다음과 같음.

* the number of (hidden) layers
* the number of neurons in each layer
* the type of activation function in each layer
* the weight initialization algorithm
* the type of optimizer
    * learning rate of optimizer
    * decay constant of optimizer
* the batch size
* and so on.

---

## Number of Layers

모델이 가지고 있는 전체 parameters (=weights + bias)가 같은 경우,  
deeper architecture가 wider architectre 보다  
일반적으로 보다 높은 parameter efficiency를 보인다.

Deeper networks는 Hierarchical Feature Extraction이 가능함.

> Deep Learning (or DNN, Deep Neural Networks)의 장점임!!

* real world의 대부분의 데이터가 low-level structures가 조합되어 higher level structure를 이루는 구조임.
* 때문에 Deep하게 쌓여진 ANN은 hierarchical way로 feature를 추출 및 인식할 수 있게 된다.
    * lower hidden layers model low-level structures (e.g., line segments of various shapes and orientations), 
    * intermediate hidden layers combine these low-level structures to model intermediate-level structures (e.g., squares, circles), and 
    * the highest hidden layers and the output layer combine these intermediate structures to model high-level structures (e.g., faces).

이같은 Hierarchical architecture는 

* 높은 parameter efficiency를 보이기 때문에,
* 보다 적은 수의 training data에서도 학습이 잘 된다.
* (많은 수의 parameters = complex model = 보다 많은 양의 data요구)

또한 ***Transfer Learning이 가능*** 하기 때문에 다른 task로의 변경이 보다 효과적으로 이루어질 수 있음.

> 추가적으로 Training에서 보다 빠른 converge speed를 보임.


## Number of Neurons per Hidden Layer

가급적 같은 수의 Neurons를 가지도록 설계하는 것이 최근 방식임.

* 과거 출력단에 가까울수록 (downstream layers or topper layers) 
* layer의 Neurons의 수가 줄어드는 구조가 MLP등에서 일반적이었으나
* 최근에 같은 수의 neurons를 가지는 layer들로 쌓이는 구조가 보다 효과적인 것으로 여겨짐.

> hyper-parameters의 선택이 보다 쉽다는 장점을 가짐.



일반적으로 over-fitting이 일어나기 직전까지 neurons의 수를 늘림.

* 단, layer의 수를 늘리는게 권장됨.
* 즉, 폭을 넓히는 것보다 깊게 모델의 구조를 만드는게 좋음.