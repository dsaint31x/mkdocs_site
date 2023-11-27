# Model 저장하기 : Keras

[ref. : Save, serialize, and export models](https://www.tensorflow.org/guide/keras/serialization_and_saving#simple_exporting_with_export)

---

Keras나 Tensorflow의 모델 저장은 다음과 같은 3가지가 현재 지원됨.

* `keras3.0` foramt : JSON (configuration and metadata) 과 H5 (parameters)를 zip으로 묶어 저장되며 확장자가 `.keras`임. (recomended)
* `tf` format : Tensorflow에서 `SaveModel` format이라고 부르는 형태로 directory로 저장을 남김. (`save_format='tf'`)
* `h5` format : Keras의 오래된 H5 fromat으로 `.h5`임. (`save_format='h5'`)

2023.10 현재 권장되는 포맷은 `keras3.0`임.

---

## Keras3.0 에 저장되는 목록.

* `config.json` : Records of model, layer, and other trackables' configuration.
* `model.weights.h5` : 전체 모델의 parameters 를 저장하고 있는 H5-based state file (layers와 이들의 weights들의 dictionary 등을 저장)
* metadata file (JSON) : Keras version 등과 같은 메타데이터.

keras3.0 포맷의 경우, 

다음이 4가지를 위의 3가지 형태로 모두 저장하고 있음.

* model architecture와 configuration : 모델의 구성
* model parameters : weights + bias = state of the model
* optimizer : compile 단계에서 결정됨.
* a set of losses and metrics : compile 단계에서 결정됨.

keras3.0에서 저장하는 것을 크게 나누면, model의 구조(=configuraiton)과 model의 parameter의 값(=state) 두가지로 볼 수 있음.

* Model architecture : Model Serialization 을 통해 저장됨 (model state와 compilation information은 저장되지 않음)
* Model state : `save_weights`와 `load_weights` 등을 이용하며, callback등을 통한 ckpt 저장이 이에 해당.

---

## 사용법.

다음을 통해 저장됨.

```Python
model = ... # Sequential, Functional Model, or Model subclass

model.save('path/to/location.keras')
```

아니면 `tf.keras.models.save_model(model, 'path/to/locaton.keras')`

```Python
tf.keras.saving.save_model(
    model, filepath, overwrite=True, save_format=None, **kwargs
)
```
* `model` : 저장할 Keras 모델
* `filepath` : 파일 저장 경로
* `overwrite` : 덮어쓰기 여부
* `include_optimizer` : True인 경우 optimizer의 상태를 함께 저장

* [ref.](https://www.tensorflow.org/api_docs/python/tf/keras/saving/save_model)

다음을 통해 loading됨.

```Python
model = keras.models.load_model('path/to/location.keras')
```

---

## Model Serialization

Model의 architecture (or configuration)은 다음의 방법들을 통해 Serialization됨.

* `tf.keras.models.clone_model(model)` : model의 copy를 만들어냄 (in-memory cloning).
* `get_config()` and `cls.from_config()` : subclassing을 통해 만든 layer와 model의 configuration (`dict`)을 반환하고, configuration (`dict`) 를 통해 해당하는 instance를 생성.
    * subclass의 `__init__()` method에서 요구되는 arguments를 `get_config()` 메서드에서 반환해야함.
    * loading 하는 경우엔, `from_config(config)` 메서드가 `__init__()`를 적절한 argument와 함께 호출하여 해당 layer나 model을 reconstruction함.
* `tf.keras.models.to_json()` and `tf.keras.models.model_from_json()` : 위와 비슷하지만, JSON 문자열를 통해 이루어짐.
* `tf.keras.saving.serialize_keras_object()` : 임의의 keras object의 설정을 얻어냄.
* `tf.keras.saving.deserialize_keras_object()` : 특정 configuration으로부터 새 keras object의 instance를 재생성.

> 위의 방법들은 model state나 compilation information이 보존되지 않음

---

### Custom Model의 save 와 load.

다음과 같이 `get_config()` 메서드와 `cls.from_config()` 클래스 메서드를 구현함.

* custom layer나 custom model의 경우 반드시 `get_config()` 메서드를 구현해야 한다.
* `__init__()`의 arguments 중, Python의 object가 아닌 것의 경우 반드시 serialization 처리가 `get_config()`에 구현되어있어야 하며, deserialization처리가 `from_config()`에 구현되어야 한다.

```Python
class CustomModel(keras.Model):
    def __init__(self, hidden_units):
        super(CustomModel, self).__init__()
        self.hidden_units = hidden_units
        self.dense_layers = [keras.layers.Dense(u) for u in hidden_units]
    
    def call(self, inputs):
        x = inputs
        for layer in self.dense_layers:
            x = layer(x)
        return x
    
    def get_config(self):
        return {"hidden_units": self.hidden_units}
    
    @classmethod
    def from_config(cls, config):
        return cls(**config)
```

저장하는 방법은 다음과 같음.

```Python
model = CustomModel([16, 16, 10])
# 호출함으로써 모델을 만듭니다
input_arr = tf.random.uniform((1, 5))
outputs = model(input_arr)
model.save("my_model")
```

불러들이는 방법은 다음의 2가지임.

source code가 있는 경우.
```Python
# 선택 1: custom_object 인자로 불러옵니다.
loaded_1 = keras.models.load_model(
    "my_model", custom_objects={"CustomModel": CustomModel}
)
```

source code없이 동적으로 생성.
```Python
# 맞춤 정의된 모델 클래스를 지워
# 불러올 때 접근을 가지지 못하게 보장합니다.
del CustomModel

# 파일로부터 생성.
loaded_2 = keras.models.load_model("my_model")
```

이들이 같은지 확인하는 코드는 다음과 같음.

```Python
import numpy as np

np.testing.assert_allclose(loaded_1(input_arr), outputs)
np.testing.assert_allclose(loaded_2(input_arr), outputs)

print("Original model:", model)
print("Model loaded with custom objects:", loaded_1)
print("Model loaded without the custom object class:", loaded_2)
```

* [ref.](https://www.kaggle.com/code/daddy321/save-and-load-keras-models-ko-ver-tf-guide)