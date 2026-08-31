---
title: "PyTorch nn.RNNCell and nn.RNN"
description: "PyTorch의 nn.RNNCell과 nn.RNN의 기본 사용법과 두 module의 동등한 recurrent computation을 확인하는 tutorial."
categories:
  - Deep Learning
  - PyTorch
tags:
  - PyTorch
  - RNN
  - RNNCell
  - Recurrent Neural Network
---

# PyTorch `nn.RNNCell`과 `nn.RNN`

PyTorch는 Simple RNN을 구현하기 위한 두 모듈을 제공한다.

- `nn.RNNCell`
  
  한 시점의 순환 연산을 수행한다. 전체 시퀀스를 처리하려면 반복문과 hidden state 전달을 직접 작성해야 한다.

- `nn.RNN`
  
  전체 시퀀스의 순환 연산을 수행한다. 시점 반복과 hidden state 전달을 모듈 내부에서 처리한다.

두 모듈이 반환하는 값은 hidden state이다. 별도의 prediction output layer는 포함하지 않는다.

분류나 회귀를 위한 예측값이 필요하면 다음과 같은 출력 층을 추가한다.

```python
output_layer = nn.Linear(hidden_size, output_size)
prediction = output_layer(hidden_state)
```

---


## `nn.RNNCell`

`nn.RNNCell`은 한 시점의 입력과 이전 hidden state를 받아 새로운 hidden state를 계산한다.

### 생성자

```python
nn.RNNCell(
    input_size,              # 각 시점의 입력 feature 수
    hidden_size,             # hidden state의 feature 수
    bias=True,               # bias 사용 여부
    nonlinearity="tanh",     # 활성화 함수: "tanh" 또는 "relu"
    device=None,             # parameter를 생성할 device
    dtype=None,              # parameter의 data type
)
```

### 한 시점 처리

```python
import torch
from torch import nn

batch_size = 4
input_size = 3
hidden_size = 5

rnn_cell = nn.RNNCell(
    input_size=input_size,
    hidden_size=hidden_size,
)

X_t = torch.randn(batch_size, input_size)
H_prev = torch.zeros(batch_size, hidden_size)

H_t = rnn_cell(X_t, H_prev)
```

Tensor shape은 다음과 같다.

```text
X_t:     (batch_size, input_size)   = (4, 3)
H_prev:  (batch_size, hidden_size)  = (4, 5)
H_t:     (batch_size, hidden_size)  = (4, 5)
```

<svg viewBox="0 0 760 260" width="100%" role="img" aria-labelledby="rnncell-title rnncell-desc" xmlns="http://www.w3.org/2000/svg">
  <title id="rnncell-title">RNNCell의 한 시점 데이터 흐름</title>
  <desc id="rnncell-desc">현재 입력 X_t와 이전 hidden state H_(t-1)가 RNNCell에 들어가 새로운 hidden state H_t가 나온다.</desc>
  <defs>
    <marker id="rnncell-arrow" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor" />
    </marker>
  </defs>
  <g fill="none" stroke="currentColor" stroke-width="2">
    <rect x="42" y="42" width="150" height="58" rx="9" />
    <rect x="42" y="160" width="150" height="58" rx="9" />
    <rect x="300" y="94" width="168" height="72" rx="10" />
    <rect x="570" y="101" width="150" height="58" rx="9" />
    <path d="M 192 71 C 238 71, 252 105, 300 118" marker-end="url(#rnncell-arrow)" />
    <path d="M 192 189 C 238 189, 252 155, 300 142" marker-end="url(#rnncell-arrow)" />
    <line x1="468" y1="130" x2="570" y2="130" marker-end="url(#rnncell-arrow)" />
  </g>
  <g fill="currentColor" font-family="sans-serif" text-anchor="middle">
    <text x="117" y="67" font-size="18">현재 입력</text>
    <text x="117" y="89" font-size="17">X<tspan baseline-shift="sub" font-size="12">t</tspan></text>
    <text x="117" y="185" font-size="18">이전 hidden state</text>
    <text x="117" y="207" font-size="17">H<tspan baseline-shift="sub" font-size="12">t−1</tspan></text>
    <text x="384" y="137" font-size="20">RNNCell</text>
    <text x="645" y="126" font-size="18">새 hidden state</text>
    <text x="645" y="148" font-size="17">H<tspan baseline-shift="sub" font-size="12">t</tspan></text>
  </g>
</svg>

반환값

```text
H_t
```

* 이 값은 새로운 hidden state이다. 
* 분류 점수나 회귀값과 같은 prediction output이 아니다.

### 전체 시퀀스 처리

`nn.RNNCell`은 한 번 호출할 때 한 시점만 처리한다.  
전체 시퀀스는 반복문으로 처리한다.

```python
batch_size = 4
sequence_length = 10
input_size = 3
hidden_size = 5

X = torch.randn(batch_size, sequence_length, input_size)
H = torch.zeros(batch_size, hidden_size)

hidden_states = []

for X_t in X.unbind(dim=1):
    H = rnn_cell(X_t, H)
    hidden_states.append(H)

H_all = torch.stack(hidden_states, dim=1)
```

* `H_all` : 모든 시점의 hidden state가 저장된다.
* `H` : 마지막 시점의 hidden state가 저장된다.

각각의 dimension은 다음과 같음:

```text
X:      (batch_size, sequence_length, input_size)
H_all:  (batch_size, sequence_length, hidden_size)
H:      (batch_size, hidden_size)
```

---

### Prediction output 추가

`nn.RNNCell`

hidden state를 prediction으로 바꾸는 출력 층이 없다.

예측값이 필요하면 다음 층을 별도로 추가한다.

```text
nn.Linear
```

다음 모델은 RNNCell과 prediction output weight를 하나의 모듈로 구현한다.

```python
import torch
from torch import nn


class RNNCellModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()

        self.hidden_size = hidden_size

        # input과 이전 hidden state로 새 hidden state를 계산
        self.rnn_cell = nn.RNNCell(
            input_size=input_size,
            hidden_size=hidden_size,
        )

        # hidden state를 prediction으로 변환하는 output weights
        self.output_layer = nn.Linear(
            in_features=hidden_size,
            out_features=output_size,
        )

    def forward(self, X, H_0=None):
        batch_size = X.size(0)

        if H_0 is None:
            H = X.new_zeros(batch_size, self.hidden_size)
        else:
            H = H_0

        hidden_states = []
        predictions = []

        for X_t in X.unbind(dim=1):
            H = self.rnn_cell(X_t, H)
            Y_t = self.output_layer(H)

            hidden_states.append(H)
            predictions.append(Y_t)

        H_all = torch.stack(hidden_states, dim=1)
        Y_all = torch.stack(predictions, dim=1)

        return Y_all, H_all, H
```

사용 방법:

```python
model = RNNCellModel(
    input_size=3,
    hidden_size=5,
    output_size=2,
)

X = torch.randn(4, 10, 3)
Y_all, H_all, H_last = model(X)
```

각각의 Tensor shape 는 다음과 같음:

```text
X:       (batch_size, sequence_length, input_size)
H_all:   (batch_size, sequence_length, hidden_size)
H_last:  (batch_size, hidden_size)
Y_all:   (batch_size, sequence_length, output_size)
```

Prediction output의 학습 가능한 parameter 는 다음과 같음:

```python
model.output_layer.weight  # (output_size, hidden_size)
model.output_layer.bias    # (output_size,)
```

각 시점의 prediction 계산:

```text
Y_t = H_t @ output_layer.weight.T + output_layer.bias
```

<svg viewBox="0 0 820 190" width="100%" role="img" aria-labelledby="cell-output-title cell-output-desc" xmlns="http://www.w3.org/2000/svg">
  <title id="cell-output-title">RNNCell과 별도의 출력 층</title>
  <desc id="cell-output-desc">RNNCell은 hidden state를 반환하고 별도의 Linear 층이 hidden state를 prediction으로 변환한다.</desc>
  <defs>
    <marker id="cell-output-arrow" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor" />
    </marker>
  </defs>
  <g fill="none" stroke="currentColor" stroke-width="2">
    <rect x="35" y="64" width="155" height="62" rx="10" />
    <rect x="275" y="64" width="155" height="62" rx="10" />
    <rect x="515" y="64" width="130" height="62" rx="10" stroke-dasharray="7 5" />
    <rect x="710" y="64" width="75" height="62" rx="10" stroke-dasharray="7 5" />
    <line x1="190" y1="95" x2="275" y2="95" marker-end="url(#cell-output-arrow)" />
    <line x1="430" y1="95" x2="515" y2="95" marker-end="url(#cell-output-arrow)" />
    <line x1="645" y1="95" x2="710" y2="95" marker-end="url(#cell-output-arrow)" />
  </g>
  <g fill="currentColor" font-family="sans-serif" text-anchor="middle">
    <text x="112" y="102" font-size="19">RNNCell</text>
    <text x="352" y="88" font-size="18">hidden state</text>
    <text x="352" y="111" font-size="17">H<tspan baseline-shift="sub" font-size="12">t</tspan></text>
    <text x="580" y="88" font-size="18">별도 추가</text>
    <text x="580" y="111" font-size="17">nn.Linear</text>
    <text x="747" y="88" font-size="18">prediction</text>
    <text x="747" y="111" font-size="17">Y<tspan baseline-shift="sub" font-size="12">t</tspan></text>
  </g>
</svg>

점선으로 표시한 부분은 모듈 외부에 별도로 추가한 부분이다.

---

## `nn.RNN`

`nn.RNN`

* 전체 시퀀스를 한 번에 처리한다. 
* 시점 반복과 hidden state 전달은 모듈 내부에서 수행된다.

### 생성자

```python
nn.RNN(
    input_size,              # 각 시점의 입력 feature 수
    hidden_size,             # hidden state의 feature 수
    num_layers=1,            # 쌓을 recurrent layer 수
    nonlinearity="tanh",     # 활성화 함수: "tanh" 또는 "relu"
    bias=True,               # bias 사용 여부
    batch_first=False,       # batch 차원을 첫 번째로 둘지 여부
    dropout=0.0,             # 마지막 층을 제외한 층 사이의 dropout 확률
    bidirectional=False,     # 양방향 RNN 사용 여부
    device=None,             # parameter를 생성할 device
    dtype=None,              # parameter의 data type
)
```

### 전체 시퀀스 처리

다음 예제는 batch 차원을 첫 번째로 배치한다.

```python
import torch
from torch import nn

batch_size = 4
sequence_length = 10
input_size = 3
hidden_size = 5

rnn = nn.RNN(
    input_size=input_size,
    hidden_size=hidden_size,
    batch_first=True,
)

X = torch.randn(batch_size, sequence_length, input_size)
H_0 = torch.zeros(1, batch_size, hidden_size)

output, H_n = rnn(X, H_0)
```

각 tensor의 dimension은 다음과 같음:

```text
X:       (batch_size, sequence_length, input_size)
H_0:     (num_layers, batch_size, hidden_size)
output:  (batch_size, sequence_length, hidden_size)
H_n:     (num_layers, batch_size, hidden_size)
```

위 shape은 다음 설정을 기준으로 함:

```text
num_layers = 1
bidirectional = False
batch_first = True
```

<svg viewBox="0 0 900 280" width="100%" role="img" aria-labelledby="rnn-title rnn-desc" xmlns="http://www.w3.org/2000/svg">
  <title id="rnn-title">RNN의 시퀀스 데이터 흐름</title>
  <desc id="rnn-desc">입력 시퀀스와 초기 hidden state가 RNN으로 들어가 모든 시점의 hidden state와 마지막 hidden state가 반환된다.</desc>
  <defs>
    <marker id="rnn-arrow" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor" />
    </marker>
  </defs>
  <g fill="none" stroke="currentColor" stroke-width="2">
    <rect x="35" y="45" width="190" height="62" rx="10" />
    <rect x="35" y="173" width="190" height="62" rx="10" />
    <rect x="340" y="92" width="185" height="96" rx="12" />
    <rect x="660" y="45" width="205" height="62" rx="10" />
    <rect x="660" y="173" width="205" height="62" rx="10" />
    <path d="M 225 76 C 280 76, 294 111, 340 122" marker-end="url(#rnn-arrow)" />
    <path d="M 225 204 C 280 204, 294 169, 340 158" marker-end="url(#rnn-arrow)" />
    <path d="M 525 122 C 575 111, 600 76, 660 76" marker-end="url(#rnn-arrow)" />
    <path d="M 525 158 C 575 169, 600 204, 660 204" marker-end="url(#rnn-arrow)" />
  </g>
  <g fill="currentColor" font-family="sans-serif" text-anchor="middle">
    <text x="130" y="70" font-size="18">입력 시퀀스</text>
    <text x="130" y="94" font-size="17">X</text>
    <text x="130" y="198" font-size="18">초기 hidden state</text>
    <text x="130" y="222" font-size="17">H<tspan baseline-shift="sub" font-size="12">0</tspan></text>
    <text x="432" y="132" font-size="21">RNN</text>
    <text x="432" y="159" font-size="16">시점 반복 내장</text>
    <text x="762" y="70" font-size="18">시점별 hidden states</text>
    <text x="762" y="94" font-size="17">output</text>
    <text x="762" y="198" font-size="18">마지막 hidden state</text>
    <text x="762" y="222" font-size="17">H<tspan baseline-shift="sub" font-size="12">n</tspan></text>
  </g>
</svg>

반환값은 다음과 같음:

```python
output, H_n = rnn(X, H_0)
```

* `output` : 
    * 마지막 recurrent layer가 각 시점에서 만든 hidden state를 모은 tensor이다.
    * 여기서 변수 이름의 output은 prediction output을 뜻하지 않는다.
* `H_n` : 각 recurrent layer와 각 방향의 마지막 hidden state를 모은 tensor이다.

`nn.RNN` 도 별도의 prediction output layer가 없다.

### Multi-layer RNN

`num_layers`는 쌓을 recurrent layer의 수를 지정한다.

다음은 2개의 recurrent layer를 쌓은 RNN이다.

```python
rnn = nn.RNN(
    input_size=3,
    hidden_size=5,
    num_layers=2,
    batch_first=True,
)
```

첫 번째 recurrent layer는 입력 시퀀스를 처리한다.

두 번째 recurrent layer는 첫 번째 층이 모든 시점에서 만든 hidden state를 입력으로 받는다.

<svg viewBox="0 0 820 340" width="100%" role="img" aria-labelledby="multilayer-rnn-title multilayer-rnn-desc" xmlns="http://www.w3.org/2000/svg">
  <title id="multilayer-rnn-title">2층 RNN의 데이터 흐름</title>
  <desc id="multilayer-rnn-desc">입력 시퀀스가 첫 번째 recurrent layer를 통과하고 첫 번째 층의 시점별 hidden state가 두 번째 recurrent layer의 입력이 된다. 두 번째 층의 시점별 hidden state가 output으로 반환된다.</desc>
  <defs>
    <marker id="multilayer-rnn-arrow" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor" />
    </marker>
  </defs>
  <g fill="none" stroke="currentColor" stroke-width="2">
    <rect x="280" y="252" width="260" height="60" rx="10" />
    <rect x="280" y="143" width="260" height="70" rx="10" />
    <rect x="280" y="34" width="260" height="70" rx="10" />
    <rect x="640" y="39" width="145" height="60" rx="10" />
    <line x1="410" y1="252" x2="410" y2="213" marker-end="url(#multilayer-rnn-arrow)" />
    <line x1="410" y1="143" x2="410" y2="104" marker-end="url(#multilayer-rnn-arrow)" />
    <line x1="540" y1="69" x2="640" y2="69" marker-end="url(#multilayer-rnn-arrow)" />
  </g>
  <g fill="currentColor" font-family="sans-serif" text-anchor="middle">
    <text x="410" y="289" font-size="19">입력 시퀀스 X</text>
    <text x="410" y="173" font-size="20">recurrent layer 1</text>
    <text x="410" y="196" font-size="15">시점별 hidden states</text>
    <text x="410" y="64" font-size="20">recurrent layer 2</text>
    <text x="410" y="87" font-size="15">시점별 hidden states</text>
    <text x="712" y="76" font-size="19">output</text>
  </g>
</svg>

반환값의 의미는 다음과 같다.

* `output`
    * 마지막 recurrent layer의 모든 시점별 hidden state
* `H_n[0]`
    * 첫 번째 recurrent layer의 마지막 hidden state
* `H_n[1]`
    * 두 번째 recurrent layer의 마지막 hidden state

2층 단방향 RNN의 tensor shape은 다음과 같다.

```text
X:       (batch_size, sequence_length, input_size)
H_0:     (2, batch_size, hidden_size)
output:  (batch_size, sequence_length, hidden_size)
H_n:     (2, batch_size, hidden_size)
```

각 recurrent layer는 독립적인 parameter를 가진다.

```text
첫 번째 recurrent layer:
weight_ih_l0:  (hidden_size, input_size)
weight_hh_l0:  (hidden_size, hidden_size)
bias_ih_l0:    (hidden_size)
bias_hh_l0:    (hidden_size)

두 번째 recurrent layer:
weight_ih_l1:  (hidden_size, hidden_size)
weight_hh_l1:  (hidden_size, hidden_size)
bias_ih_l1:    (hidden_size)
bias_hh_l1:    (hidden_size)
```

`dropout`이 0보다 크면 마지막 recurrent layer를 제외한 층 사이에 적용된다.

---

### 단방향과 양방향 설정의 shape

다음은 단방향 설정이다.

```python
bidirectional=False
batch_first=True
```

단방향 RNN의 shape은 다음과 같다.

```text
X:       (batch_size, sequence_length, input_size)
H_0:     (num_layers, batch_size, hidden_size)
output:  (batch_size, sequence_length, hidden_size)
H_n:     (num_layers, batch_size, hidden_size)
```

다음은 양방향 설정이다.

```python
bidirectional=True
batch_first=True
```

양방향 RNN의 shape은 다음과 같다.

```text
X:       (batch_size, sequence_length, input_size)
H_0:     (2 * num_layers, batch_size, hidden_size)
output:  (batch_size, sequence_length, 2 * hidden_size)
H_n:     (2 * num_layers, batch_size, hidden_size)
```

정방향과 역방향의 hidden state가 함께 저장되므로 관련 차원의 크기가 두 배가 된다.

`batch_first`는 `X`와 `output`의 차원 순서만 바꾼다. `H_0`과 `H_n`의 차원 순서에는 영향을 주지 않는다.


### Prediction output 추가

다음 모델은 RNN과 prediction output weight를 하나의 모듈로 구현한다.

```python
import torch
from torch import nn


class RNNModel(nn.Module):
    def __init__(
        self,
        input_size,
        hidden_size,
        output_size,
        num_layers=1,
        bidirectional=False,
    ):
        super().__init__()

        # 전체 시퀀스의 hidden states를 계산
        self.rnn = nn.RNN(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=bidirectional,
        )

        if bidirectional:
            recurrent_output_size = 2 * hidden_size
        else:
            recurrent_output_size = hidden_size

        # hidden states를 predictions로 변환하는 output weights
        self.output_layer = nn.Linear(
            in_features=recurrent_output_size,
            out_features=output_size,
        )

    def forward(self, X, H_0=None):
        hidden_states, H_n = self.rnn(X, H_0)
        predictions = self.output_layer(hidden_states)

        return predictions, hidden_states, H_n
```

사용 방법:

```python
model = RNNModel(
    input_size=3,
    hidden_size=5,
    output_size=2,
    num_layers=2,
    bidirectional=False,
)

X = torch.randn(4, 10, 3)
Y_all, H_all, H_n = model(X)
```

Tensor shape:

```text
X:      (batch_size, sequence_length, input_size)
H_all:  (batch_size, sequence_length, hidden_size)
H_n:    (2, batch_size, hidden_size)
Y_all:  (batch_size, sequence_length, output_size)
```

Prediction output의 학습 가능한 parameter:

```python
model.output_layer.weight  # (output_size, hidden_size)
model.output_layer.bias    # (output_size,)
```

위 parameter shape은 단방향 설정을 기준으로 한다.

양방향 설정에서는 정방향과 역방향 hidden state가 결합되므로 다음 shape을 사용한다.

```text
model.output_layer.weight:  (output_size, 2 * hidden_size)
model.output_layer.bias:    (output_size)
```

각 시점의 prediction 계산:

```text
Y_t = H_t @ output_layer.weight.T + output_layer.bias
```

단방향 RNN에서 마지막 recurrent layer의 최종 hidden state만 사용하려면 다음과 같이 구현한다.

```python
H_last = H_n[-1]
Y_last = model.output_layer(H_last)
```

```text
H_last:  (batch_size, hidden_size)
Y_last:  (batch_size, output_size)
```

양방향 RNN에서는 마지막 recurrent layer의 정방향 최종 state와 역방향 최종 state를 결합한다.

```python
bidirectional_model = RNNModel(
    input_size=3,
    hidden_size=5,
    output_size=2,
    num_layers=2,
    bidirectional=True,
)

Y_all, H_all, H_n = bidirectional_model(X)

# H_n: (2 * num_layers, batch_size, hidden_size)
H_n_by_layer = H_n.reshape(
    bidirectional_model.rnn.num_layers,
    2,
    H_n.size(1),
    bidirectional_model.rnn.hidden_size,
)

H_forward = H_n_by_layer[-1, 0]
H_backward = H_n_by_layer[-1, 1]
H_last = torch.cat((H_forward, H_backward), dim=-1)

Y_last = bidirectional_model.output_layer(H_last)
```

```text
H_forward:  (batch_size, hidden_size)
H_backward: (batch_size, hidden_size)
H_last:     (batch_size, 2 * hidden_size)
Y_last:     (batch_size, output_size)
```

<svg viewBox="0 0 850 190" width="100%" role="img" aria-labelledby="rnn-output-title rnn-output-desc" xmlns="http://www.w3.org/2000/svg">
  <title id="rnn-output-title">RNN과 별도의 출력 층</title>
  <desc id="rnn-output-desc">RNN은 hidden states를 반환하고 별도의 Linear 층이 이를 prediction으로 변환한다.</desc>
  <defs>
    <marker id="rnn-output-arrow" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor" />
    </marker>
  </defs>
  <g fill="none" stroke="currentColor" stroke-width="2">
    <rect x="35" y="64" width="145" height="62" rx="10" />
    <rect x="260" y="64" width="190" height="62" rx="10" />
    <rect x="535" y="64" width="135" height="62" rx="10" stroke-dasharray="7 5" />
    <rect x="750" y="64" width="75" height="62" rx="10" stroke-dasharray="7 5" />
    <line x1="180" y1="95" x2="260" y2="95" marker-end="url(#rnn-output-arrow)" />
    <line x1="450" y1="95" x2="535" y2="95" marker-end="url(#rnn-output-arrow)" />
    <line x1="670" y1="95" x2="750" y2="95" marker-end="url(#rnn-output-arrow)" />
  </g>
  <g fill="currentColor" font-family="sans-serif" text-anchor="middle">
    <text x="107" y="102" font-size="20">RNN</text>
    <text x="355" y="88" font-size="18">시점별 hidden states</text>
    <text x="355" y="111" font-size="17">output</text>
    <text x="602" y="88" font-size="18">별도 추가</text>
    <text x="602" y="111" font-size="17">nn.Linear</text>
    <text x="787" y="88" font-size="18">prediction</text>
    <text x="787" y="111" font-size="17">Y</text>
  </g>
</svg>

점선으로 표시한 부분은 모듈 외부에 별도로 추가한 부분이다.

## 동일한 가중치로 `nn.RNNCell`과 `nn.RNN` 비교

단일 층, 단방향, 동일한 활성화 함수를 사용하면 두 모듈은 같은 순환 연산을 수행할 수 있다.

정확한 비교를 위해 두 모듈의 가중치와 bias를 동일하게 만든다.

```python
import torch
from torch import nn

torch.manual_seed(0)

batch_size = 4
sequence_length = 10
input_size = 3
hidden_size = 5

X = torch.randn(batch_size, sequence_length, input_size)
H_0 = torch.zeros(batch_size, hidden_size)

rnn = nn.RNN(
    input_size=input_size,
    hidden_size=hidden_size,
    num_layers=1,
    nonlinearity="tanh",
    bias=True,
    batch_first=True,
    bidirectional=False,
)

rnn_cell = nn.RNNCell(
    input_size=input_size,
    hidden_size=hidden_size,
    bias=True,
    nonlinearity="tanh",
)

with torch.no_grad():
    rnn_cell.weight_ih.copy_(rnn.weight_ih_l0)
    rnn_cell.weight_hh.copy_(rnn.weight_hh_l0)
    rnn_cell.bias_ih.copy_(rnn.bias_ih_l0)
    rnn_cell.bias_hh.copy_(rnn.bias_hh_l0)

# RNNCell로 시퀀스를 직접 순회
H_cell = H_0.clone()
cell_hidden_states = []

for X_t in X.unbind(dim=1):
    H_cell = rnn_cell(X_t, H_cell)
    cell_hidden_states.append(H_cell)

cell_output = torch.stack(cell_hidden_states, dim=1)

# RNN으로 전체 시퀀스를 한 번에 처리
rnn_output, H_rnn = rnn(X, H_0.unsqueeze(0))

print(torch.allclose(cell_output, rnn_output))
print(torch.allclose(H_cell.unsqueeze(0), H_rnn))
```

실행 결과:

```text
True
True
```

첫 번째 결과는 모든 시점의 hidden state가 같음을 나타낸다.

두 번째 결과는 마지막 hidden state가 같음을 나타낸다.

두 모듈의 핵심 차이는 순환 계산식이 아니라 시퀀스 반복을 누가 담당하는지에 있다.

| 항목 | `nn.RNNCell` | `nn.RNN` |
|---|---|---|
| 한 번에 처리하는 범위 | 한 시점 | 전체 시퀀스 |
| 시점 반복 | 직접 작성 | 모듈 내부에서 처리 |
| 주 반환값 | 새 hidden state | 시점별 hidden states와 마지막 hidden state |
| 여러 recurrent layer | 직접 구성 | `num_layers`로 구성 |
| 양방향 처리 | 직접 구성 | `bidirectional=True`로 구성 |
| prediction output layer | 포함하지 않음 | 포함하지 않음 |

세밀한 시점별 제어가 필요하면 `nn.RNNCell`이 적합하다.

일반적인 시퀀스 처리가 목적이면 `nn.RNN`이 간결하다.
