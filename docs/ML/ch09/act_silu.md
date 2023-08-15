# Sigmoid Linear Unit (SiLU) : from GELU to MiSH

ELU에서 smooth function과 ReLU의 장점을 조합한 것을 넘어서는 성능을 보이며 보다 복잡한 task의 ANN에 많이 사용되는 activation functions는 Swish라는 이름으로 더 유명한 Sigmoid Linear Unit (SiLU)임.

ELU 까지는 activation functions 의 경우 monotonic 과 convex라는 특성을 가지고 있었음. 

하지만 2016년 Gaussian Exponential Linear Unit (GELU)가 등장하면서 기존의 activation functions 이상의 성능을 보임에 따라, montonic 하지 않고 convexity 도 만족하지 않는 복잡한 형태이면서 smooth 한 activation function의 유용성을 확인하게 된다.

Dan Hendrycks and Kevin Gimpel, “Gaussian Error Linear Units (GELUs)”, arXiv preprint arXiv:1606.08415 (2016).

GELU를 제안한 논문에서 등장한 Sigmoid Linear Unit의 경우, 해당 논문에서는 GELU보다 떨어지는 성능을 보였으나, 이후 다음 논문에서 그 높은 활용도를 인정받아 널리 사용되기 시작한다.

Prajit Ramachandran et al., “Searching for Activation Functions”, arXiv preprint arXiv:1710.05941 (2017).

SiLU의 경우, sigmoid function의 input에 $\beta$로 scaling을 하sms 