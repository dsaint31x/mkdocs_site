---
title: "Group Normalization"
description: "Group Normalization의 동작 원리와 BN·LN의 차이 및 PyTorch 비교 예제"
tags:
  - deep learning
  - normalization
  - group normalization
  - batch normalization
  - layer normalization
  - regularization
  - cnn
  - transformer
  - pytorch
---

# Group Normalization

**Group Normalization (GN)** 은  
* **Yuxin Wu와 Kaiming He가 2018년 ECCV에서 발표한 normalization 기법**. 
* 각 sample의 channel을 여러 group으로 나누고, 
* **각 group 내부의 channel 및 spatial 축에 걸쳐 mean과 variance를 구하여 normalization함**.

## 사전 지식

* [Solutions for the Gradient Vanishing or Exploding Problem](https://dsaint31.me/mkdocs_site/ML/ch09/sol_gv_ge/)
* [Batch Normalization, 2015](https://dsaint31.me/mkdocs_site/ML/ch09/batch_normalization/)
* [Layer Normalization, 2016](https://ds31x.github.io/wiki/review/LayerNormalization)

## 특징

* **Group 구성 예**: 입력 shape이 `(N, C, H, W) = (8, 32, 16, 16)`이고 group 수가 8인 경우:
    * 각 sample의 32개 channel을 **4개 channel씩 8개 group** 으로 나눔.
        * Group 수는 channel 수의 약수여야 함.
    * 각 group에서 **4 × 16 × 16 = 1,024개 값** 으로 하나의 mean과 variance를 구하여 normalization함.
    * Normalization 이후 **학습 가능한 scale과 bias를 channel별로 적용함**.
    * Batch의 8개 sample은 서로 독립적으로 처리하며, 총 **8 × 8 = 64개 group** 의 통계를 각각 계산함.
* **Batch size와 무관함**: 각 sample에서 독립적으로 통계를 계산하므로, **작은 batch size에서도 안정적으로 동작** 함.
* **BN과의 차이**: 
    * LN과 마찬가지로 batch 구성에 따른 통계 변동이 없으므로, 
    * **BN의 batch 통계 변동에 따른 부수적인 regularization 효과는 GN도 없음**.
* **대표적 활용**:
    * **CNN 기반 object detection 및 segmentation**: 고해상도 영상 등으로 batch size가 제한되는 경우에 활용됨.
    * **U-Net 기반 diffusion model**: 이미지 생성 모델의 convolution block 등에서 사용됨.
* **Group 수에 따른 관계**:
    * **Group 수가 1인 경우**: 
        * `(C, H, W)` 전체로 통계를 계산하므로, **같은 축을 사용하는 LN과 normalization 결과가 같음**. 
        * 단, GN의 scale과 bias는 channel별이므로, sample 별로 적용하는 LN과 파라미터 구조는 다를 수 있음.
    * **Group 수가 channel 수와 같은 경우**: 각 channel의 `(H, W)`로 통계를 계산하므로, **Instance Normalization과 normalization 범위가 같음**.
    
## 일반적인 LN, Transformer의 LN, group 수가 1인 GN의 구분:

* **일반적인 LN**: 각 sample에서 **지정한 feature 축들** 에 걸쳐 mean과 variance를 구하여 normalization함. 
    * **Normalization 범위는 지정한 축에 따라 달라짐.**
    * 예를 들어 입력이 `(N, L, C) = (8, 16, 32)`이고 `(L, C)`를 지정하면, 각 sample의 **16 × 32 = 512개 값** 으로 하나의 mean과 variance를 계산함.
    * Sample별로 독립적으로 처리하므로, 총 **8개** 의 mean과 variance를 각각 계산함.
* **Transformer의 LN**: 입력 `(N, L, C)`에서 **마지막 feature 축인 C만 지정한 LN** 임.
    * 입력이 `(8, 16, 32)`이면, 각 token의 **32개 값** 으로 하나의 mean과 variance를 계산함.
    * Sample과 token별로 독립적으로 처리하므로, 총 **8 × 16 = 128개** 의 mean과 variance를 각각 계산함.
    * **다른 token의 값은 해당 token의 통계 계산에 포함하지 않음**.
* **Group 수가 1인 GN**: 같은 데이터를 `(N, C, L) = (8, 32, 16)`로 배치하면, 각 sample의 **32 × 16 = 512개 값** 으로 하나의 mean과 variance를 계산함.
        * Sample별로 독립적으로 처리하므로, 총 **8개** 의 mean과 variance를 각각 계산함.
        * **모든 token이 하나의 mean과 variance를 공유함**.

따라서 group 수가 1인 GN은 
* 같은 축을 지정한 LN과 normalization 범위가 같지만, 
* Transformer의 token별 LN과는 다름. 

단, 학습 가능한 scale과 bias는 GN에서 channel별로, LN에서 지정한 축의 element별로 적용하므로 파라미터 구조는 다를 수 있음.

## PyTorch 예제

같은 sequence data에  
**BN, 일반 LN, Transformer의 LN, group 수가 1인 GN과 4인 GN** 을 적용하고,  
**training mode와 eval mode의 동작도 비교하는 예제**.

* 입력은 `(N, L, C) = (8, 16, 32)`임.
* BN과 GN에는 `transpose`로 `(N, C, L)` 형태로 전달함.
* **Normalization 범위만 비교하기 위해 학습 가능한 scale과 bias는 비활성화함**.
    * BN과 GN은 **`affine=False`**, LN은 **`elementwise_affine=False`**로 지정함.
    * 기본값은 모두 `True`이며, `False`로 지정하면 scale (`weight`)과 bias (`bias`)를 생성하지 않음.
    * 이때 `.weight`와 `.bias`는 모두 `None`이며, mean과 variance를 이용한 normalization만 수행함.

```python
import torch
from torch import nn

torch.manual_seed(23)

N, L, C = 8, 16, 32
x = torch.randn(N, L, C)
x_ncl = x.transpose(1, 2)  # (N, C, L)

# BN: channel별로 batch와 sequence 축을 함께 사용함.
# affine=False로 학습 가능한 scale과 bias를 생성하지 않음.
bn = nn.BatchNorm1d(C, affine=False)

# 일반 LN: 각 sample의 (L, C) 전체를 사용하도록 지정함.
# elementwise_affine=False로 학습 가능한 scale과 bias를 생성하지 않음.
ln_all = nn.LayerNorm((L, C), elementwise_affine=False)

# Transformer의 LN: 각 token의 C개 feature만 사용함.
ln_token = nn.LayerNorm(C, elementwise_affine=False)

# GN (1 group): 각 sample의 (C, L) 전체를 사용함.
gn1 = nn.GroupNorm(num_groups=1, num_channels=C, affine=False)

# GN (4 groups): channel을 8개씩 4개 group으로 나눔.
# 각 group의 8개 channel과 전체 sequence 위치를 함께 사용함.
G = 4
gn4 = nn.GroupNorm(num_groups=G, num_channels=C, affine=False)

# 각 layer에 필요한 입력 형태를 지정함.
cases = [
    ("BN", bn, x_ncl),
    ("LN (L, C)", ln_all, x),
    ("LN (token)", ln_token, x),
    ("GN (1 group)", gn1, x_ncl),
    ("GN (4 groups)", gn4, x_ncl),
]

# Training mode에서 출력값을 계산함.
train_outputs = {}
for name, layer, data in cases:
    layer.train()
    train_outputs[name] = layer(data)

# 출력 비교를 위해 (N, L, C) 형태로 맞춤.
y_bn = train_outputs["BN"].transpose(1, 2)
y_ln_all = train_outputs["LN (L, C)"]
y_ln_token = train_outputs["LN (token)"]
y_gn1 = train_outputs["GN (1 group)"].transpose(1, 2)
y_gn4_ncl = train_outputs["GN (4 groups)"]
y_gn4 = y_gn4_ncl.transpose(1, 2)


def report(name, y, dims):
    mean = y.mean(dim=dims)
    var = y.var(dim=dims, unbiased=False)

    # 각 normalization 단위에서 계산한 mean과 variance를 확인함.
    # mean의 절댓값과 variance의 1에 대한 차이의 최댓값을 출력함.
    print(
        f"{name:16s} "
        f"통계 shape={tuple(mean.shape)}, "
        f"max |mean|={mean.abs().max().item():.4f}, "
        f"max |var - 1|={(var - 1).abs().max().item():.4f}"
    )


# (N, L, C) 형태에서 각 방식의 normalization 축을 확인함.
report("BN", y_bn, (0, 1))
report("LN (L, C)", y_ln_all, (1, 2))
report("LN (token)", y_ln_token, (2,))
report("GN (1 group)", y_gn1, (1, 2))

# GN (4 groups)는 group별 통계를 확인하기 위해 reshape함.
# (N, C, L)에서 (N, G, C // G, L)로 변환함.
y_gn4_grouped = y_gn4_ncl.reshape(N, G, C // G, L)
report("GN (4 groups)", y_gn4_grouped, (2, 3))

print(
    "LN (L, C)와 GN (1 group)의 결과 일치:",
    torch.allclose(y_ln_all, y_gn1, atol=1e-6),
)

print(
    "모든 layer의 scale과 bias가 None:",
    all(
        layer.weight is None and layer.bias is None
        for _, layer, _ in cases
    ),
)

# 같은 입력에 대해 training mode와 eval mode의 출력을 비교함.
for name, layer, data in cases:
    layer.eval()
    y_eval = layer(data)

    print(
        f"{name}: train/eval 결과 일치:",
        torch.allclose(train_outputs[name], y_eval, atol=1e-6),
    )

# 예상 출력: 소수점 넷째 자리까지 표시한 예시이며, 실제 실행 확인 전임.
#
# BN               통계 shape=(32,), max |mean|=0.0000, max |var - 1|=0.0000
# LN (L, C)        통계 shape=(8,), max |mean|=0.0000, max |var - 1|=0.0000
# LN (token)       통계 shape=(8, 16), max |mean|=0.0000, max |var - 1|=0.0000
# GN (1 group)     통계 shape=(8,), max |mean|=0.0000, max |var - 1|=0.0000
# GN (4 groups)    통계 shape=(8, 4), max |mean|=0.0000, max |var - 1|=0.0000
# LN (L, C)와 GN (1 group)의 결과 일치: True
# 모든 layer의 scale과 bias가 None: True
# BN: train/eval 결과 일치: False
# LN (L, C): train/eval 결과 일치: True
# LN (token): train/eval 결과 일치: True
# GN (1 group): train/eval 결과 일치: True
# GN (4 groups): train/eval 결과 일치: True
#
# 통계 shape은 normalization에 사용한 축들을 축약한 후 남는 shape임.
# BN의 (32,)는 channel별 32쌍의 통계를 의미함.
# LN (L, C)와 GN (1 group)의 (8,)은 sample별 8쌍의 통계를 의미함.
# LN (token)의 (8, 16)은 sample별·token별 총 128쌍의 통계를 의미함.
# GN (4 groups)의 (8, 4)는 sample별·group별 총 32쌍의 통계를 의미함.
#
# max |mean|이 약 0이면 각 normalization 단위의 mean이 약 0임.
# max |var - 1|이 약 0이면 각 normalization 단위의 variance가 약 1임.
# 0.0000은 반올림된 표시이며, 정확히 0이라는 의미는 아님.
# eps 때문에 variance는 정확히 1이 되지는 않음.
#
# LN (L, C)와 GN (1 group)은 scale과 bias가 비활성화된 상태에서
# 동일한 값들을 사용하여 normalization하므로 결과가 허용 오차 내에서 같음.
#
# BN은 training mode에서 현재 batch의 통계를 사용하고,
# eval mode에서는 running statistics를 사용하므로 이 예제의 출력이 다름.
# LN과 GN은 두 mode 모두 현재 입력의 통계를 사용하므로 출력이 같음.
```

입력 데이터 shape: **`(N, L, C) = (8, 16, 32)`**. 
BN과 GN에는 **`(N, C, L) = (8, 32, 16)`**으로 변환하여 전달함.

| 방식 | 통계 계산에 사용하는 값 | Mean·variance 쌍의 수 |
|---|---|---:|
| **BN** | 각 channel에서 batch와 sequence 전체의 **8 × 16 = 128개 값** | 32 |
| **일반 LN: `(L, C)` 지정** | 각 sample에서 **16 × 32 = 512개 값** | 8 |
| **Transformer의 LN: `C` 지정** | 각 token에서 **32개 값** | 128 |
| **GN: group 수 1** | 각 sample에서 **32 × 16 = 512개 값** | 8 |
| **GN: group 수 4** | 각 sample의 각 group에서 **8 × 16 = 128개 값** | 8 × 4 = 32 |

* **일반 LN과 Transformer의 LN은 같은 `nn.LayerNorm`이며, `normalized_shape`로 지정한 normalization 범위가 다름**.
* **GN의 group 수가 4이면 channel 0–7, 8–15, 16–23, 24–31이 각각 하나의 group을 구성함**.
* 각 group은 모든 sequence 위치를 함께 사용하므로 token별 normalization과 다름.

참고로, BN은 training mode와 eval mode가 다른 동작임:

| 방식 | Training mode | Eval mode |
|---|---|---|
| **BN** | 현재 batch의 mean과 variance를 사용함. | 누적한 running mean과 running variance를 사용함. |
| **LN** | 현재 입력에서 지정한 축의 mean과 variance를 사용함. | Training mode와 동일함. |
| **GN** | 현재 입력에서 group별 mean과 variance를 사용함. | Training mode와 동일함. |

* **LN과 GN은 running statistics를 저장하지 않으므로, 같은 입력과 파라미터에 대해 두 mode의 출력이 같음**.
* BN도 **`track_running_stats=False`** 로 설정하면 두 mode 모두 현재 batch의 통계를 사용함.
* **`affine=False`는 BN의 running statistics를 비활성화하는 설정이 아님**: Scale과 bias의 생성 여부만 제어함.
* **`eval()`은 scale과 bias를 비활성화하거나 gradient 계산을 끄는 기능이 아님**.
