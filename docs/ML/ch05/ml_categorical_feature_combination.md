# Categorical Feature Combination

Categorical data를 다루는 경우에 사용되는 기법으로 information gain을 계산하여 실제 다루는 category의 수를 감소시켜준다.

* information gain이 0이거나 거의 없는 variable들은 data의 dimension만 증가시킬 뿐 information의 관점에서 이득이 없음.
* 이는 data가 가지고 있는 information은 그대로인데 dimension만 커지기 때문에 overfitting이 일어날 확률이 커진다는 것을 의미함.

예를 들어서 두 categorical variable 이 서로 대체가능하다면, 이 둘을 그냥 합친 하나의 categorical variable을 추가하고 기존의 두 variable을 지우는 방식이다.

> combining의 실제 동작은 사실 concatenation으로 이루어진다.  
> categorical variable의 값 문자열을 concatenation으로 묶고 이후 이를 one-hot encoding을 하는 등의 처리가 이루어짐.  
> 조합된 categorical variable의 cardinality가 낮은 경우는 one-hot encoding이 효과적이나 높을 경우엔 label encoding등이 사용되기도 함.

information gain이란 entropy등을 계산해서 특정 column (=categorical variable)을 통해 얻을 수 있는 정보량을 의미한다.

예를 들어, A의 아내는 B라는 정보를 알고 있을 때 A가 기혼자라는 정보는 전혀 information gain이 없다고 할 수 있다.


CatBoost 등에서 사용(이 경우에는 뒤의 One-hot encoding 대신 Ordered Target Encoding이라는 기법을 사용함)되고 있으며, 데이터 전처리 등에서 많이 사용된다. 많은 경우 실제 모델의 성능을 올려주기도 하지만, 그렇지 않은 경우도 있기 때문에 evaluation을 반드시 해봐야한다. 

간단한 tutorial로는 다음 URL을 참고하라.

[How to Improve Machine Learning Model Performance by Combining Categorical Features](https://www.freecodecamp.org/news/improve-machine-learning-model-performance-by-combining-categorical-features/)