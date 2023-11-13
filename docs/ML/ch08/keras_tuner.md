# Keras Tuner

Keras Tuner는 TF 또는 Keras로 구현된 모델에 대해,  
최적의 Hyper-Parameters 를 구할 수 있도록 도와주는 라이브러리임.

## keras_tuner.HyperParameter

***모델의 hyperparameters를 추상화한 객체*** 로서
모델이 hyperparameter tuning 과정에서 취할 수 있는 
특정 범위의 가능한 hyperparameters의 값들을 정의하고 있는 object임.


Keras Tuner는 해당 object의 값들을 기반으로 최적의 Hyper-Parameters를 구함.

아래의 code snippet 은 keras_tuner.Hyperparameter 를 통해,  

* hidden layer의 갯수
* 각 layer의 neuron의 갯수
* learning rate
* optimizer 

등의 hyper parameters에 사용가능한 값들을 지정하고,  
이를 통해 모델을 build하고 compile하여 반환하는 함수를 보여줌.

```Python
import keras_tuner as kt

def build_model(hp):
  # build model.
  n_hidden      = hp.Int("n_hidden",  min_value=0 , max_value=8, default=2)
  n_neurons     = hp.Int("n_neurons", min_value=16, max_value=256)
 
  model = tf.keras.Sequential()
  model.add(tf.keras.layers.Flatten())
  for _ in range(n_hidden):
    model.add(tf.keras.layers.Dense(n_neurons, activation="relu"))
  model.add(tf.keras.layers.Dense(10, activation="softmax"))

  # set optimizer
  learning_rate = hp.Float("learning_rate", 
                           min_value=1e-4, 
                           max_value=1e-2,
                           sampling="log")
  optimizer = hp.Choice("optimizer", values=["sgd", "adam"])
  if optimizer == "sgd":
    optimizer = tf.keras.optimizers.SGD(learning_rate=learning_rate)
  else:
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
  
  # comple model
  model.compile(loss="sparse_categorical_crossentropy", optimizer=optimizer,
                metrics=["accuracy"])
  return model
```

---

## Keras Tuner

위의 `build_model` 함수는 `keras_tuner`의 `RandomSearch`와 같은  
`Tuner Object`에 넘겨지며,
해당 Tuner Object에 의해 각 hyper-parameters의 조합이 테스트 되며,  
이를 바탕으로 최적의 조합의 hyper-parameters를 얻게 된다.

> Keras Tuner 오브젝트에  
> `keras_tuner.HyperModel`의 인스턴스가
> `build_model` 대신 넘겨질 수 있으며,
> 이 경우, data-preprocessing 이나 fit과정 중의 hyper-parameters에 대한  
> tuning이 가능해짐.

가장 기본적인 Tuner Object인 `RandomSearch`를 사용하는 code snippet은 다음과 같음.

```Python
random_search_tuner = kt.RandomSearch(
    build_model, # 앞서 예에서 만든 build and comple model 함수
    objective="val_accuracy", # 시도한 모델간의 성능을 validation set에서의 accuracy로 비교.
    max_trials=5,   # 5번의 시도를 수행한다.
    overwrite=True, # True 시 project_name으로 지정된 디렉토리를 지우고 시작.
    directory="my_fashion_mnist", # 작업이 이루어지는 root directory
    project_name="my_rnd_search", # root directory의 subdirectory로 학습된 모델이 저장됨.
    seed=42
)

# 위의 RandomSearch에서 이어서 작업을 하려면,
# overwrite를 False로 놓고 RandomSearch 의 인스턴스를 얻으면 됨.

# 위의 Tuner 인스턴스로 최적의 hyper-parameters를 찾는 작업 수행.
random_search_tuner.search(
    X_train, y_train, 
    epochs=10,
    validation_data=(X_valid, y_valid)
)
```

---

### search 과정에서 callback 사용하기.

Keras Tuner의 search 메소드 호출에서 `callbacks` 파라메터를 사용하여 callback을 사용가능함.

다음은 `TensorBoard` 와 `EarlyStopping` callback을 사용한 code snippet임.

```Python
root_logdir       = Path(random_search_tuner.project_dir) / "tensorboard"
tensorboard_cb    = tf.keras.callbacks.TensorBoard(root_logdir)
early_stopping_cb = tf.keras.callbacks.EarlyStopping(patience=2)
random_search_tuner.search(X_train, y_train, epochs=10,
                       validation_data=(X_valid, y_valid),
                       callbacks=[early_stopping_cb, tensorboard_cb])
```

* `my_fashion_mnist/my_rnd_search/tensorboard` 디렉토리에 TensorBoard의 log 가 저장됨 (`--logdir`로 지정하여 tensorboard수행.)

---

이후 Tuner 인스턴스의 `get_best_models()` 메소드를 통해 최적의 모델을 얻을 수 있음  
(`num_models` 파라메터를 통해 상위 몇 개를 얻을지 지정가능함.)

```Python
top3_models = random_search_tuner.get_best_models(num_models=3)
best_model = top3_models[0]
```

* 이렇게 얻어진 best model을 사용하기로 결정한 경우,
* test set에서 결과를 구하기 전에
* 전체 training dataset에 대해 다시 훈련을 시켜야 함.

또는 `get_best_hyperparameters()` 메소드를 통해,  
최적의 hyper-parameters 에 대한 `Hyperparameters` 인스턴스를 얻을 수 있음.

```Python
>>> top3_params = random_search_tuner.get_best_hyperparameters(num_trials=3)
>>> top3_params[0].values # best hyperparameter values 의 dictionary 인스턴스.
{'n_hidden': 5,
 'n_neurons': 70,
 'learning_rate': 0.00041268008323824807,
 'optimizer': 'adam'}
```

* 엄밀하게 한다면
* 해당 hyper-parameter로 모델을 build and compile하고
* 이를 전체 training dataset에서 훈련시키고,
* 이를 test set으로 최종 평가해야 한다.

---

## Oracle

Keras Tuner 오브젝트들은 ***Oracle*** 객체에 따라  
최적의 hyper-parameters를 찾기 위한 trial을 수행함.

때문에 각 Keras Tuner의 Oracle 객체를 통해  
최적의 hyper-parameters를 찾은 trial의 세부 정보를 얻을 수도 있음.

```Python
>>> best_trial = random_search_tuner.oracle.get_best_trials(num_trials=1)[0]
>>> best_trial.summary()
Trial summary
Hyperparameters:
n_hidden: 5
n_neurons: 70
learning_rate: 0.00041268008323824807
optimizer: adam
Score: 0.8736000061035156
```

Oracle을 통해 얻은 `trial`에 대한 인스턴스에서 `metrics` 객체를 통해  
해당 시도(trial)에서의 score (or metric)을 확인 가능함.

```Python
>>> best_trial.metrics.get_last_value("val_accuracy")
0.8736000061035156
```

---

## `keras_tuner.HyperModel`

데이터 전처리나 fit 과정 중의 hyper-parameter tuning을 위해 사용됨.

해당 `keras_tuner.HyperModel` 을 상속한 클래스를 만들고,  

* `build` 와 
* `fit` 

메소드를 오버라이드하면서,  
각 메소드에 넘겨지는 `Hyperparameters` 객체를 통해  
모델의 빌드과정이나 fit 과정에서의 hyper-parameter에 따라 다른 처리가 이루어지도록 구현.

다음 code snippet은  
`Hyperparameters`에서 `bool` type인 `normalize`라는 hyper-parameter가 있고, 
이를 통해 훈련데이터가 normalize된 경우와 아닌 경우 에 따른 모델의 성능차를 비교해보고  
보다 나은 hyper-parameter를 구할 수 있음.

> 해당 `HyperModel`을 상속하여 구현한 class의 인스턴스를  
> Keras Tuner 객체에 넘겨 search를 수행하면 됨.

```Python
class MyClassificationHyperModel(kt.HyperModel):
  def build(self, hp):
    return build_model(hp)

  def fit(self, hp, model, X, y, **kwargs):
    if hp.Boolean("normalize"):
      norm_layer = tf.keras.layers.Normalization()
      X = norm_layer(X)
    return model.fit(X, y, **kwargs)
```

위의 `HyerModel`의 subclass 객체를 이용한 Tuning은 다음과 같이 수행가능함.

```Python
random_search_tuner = kt.RandomSearch(
    MyClassificationHyperModel(), # 첫번째 argument로 HyperModel의 subclass 객체 넘겨줌. 
    objective="val_accuracy", # 시도한 모델간의 성능을 validation set에서의 accuracy로 비교.
    max_trials=5,   # 5번의 시도를 수행한다.
    overwrite=True, # True 시 project_name으로 지정된 디렉토리를 지우고 시작.
    directory="my_fashion_mnist", # 작업이 이루어지는 root directory
    project_name="my_rnd_search", # root directory의 subdirectory로 학습된 모델이 저장됨.
    seed=42
)

# 위의 Tuner 인스턴스로 최적의 hyper-parameters를 찾는 작업 수행.
random_search_tuner.search(
    X_train, y_train, 
    epochs=10,
    validation_data=(X_valid, y_valid)
)
```