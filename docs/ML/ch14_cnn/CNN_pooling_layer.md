# Pooling Layer

CNN에서  
각 layer별로 입력에 대한 subsample을 출력으로 얻어내게 해주는
layer임.

* CNN에서 계산량과 메모리 사용량을 줄여줌.
* over-fitting 의 위험도(CNN의 translation invairance를 얻게해줌)를 줄여줌.
* down-sampling을 수행!
* global pooling의 경우, flatten layer로 사용됨.

> depth 방향의 pooling을 통해 CNN에 강력한 invariance를 부여해 주는데 사용됨.  
> invariance는 입력의 변화에 상관없이 출력이 나오는 것을 의미함.

---

## Pooling의 종류.

max-pooling과 average-pooling 두 종류가 있음.

---

## Hyper-Parameters

convolutional layer와 달리, 입력과 같은 폭과 크기를 유지할 필요가 없으므로, padding을 하지 않는게 일반적임.

> TensorFlow 에서는 `padding` 파라메터의 기본값이  `valid`로 설정됨.(padding이 이루어지지 않음)

### kernel size

클 경우, over-fitting이 될 확률이 줄어들지만, layer에서의 정보손실이 너무 커짐.

* invariance가 너무 커지게 됨.

---

### stride

일반적으로 non-overlapping pooling이 선호되기 때문에, stride도 kernel size에 따라 정해지는게 일반적임.(kernel size 이상의 stride를 가짐.)

> 많은 CNN 구조에서 Pooling layer를 사용하지만, convolution에서의 stride를 크게 잡아서 subsampling을 수행함으로 pooling layer사용을 대신하는 구조들도 있음.
  


