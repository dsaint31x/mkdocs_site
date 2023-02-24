# Feature란?

ML에서 feature는 data sample이 가지고 있는 한가지 특징이라고 할 수 있다. 
보통 training dataset들은 여러 data sample (혹은 data point)들로 구성되며, 각각의 data sample은 여러 특징으로 구성된다.
ML에서는 하나의 data sample을 vector로 표현하게 되는데, vector란 숫자들의 ordered list이다. 
vector를 이루는 각 숫자 하나 하나가 해당 data sample이 가지고 있는 feature라고 생각할 수 있다. 
예를 들어, 한 학생을 나타내는 data sample은 나이, 학번, 몸무게, 성적을 나타내는 4개의 숫자로 구성된 vector로 표시될 수 있다. 이 경우 feature가 4개이다.

Dataset은 matrix로 표현되며, 일반적으로 row는 data sample에 해당하며, column은 data sample이 가지고 있는 각각의 feature에 해당한다.

## Feature 와 Attribute의 차이

Attribute는 dataset에서 나타내는 column의 종류(or type)를 가르킬 때 많이 사용된다. 앞서 예에서 나이, 학번, 몸무게, 성적 과 같은 column의 title이 바로 attribute라고 불린다.

반면, feature는 해당 type을 가르키는데 사용되기도 하지만, 특정 data sample의 해당 type에 할당된 value를 가르키는데에도 사용된다. 

요약하면 attribute는 type만을 가르킬 때 사용되며, feature는 type과 value를 둘 다 가르킬 수 있다. 하지만 많은 경우 혼재되어 사용되므로 context에 맞춰 해석해야한다.

## Feature vector와 representation

Representation, Feature Descritor (or description), feature vector등은 ML에서 input data에 해당하는 vector를 가르키기도 하지만, feature engineering이나 Deep learning에서 lower laryer들로부터 얻어진 현재 task를 가장 잘 수행할 수 있도록 추출된 temporary data들을 가르키는 경우도 많다.

Deep learning의 경우, raw data를 input으로 그냥 사용하는 경우가 많다. Deep learning model은 자체적으로 data로부터 적절한 feature vector를 추출해낸다. 하지만 classical ML 알고리즘들의 경우, task를 잘 수행하기 위해서는 model에게 적절한 feature vector로 input을 변환시켜서 입력해야하는 경우가 대다수이다.

때문에 representation이나 feature vector가 input을 가르키는 경우는 Deep Learning에서 많고, ML에서는 feature extractor등을 거친 데이터를 가르키는 경우도 많다.

## Data sample과 Data point.

Dataset에서 한 case, 또는 한 샘플의 데이터가 vector로 표현되는게 ML에서는 일반적이다. vector는 가지고 있는 숫자의 갯수 (number of elements)를 차원이라고 부르며, 해당 vector는 해당 차원수의 vector space에서의 한 point라고 정의할 수 있다.

쉬운 예로 3개의 숫자를 가진 vector는 3차원 공간에서의 특정 위치를 나타내는 position vector라고 생각할 수 있다 (물리시간에 배운 위치벡터를 생각해보자). 이는 다차원 공간으로 확장이 가능하다. 즉, vector space는 일종의 vector들의 set이라고 봐도 된다 (vector addition과 scalar multiple과 같이 해당 set에 닫힌 연산들이 정의되고, 몇가지 axiom들을 만족해야하는 수학적 정의가 있긴 하자민, 일단 set이라고 해도 틀린 건 아님). 

때문에, 하나의 sample을 가르켜서 data point라고도 많이 애기하게 된다.