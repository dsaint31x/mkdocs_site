# Simple RNN: Forward Pass, BPTT, and Long-term Dependency Problem

## RNN의 Forward Pass

그림의 symbol은 다음과 같음.

- `x_t`: time step `t`의 input vector
- `h_t`: time step `t`의 hidden state vector
- `o_t`: time step `t`의 output vector
- `U`: input-to-hidden weight matrix
- `V`: hidden-to-hidden recurrent weight matrix
- `W`: hidden-to-output weight matrix
- `b_h`: hidden state의 bias vector
- `b_o`: output의 bias vector

Simple RNN에서 hidden state의 계산은 다음과 같음:

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

여기서 중요한 특징은 **parameter sharing**임.

- 모든 time step에서 동일한 `U`를 사용함.
- 모든 time step에서 동일한 `V`를 사용함.
- 모든 time step에서 동일한 `W`를 사용함.

따라서 RNN을 time dimension을 따라 unfold하더라도 새로운 weight가 생성되는 것이 아님.

Unfolded computational graph의 각 위치를 구별하기 위해 `U_t`, `V_t`, `W_t`처럼 표시할 수는 있지만, 이들은 실제로 서로 다른 parameter가 아니라 동일한 shared parameter의 서로 다른 **usage**를 나타냄.

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

## BPTT

RNN을 time dimension을 따라 unfold하면 하나의 깊은 computational graph처럼 볼 수 있음.

Forward pass에서는 input과 hidden state가 다음 time step으로 순차적으로 계산됨.

Backward pass에서는 loss에서 시작하여 이 unfolded computational graph에 **backpropagation**을 적용함.

이때 핵심은 **chain rule**임.

Current loss와 earlier time step 사이의 gradient를 계산하려면, chain rule에 의해 각 recurrent step의 **local gradient가 연속적으로 곱해짐**.

따라서 일반적인 neural network의 backpropagation과 원리는 같지만, RNN에서는 backpropagation이 **time dimension을 따라 수행**되므로 이를 **Backpropagation Through Time, BPTT**라고 부름.

---

## Shared Parameter의 Gradient

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

즉 unfolded graph에서 각 time step의 weight를 서로 다른 parameter처럼 update하는 것이 아님.

각 usage에서 계산된 gradient contribution을 합산하여 **하나의 shared parameter `U`, `V`, `W`에 대한 gradient**를 구하고, optimizer가 이를 이용하여 parameter를 update함.

Loss 자체를 time step에 대해 mean으로 정의했다면 gradient의 전체 scale은 달라질 수 있지만, **shared parameter의 여러 usage에서 발생한 gradient contribution은 accumulation됨**.

---

# BPTT에서 Recurrent Local Gradient가 곱해지는 과정

Simple RNN의 hidden state를 `tanh` activation을 사용하여 나타내면 다음과 같음:

$$
h_t = \tanh(Ux_t + Vh_{t-1} + b_h)
$$

Pre-activation은 다음과 같음:

$$
a_t = Ux_t + Vh_{t-1} + b_h
$$

한 recurrent step에서 이전 hidden state에 대한 local Jacobian은 다음과 같음:

$$
\frac{\partial h_t}{\partial h_{t-1}} = D_tV
$$

여기서 activation function의 derivative로 이루어진 diagonal matrix는 다음과 같음:

$$
D_t = \operatorname{diag}\!\left(\tanh'(a_t)\right)
$$

따라서 current loss와 distant earlier time step 사이의 gradient를 계산할 때, chain rule에 의해 여러 recurrent step의 local gradient가 연속적으로 곱해짐.

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

Time step `t`의 loss가 time step `k`의 hidden state에 미치는 gradient에 포함되는 chain rule은 다음과 같음:

$$
\frac{\partial L_t}{\partial h_k}
= \frac{\partial L_t}{\partial h_t}
\frac{\partial h_t}{\partial h_{t-1}}
\cdots
\frac{\partial h_{k+1}}{\partial h_k}
$$

각 recurrent local Jacobian을 대입한 product의 형태는 다음과 같음:

$$
\cdots (D_tV)(D_{t-1}V)(D_{t-2}V)\cdots
$$

여기서 중요한 점은 다음과 같음.

- `V`는 shared recurrent weight이므로 **모든 time step에서 동일한 `V`가 반복해서 사용됨.**
- `D_t`는 해당 time step의 activation에 따라 결정되므로 **time step마다 달라짐.**
- 따라서 매 time step에서 완전히 동일한 local gradient가 반복되는 것은 아님.
- 하지만 동일한 recurrent weight `V`가 모든 recurrent local gradient에 반복적으로 포함됨.

---

# Vanishing Gradient

`tanh`의 derivative가 가지는 범위는 다음과 같음:

$$
0 < \tanh'(a_t) \le 1
$$

특히 `tanh`가 saturation 영역에 들어가면 derivative가 0에 가까워짐.

따라서 `D_t`는 많은 경우 local gradient의 magnitude를 감소시키는 방향으로 작용함.

여기에 recurrent weight `V`도 해당 direction에서 gradient를 충분히 증폭시키지 못하면 recurrent local Jacobian이 gradient를 줄이는 방향으로 작용함.

이러한 local gradient가 chain rule에 의해 많은 recurrent step에 걸쳐 계속 곱해지면 전체 gradient가 매우 작아질 수 있음.

이를 **vanishing gradient**라고 함.

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

- Distant earlier time step의 input이나 hidden state가 current output에 실제로 중요한 영향을 미치더라도
- 해당 time step에 대한 gradient가 거의 0이 될 수 있음.
- 그러면 그 dependency가 parameter update에 충분히 반영되지 못함.
- 결국 simple RNN이 distant time steps 사이의 dependency를 학습하기 어려워짐.

즉 **vanishing gradient는 long-term dependency problem과 직접적으로 연결됨.**

---

# Exploding Gradient

반대로 recurrent weight `V`가 특정 direction에서 gradient를 크게 증폭시키고, 그 효과가 activation derivative에 의한 감소보다 크면 recurrent local Jacobian이 gradient를 증폭시키는 방향으로 작용할 수 있음.

이러한 local gradient가 chain rule에 의해 여러 recurrent step에 걸쳐 계속 곱해지면 전체 gradient의 magnitude가 매우 커질 수 있음.

이를 **exploding gradient**라고 함.

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
- Parameter가 적절한 solution 주변을 크게 벗어나면서 loss가 oscillate하거나 급격하게 증가할 수 있음.
- 변경된 parameter로 다음 forward pass를 수행하면서 hidden state가 매우 큰 값이나 unstable한 값을 가질 수 있음.
- 이후 계산되는 gradient도 다시 매우 커지는 현상이 반복될 수 있음.
- 심한 경우 numerical overflow가 발생하여 `Inf` 또는 `NaN`이 생성될 수 있음.
- 결국 optimization이 unstable해지거나 training이 diverge하여 정상적인 학습이 불가능해질 수 있음.

따라서 **exploding gradient는 long-term dependency를 직접적으로 학습하지 못하게 만드는 원인이라기보다 optimization stability를 해치는 문제**임.

`gradient clipping`은 이러한 exploding gradient를 완화하기 위해 널리 사용하는 방법임.

---

# Long-term Dependency Problem

**Long-term dependency**는 distant time step의 정보가 current output을 결정하는 데 중요한 dependency를 의미함.

Simple RNN이 이러한 dependency를 학습하려면 current loss와 distant earlier time step 사이의 gradient를 계산해야 함.

BPTT에서는 이를 위해 chain rule에 따라 많은 recurrent step의 local gradient가 연속적으로 곱해짐.

Recurrent step의 수가 많아질수록 이러한 product가 길어지므로 gradient magnitude를 안정적으로 유지하기 어려워짐.

특히 **vanishing gradient**가 발생하면 distant earlier time step에 대한 gradient가 거의 0이 됨.

<!-- Distant input과 current output 사이의 dependency가 vanishing gradient 때문에 parameter update에 반영되지 못하는 과정 | source: ./figures/06_long_term_dependency.svg -->
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="600" viewBox="0 0 1200 600" role="img" aria-labelledby="title desc">
  <title id="title">Long-term dependency와 vanishing gradient</title>
  <desc id="desc">Forward pass에서는 distant input이 current output에 중요한 영향을 미치지만, BPTT에서는 current output에서 distant input 방향으로 갈수록 gradient를 나타내는 원의 크기가 점차 감소하는 그림</desc>
  <defs>
    <marker id="green-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M0 0L10 5L0 10Z" fill="#16a34a"/>
    </marker>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-opacity=".10"/>
    </filter>
  </defs>

  <rect width="1200" height="600" rx="24" fill="#f8fafc"/>

  <text x="60" y="55" font-family="Arial, 'Noto Sans KR', sans-serif" font-size="28" font-weight="700" fill="#0f172a">
    Long-term Dependency와 Vanishing Gradient
  </text>

  <g filter="url(#shadow)">
    <rect x="390" y="82" width="420" height="52" rx="26" fill="#ffffff" stroke="#86efac" stroke-width="2"/>
  </g>
  <text x="600" y="116" text-anchor="middle" font-family="Arial, 'Noto Sans KR', sans-serif" font-size="19" font-weight="700" fill="#15803d">
    Forward pass: 중요한 long-term dependency
  </text>

  <g filter="url(#shadow)">
    <rect x="70" y="180" width="220" height="110" rx="22" fill="#dbeafe" stroke="#2563eb" stroke-width="3"/>
    <rect x="910" y="180" width="220" height="110" rx="22" fill="#dcfce7" stroke="#16a34a" stroke-width="3"/>
  </g>
  <g font-family="Arial, 'Noto Sans KR', sans-serif" text-anchor="middle">
    <text x="180" y="222" font-size="18" fill="#1e40af">distant input</text>
    <text x="180" y="263" font-size="30" font-weight="700" fill="#1e3a8a">x<tspan baseline-shift="sub" font-size="18">k</tspan></text>
    <text x="1020" y="222" font-size="18" fill="#166534">current output</text>
    <text x="1020" y="263" font-size="30" font-weight="700" fill="#14532d">o<tspan baseline-shift="sub" font-size="18">t</tspan></text>
  </g>

  <path d="M290 205 C470 130 730 130 910 205" fill="none" stroke="#16a34a" stroke-width="5" marker-end="url(#green-arrow)"/>

  <path d="M910 270 Q600 486 290 270" fill="none" stroke="#c4b5fd" stroke-width="3"/>
  <g fill="#7c3aed" stroke="#ffffff" stroke-width="2">
    <circle cx="895" cy="280" r="18"/>
    <circle cx="830" cy="318" r="15"/>
    <circle cx="755" cy="351" r="12"/>
    <circle cx="675" cy="372" r="10"/>
    <circle cx="595" cy="378" r="8"/>
    <circle cx="515" cy="372" r="6.5"/>
    <circle cx="435" cy="351" r="5"/>
    <circle cx="360" cy="318" r="3.5"/>
    <circle cx="305" cy="280" r="2"/>
  </g>

  <rect x="335" y="403" width="530" height="48" rx="24" fill="#ede9fe" stroke="#c4b5fd" stroke-width="2"/>
  <text x="600" y="434" text-anchor="middle" font-family="Arial, 'Noto Sans KR', sans-serif" font-size="18" font-weight="700" fill="#6d28d9">
    BPTT: current loss → distant earlier time step
  </text>

  <rect x="255" y="485" width="690" height="82" rx="20" fill="#fff7ed" stroke="#ea580c" stroke-width="3"/>
  <g font-family="Arial, 'Noto Sans KR', sans-serif" text-anchor="middle" fill="#9a3412">
    <text x="600" y="520" font-size="18">distant earlier time step의 gradient ≈ 0</text>
    <text x="600" y="550" font-size="20" font-weight="700">dependency가 parameter update에 충분히 반영되지 못함</text>
  </g>
</svg>

그 결과 해당 time step의 정보가 current output에 중요하더라도 그 dependency가 parameter update에 충분히 반영되지 못하므로 simple RNN은 **long-term dependency를 학습하기 어려움**.

반면 **exploding gradient**도 동일한 recurrent local gradient의 반복 multiplication 과정에서 발생할 수 있지만, 이는 long-term dependency problem의 직접적인 원인이라기보다 optimization을 unstable하게 만드는 별도의 문제임.

정리하면 다음과 같음.

- **BPTT**
  - chain rule에 따라 recurrent step의 local gradient를 연속적으로 곱하여 gradient를 계산함.
- **Vanishing gradient**
  - 반복 multiplication으로 gradient가 지나치게 작아짐.
  - distant time step의 dependency가 parameter update에 반영되지 못함.
  - **long-term dependency problem과 직접적으로 연결됨.**
- **Exploding gradient**
  - 반복 multiplication으로 gradient가 지나치게 커짐.
  - parameter update와 loss가 unstable해지고 training이 diverge할 수 있음.
  - **주로 optimization stability problem임.**

LSTM과 GRU는 simple RNN에서 발생하는 long-term dependency problem을 완화하기 위해, information과 gradient가 long time span에 걸쳐 더 안정적으로 유지될 수 있도록 **gating mechanism**을 도입한 RNN architecture임.

