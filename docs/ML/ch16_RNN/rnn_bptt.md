# Simple RNN: Forward Pass, BPTT, and Long-term Dependency Problem

## 1. Simple RNN의 Forward Pass

### 1.1 Forward Computation

이 글에서 사용하는 symbol은 다음과 같음.

- `x_t`: time step `t`의 input vector
- `h_t`: time step `t`의 hidden state vector
- `o_t`: time step `t`의 output vector
- `U`: input-to-hidden weight matrix
- `V`: hidden-to-hidden recurrent weight matrix
- `W`: hidden-to-output weight matrix
- `b_h`: hidden state의 bias vector
- `b_o`: output의 bias vector

Simple RNN의 hidden state update는 다음과 같음:

$$
h_t = f(Ux_t + Vh_{t-1} + b_h)
$$

Output의 계산은 다음과 같음:

$$
o_t = g(Wh_t + b_o)
$$

<!-- Unfolded RNN에서 x_t, h_t, o_t와 shared U, V, W | source: ./figures/01_unfolded_rnn.svg -->
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="520" viewBox="0 0 1200 520" role="img" aria-labelledby="title desc">
  <title id="title">Unfolded RNN과 shared parameter</title>
  <desc id="desc">세 time step의 input, hidden state, output과 공유되는 U, V, W를 나타낸 그림</desc>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#334155"/></marker>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="3" stdDeviation="4" flood-opacity=".12"/></filter>
  </defs>
  <rect width="1200" height="520" rx="24" fill="#f8fafc"/>
  <text x="60" y="55" font-family="Arial, 'Noto Sans KR', sans-serif" font-size="28" font-weight="700" fill="#0f172a">Unfolded RNN: 동일한 U, V, W의 반복 usage</text>
  <g font-family="Arial, 'Noto Sans KR', sans-serif" text-anchor="middle">
    <g stroke="#334155" stroke-width="3" fill="none" marker-end="url(#arrow)">
      <path d="M180 385V315"/><path d="M545 385V315"/><path d="M910 385V315"/>
      <path d="M180 215V145"/><path d="M545 215V145"/><path d="M910 215V145"/>
      <path d="M270 265H455"/><path d="M635 265H820"/>
    </g>
    <g filter="url(#shadow)">
      <g fill="#dbeafe" stroke="#2563eb" stroke-width="3"><rect x="110" y="385" width="140" height="72" rx="16"/><rect x="475" y="385" width="140" height="72" rx="16"/><rect x="840" y="385" width="140" height="72" rx="16"/></g>
      <g fill="#ede9fe" stroke="#7c3aed" stroke-width="3"><rect x="90" y="215" width="180" height="100" rx="22"/><rect x="455" y="215" width="180" height="100" rx="22"/><rect x="820" y="215" width="180" height="100" rx="22"/></g>
      <g fill="#dcfce7" stroke="#16a34a" stroke-width="3"><rect x="110" y="75" width="140" height="70" rx="16"/><rect x="475" y="75" width="140" height="70" rx="16"/><rect x="840" y="75" width="140" height="70" rx="16"/></g>
    </g>
    <g fill="#0f172a" font-size="24" font-weight="700">
      <text x="180" y="430">x<tspan baseline-shift="sub" font-size="16">t−1</tspan></text><text x="545" y="430">x<tspan baseline-shift="sub" font-size="16">t</tspan></text><text x="910" y="430">x<tspan baseline-shift="sub" font-size="16">t+1</tspan></text>
      <text x="180" y="275">h<tspan baseline-shift="sub" font-size="16">t−1</tspan></text><text x="545" y="275">h<tspan baseline-shift="sub" font-size="16">t</tspan></text><text x="910" y="275">h<tspan baseline-shift="sub" font-size="16">t+1</tspan></text>
      <text x="180" y="119">o<tspan baseline-shift="sub" font-size="16">t−1</tspan></text><text x="545" y="119">o<tspan baseline-shift="sub" font-size="16">t</tspan></text><text x="910" y="119">o<tspan baseline-shift="sub" font-size="16">t+1</tspan></text>
    </g>
    <g font-size="20" font-weight="700"><text x="140" y="358" fill="#2563eb">U</text><text x="505" y="358" fill="#2563eb">U</text><text x="870" y="358" fill="#2563eb">U</text><text x="360" y="245" fill="#7c3aed">V</text><text x="725" y="245" fill="#7c3aed">V</text><text x="140" y="187" fill="#16a34a">W</text><text x="505" y="187" fill="#16a34a">W</text><text x="870" y="187" fill="#16a34a">W</text></g>
  </g>
  <rect x="1020" y="125" width="130" height="315" rx="18" fill="#fff" stroke="#cbd5e1" stroke-width="2"/>
  <text x="1085" y="158" text-anchor="middle" font-family="Arial, 'Noto Sans KR', sans-serif" font-size="18" font-weight="700" fill="#0f172a">Shared</text>
  <text x="1085" y="205" text-anchor="middle" font-family="Arial, sans-serif" font-size="28" font-weight="700" fill="#2563eb">U</text><text x="1085" y="230" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="#475569">input→hidden</text>
  <text x="1085" y="295" text-anchor="middle" font-family="Arial, sans-serif" font-size="28" font-weight="700" fill="#7c3aed">V</text><text x="1085" y="320" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="#475569">hidden→hidden</text>
  <text x="1085" y="385" text-anchor="middle" font-family="Arial, sans-serif" font-size="28" font-weight="700" fill="#16a34a">W</text><text x="1085" y="410" text-anchor="middle" font-family="Arial, sans-serif" font-size="14" fill="#475569">hidden→output</text>
  <text x="600" y="495" text-anchor="middle" font-family="Arial, 'Noto Sans KR', sans-serif" font-size="18" fill="#475569">각 위치의 label은 별도 parameter가 아니라 동일한 matrix의 usage를 나타냄</text>
</svg>

### 1.2 Parameter Sharing

모든 time step에서 동일한 parameter를 반복해서 사용함.

- 모든 time step에서 동일한 `U`를 사용함.
- 모든 time step에서 동일한 `V`를 사용함.
- 모든 time step에서 동일한 `W`를 사용함.

따라서 RNN을 time dimension을 따라 unfold하더라도 새로운 weight가 생성되는 것이 아님.

Unfolded computational graph에서 `U_t`, `V_t`, `W_t`처럼 표시할 수는 있지만, 이는 서로 다른 parameter가 아니라 동일한 shared parameter의 서로 다른 **usage** 를 나타냄.

`U`의 usage 사이에 성립하는 관계는 다음과 같음:

$$
U_{t-1} = U_t = U_{t+1} = U
$$

`V`의 usage 사이에 성립하는 관계는 다음과 같음:

$$
V_{t-1} = V_t = V_{t+1} = V
$$

`W`의 usage 사이에 성립하는 관계는 다음과 같음:

$$
W_{t-1} = W_t = W_{t+1} = W
$$

---

### 1.3 Earlier Information이 Hidden State에 유지되는 과정

Time step `k`의 input information은 later time step으로 직접 연결되는 것이 아니라, successive hidden states를 통해 간접적으로 반영됨.

Forward path는 다음과 같음:

$$
x_k \rightarrow h_k \rightarrow h_{k+1} \rightarrow \cdots \rightarrow h_t \rightarrow o_t
$$

<!-- Forward pass에서 earlier information이 hidden-state representation에 유지되는 과정 | source: ./figures/forward_information_retention.svg -->
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="430" viewBox="0 0 1200 430" role="img" aria-labelledby="title desc">
  <title id="title">Forward pass에서 earlier information retention</title>
  <desc id="desc">서로 다른 earlier input을 반영한 hidden-state representation이 successive recurrent state transition을 거치며 서로 구분하기 어려워질 수 있음을 나타낸 그림</desc>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#2563eb"/></marker>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity=".10"/></filter>
  </defs>
  <rect width="1200" height="430" rx="24" fill="#f8fafc"/>
  <text x="55" y="52" font-family="Arial, 'Noto Sans KR', sans-serif" font-size="28" font-weight="700" fill="#0f172a">Forward Pass: Earlier Information Retention</text>
  <g font-family="Arial, 'Noto Sans KR', sans-serif" text-anchor="middle">
    <rect x="55" y="145" width="140" height="86" rx="18" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/><text x="125" y="180" font-size="16" fill="#1e40af">earlier input</text><text x="125" y="213" font-size="26" font-weight="700" fill="#1e3a8a">x<tspan baseline-shift="sub" font-size="15">k</tspan></text>
    <g filter="url(#shadow)" fill="#ede9fe" stroke="#7c3aed" stroke-width="2"><rect x="255" y="135" width="155" height="106" rx="18"/><rect x="500" y="135" width="155" height="106" rx="18"/><rect x="785" y="135" width="155" height="106" rx="18"/></g>
    <g fill="#0f172a" font-size="25" font-weight="700"><text x="332" y="177">h<tspan baseline-shift="sub" font-size="15">k</tspan></text><text x="577" y="177">h<tspan baseline-shift="sub" font-size="15">k+1</tspan></text><text x="862" y="177">h<tspan baseline-shift="sub" font-size="15">t</tspan></text></g>
    <rect x="1010" y="145" width="140" height="86" rx="18" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/><text x="1080" y="180" font-size="16" fill="#166534">current output</text><text x="1080" y="213" font-size="26" font-weight="700" fill="#14532d">o<tspan baseline-shift="sub" font-size="15">t</tspan></text>
    <g stroke="#2563eb" stroke-width="3" fill="none" marker-end="url(#arrow)"><path d="M195 188H255"/><path d="M410 188H500"/><path d="M655 188H785"/><path d="M940 188H1010"/></g>
    <text x="720" y="184" font-size="27" font-weight="700" fill="#64748b">···</text>
    <text x="430" y="291" font-size="15" fill="#475569">sequence A</text><text x="430" y="324" font-size="15" fill="#475569">sequence B</text>
    <g stroke-width="5" stroke-linecap="round"><path d="M500 286H625" stroke="#2563eb"/><path d="M500 319H625" stroke="#06b6d4"/><path d="M785 296H910" stroke="#2563eb"/><path d="M785 309H910" stroke="#06b6d4"/></g>
    <path d="M625 286C690 286 725 294 785 296" fill="none" stroke="#2563eb" stroke-width="2"/><path d="M625 319C690 319 725 311 785 309" fill="none" stroke="#06b6d4" stroke-width="2"/>
    <text x="1020" y="292" font-size="15" fill="#475569">earlier input의 차이가</text><text x="1020" y="315" font-size="15" fill="#475569">later state에서 충분히</text><text x="1020" y="338" font-size="15" fill="#475569">구분되지 않을 수 있음</text>
  </g>
  <rect x="205" y="365" width="790" height="42" rx="21" fill="#ffffff" stroke="#bfdbfe" stroke-width="2"/>
  <text x="600" y="392" text-anchor="middle" font-family="Arial, 'Noto Sans KR', sans-serif" font-size="17" font-weight="700" fill="#1e40af">Earlier information이 successive hidden states에 유지되어야 함</text>
</svg>

각 recurrent step에서는 previous hidden state와 current input을 사용하여 next hidden state를 계산함. 따라서 earlier information은 별도의 storage에 독립적으로 보존되는 것이 아니라, 매 time step에서 새로 계산되는 hidden-state representation 안에 유지되어야 함.

Simple RNN에는 earlier information을 선택적으로 preserve하거나 update하는 gating mechanism과 별도의 memory cell이 없음. Earlier information이 later hidden state까지 유지되는지는 recurrent weight `V`, subsequent input, activation function, 그리고 전체 recurrent state dynamics에 의해 결정됨.

`tanh`와 같은 nonlinear activation이 saturation 영역에 들어가면 서로 다른 pre-activation이 비슷한 hidden-state value로 mapping될 수 있음. 또한 recurrent state transition이 반복되면서 earlier input이 달랐던 두 sequence의 hidden-state representation이 later time step에서 서로 유사해질 수 있음.

이 경우 current hidden state만으로는 earlier input의 차이를 충분히 구분하기 어려우며, current output이 해당 earlier information을 사용하는 것도 어려워짐.

즉 forward pass의 핵심 문제는 **earlier information을 구분하고 사용하는 데 필요한 state representation이 successive recurrent state transition 동안 안정적으로 유지되지 않을 수 있다는 것** 임.

---

## 2. BPTT

### 2.1 Unfolded Computational Graph와 Backward Pass

RNN을 time dimension을 따라 unfold하면 하나의 깊은 computational graph처럼 볼 수 있음.

Forward pass에서는 input과 hidden state가 time step 순서대로 계산됨.

Backward pass에서는 loss에서 시작하여 unfolded computational graph에 **backpropagation** 을 적용함.

Current loss와 earlier time step 사이의 gradient를 계산할 때는 chain rule에 의해 각 recurrent step의 **local gradient가 연속적으로 곱해짐**.

따라서 일반적인 neural network의 backpropagation과 원리는 같지만, RNN에서는 backpropagation이 time dimension을 따라 수행되므로 이를 **Backpropagation Through Time, BPTT** 라고 부름.

### 2.2 Shared Parameter의 Gradient

Forward pass에서 같은 `U`, `V`, `W`가 여러 time step에서 반복해서 사용되므로, backward pass에서는 각 usage에서 해당 shared parameter에 대한 gradient contribution이 발생함.

<!-- 각 time step의 gradient contribution이 shared parameter로 accumulation되는 과정 | source: ./figures/02_gradient_accumulation.svg -->
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="500" viewBox="0 0 1200 500" role="img" aria-labelledby="title desc">
  <title id="title">Shared parameter gradient accumulation</title><desc id="desc">각 time step의 gradient contribution이 합산되어 하나의 shared parameter gradient가 되는 과정</desc>
  <defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#64748b"/></marker></defs>
  <rect width="1200" height="500" rx="24" fill="#f8fafc"/>
  <text x="60" y="55" font-family="Arial, 'Noto Sans KR', sans-serif" font-size="28" font-weight="700" fill="#0f172a">Shared Parameter의 Gradient</text>
  <g font-family="Arial, 'Noto Sans KR', sans-serif" text-anchor="middle">
    <g fill="#ede9fe" stroke="#7c3aed" stroke-width="3"><rect x="60" y="115" width="250" height="100" rx="18"/><rect x="60" y="250" width="250" height="100" rx="18"/><rect x="60" y="385" width="250" height="70" rx="18"/></g>
    <g fill="#0f172a"><text x="185" y="154" font-size="18">usage at time step 1</text><text x="185" y="187" font-size="23" font-weight="700">∂L/∂V |₁</text><text x="185" y="289" font-size="18">usage at time step 2</text><text x="185" y="322" font-size="23" font-weight="700">∂L/∂V |₂</text><text x="185" y="425" font-size="22" font-weight="700">⋮   ∂L/∂V |ₜ</text></g>
    <g stroke="#64748b" stroke-width="3" fill="none" marker-end="url(#a)"><path d="M310 165C430 165 430 240 505 240"/><path d="M310 300C430 300 430 260 505 260"/><path d="M310 420C430 420 430 280 505 280"/></g>
    <circle cx="560" cy="260" r="58" fill="#fff7ed" stroke="#ea580c" stroke-width="4"/><text x="560" y="272" font-size="44" font-weight="700" fill="#ea580c">Σ</text>
    <path d="M618 260H760" stroke="#64748b" stroke-width="3" marker-end="url(#a)"/>
    <rect x="760" y="170" width="370" height="180" rx="24" fill="#dcfce7" stroke="#16a34a" stroke-width="3"/>
    <text x="945" y="217" font-size="19" fill="#166534">one shared parameter</text><text x="945" y="270" font-size="34" font-weight="700" fill="#14532d">∂L/∂V</text><text x="945" y="313" font-size="18" fill="#166534">optimizer가 V를 한 번 update</text>
  </g>
  <text x="600" y="475" text-anchor="middle" font-family="Arial, 'Noto Sans KR', sans-serif" font-size="18" fill="#475569">U와 W에도 같은 accumulation 원리가 적용됨</text>
</svg>

`U`에 대한 최종 gradient는 다음과 같음:

$$
\frac{\partial L}{\partial U}
= \sum_{i=1}^{T}\left.\frac{\partial L}{\partial U}\right|_{\text{usage at }i}
$$

`V`에 대한 최종 gradient는 다음과 같음:

$$
\frac{\partial L}{\partial V}
= \sum_{i=1}^{T}\left.\frac{\partial L}{\partial V}\right|_{\text{usage at }i}
$$

`W`에 대한 최종 gradient는 다음과 같음:

$$
\frac{\partial L}{\partial W}
= \sum_{i=1}^{T}\left.\frac{\partial L}{\partial W}\right|_{\text{usage at }i}
$$

각 usage에서 계산된 gradient contribution을 합산하여 하나의 shared parameter에 대한 gradient를 구하고, optimizer가 이를 이용하여 parameter를 update함.

Loss를 time step에 대해 mean으로 정의했다면 gradient의 전체 scale은 달라질 수 있지만, shared parameter의 각 usage에서 발생한 contribution이 하나의 parameter gradient로 accumulation된다는 원리는 동일함.

---

### 2.3 Recurrent Local Gradient와 Chain Rule

Simple RNN의 hidden state를 `tanh` activation으로 나타내면 다음과 같음:

$$
h_t = \tanh(Ux_t + Vh_{t-1} + b_h)
$$

Pre-activation은 다음과 같음:

$$
a_t = Ux_t + Vh_{t-1} + b_h
$$

Hidden state는 vector이므로 한 recurrent step의 local gradient는 정확히는 Jacobian임. Previous hidden state에 대한 local Jacobian은 다음과 같음:

$$
\frac{\partial h_t}{\partial h_{t-1}} = D_tV
$$

Activation derivative로 이루어진 diagonal matrix는 다음과 같음:

$$
D_t = \operatorname{diag}\!\left(\tanh'(a_t)\right)
$$

<!-- Chain rule에 따라 recurrent local gradient가 연속적으로 곱해지는 과정 | source: ./figures/03_chain_rule.svg -->
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="500" viewBox="0 0 1200 500" role="img" aria-labelledby="title desc">
  <title id="title">Chain rule과 local gradient multiplication</title><desc id="desc">Current loss에서 earlier hidden state까지 local Jacobian이 연속적으로 곱해지는 과정</desc>
  <defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#7c3aed"/></marker></defs>
  <rect width="1200" height="500" rx="24" fill="#f8fafc"/>
  <text x="60" y="55" font-family="Arial, 'Noto Sans KR', sans-serif" font-size="28" font-weight="700" fill="#0f172a">Chain Rule: recurrent local gradient의 연속 multiplication</text>
  <g font-family="Arial, 'Noto Sans KR', sans-serif" text-anchor="middle">
    <g fill="#ede9fe" stroke="#7c3aed" stroke-width="3"><rect x="75" y="150" width="170" height="90" rx="18"/><rect x="350" y="150" width="170" height="90" rx="18"/><rect x="680" y="150" width="170" height="90" rx="18"/><rect x="955" y="150" width="170" height="90" rx="18"/></g>
    <g font-size="28" font-weight="700" fill="#0f172a"><text x="160" y="205">h<tspan baseline-shift="sub" font-size="18">k</tspan></text><text x="435" y="205">h<tspan baseline-shift="sub" font-size="18">k+1</tspan></text><text x="765" y="205">h<tspan baseline-shift="sub" font-size="18">t−1</tspan></text><text x="1040" y="205">h<tspan baseline-shift="sub" font-size="18">t</tspan></text></g>
    <g stroke="#7c3aed" stroke-width="4" fill="none" marker-end="url(#a)"><path d="M955 280H850"/><path d="M680 280H520"/><path d="M350 280H245"/></g>
    <g font-size="20" font-weight="700" fill="#6d28d9"><text x="902" y="315">D<tspan baseline-shift="sub" font-size="14">t</tspan>V</text><text x="600" y="315">⋯</text><text x="297" y="315">D<tspan baseline-shift="sub" font-size="14">k+1</tspan>V</text></g>
    <rect x="850" y="365" width="275" height="76" rx="16" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/><text x="987" y="397" font-size="17" fill="#991b1b">current loss gradient</text><text x="987" y="425" font-size="22" font-weight="700" fill="#991b1b">∂L<tspan baseline-shift="sub" font-size="14">t</tspan>/∂h<tspan baseline-shift="sub" font-size="14">t</tspan></text>
    <path d="M1040 365V245" stroke="#dc2626" stroke-width="3" marker-end="url(#a)"/>
  </g>
  <rect x="250" y="80" width="700" height="44" rx="12" fill="#fff" stroke="#cbd5e1"/>
  <text x="600" y="109" text-anchor="middle" font-family="Arial, sans-serif" font-size="21" fill="#334155">∂Lₜ/∂hₖ = ∂Lₜ/∂hₜ · (DₜV) ··· (Dₖ₊₁V)</text>
  <text x="600" y="475" text-anchor="middle" font-family="Arial, 'Noto Sans KR', sans-serif" font-size="18" fill="#475569">V는 모든 step에서 동일하지만 D는 activation에 따라 달라짐</text>
</svg>

Time step `t` 의 loss가 time step `k` 의 hidden state에 미치는 gradient는 다음과 같음:

$$
\frac{\partial L_t}{\partial h_k}
= \frac{\partial L_t}{\partial h_t}
  \frac{\partial h_t}{\partial h_{t-1}}
  \cdots
  \frac{\partial h_{k+1}}{\partial h_k}
$$

여기서 $\partial L_t / \partial h_t$ 는 output layer를 거치는 경로를 한 항으로 축약한 표기임.
Output layer를 $o_t = W h_t + b_y$, $\hat{y}_t = \mathrm{softmax}(o_t)$, $L_t = \mathrm{CE}(\hat{y}_t, y_t)$ 로 두면 다음과 같이 풀림:

$$
\frac{\partial L_t}{\partial h_t}
= \frac{\partial L_t}{\partial \hat{y}_t}
  \frac{\partial \hat{y}_t}{\partial o_t}
  \frac{\partial o_t}{\partial h_t}
= \frac{\partial L_t}{\partial o_t} W
$$

이 factor는 $k$ 에 의존하지 않는 상수 항이므로, 이하에서는 다시 $\partial L_t / \partial h_t$ 로 축약함.

각 recurrent local Jacobian을 대입한 product는 다음과 같음:

$$
\frac{\partial L_t}{\partial h_k}
= \frac{\partial L_t}{\partial h_t}
  (D_t V)(D_{t-1} V) \cdots (D_{k+1} V)
= \frac{\partial L_t}{\partial h_t} \prod_{i=k+1}^{t} D_i V
$$

Product는 index $t$ 에서 시작하여 $k+1$ 에서 끝남.  
행렬 곱은 non-commutative이므로 순서를 바꿀 수 없으며, gradient를 row vector로 두는 numerator layout에서는 index가 큰 쪽이 왼쪽에 옴.

여기서 중요한 점은 다음과 같음.

- `V`는 shared recurrent weight이므로 모든 time step에서 동일한 `V`가 포함됨.
- `D_t`는 해당 time step의 activation에 따라 결정되므로 time step마다 달라짐.
- 따라서 매 time step에서 완전히 동일한 local gradient가 반복되는 것은 아님.
- 동일한 recurrent weight `V`는 모든 recurrent local gradient에 반복적으로 포함됨.

---

## 3. Gradient Problems

### 3.1 Vanishing Gradient

`tanh`의 derivative가 가지는 범위는 다음과 같음:

$$
0 < \tanh'(a_t) \le 1
$$

`tanh`가 saturation 영역에 들어가면 derivative가 0에 가까워짐. 따라서 `D_t`는 많은 경우 local gradient의 magnitude를 감소시키는 방향으로 작용함.

Recurrent weight `V`도 해당 direction에서 gradient를 충분히 증폭시키지 못하면 recurrent local Jacobian이 gradient를 줄이는 방향으로 작용함.

이러한 local gradient가 chain rule에 의해 많은 recurrent step에 걸쳐 계속 곱해지면 distant earlier time step에 대한 gradient가 매우 작아질 수 있음. 이를 **vanishing gradient** 라고 함.

<!-- Recurrent step이 누적될수록 gradient magnitude가 0에 가까워지는 vanishing gradient | source: ./figures/04_vanishing_gradient.svg -->
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="500" viewBox="0 0 1200 500" role="img" aria-labelledby="title desc">
  <title id="title">Vanishing gradient</title><desc id="desc">1보다 작은 local factor가 반복해서 곱해질 때 gradient magnitude가 0에 가까워지는 현상</desc>
  <rect width="1200" height="500" rx="24" fill="#f8fafc"/>
  <text x="60" y="55" font-family="Arial, 'Noto Sans KR', sans-serif" font-size="28" font-weight="700" fill="#0f172a">Vanishing Gradient</text>
  <g stroke="#cbd5e1" stroke-width="2"><path d="M100 400H1130"/><path d="M100 100V400"/></g>
  <g fill="#64748b" font-family="Arial, sans-serif" font-size="16"><text x="70" y="405">0</text><text x="55" y="110">1.0</text><text x="80" y="438">number of recurrent steps in the product →</text><text x="25" y="275" transform="rotate(-90 25 275)">gradient magnitude</text></g>
  <path d="M110 120C240 155 300 235 390 300S600 375 760 390S990 397 1120 398" fill="none" stroke="#2563eb" stroke-width="8"/>
  <g fill="#2563eb"><circle cx="110" cy="120" r="9"/><circle cx="390" cy="300" r="9"/><circle cx="760" cy="390" r="9"/><circle cx="1120" cy="398" r="9"/></g>
  <rect x="700" y="105" width="400" height="120" rx="20" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
  <text x="900" y="150" text-anchor="middle" font-family="Arial, sans-serif" font-size="23" font-weight="700" fill="#1e3a8a">0.7 × 0.7 × 0.7 × ··· → 0</text>
  <text x="900" y="190" text-anchor="middle" font-family="Arial, 'Noto Sans KR', sans-serif" font-size="18" fill="#1e40af">긴 product일수록 earlier step의 gradient가 작아짐</text>
</svg>

그 결과는 다음과 같음.

- Distant earlier time step의 input이나 hidden state가 current output에 중요하더라도 해당 time step에 대한 gradient가 거의 0이 될 수 있음.
- 해당 dependency에 대한 gradient contribution이 shared parameter update에 충분히 반영되지 못함.
- Simple RNN이 distant time steps 사이의 dependency를 학습하기 어려워짐.

즉 **vanishing gradient는 distant earlier time step의 gradient contribution이 parameter update에 충분히 반영되지 못하게 하므로 long-term dependency 학습과 직접적으로 연결됨.**

---

### 3.2 Exploding Gradient

Recurrent weight `V`가 특정 direction에서 gradient를 크게 증폭시키고 그 효과가 activation derivative에 의한 감소보다 크면, recurrent local Jacobian이 gradient를 증폭시키는 방향으로 작용할 수 있음.

이러한 local gradient가 여러 recurrent step에 걸쳐 계속 곱해지면 전체 gradient magnitude가 매우 커질 수 있음. 이를 **exploding gradient** 라고 함.

<!-- Recurrent step이 누적될수록 gradient magnitude가 급격히 증가하는 exploding gradient | source: ./figures/05_exploding_gradient.svg -->
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="500" viewBox="0 0 1200 500" role="img" aria-labelledby="title desc">
  <title id="title">Exploding gradient</title><desc id="desc">1보다 큰 local factor가 반복해서 곱해질 때 gradient magnitude가 급격히 증가하는 현상</desc>
  <rect width="1200" height="500" rx="24" fill="#f8fafc"/>
  <text x="60" y="55" font-family="Arial, 'Noto Sans KR', sans-serif" font-size="28" font-weight="700" fill="#0f172a">Exploding Gradient</text>
  <g stroke="#cbd5e1" stroke-width="2"><path d="M100 400H1130"/><path d="M100 100V400"/></g>
  <g fill="#64748b" font-family="Arial, sans-serif" font-size="16"><text x="70" y="405">0</text><text x="42" y="110">large</text><text x="80" y="438">number of recurrent steps in the product →</text><text x="25" y="275" transform="rotate(-90 25 275)">gradient magnitude</text></g>
  <path d="M110 390C320 389 470 380 590 350S790 265 890 180S1030 110 1120 85" fill="none" stroke="#dc2626" stroke-width="8"/>
  <g fill="#dc2626"><circle cx="110" cy="390" r="9"/><circle cx="590" cy="350" r="9"/><circle cx="890" cy="180" r="9"/><circle cx="1120" cy="85" r="9"/></g>
  <rect x="155" y="110" width="410" height="120" rx="20" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="360" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="23" font-weight="700" fill="#7f1d1d">1.4 × 1.4 × 1.4 × ··· → ∞</text>
  <text x="360" y="195" text-anchor="middle" font-family="Arial, 'Noto Sans KR', sans-serif" font-size="18" fill="#991b1b">large update · oscillation · Inf / NaN</text>
</svg>

그 결과는 다음과 같음.

- 일부 parameter의 gradient가 지나치게 커질 수 있음.
- 한 번의 optimizer step에서 parameter가 지나치게 크게 변경될 수 있음.
- Loss가 oscillate하거나 급격하게 증가할 수 있음.
- 심한 경우 numerical overflow로 `Inf` 또는 `NaN`이 생성될 수 있음.
- 결국 optimization이 unstable해지거나 training이 diverge할 수 있음.

따라서 **exploding gradient는 long-term dependency를 직접적으로 학습하지 못하게 만드는 원인이라기보다 optimization stability를 해치는 문제** 임.

`gradient clipping`은 exploding gradient를 완화하기 위해 널리 사용하는 방법임.

---

## 4. Long-term Dependency Problem

### 4.1 Definition

**Long-term dependency** 는 distant time step의 information이 current output을 결정하는 데 중요한 dependency를 의미함.

Simple RNN에서 이 문제는 forward pass에서 earlier information을 hidden state에 유지하는 문제와 backward pass의 **vanishing gradient** 를 구분하여 이해해야 함.

### 4.2 Forward Pass에서 Earlier Information 유지

Earlier information은 successive recurrent state transition 동안 hidden-state representation에 유지되어야 함. 하지만 Simple RNN에는 이를 선택적으로 preserve하거나 update하는 gating mechanism과 별도의 memory cell이 없으므로, later hidden state에서 earlier information을 충분히 구분하거나 사용하는 것이 어려워질 수 있음.

### 4.3 Backward Pass의 Vanishing Gradient

BPTT에서는 current loss와 distant earlier time step 사이의 gradient를 계산하기 위해 많은 recurrent local gradient를 연속적으로 곱함. Vanishing gradient가 발생하면 distant earlier time step에 대한 gradient가 거의 0이 되어 해당 dependency의 gradient contribution이 parameter update에 충분히 반영되지 못함.

<!-- Forward pass에서 earlier information을 유지하는 문제와 backward vanishing gradient의 구분 | source: ./figures/06_long_term_dependency.svg -->
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="720" viewBox="0 0 1200 720" role="img" aria-labelledby="title desc">
  <title id="title">Long-term dependency의 forward와 backward 문제</title>
  <desc id="desc">Forward pass에서는 서로 다른 earlier information을 담은 hidden-state representation이 successive recurrent transition을 거치며 구분하기 어려워질 수 있고, backward pass에서는 gradient가 distant earlier time step으로 갈수록 작아지는 과정을 분리해 나타낸 그림</desc>
  <defs>
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#2563eb"/></marker>
    <marker id="arrow-purple" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#7c3aed"/></marker>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity=".10"/></filter>
  </defs>
  <rect width="1200" height="720" rx="24" fill="#f8fafc"/>
  <text x="55" y="52" font-family="Arial, 'Noto Sans KR', sans-serif" font-size="28" font-weight="700" fill="#0f172a">Long-term Dependency Problem</text>
  <rect x="45" y="80" width="1110" height="285" rx="22" fill="#ffffff" stroke="#bfdbfe" stroke-width="2"/>
  <rect x="65" y="98" width="400" height="42" rx="21" fill="#dbeafe"/>
    <text x="265" y="126" text-anchor="middle" font-family="Arial, 'Noto Sans KR', sans-serif" font-size="18" font-weight="700" fill="#1e40af">A. Forward pass · earlier information 유지</text>
  <g font-family="Arial, 'Noto Sans KR', sans-serif" text-anchor="middle">
    <rect x="75" y="185" width="130" height="76" rx="16" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/><text x="140" y="218" font-size="16" fill="#1e40af">earlier input</text><text x="140" y="246" font-size="24" font-weight="700" fill="#1e3a8a">x<tspan baseline-shift="sub" font-size="14">k</tspan></text>
    <g filter="url(#shadow)" fill="#ede9fe" stroke="#7c3aed" stroke-width="2"><rect x="270" y="175" width="150" height="96" rx="18"/><rect x="505" y="175" width="150" height="96" rx="18"/><rect x="780" y="175" width="150" height="96" rx="18"/></g>
    <g fill="#0f172a" font-size="24" font-weight="700"><text x="345" y="213">h<tspan baseline-shift="sub" font-size="14">k</tspan></text><text x="580" y="213">h<tspan baseline-shift="sub" font-size="14">k+1</tspan></text><text x="855" y="213">h<tspan baseline-shift="sub" font-size="14">t</tspan></text></g>
    <rect x="1000" y="185" width="130" height="76" rx="16" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/><text x="1065" y="218" font-size="16" fill="#166534">current output</text><text x="1065" y="246" font-size="24" font-weight="700" fill="#14532d">o<tspan baseline-shift="sub" font-size="14">t</tspan></text>
    <g stroke="#2563eb" stroke-width="3" fill="none" marker-end="url(#arrow-blue)"><path d="M205 223H270"/><path d="M420 223H505"/><path d="M655 223H780"/><path d="M930 223H1000"/></g>
    <text x="717" y="218" font-size="27" font-weight="700" fill="#64748b">···</text>
    <text x="462" y="300" font-size="15" fill="#475569">sequence A</text><text x="462" y="326" font-size="15" fill="#475569">sequence B</text>
    <g stroke-width="4" stroke-linecap="round"><path d="M530 296H625" stroke="#2563eb"/><path d="M530 322H625" stroke="#06b6d4"/><path d="M805 304H900" stroke="#2563eb"/><path d="M805 314H900" stroke="#06b6d4"/></g>
    <path d="M625 296C690 296 735 302 805 304" fill="none" stroke="#2563eb" stroke-width="2"/><path d="M625 322C690 322 735 316 805 314" fill="none" stroke="#06b6d4" stroke-width="2"/>
    <text x="1000" y="309" font-size="15" fill="#475569">state representations가</text><text x="1000" y="330" font-size="15" fill="#475569">서로 구분되기 어려워질 수 있음</text>
  </g>
  <rect x="45" y="385" width="1110" height="250" rx="22" fill="#ffffff" stroke="#ddd6fe" stroke-width="2"/>
  <rect x="65" y="403" width="380" height="42" rx="21" fill="#ede9fe"/>
  <text x="255" y="431" text-anchor="middle" font-family="Arial, 'Noto Sans KR', sans-serif" font-size="18" font-weight="700" fill="#6d28d9">B. Backward pass · vanishing gradient</text>
  <g font-family="Arial, 'Noto Sans KR', sans-serif" text-anchor="middle">
    <rect x="75" y="495" width="150" height="76" rx="16" fill="#f5f3ff" stroke="#7c3aed" stroke-width="2"/><text x="150" y="526" font-size="15" fill="#6d28d9">distant state</text><text x="150" y="553" font-size="24" font-weight="700" fill="#4c1d95">h<tspan baseline-shift="sub" font-size="14">k</tspan></text>
    <rect x="975" y="495" width="155" height="76" rx="16" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/><text x="1052" y="526" font-size="15" fill="#991b1b">current loss</text><text x="1052" y="553" font-size="24" font-weight="700" fill="#7f1d1d">L<tspan baseline-shift="sub" font-size="14">t</tspan></text>
    <path d="M975 533H225" stroke="#c4b5fd" stroke-width="3" marker-end="url(#arrow-purple)"/>
    <g fill="#7c3aed" stroke="#ffffff" stroke-width="2"><circle cx="920" cy="533" r="20"/><circle cx="820" cy="533" r="17"/><circle cx="720" cy="533" r="14"/><circle cx="620" cy="533" r="11"/><circle cx="520" cy="533" r="8"/><circle cx="420" cy="533" r="5"/><circle cx="320" cy="533" r="2.5"/></g>
    <text x="600" y="607" font-size="17" font-weight="700" fill="#6d28d9">chain rule의 recurrent local-gradient product가 길어질수록 gradient가 작아질 수 있음</text>
  </g>
  <rect x="215" y="655" width="770" height="42" rx="21" fill="#fff7ed" stroke="#fdba74" stroke-width="2"/>
  <text x="600" y="682" text-anchor="middle" font-family="Arial, 'Noto Sans KR', sans-serif" font-size="17" font-weight="700" fill="#9a3412">Forward pass의 information 유지와 backward pass의 vanishing gradient는 구분해야 함</text>
</svg>

두 문제의 관계는 다음과 같음.

- Forward pass에서는 earlier information을 later hidden state의 representation에 유지하고 사용하는 것이 어려울 수 있음.
- Backward pass에서는 vanishing gradient 때문에 distant earlier time step의 gradient contribution이 parameter update에 충분히 반영되지 못할 수 있음.
- Exploding gradient는 같은 recurrent local-gradient multiplication에서 발생할 수 있지만, 주로 optimization stability를 해치는 별도의 문제임.

즉 Simple RNN의 long-term dependency problem을 설명할 때는 **forward pass에서 earlier information을 hidden state에 유지하는 문제** 와 **backward pass의 vanishing gradient problem** 을 구분해야 함.

### 4.4 LSTM과 GRU

LSTM과 GRU는 information을 선택적으로 preserve하고 update하는 **gating mechanism** 을 도입하여 Simple RNN의 long-term dependency problem을 완화하는 RNN architecture임.
