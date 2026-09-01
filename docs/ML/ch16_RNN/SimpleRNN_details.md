---
title: Simple RNN의 Forward Pass, BPTT, 그리고 Long-term Dependency Problem
description: >
  Simple RNN의 forward computation과 parameter sharing에서 시작하여 BPTT로 W, U, V의
  gradient를 vector 경우와 scalar 경우로 각각 유도하고, 반복 곱 D_i V가 vanishing gradient와
  exploding gradient로 이어지는 과정과 long-term dependency problem을 정리함.
tags:
  - RNN
  - Simple RNN
  - forward pass
  - parameter sharing
  - BPTT
  - backpropagation through time
  - chain rule
  - Jacobian
  - local derivative
  - gradient accumulation
  - vanishing gradient
  - exploding gradient
  - gradient clipping
  - long-term dependency
  - LSTM
  - GRU
---

# Simple RNN: Forward Pass, BPTT, and Long-term Dependency Problem

## 1. Simple RNN의 Forward Pass

### 1.1 Forward Computation

이 글에서 사용하는 symbol은 다음과 같음.

- $x_t$: time step $t$의 input vector
- $h_t$: time step $t$의 hidden state vector
- $a_t$: hidden state의 pre-activation vector
- $z_t$: output의 pre-activation vector
- $o_t$: time step $t$의 output vector
- $U$: input-to-hidden weight matrix
- $V$: hidden-to-hidden recurrent weight matrix
- $W$: hidden-to-output weight matrix
- $b_h$: hidden state의 bias vector
- $b_o$: output의 bias vector

Simple RNN의 hidden state update는 다음과 같음:

$$
a_t = Ux_t + Vh_{t-1} + b_h
$$

$$
h_t = f(a_t)
$$

Output의 계산은 다음과 같음:

$$
z_t = Wh_t + b_o
$$

$$
o_t = g(z_t)
$$

Pre-activation $a_t$와 $z_t$를 명시적으로 분리해 둔 이유는 BPTT를 유도할 때 activation을 통과하는 local derivative와 weight를 통과하는 local derivative를 각각 따로 다루기 위함임.

<!-- 한 time step의 계산을 pre-activation 단위로 분리한 그림 | source: ./figures/00_single_step.svg -->
<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 680 500" role="img" aria-labelledby="f0t f0d">
  <title id="f0t">한 time step의 계산 단계</title>
  <desc id="f0d">입력과 이전 hidden state가 weight를 통과해 pre-activation이 되고 activation을 통과해 hidden state와 output이 되는 과정을, 이후 그림과 같은 세로 배치로 나눈 그림</desc>
  <defs><marker id="ar0" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#334155"/></marker></defs>
  <rect width="680" height="500" rx="20" fill="#f8fafc"/>
  <g font-family="Arial, 'Noto Sans KR', sans-serif">
    <text x="32" y="36" font-size="17" font-weight="700" fill="#0f172a">한 time step: weight 단계와 activation 단계의 분리</text>
    <rect x="275" y="60" width="130" height="44" rx="10" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
    <text x="340" y="87" text-anchor="middle" font-size="15" font-weight="700" fill="#14532d">o<tspan baseline-shift="sub" font-size="10">t</tspan></text>
    <rect x="275" y="146" width="130" height="44" rx="10" fill="#f1f5f9" stroke="#64748b" stroke-width="1.5"/>
    <text x="340" y="173" text-anchor="middle" font-size="15" font-weight="700" fill="#334155">z<tspan baseline-shift="sub" font-size="10">t</tspan></text>
    <rect x="275" y="232" width="130" height="44" rx="10" fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5"/>
    <text x="340" y="259" text-anchor="middle" font-size="15" font-weight="700" fill="#4c1d95">h<tspan baseline-shift="sub" font-size="10">t</tspan></text>
    <rect x="275" y="318" width="130" height="44" rx="10" fill="#f1f5f9" stroke="#64748b" stroke-width="1.5"/>
    <text x="340" y="345" text-anchor="middle" font-size="15" font-weight="700" fill="#334155">a<tspan baseline-shift="sub" font-size="10">t</tspan></text>
    <rect x="275" y="404" width="130" height="44" rx="10" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
    <text x="340" y="431" text-anchor="middle" font-size="15" font-weight="700" fill="#1e3a8a">x<tspan baseline-shift="sub" font-size="10">t</tspan></text>
    <rect x="100" y="318" width="130" height="44" rx="10" fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5"/>
    <text x="165" y="345" text-anchor="middle" font-size="15" font-weight="700" fill="#4c1d95">h<tspan baseline-shift="sub" font-size="10">t−1</tspan></text>
    <g stroke="#334155" stroke-width="1.6" fill="none" marker-end="url(#ar0)"><path d="M340 402V366"/><path d="M340 316V280"/><path d="M340 230V194"/><path d="M340 144V108"/><path d="M232 340H271"/></g>
    <g font-size="12" font-weight="700">
      <text x="352" y="388" fill="#2563eb">U</text>
      <text x="252" y="332" text-anchor="middle" fill="#7c3aed">V</text>
      <text x="352" y="302" fill="#334155">f</text>
      <text x="352" y="216" fill="#16a34a">W</text>
      <text x="352" y="130" fill="#334155">g</text>
    </g>
    <g font-size="10" fill="#64748b"><text x="415" y="345">pre-activation</text><text x="415" y="173">pre-activation</text></g>
    <text x="340" y="478" text-anchor="middle" font-size="11" fill="#475569">weight를 통과하는 단계(U, V, W)와 activation을 통과하는 단계(f, g)가 서로 다른 local derivative를 만듦</text>
  </g>
</svg>

이후 그림에서는 표기를 간단히 하기 위해 $a_t$와 $z_t$를 생략하고 $x_t \rightarrow h_t \rightarrow o_t$ 로만 나타냄. 생략된 두 단계는 2.2에서 local derivative를 정의할 때 다시 등장함.

<!-- Unfolded RNN에서 x_t, h_t, o_t와 shared U, V, W | source: ./figures/01_unfolded_rnn.svg -->
<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 680 430" role="img" aria-labelledby="f1t f1d">
  <title id="f1t">Unfolded RNN과 shared parameter</title>
  <desc id="f1d">세 time step의 input, hidden state, output과 모든 time step에서 공유되는 U, V, W를 나타낸 그림</desc>
  <defs><marker id="ar1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#334155"/></marker></defs>
  <rect width="680" height="430" rx="20" fill="#f8fafc"/>
  <g font-family="Arial, 'Noto Sans KR', sans-serif">
    <text x="32" y="38" font-size="17" font-weight="700" fill="#0f172a">Unfolded RNN: 동일한 U, V, W의 반복 usage</text>
    <g fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"><rect x="60" y="86" width="130" height="44" rx="10"/><rect x="270" y="86" width="130" height="44" rx="10"/><rect x="480" y="86" width="130" height="44" rx="10"/></g>
    <g fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5"><rect x="60" y="196" width="130" height="52" rx="12"/><rect x="270" y="196" width="130" height="52" rx="12"/><rect x="480" y="196" width="130" height="52" rx="12"/></g>
    <g fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"><rect x="60" y="314" width="130" height="44" rx="10"/><rect x="270" y="314" width="130" height="44" rx="10"/><rect x="480" y="314" width="130" height="44" rx="10"/></g>
    <g text-anchor="middle" font-size="15" font-weight="700">
      <g fill="#14532d"><text x="125" y="113">o<tspan baseline-shift="sub" font-size="10">t−2</tspan></text><text x="335" y="113">o<tspan baseline-shift="sub" font-size="10">t−1</tspan></text><text x="545" y="113">o<tspan baseline-shift="sub" font-size="10">t</tspan></text></g>
      <g fill="#4c1d95"><text x="125" y="228">h<tspan baseline-shift="sub" font-size="10">t−2</tspan></text><text x="335" y="228">h<tspan baseline-shift="sub" font-size="10">t−1</tspan></text><text x="545" y="228">h<tspan baseline-shift="sub" font-size="10">t</tspan></text></g>
      <g fill="#1e3a8a"><text x="125" y="341">x<tspan baseline-shift="sub" font-size="10">t−2</tspan></text><text x="335" y="341">x<tspan baseline-shift="sub" font-size="10">t−1</tspan></text><text x="545" y="341">x<tspan baseline-shift="sub" font-size="10">t</tspan></text></g>
    </g>
    <g stroke="#334155" stroke-width="1.6" fill="none" marker-end="url(#ar1)">
      <path d="M125 312V250"/><path d="M335 312V250"/><path d="M545 312V250"/>
      <path d="M125 194V132"/><path d="M335 194V132"/><path d="M545 194V132"/>
      <path d="M192 222H266"/><path d="M402 222H476"/>
    </g>
    <g font-size="12" font-weight="700" text-anchor="middle">
      <g fill="#2563eb"><text x="112" y="286">U</text><text x="322" y="286">U</text><text x="532" y="286">U</text></g>
      <g fill="#16a34a"><text x="112" y="168">W</text><text x="322" y="168">W</text><text x="532" y="168">W</text></g>
      <g fill="#7c3aed"><text x="229" y="212">V</text><text x="439" y="212">V</text></g>
    </g>
    <text x="340" y="398" text-anchor="middle" font-size="12" fill="#475569">각 위치의 label은 별도 parameter가 아니라 동일한 matrix의 usage를 나타냄</text>
  </g>
</svg>

### 1.2 Parameter Sharing

모든 time step에서 동일한 parameter를 반복해서 사용함.

- 모든 time step에서 동일한 $U$를 사용함.
- 모든 time step에서 동일한 $V$를 사용함.
- 모든 time step에서 동일한 $W$를 사용함.

따라서 RNN을 time dimension을 따라 unfold하더라도 새로운 weight가 생성되는 것이 아님.

Unfolded computational graph에서 $U_t$, $V_t$, $W_t$처럼 표시할 수는 있지만, 이는 서로 다른 parameter가 아니라 동일한 shared parameter의 서로 다른 **usage** 를 나타냄.

$U$의 usage 사이에 성립하는 관계는 다음과 같음:

$$
U_{t-2} = U_{t-1} = U_t = U
$$

$V$의 usage 사이에 성립하는 관계는 다음과 같음:

$$
V_{t-2} = V_{t-1} = V_t = V
$$

$W$의 usage 사이에 성립하는 관계는 다음과 같음:

$$
W_{t-2} = W_{t-1} = W_t = W
$$

이 parameter sharing이 이후 BPTT에서 하나의 parameter gradient가 **여러 개의 항의 합** 으로 나타나는 직접적인 이유가 됨.

동일한 parameter가 여러 time step에서 사용되므로 loss에 영향을 주는 경로가 여러 개이고, chain rule에 의해 각 경로의 gradient contribution이 더해짐. 각 time step의 parameter는 같지만 그 usage에서 발생하는 contribution은 time step마다 다르므로, 항들을 하나로 묶을 수 없음.

---

### 1.3 Earlier Information이 Hidden State에 유지되는 과정

Time step $k$의 input information은 later time step으로 직접 연결되는 것이 아니라, successive hidden states를 통해 간접적으로 반영됨.

Forward path는 다음과 같음:

$$
x_k \rightarrow h_k \rightarrow h_{k+1} \rightarrow \cdots \rightarrow h_t \rightarrow o_t
$$

<!-- Forward pass에서 earlier information이 hidden-state representation에 유지되는 과정 | source: ./figures/02_forward_information_retention.svg -->
<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 680 330" role="img" aria-labelledby="f2t f2d">
  <title id="f2t">Forward pass에서 earlier information retention</title>
  <desc id="f2d">서로 다른 earlier input을 반영한 hidden-state representation이 successive recurrent state transition을 거치며 서로 구분하기 어려워질 수 있음을 나타낸 그림</desc>
  <defs><marker id="ar2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#334155"/></marker></defs>
  <rect width="680" height="330" rx="20" fill="#f8fafc"/>
  <g font-family="Arial, 'Noto Sans KR', sans-serif">
    <text x="32" y="38" font-size="17" font-weight="700" fill="#0f172a">Forward pass: earlier information의 유지</text>
    <rect x="32" y="86" width="96" height="52" rx="10" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
    <text x="80" y="106" text-anchor="middle" font-size="11" fill="#1e40af">earlier input</text>
    <text x="80" y="126" text-anchor="middle" font-size="15" font-weight="700" fill="#1e3a8a">x<tspan baseline-shift="sub" font-size="10">k</tspan></text>
    <g fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5"><rect x="168" y="86" width="104" height="52" rx="12"/><rect x="312" y="86" width="104" height="52" rx="12"/><rect x="456" y="86" width="104" height="52" rx="12"/></g>
    <g text-anchor="middle" font-size="15" font-weight="700" fill="#4c1d95"><text x="220" y="118">h<tspan baseline-shift="sub" font-size="10">k</tspan></text><text x="364" y="118">h<tspan baseline-shift="sub" font-size="10">k+1</tspan></text><text x="508" y="118">h<tspan baseline-shift="sub" font-size="10">t</tspan></text></g>
    <rect x="600" y="86" width="48" height="52" rx="10" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
    <text x="624" y="118" text-anchor="middle" font-size="15" font-weight="700" fill="#14532d">o<tspan baseline-shift="sub" font-size="10">t</tspan></text>
    <g stroke="#334155" stroke-width="1.6" fill="none" marker-end="url(#ar2)"><path d="M130 112H166"/><path d="M274 112H310"/><path d="M418 112H454"/><path d="M562 112H598"/></g>
    <text x="435" y="80" text-anchor="middle" font-size="14" font-weight="700" fill="#64748b">···</text>
    <text x="150" y="196" text-anchor="end" font-size="11" fill="#475569">sequence A</text>
    <text x="150" y="220" text-anchor="end" font-size="11" fill="#475569">sequence B</text>
    <g stroke-width="4" stroke-linecap="round"><path d="M168 192H272" stroke="#2563eb"/><path d="M168 216H272" stroke="#06b6d4"/><path d="M456 200H560" stroke="#2563eb"/><path d="M456 208H560" stroke="#06b6d4"/></g>
    <path d="M272 192C340 192 400 198 456 200" fill="none" stroke="#2563eb" stroke-width="1.5"/>
    <path d="M272 216C340 216 400 210 456 208" fill="none" stroke="#06b6d4" stroke-width="1.5"/>
    <text x="340" y="268" text-anchor="middle" font-size="12" fill="#475569">earlier input이 달랐던 두 sequence의 representation이 later state에서 가까워질 수 있음</text>
    <rect x="120" y="286" width="440" height="30" rx="15" fill="#ffffff" stroke="#bfdbfe" stroke-width="1.5"/>
    <text x="340" y="306" text-anchor="middle" font-size="12" font-weight="700" fill="#1e40af">Earlier information은 매 step 새로 계산되는 hidden state 안에 유지되어야 함</text>
  </g>
</svg>

각 recurrent step에서는 previous hidden state와 current input을 사용하여 next hidden state를 계산함. 따라서 earlier information은 별도의 storage에 독립적으로 보존되는 것이 아니라, 매 time step에서 새로 계산되는 hidden-state representation 안에 유지되어야 함.

Simple RNN에는 earlier information을 선택적으로 preserve하거나 update하는 gating mechanism과 별도의 memory cell이 없음. Earlier information이 later hidden state까지 유지되는지는 recurrent weight $V$, subsequent input, activation function, 그리고 전체 recurrent state dynamics에 의해 결정됨.

$\tanh$와 같은 nonlinear activation이 saturation 영역에 들어가면 서로 다른 pre-activation이 비슷한 hidden-state value로 mapping될 수 있음. 또한 recurrent state transition이 반복되면서 earlier input이 달랐던 두 sequence의 hidden-state representation이 later time step에서 서로 유사해질 수 있음.

이 경우 current hidden state만으로는 earlier input의 차이를 충분히 구분하기 어려우며, current output이 해당 earlier information을 사용하는 것도 어려워짐.

즉 forward pass의 핵심 문제는 **earlier information을 구분하고 사용하는 데 필요한 state representation이 successive recurrent state transition 동안 안정적으로 유지되지 않을 수 있다는 것** 임.

여기까지는 output이 earlier input의 차이에 반응하지 못할 수 있다는 forward 쪽 이야기임. 다음 장에서는 같은 구조를 backward 쪽에서 보았을 때 왜 그 dependency를 **학습** 하는 것까지 어려워지는지를 다룸.

---

## 2. BPTT

### 2.1 Unfolded Computational Graph와 Backward Pass

RNN을 time dimension을 따라 unfold하면 하나의 깊은 computational graph처럼 볼 수 있음.

Forward pass에서는 input과 hidden state가 time step 순서대로 계산됨. Backward pass에서는 loss에서 시작하여 unfolded computational graph에 **backpropagation** 을 적용함.

일반적인 neural network의 backpropagation과 원리는 같지만, RNN에서는 backpropagation이 time dimension을 따라 수행되므로 이를 **Backpropagation Through Time, BPTT** 라고 부름.

이 장은 하나의 time step loss $L_t$를 기준으로 다음 순서를 따름. 먼저 반복해서 등장하는 local derivative를 정의하고(2.2), loss에서 출발한 gradient가 각 node에 도달할 때의 값을 구함(2.3). 그 값을 출발점으로 $W$, $U$, $V$의 gradient를 차례로 전개하고(2.4~2.6), 마지막에 서로 다른 두 종류의 합을 정리함(2.7).

$W$를 먼저 다루는 이유는 $W$가 recurrent 경로를 지나지 않아 항이 하나로 끝나기 때문이며, $U$와 $V$는 recurrent 경로를 따라 여러 항의 합이 됨.

### 2.2 Local Derivative의 정의

이후 전개에서 반복적으로 등장하는 local derivative는 다음과 같음.

$$
\begin{aligned}
D_i &= \frac{\partial h_i}{\partial a_i} \\
&= \frac{\partial f(a_i)}{\partial a_i} \\
&= \frac{\partial f(U x_i + V h_{i-1} + b_h)}{\partial a_i}
\end{aligned}
$$

$$
\begin{aligned}
G_i &= \frac{\partial o_i}{\partial z_i} \\
&= \frac{\partial g(z_i)}{\partial z_i} \\
&= \frac{\partial g(W h_i + b_o)}{\partial z_i}
\end{aligned}
$$

vector 경우에는 activation이 element-wise이므로 두 local derivative가 diagonal matrix가 됨:

$$
D_i = \operatorname{diag}\!\left(f'(a_i)\right)
$$

$$
G_i = \operatorname{diag}\!\left(g'(z_i)\right)
$$

scalar 경우에는 단순한 실수임:

$$
D_i = f'(a_i)
$$

$$
G_i = g'(z_i)
$$

이를 이용하면 recurrent step과 output layer의 local derivative는 각각 다음과 같이 정리됨:

$$
\frac{\partial h_i}{\partial h_{i-1}} = D_i V
$$

$$
\frac{\partial o_t}{\partial h_t} = G_t W
$$

여기서 $V$는 모든 time step에서 동일하지만 $D_i$는 해당 step의 activation에 따라 달라지므로, 매 step의 local derivative가 완전히 동일하지는 않음.

세 weight 중 $V$ 만 특별한 위치에 있다는 점도 미리 확인해 둘 필요가 있음. Backward path에서 여러 번 지나게 되는 edge는 $h_{i-1} \rightarrow h_i$ 하나뿐이고, 그 edge의 local derivative가 $D_i V$ 임. 즉 $V$ 는 gradient가 통과할 때마다 다시 곱해짐.

반면 $U$ 가 놓인 $x_i \rightarrow h_i$ edge는 $x_i$ 가 외부 입력이라 gradient가 들어가면 다시 나오지 않는 leaf edge이고, $W$ 가 놓인 $h_t \rightarrow o_t$ edge도 마찬가지임. 두 edge는 하나의 경로에서 한 번만 지나감.

따라서 이후 전개에서 반복해서 곱해지는 것은 $D_i V$ 뿐이며, $U$ 와 $W$ 는 각 항에 한 번씩만 등장함.

### 2.3 Loss에서 각 Node로 전파되는 Gradient

Backward pass의 출발점은 loss를 output으로 미분한 값임. 이 값은 loss의 정의에 따라 결정되며 recurrent 구조와는 무관함:

$$
\frac{\partial L_t}{\partial o_t}
$$

Output layer를 지나면 같은 time step의 hidden state에 도달함:

$$
\begin{aligned}
\frac{\partial L_t}{\partial h_t}
&= \frac{\partial L_t}{\partial o_t} \frac{\partial o_t}{\partial h_t} \\
&= \frac{\partial L_t}{\partial o_t} G_t W
\end{aligned}
$$

여기서부터는 recurrent 경로를 따라 한 step씩 거슬러 올라감:

$$
\begin{aligned}
\frac{\partial L_t}{\partial h_{i-1}}
&= \frac{\partial L_t}{\partial h_i} \frac{\partial h_i}{\partial h_{i-1}} \\
&= \frac{\partial L_t}{\partial h_i} D_i V
\end{aligned}
$$

이를 $k$까지 반복하면 chain rule에 의해 다음과 같음:

$$
\frac{\partial L_t}{\partial h_k}
= \frac{\partial L_t}{\partial h_t}
  \frac{\partial h_t}{\partial h_{t-1}}
  \frac{\partial h_{t-1}}{\partial h_{t-2}}
  \cdots
  \frac{\partial h_{k+1}}{\partial h_k}
$$

local derivative를 대입하면 다음과 같음:

$$
\begin{aligned}
\frac{\partial L_t}{\partial h_k}
&= \frac{\partial L_t}{\partial h_t} (D_t V)(D_{t-1} V) \cdots (D_{k+1} V) \\
&= \frac{\partial L_t}{\partial h_t} \prod_{i=k+1}^{t} D_i V
\end{aligned}
$$

Product는 index $t$에서 시작하여 $k+1$에서 끝남. 행렬 곱은 non-commutative이므로 순서를 바꿀 수 없으며, gradient를 row vector로 두는 numerator layout에서는 index가 큰 쪽이 왼쪽에 옴.

<!-- Loss에서 earlier hidden state로 gradient가 전파되는 경로 | source: ./figures/03_backward_path.svg -->
<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 680 612" role="img" aria-labelledby="f3t f3d">
  <title id="f3t">Loss에서 earlier hidden state로 전파되는 gradient 경로</title>
  <desc id="f3d">L_t에서 출발한 gradient가 o_t를 거쳐 h_t에 도달한 뒤 recurrent local derivative를 곱하며 이전 hidden state로 전파되는 경로</desc>
  <defs><marker id="ar3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#334155"/></marker><marker id="ac3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#ea580c"/></marker></defs>
  <rect width="680" height="612" rx="20" fill="#f8fafc"/>
  <g font-family="Arial, 'Noto Sans KR', sans-serif">
    <text x="32" y="36" font-size="17" font-weight="700" fill="#0f172a">Backward: L 에서 earlier hidden state까지의 gradient 경로</text>
    <line x1="32" y1="62" x2="62" y2="62" stroke="#334155" stroke-width="1.6"/><text x="68" y="66" font-size="11" fill="#475569">forward</text>
    <line x1="140" y1="62" x2="170" y2="62" stroke="#ea580c" stroke-width="1.6"/><text x="176" y="66" font-size="11" fill="#ea580c">backward (gradient)</text>
    <rect x="480" y="86" width="130" height="40" rx="10" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
    <text x="545" y="112" text-anchor="middle" font-size="15" font-weight="700" fill="#7f1d1d">L<tspan baseline-shift="sub" font-size="10">t</tspan></text>
    <g fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"><rect x="60" y="168" width="130" height="68" rx="12"/><rect x="270" y="168" width="130" height="68" rx="12"/><rect x="480" y="168" width="130" height="68" rx="12"/></g>
    <g text-anchor="middle" fill="#14532d"><text x="125" y="193" font-size="15" font-weight="700">o<tspan baseline-shift="sub" font-size="10">t−2</tspan></text><text x="335" y="193" font-size="15" font-weight="700">o<tspan baseline-shift="sub" font-size="10">t−1</tspan></text><text x="545" y="193" font-size="15" font-weight="700">o<tspan baseline-shift="sub" font-size="10">t</tspan></text>
    <text x="125" y="212" font-size="10">gradient 0</text><text x="335" y="212" font-size="10">gradient 0</text></g>
    <text x="545" y="210" text-anchor="middle" font-size="10" fill="#14532d">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text>
    <line x1="529" y1="216" x2="561" y2="216" stroke="#14532d" stroke-width="0.7"/>
    <text x="545" y="228" text-anchor="middle" font-size="10" fill="#14532d">∂o<tspan baseline-shift="sub" font-size="8">t</tspan></text>
    <g fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5"><rect x="60" y="288" width="130" height="68" rx="12"/><rect x="270" y="288" width="130" height="68" rx="12"/><rect x="480" y="288" width="130" height="68" rx="12"/></g>
    <g text-anchor="middle" fill="#4c1d95" font-size="15" font-weight="700"><text x="125" y="311">h<tspan baseline-shift="sub" font-size="10">t−2</tspan></text><text x="335" y="311">h<tspan baseline-shift="sub" font-size="10">t−1</tspan></text><text x="545" y="311">h<tspan baseline-shift="sub" font-size="10">t</tspan></text></g>
    <g text-anchor="middle" fill="#4c1d95" font-size="10">
      <text x="125" y="330">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="335" y="330">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="545" y="330">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text>
      <text x="125" y="348">∂h<tspan baseline-shift="sub" font-size="8">t−2</tspan></text><text x="335" y="348">∂h<tspan baseline-shift="sub" font-size="8">t−1</tspan></text><text x="545" y="348">∂h<tspan baseline-shift="sub" font-size="8">t</tspan></text>
    </g>
    <g stroke="#4c1d95" stroke-width="0.7"><line x1="109" y1="336" x2="141" y2="336"/><line x1="319" y1="336" x2="351" y2="336"/><line x1="529" y1="336" x2="561" y2="336"/></g>
    <g fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"><rect x="60" y="418" width="130" height="40" rx="10"/><rect x="270" y="418" width="130" height="40" rx="10"/><rect x="480" y="418" width="130" height="40" rx="10"/></g>
    <g text-anchor="middle" fill="#1e3a8a" font-size="15" font-weight="700"><text x="125" y="443">x<tspan baseline-shift="sub" font-size="10">t−2</tspan></text><text x="335" y="443">x<tspan baseline-shift="sub" font-size="10">t−1</tspan></text><text x="545" y="443">x<tspan baseline-shift="sub" font-size="10">t</tspan></text></g>
    <g stroke="#334155" stroke-width="1.6" fill="none" marker-end="url(#ar3)">
      <path d="M93 416V362"/><path d="M303 416V362"/><path d="M513 416V362"/>
      <path d="M93 286V240"/><path d="M303 286V240"/><path d="M513 286V240"/>
      <path d="M192 306H266"/><path d="M402 306H476"/>
    </g>
    <g font-size="11" font-weight="700" text-anchor="end">
      <g fill="#2563eb"><text x="85" y="389">U</text><text x="295" y="389">U</text><text x="505" y="389">U</text></g>
      <g fill="#16a34a"><text x="85" y="264">W</text><text x="295" y="264">W</text><text x="505" y="264">W</text></g>
    </g>
    <g font-size="11" font-weight="700" text-anchor="middle" fill="#7c3aed"><text x="229" y="296">V</text><text x="439" y="296">V</text></g>
    <g stroke="#ea580c" stroke-width="1.6" fill="none" marker-end="url(#ac3)">
      <path d="M577 128V164"/><path d="M577 240V282"/>
      <path d="M478 334H406"/><path d="M268 334H196"/>
    </g>
    <path d="M58 334H44" stroke="#ea580c" stroke-width="1.6" fill="none" stroke-dasharray="4 4" marker-end="url(#ac3)"/>
    <g text-anchor="middle" fill="#ea580c" font-size="10">
      <text x="440" y="364">∂h<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="440" y="392">∂h<tspan baseline-shift="sub" font-size="8">t−1</tspan></text>
      <text x="230" y="364">∂h<tspan baseline-shift="sub" font-size="8">t−1</tspan></text><text x="230" y="392">∂h<tspan baseline-shift="sub" font-size="8">t−2</tspan></text>
    </g>
    <g stroke="#ea580c" stroke-width="0.7"><line x1="424" y1="372" x2="456" y2="372"/><line x1="214" y1="372" x2="246" y2="372"/></g>
    <text x="597" y="262" font-size="10" fill="#ea580c">∂o<tspan baseline-shift="sub" font-size="8">t</tspan></text>
    <line x1="591" y1="268" x2="623" y2="268" stroke="#ea580c" stroke-width="0.7"/>
    <text x="597" y="282" font-size="10" fill="#ea580c">∂h<tspan baseline-shift="sub" font-size="8">t</tspan></text>
    <rect x="40" y="502" width="600" height="84" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <g fill="#0f172a" text-anchor="middle" font-size="10">
      <text x="62" y="536">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="62" y="560">∂h<tspan baseline-shift="sub" font-size="8">t−2</tspan></text>
      <text x="94" y="548" font-size="12">=</text>
      <text x="130" y="536">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="130" y="560">∂h<tspan baseline-shift="sub" font-size="8">t</tspan></text>
      <text x="165" y="536">∂h<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="165" y="560">∂h<tspan baseline-shift="sub" font-size="8">t−1</tspan></text>
      <text x="200" y="536">∂h<tspan baseline-shift="sub" font-size="8">t−1</tspan></text><text x="200" y="560">∂h<tspan baseline-shift="sub" font-size="8">t−2</tspan></text>
      <text x="232" y="548" font-size="12">=</text>
      <text x="268" y="536">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="268" y="560">∂h<tspan baseline-shift="sub" font-size="8">t</tspan></text>
    </g>
    <g stroke="#0f172a" stroke-width="0.7"><line x1="46" y1="544" x2="78" y2="544"/><line x1="114" y1="544" x2="146" y2="544"/><line x1="149" y1="544" x2="181" y2="544"/><line x1="184" y1="544" x2="216" y2="544"/><line x1="252" y1="544" x2="284" y2="544"/></g>
    <text x="292" y="548" font-size="11" fill="#0f172a">D<tspan baseline-shift="sub" font-size="8">t</tspan> V D<tspan baseline-shift="sub" font-size="8">t−1</tspan> V</text>
    <text x="340" y="596" text-anchor="middle" font-size="11" fill="#475569">왼쪽으로 갈수록 D V 가 하나씩 더 곱해짐</text>
  </g>
</svg>

$o_{t-1}$과 $o_{t-2}$에 gradient가 없는 것은 지금 $L_t$ 하나만 보고 있기 때문임. 다른 time step의 output은 이 loss에 대한 gradient를 받지 않음.

이 절에서 얻은 두 값이 이후 세 절의 출발점이 됨. $W$는 recurrent 경로를 지나지 않으므로 $\partial L_t / \partial o_t$ 에서, $U$와 $V$는 recurrent 경로 위에 있으므로 각 step의 $\partial L_t / \partial h_i$ 에서 시작함.

---

### 2.4 W에 대한 Gradient

$W$는 $z_t = W h_t + b_o$ 에서 한 번만 사용되고 recurrent 경로를 지나지 않음. 따라서 2.3의 출발점 $\partial L_t / \partial o_t$ 에 output layer의 local derivative만 곱하면 끝남.

**vector 경우**

$$
\begin{aligned}
\frac{\partial L_t}{\partial W}
&= \left( \frac{\partial L_t}{\partial o_t} \frac{\partial o_t}{\partial z_t} \right)^{\top} h_t^{\top} \\
&= \left( \frac{\partial L_t}{\partial o_t} G_t \right)^{\top} h_t^{\top}
\end{aligned}
$$

**scalar 경우**

$$
\begin{aligned}
\frac{\partial L_t}{\partial W}
&= \frac{\partial L_t}{\partial o_t} \frac{\partial o_t}{\partial z_t} \frac{\partial z_t}{\partial W} \\
&= \frac{\partial L_t}{\partial o_t} G_t \, h_t
\end{aligned}
$$

- vector에서 $\partial z_t / \partial W$ 는 matrix를 matrix로 미분한 3차 tensor라 곱셈 표기로 쓸 수 없어 $h_t^{\top}$ 로 남김
- scalar에서는 $\partial z_t / \partial W = h_t$ 이며 transpose 없이 그대로 곱해짐
- $b_o$는 $W$와 무관하므로 이 미분에서 사라짐
- $W$는 $h$를 거치지 않고 $z_t$에만 들어가므로 항이 하나이며, 따라서 $D_i V$의 반복 곱이 나타나지 않음

<!-- W에 대한 gradient와 대응하는 항 | source: ./figures/04_grad_W.svg -->
<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 680 612" role="img" aria-labelledby="f4t f4d">
  <title id="f4t">W에 대한 gradient</title>
  <desc id="f4d">o_t 하나에서만 기여가 발생하여 W의 gradient가 단일 항으로 구성되는 구조</desc>
  <defs><marker id="ar4" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#334155"/></marker><marker id="ac4" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#ea580c"/></marker><marker id="at4" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#0d9488"/></marker></defs>
  <rect width="680" height="612" rx="20" fill="#f8fafc"/>
  <g font-family="Arial, 'Noto Sans KR', sans-serif">
    <text x="32" y="36" font-size="17" font-weight="700" fill="#0f172a">W 에 대한 gradient: 항이 하나</text>
    <line x1="32" y1="62" x2="62" y2="62" stroke="#334155" stroke-width="1.6"/><text x="68" y="66" font-size="11" fill="#475569">forward</text>
    <line x1="140" y1="62" x2="170" y2="62" stroke="#ea580c" stroke-width="1.6"/><text x="176" y="66" font-size="11" fill="#ea580c">backward (gradient)</text>
    <line x1="330" y1="62" x2="360" y2="62" stroke="#0d9488" stroke-width="1.6"/><text x="366" y="66" font-size="11" fill="#0d9488">term 대응</text>
    <rect x="480" y="86" width="130" height="40" rx="10" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
    <text x="545" y="112" text-anchor="middle" font-size="15" font-weight="700" fill="#7f1d1d">L<tspan baseline-shift="sub" font-size="10">t</tspan></text>
    <g fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"><rect x="60" y="168" width="130" height="68" rx="12"/><rect x="270" y="168" width="130" height="68" rx="12"/><rect x="480" y="168" width="130" height="68" rx="12"/></g>
    <g text-anchor="middle" fill="#14532d"><text x="125" y="193" font-size="15" font-weight="700">o<tspan baseline-shift="sub" font-size="10">t−2</tspan></text><text x="335" y="193" font-size="15" font-weight="700">o<tspan baseline-shift="sub" font-size="10">t−1</tspan></text><text x="545" y="193" font-size="15" font-weight="700">o<tspan baseline-shift="sub" font-size="10">t</tspan></text>
    <text x="125" y="212" font-size="10">gradient 0</text><text x="335" y="212" font-size="10">gradient 0</text></g>
    <text x="545" y="210" text-anchor="middle" font-size="10" fill="#14532d">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text>
    <line x1="529" y1="216" x2="561" y2="216" stroke="#14532d" stroke-width="0.7"/>
    <text x="545" y="228" text-anchor="middle" font-size="10" fill="#14532d">∂o<tspan baseline-shift="sub" font-size="8">t</tspan></text>
    <g fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5"><rect x="60" y="288" width="130" height="68" rx="12"/><rect x="270" y="288" width="130" height="68" rx="12"/><rect x="480" y="288" width="130" height="68" rx="12"/></g>
    <g text-anchor="middle" fill="#4c1d95" font-size="15" font-weight="700"><text x="125" y="311">h<tspan baseline-shift="sub" font-size="10">t−2</tspan></text><text x="335" y="311">h<tspan baseline-shift="sub" font-size="10">t−1</tspan></text><text x="545" y="311">h<tspan baseline-shift="sub" font-size="10">t</tspan></text></g>
    <g text-anchor="middle" fill="#4c1d95" font-size="10">
      <text x="125" y="330">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="335" y="330">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="545" y="330">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text>
      <text x="125" y="348">∂h<tspan baseline-shift="sub" font-size="8">t−2</tspan></text><text x="335" y="348">∂h<tspan baseline-shift="sub" font-size="8">t−1</tspan></text><text x="545" y="348">∂h<tspan baseline-shift="sub" font-size="8">t</tspan></text>
    </g>
    <g stroke="#4c1d95" stroke-width="0.7"><line x1="109" y1="336" x2="141" y2="336"/><line x1="319" y1="336" x2="351" y2="336"/><line x1="529" y1="336" x2="561" y2="336"/></g>
    <g fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"><rect x="60" y="418" width="130" height="40" rx="10"/><rect x="270" y="418" width="130" height="40" rx="10"/><rect x="480" y="418" width="130" height="40" rx="10"/></g>
    <g text-anchor="middle" fill="#1e3a8a" font-size="15" font-weight="700"><text x="125" y="443">x<tspan baseline-shift="sub" font-size="10">t−2</tspan></text><text x="335" y="443">x<tspan baseline-shift="sub" font-size="10">t−1</tspan></text><text x="545" y="443">x<tspan baseline-shift="sub" font-size="10">t</tspan></text></g>
    <g stroke="#334155" stroke-width="1.6" fill="none" marker-end="url(#ar4)">
      <path d="M93 416V362"/><path d="M303 416V362"/><path d="M513 416V362"/>
      <path d="M93 286V240"/><path d="M303 286V240"/><path d="M513 286V240"/>
      <path d="M192 306H266"/><path d="M402 306H476"/>
    </g>
    <g font-size="11" font-weight="700" text-anchor="end">
      <g fill="#2563eb"><text x="85" y="389">U</text><text x="295" y="389">U</text><text x="505" y="389">U</text></g>
      <g fill="#16a34a"><text x="85" y="264">W</text><text x="295" y="264">W</text><text x="505" y="264">W</text></g>
    </g>
    <g font-size="11" font-weight="700" text-anchor="middle" fill="#7c3aed"><text x="229" y="296">V</text><text x="439" y="296">V</text></g>
    <g stroke="#ea580c" stroke-width="1.6" fill="none" marker-end="url(#ac4)">
      <path d="M577 128V164"/><path d="M577 240V282"/>
      <path d="M478 334H406"/><path d="M268 334H196"/>
    </g>
    <path d="M58 334H44" stroke="#ea580c" stroke-width="1.6" fill="none" stroke-dasharray="4 4" marker-end="url(#ac4)"/>
    <path d="M612 198H648V474H84V498" fill="none" stroke="#0d9488" stroke-width="1.6" marker-end="url(#at4)"/>
    <rect x="40" y="502" width="600" height="84" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <g fill="#0f172a" text-anchor="middle" font-size="10">
      <text x="62" y="536">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="62" y="560">∂o<tspan baseline-shift="sub" font-size="8">t</tspan></text>
      <text x="97" y="536">∂o<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="97" y="560">∂W</text>
      <text x="126" y="548" font-size="12">=</text>
      <text x="156" y="536">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="156" y="560">∂W</text>
    </g>
    <g stroke="#0f172a" stroke-width="0.7"><line x1="46" y1="544" x2="78" y2="544"/><line x1="81" y1="544" x2="113" y2="544"/><line x1="140" y1="544" x2="172" y2="544"/></g>
    <text x="340" y="596" text-anchor="middle" font-size="11" fill="#475569">W 는 recurrent 경로를 거치지 않으므로 반복 곱이 없음</text>
  </g>
</svg>

---

### 2.5 U에 대한 Gradient

$U$는 모든 time step의 $a_i = U x_i + V h_{i-1} + b_h$ 에서 반복해서 사용됨(1.2). 따라서 각 usage마다 하나의 항이 생기고, $U$의 gradient는 그 항들의 합이 됨.

Time step $i$의 usage에서 발생하는 항은 2.3에서 구한 $\partial L_t / \partial h_i$ 에 activation과 weight의 local derivative를 곱한 것임:

$$
\frac{\partial L_t}{\partial h_i}
\frac{\partial h_i}{\partial a_i}
\frac{\partial a_i}{\partial U}
$$

$i$가 작아질수록 $\partial L_t / \partial h_i$ 안에 2.3의 반복 곱 $D_i V$ 가 하나씩 더 들어가므로, 아래 식에서 뒤쪽 항일수록 길어짐.

이때 길어지는 것은 $D_i V$ 부분이고 $U$ 자체는 각 항에 한 번씩만 나타남. 2.2에서 본 것처럼 $U$ 가 놓인 edge는 한 번만 지나가기 때문임.

**vector 경우**

$$
\begin{aligned}
\frac{\partial L_t}{\partial U}
&= \left( \frac{\partial L_t}{\partial h_t} \frac{\partial h_t}{\partial a_t} \right)^{\top} x_t^{\top} \\
&\quad + \left( \frac{\partial L_t}{\partial h_t} \frac{\partial h_t}{\partial h_{t-1}} \frac{\partial h_{t-1}}{\partial a_{t-1}} \right)^{\top} x_{t-1}^{\top} \\
&\quad + \left( \frac{\partial L_t}{\partial h_t} \frac{\partial h_t}{\partial h_{t-1}} \frac{\partial h_{t-1}}{\partial h_{t-2}} \frac{\partial h_{t-2}}{\partial a_{t-2}} \right)^{\top} x_{t-2}^{\top} \\
&\quad + \cdots
\end{aligned}
$$

$$
\begin{aligned}
\frac{\partial L_t}{\partial U}
&= \left( \frac{\partial L_t}{\partial h_t} D_t \right)^{\top} x_t^{\top} \\
&\quad + \left( \frac{\partial L_t}{\partial h_t} D_t V D_{t-1} \right)^{\top} x_{t-1}^{\top} \\
&\quad + \left( \frac{\partial L_t}{\partial h_t} D_t V D_{t-1} V D_{t-2} \right)^{\top} x_{t-2}^{\top} \\
&\quad + \cdots
\end{aligned}
$$

**scalar 경우**

$$
\begin{aligned}
\frac{\partial L_t}{\partial U}
&= \frac{\partial L_t}{\partial h_t} \frac{\partial h_t}{\partial a_t} \frac{\partial a_t}{\partial U} \\
&\quad + \frac{\partial L_t}{\partial h_t} \frac{\partial h_t}{\partial h_{t-1}} \frac{\partial h_{t-1}}{\partial a_{t-1}} \frac{\partial a_{t-1}}{\partial U} \\
&\quad + \frac{\partial L_t}{\partial h_t} \frac{\partial h_t}{\partial h_{t-1}} \frac{\partial h_{t-1}}{\partial h_{t-2}} \frac{\partial h_{t-2}}{\partial a_{t-2}} \frac{\partial a_{t-2}}{\partial U} \\
&\quad + \cdots
\end{aligned}
$$

$$
\begin{aligned}
\frac{\partial L_t}{\partial U}
&= \frac{\partial L_t}{\partial h_t} D_t \, x_t \\
&\quad + \frac{\partial L_t}{\partial h_t} D_t V D_{t-1} \, x_{t-1} \\
&\quad + \frac{\partial L_t}{\partial h_t} D_t V D_{t-1} V D_{t-2} \, x_{t-2} \\
&\quad + \cdots
\end{aligned}
$$

- vector에서 $\partial a_i / \partial U$ 는 3차 tensor라 곱셈 표기로 쓸 수 없어 $x_i^{\top}$ 로 남김
- scalar에서는 $\partial a_i / \partial U = x_i$ 이며 transpose 없이 그대로 곱해짐
- $V h_{i-1}$ 과 $b_h$는 $U$와 무관하므로 이 미분에서 사라짐
- 항의 index가 작아질수록 $D_i V$ 가 하나씩 더 곱해져 항이 길어짐

<!-- U에 대한 gradient와 각 항의 대응 | source: ./figures/05_grad_U.svg -->
<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 680 612" role="img" aria-labelledby="f5t f5d">
  <title id="f5t">U에 대한 gradient</title>
  <desc id="f5d">각 hidden state에서 갈라져 나온 기여가 U의 gradient를 이루는 항들에 대응되는 구조</desc>
  <defs><marker id="ar5" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#334155"/></marker><marker id="ac5" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#ea580c"/></marker><marker id="at5" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#0d9488"/></marker></defs>
  <rect width="680" height="612" rx="20" fill="#f8fafc"/>
  <g font-family="Arial, 'Noto Sans KR', sans-serif">
    <text x="32" y="36" font-size="17" font-weight="700" fill="#0f172a">U 에 대한 gradient: 항이 길이가 다른 합</text>
    <line x1="32" y1="62" x2="62" y2="62" stroke="#334155" stroke-width="1.6"/><text x="68" y="66" font-size="11" fill="#475569">forward</text>
    <line x1="140" y1="62" x2="170" y2="62" stroke="#ea580c" stroke-width="1.6"/><text x="176" y="66" font-size="11" fill="#ea580c">backward (gradient)</text>
    <line x1="330" y1="62" x2="360" y2="62" stroke="#0d9488" stroke-width="1.6"/><text x="366" y="66" font-size="11" fill="#0d9488">term 대응</text>
    <rect x="480" y="86" width="130" height="40" rx="10" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
    <text x="545" y="112" text-anchor="middle" font-size="15" font-weight="700" fill="#7f1d1d">L<tspan baseline-shift="sub" font-size="10">t</tspan></text>
    <g fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"><rect x="60" y="168" width="130" height="68" rx="12"/><rect x="270" y="168" width="130" height="68" rx="12"/><rect x="480" y="168" width="130" height="68" rx="12"/></g>
    <g text-anchor="middle" fill="#14532d"><text x="125" y="193" font-size="15" font-weight="700">o<tspan baseline-shift="sub" font-size="10">t−2</tspan></text><text x="335" y="193" font-size="15" font-weight="700">o<tspan baseline-shift="sub" font-size="10">t−1</tspan></text><text x="545" y="193" font-size="15" font-weight="700">o<tspan baseline-shift="sub" font-size="10">t</tspan></text>
    <text x="125" y="212" font-size="10">gradient 0</text><text x="335" y="212" font-size="10">gradient 0</text></g>
    <text x="545" y="210" text-anchor="middle" font-size="10" fill="#14532d">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text>
    <line x1="529" y1="216" x2="561" y2="216" stroke="#14532d" stroke-width="0.7"/>
    <text x="545" y="228" text-anchor="middle" font-size="10" fill="#14532d">∂o<tspan baseline-shift="sub" font-size="8">t</tspan></text>
    <g fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5"><rect x="60" y="288" width="130" height="68" rx="12"/><rect x="270" y="288" width="130" height="68" rx="12"/><rect x="480" y="288" width="130" height="68" rx="12"/></g>
    <g text-anchor="middle" fill="#4c1d95" font-size="15" font-weight="700"><text x="125" y="311">h<tspan baseline-shift="sub" font-size="10">t−2</tspan></text><text x="335" y="311">h<tspan baseline-shift="sub" font-size="10">t−1</tspan></text><text x="545" y="311">h<tspan baseline-shift="sub" font-size="10">t</tspan></text></g>
    <g text-anchor="middle" fill="#4c1d95" font-size="10">
      <text x="125" y="330">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="335" y="330">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="545" y="330">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text>
      <text x="125" y="348">∂h<tspan baseline-shift="sub" font-size="8">t−2</tspan></text><text x="335" y="348">∂h<tspan baseline-shift="sub" font-size="8">t−1</tspan></text><text x="545" y="348">∂h<tspan baseline-shift="sub" font-size="8">t</tspan></text>
    </g>
    <g stroke="#4c1d95" stroke-width="0.7"><line x1="109" y1="336" x2="141" y2="336"/><line x1="319" y1="336" x2="351" y2="336"/><line x1="529" y1="336" x2="561" y2="336"/></g>
    <g fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"><rect x="60" y="418" width="130" height="40" rx="10"/><rect x="270" y="418" width="130" height="40" rx="10"/><rect x="480" y="418" width="130" height="40" rx="10"/></g>
    <g text-anchor="middle" fill="#1e3a8a" font-size="15" font-weight="700"><text x="125" y="443">x<tspan baseline-shift="sub" font-size="10">t−2</tspan></text><text x="335" y="443">x<tspan baseline-shift="sub" font-size="10">t−1</tspan></text><text x="545" y="443">x<tspan baseline-shift="sub" font-size="10">t</tspan></text></g>
    <g stroke="#334155" stroke-width="1.6" fill="none" marker-end="url(#ar5)">
      <path d="M93 416V362"/><path d="M303 416V362"/><path d="M513 416V362"/>
      <path d="M93 286V240"/><path d="M303 286V240"/><path d="M513 286V240"/>
      <path d="M192 306H266"/><path d="M402 306H476"/>
    </g>
    <g font-size="11" font-weight="700" text-anchor="end">
      <g fill="#2563eb"><text x="85" y="389">U</text><text x="295" y="389">U</text><text x="505" y="389">U</text></g>
      <g fill="#16a34a"><text x="85" y="264">W</text><text x="295" y="264">W</text><text x="505" y="264">W</text></g>
    </g>
    <g font-size="11" font-weight="700" text-anchor="middle" fill="#7c3aed"><text x="229" y="296">V</text><text x="439" y="296">V</text></g>
    <g stroke="#ea580c" stroke-width="1.6" fill="none" marker-end="url(#ac5)">
      <path d="M577 128V164"/><path d="M577 240V282"/>
      <path d="M478 334H406"/><path d="M268 334H196"/>
    </g>
    <path d="M58 334H44" stroke="#ea580c" stroke-width="1.6" fill="none" stroke-dasharray="4 4" marker-end="url(#ac5)"/>
    <g text-anchor="middle" fill="#ea580c" font-size="10">
      <text x="440" y="364">∂h<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="440" y="392">∂h<tspan baseline-shift="sub" font-size="8">t−1</tspan></text>
      <text x="230" y="364">∂h<tspan baseline-shift="sub" font-size="8">t−1</tspan></text><text x="230" y="392">∂h<tspan baseline-shift="sub" font-size="8">t−2</tspan></text>
    </g>
    <g stroke="#ea580c" stroke-width="0.7"><line x1="424" y1="372" x2="456" y2="372"/><line x1="214" y1="372" x2="246" y2="372"/></g>
    <g stroke="#0d9488" stroke-width="1.6" fill="none" marker-end="url(#at5)">
      <path d="M575 358V404H636V474H478V498"/>
      <path d="M365 358V404H440V474H338V498"/>
      <path d="M155 358V404H230V474H164V498"/>
    </g>
    <path d="M45 362V498" stroke="#0d9488" stroke-width="1.6" fill="none" stroke-dasharray="4 4" marker-end="url(#at5)"/>
    <rect x="40" y="502" width="600" height="84" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <g fill="#0f172a" text-anchor="middle" font-size="10">
      <text x="52" y="548" font-size="12">⋯</text><text x="66" y="548" font-size="12">+</text>
      <text x="94" y="536">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="94" y="560">∂h<tspan baseline-shift="sub" font-size="8">t</tspan></text>
      <text x="129" y="536">∂h<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="129" y="560">∂h<tspan baseline-shift="sub" font-size="8">t−1</tspan></text>
      <text x="164" y="536">∂h<tspan baseline-shift="sub" font-size="8">t−1</tspan></text><text x="164" y="560">∂h<tspan baseline-shift="sub" font-size="8">t−2</tspan></text>
      <text x="199" y="536">∂h<tspan baseline-shift="sub" font-size="8">t−2</tspan></text><text x="199" y="560">∂a<tspan baseline-shift="sub" font-size="8">t−2</tspan></text>
      <text x="234" y="536">∂a<tspan baseline-shift="sub" font-size="8">t−2</tspan></text><text x="234" y="560">∂U</text>
      <text x="260" y="548" font-size="12">+</text>
      <text x="286" y="536">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="286" y="560">∂h<tspan baseline-shift="sub" font-size="8">t</tspan></text>
      <text x="321" y="536">∂h<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="321" y="560">∂h<tspan baseline-shift="sub" font-size="8">t−1</tspan></text>
      <text x="356" y="536">∂h<tspan baseline-shift="sub" font-size="8">t−1</tspan></text><text x="356" y="560">∂a<tspan baseline-shift="sub" font-size="8">t−1</tspan></text>
      <text x="391" y="536">∂a<tspan baseline-shift="sub" font-size="8">t−1</tspan></text><text x="391" y="560">∂U</text>
      <text x="417" y="548" font-size="12">+</text>
      <text x="443" y="536">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="443" y="560">∂h<tspan baseline-shift="sub" font-size="8">t</tspan></text>
      <text x="478" y="536">∂h<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="478" y="560">∂a<tspan baseline-shift="sub" font-size="8">t</tspan></text>
      <text x="513" y="536">∂a<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="513" y="560">∂U</text>
      <text x="539" y="548" font-size="12">=</text>
      <text x="565" y="536">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="565" y="560">∂U</text>
    </g>
    <g stroke="#0f172a" stroke-width="0.7">
      <line x1="78" y1="544" x2="110" y2="544"/><line x1="113" y1="544" x2="145" y2="544"/><line x1="148" y1="544" x2="180" y2="544"/><line x1="183" y1="544" x2="215" y2="544"/><line x1="218" y1="544" x2="250" y2="544"/>
      <line x1="270" y1="544" x2="302" y2="544"/><line x1="305" y1="544" x2="337" y2="544"/><line x1="340" y1="544" x2="372" y2="544"/><line x1="375" y1="544" x2="407" y2="544"/>
      <line x1="427" y1="544" x2="459" y2="544"/><line x1="462" y1="544" x2="494" y2="544"/><line x1="497" y1="544" x2="529" y2="544"/>
      <line x1="549" y1="544" x2="581" y2="544"/>
    </g>
  </g>
</svg>

주황색 화살표는 gradient가 실제로 전파되는 경로이고, 아래로 꺾여 내려가는 청록색 선은 전파가 아니라 각 hidden state의 gradient가 식의 어느 항에 대응하는지를 가리키는 지시선임.

---

### 2.6 V에 대한 Gradient

$V$ 역시 모든 time step의 $a_i$ 에서 반복해서 사용되므로 구조는 2.5와 같음. 다른 점은 $\partial a_i / \partial U$ 자리에 $\partial a_i / \partial V$ 가 들어간다는 것뿐임:

$$
\frac{\partial L_t}{\partial h_i}
\frac{\partial h_i}{\partial a_i}
\frac{\partial a_i}{\partial V}
$$

**vector 경우**

$$
\begin{aligned}
\frac{\partial L_t}{\partial V}
&= \left( \frac{\partial L_t}{\partial h_t} \frac{\partial h_t}{\partial a_t} \right)^{\top} h_{t-1}^{\top} \\
&\quad + \left( \frac{\partial L_t}{\partial h_t} \frac{\partial h_t}{\partial h_{t-1}} \frac{\partial h_{t-1}}{\partial a_{t-1}} \right)^{\top} h_{t-2}^{\top} \\
&\quad + \left( \frac{\partial L_t}{\partial h_t} \frac{\partial h_t}{\partial h_{t-1}} \frac{\partial h_{t-1}}{\partial h_{t-2}} \frac{\partial h_{t-2}}{\partial a_{t-2}} \right)^{\top} h_{t-3}^{\top} \\
&\quad + \cdots
\end{aligned}
$$

$$
\begin{aligned}
\frac{\partial L_t}{\partial V}
&= \left( \frac{\partial L_t}{\partial h_t} D_t \right)^{\top} h_{t-1}^{\top} \\
&\quad + \left( \frac{\partial L_t}{\partial h_t} D_t V D_{t-1} \right)^{\top} h_{t-2}^{\top} \\
&\quad + \left( \frac{\partial L_t}{\partial h_t} D_t V D_{t-1} V D_{t-2} \right)^{\top} h_{t-3}^{\top} \\
&\quad + \cdots
\end{aligned}
$$

**scalar 경우**

$$
\begin{aligned}
\frac{\partial L_t}{\partial V}
&= \frac{\partial L_t}{\partial h_t} \frac{\partial h_t}{\partial a_t} \frac{\partial a_t}{\partial V} \\
&\quad + \frac{\partial L_t}{\partial h_t} \frac{\partial h_t}{\partial h_{t-1}} \frac{\partial h_{t-1}}{\partial a_{t-1}} \frac{\partial a_{t-1}}{\partial V} \\
&\quad + \frac{\partial L_t}{\partial h_t} \frac{\partial h_t}{\partial h_{t-1}} \frac{\partial h_{t-1}}{\partial h_{t-2}} \frac{\partial h_{t-2}}{\partial a_{t-2}} \frac{\partial a_{t-2}}{\partial V} \\
&\quad + \cdots
\end{aligned}
$$

$$
\begin{aligned}
\frac{\partial L_t}{\partial V}
&= \frac{\partial L_t}{\partial h_t} D_t \, h_{t-1} \\
&\quad + \frac{\partial L_t}{\partial h_t} D_t V D_{t-1} \, h_{t-2} \\
&\quad + \frac{\partial L_t}{\partial h_t} D_t V D_{t-1} V D_{t-2} \, h_{t-3} \\
&\quad + \cdots
\end{aligned}
$$

- vector에서 $\partial a_i / \partial V$ 는 3차 tensor라 곱셈 표기로 쓸 수 없어 $h_{i-1}^{\top}$ 로 남김
- scalar에서는 $\partial a_i / \partial V = h_{i-1}$ 이며 transpose 없이 그대로 곱해짐
- $U x_i$ 와 $b_h$는 $V$와 무관하므로 이 미분에서 사라짐
- $U$의 경우와 비교하면 각 항 끝의 $x_i$ 자리에 $h_{i-1}$ 이 들어간 것만 다름

<!-- V에 대한 gradient와 각 항의 대응 | source: ./figures/06_grad_V.svg -->
<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 680 612" role="img" aria-labelledby="f6t f6d">
  <title id="f6t">V에 대한 gradient</title>
  <desc id="f6d">각 hidden state에서 갈라져 나온 기여가 V의 gradient를 이루는 항들에 대응되며, 항마다 곱해지는 factor의 수가 달라지는 구조</desc>
  <defs><marker id="ar6" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#334155"/></marker><marker id="ac6" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#ea580c"/></marker><marker id="at6" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#0d9488"/></marker></defs>
  <rect width="680" height="612" rx="20" fill="#f8fafc"/>
  <g font-family="Arial, 'Noto Sans KR', sans-serif">
    <text x="32" y="36" font-size="17" font-weight="700" fill="#0f172a">V 에 대한 gradient: 항마다 반복 곱의 길이가 다름</text>
    <line x1="32" y1="62" x2="62" y2="62" stroke="#334155" stroke-width="1.6"/><text x="68" y="66" font-size="11" fill="#475569">forward</text>
    <line x1="140" y1="62" x2="170" y2="62" stroke="#ea580c" stroke-width="1.6"/><text x="176" y="66" font-size="11" fill="#ea580c">backward (gradient)</text>
    <line x1="330" y1="62" x2="360" y2="62" stroke="#0d9488" stroke-width="1.6"/><text x="366" y="66" font-size="11" fill="#0d9488">term 대응</text>
    <rect x="480" y="86" width="130" height="40" rx="10" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
    <text x="545" y="112" text-anchor="middle" font-size="15" font-weight="700" fill="#7f1d1d">L<tspan baseline-shift="sub" font-size="10">t</tspan></text>
    <g fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"><rect x="60" y="168" width="130" height="68" rx="12"/><rect x="270" y="168" width="130" height="68" rx="12"/><rect x="480" y="168" width="130" height="68" rx="12"/></g>
    <g text-anchor="middle" fill="#14532d"><text x="125" y="193" font-size="15" font-weight="700">o<tspan baseline-shift="sub" font-size="10">t−2</tspan></text><text x="335" y="193" font-size="15" font-weight="700">o<tspan baseline-shift="sub" font-size="10">t−1</tspan></text><text x="545" y="193" font-size="15" font-weight="700">o<tspan baseline-shift="sub" font-size="10">t</tspan></text>
    <text x="125" y="212" font-size="10">gradient 0</text><text x="335" y="212" font-size="10">gradient 0</text></g>
    <text x="545" y="210" text-anchor="middle" font-size="10" fill="#14532d">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text>
    <line x1="529" y1="216" x2="561" y2="216" stroke="#14532d" stroke-width="0.7"/>
    <text x="545" y="228" text-anchor="middle" font-size="10" fill="#14532d">∂o<tspan baseline-shift="sub" font-size="8">t</tspan></text>
    <g fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5"><rect x="60" y="288" width="130" height="68" rx="12"/><rect x="270" y="288" width="130" height="68" rx="12"/><rect x="480" y="288" width="130" height="68" rx="12"/></g>
    <g text-anchor="middle" fill="#4c1d95" font-size="15" font-weight="700"><text x="125" y="311">h<tspan baseline-shift="sub" font-size="10">t−2</tspan></text><text x="335" y="311">h<tspan baseline-shift="sub" font-size="10">t−1</tspan></text><text x="545" y="311">h<tspan baseline-shift="sub" font-size="10">t</tspan></text></g>
    <g text-anchor="middle" fill="#4c1d95" font-size="10">
      <text x="125" y="330">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="335" y="330">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="545" y="330">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text>
      <text x="125" y="348">∂h<tspan baseline-shift="sub" font-size="8">t−2</tspan></text><text x="335" y="348">∂h<tspan baseline-shift="sub" font-size="8">t−1</tspan></text><text x="545" y="348">∂h<tspan baseline-shift="sub" font-size="8">t</tspan></text>
    </g>
    <g stroke="#4c1d95" stroke-width="0.7"><line x1="109" y1="336" x2="141" y2="336"/><line x1="319" y1="336" x2="351" y2="336"/><line x1="529" y1="336" x2="561" y2="336"/></g>
    <g fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"><rect x="60" y="418" width="130" height="40" rx="10"/><rect x="270" y="418" width="130" height="40" rx="10"/><rect x="480" y="418" width="130" height="40" rx="10"/></g>
    <g text-anchor="middle" fill="#1e3a8a" font-size="15" font-weight="700"><text x="125" y="443">x<tspan baseline-shift="sub" font-size="10">t−2</tspan></text><text x="335" y="443">x<tspan baseline-shift="sub" font-size="10">t−1</tspan></text><text x="545" y="443">x<tspan baseline-shift="sub" font-size="10">t</tspan></text></g>
    <g stroke="#334155" stroke-width="1.6" fill="none" marker-end="url(#ar6)">
      <path d="M93 416V362"/><path d="M303 416V362"/><path d="M513 416V362"/>
      <path d="M93 286V240"/><path d="M303 286V240"/><path d="M513 286V240"/>
      <path d="M192 306H266"/><path d="M402 306H476"/>
    </g>
    <g font-size="11" font-weight="700" text-anchor="end">
      <g fill="#2563eb"><text x="85" y="389">U</text><text x="295" y="389">U</text><text x="505" y="389">U</text></g>
      <g fill="#16a34a"><text x="85" y="264">W</text><text x="295" y="264">W</text><text x="505" y="264">W</text></g>
    </g>
    <g font-size="11" font-weight="700" text-anchor="middle" fill="#7c3aed"><text x="229" y="296">V</text><text x="439" y="296">V</text></g>
    <g stroke="#ea580c" stroke-width="1.6" fill="none" marker-end="url(#ac6)">
      <path d="M577 128V164"/><path d="M577 240V282"/>
      <path d="M478 334H406"/><path d="M268 334H196"/>
    </g>
    <path d="M58 334H44" stroke="#ea580c" stroke-width="1.6" fill="none" stroke-dasharray="4 4" marker-end="url(#ac6)"/>
    <g text-anchor="middle" fill="#ea580c" font-size="10">
      <text x="440" y="364">∂h<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="440" y="392">∂h<tspan baseline-shift="sub" font-size="8">t−1</tspan></text>
      <text x="230" y="364">∂h<tspan baseline-shift="sub" font-size="8">t−1</tspan></text><text x="230" y="392">∂h<tspan baseline-shift="sub" font-size="8">t−2</tspan></text>
    </g>
    <g stroke="#ea580c" stroke-width="0.7"><line x1="424" y1="372" x2="456" y2="372"/><line x1="214" y1="372" x2="246" y2="372"/></g>
    <g stroke="#0d9488" stroke-width="1.6" fill="none" marker-end="url(#at6)">
      <path d="M575 358V404H636V474H478V498"/>
      <path d="M365 358V404H440V474H338V498"/>
      <path d="M155 358V404H230V474H164V498"/>
    </g>
    <path d="M45 362V498" stroke="#0d9488" stroke-width="1.6" fill="none" stroke-dasharray="4 4" marker-end="url(#at6)"/>
    <rect x="40" y="502" width="600" height="84" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <g fill="#0f172a" text-anchor="middle" font-size="10">
      <text x="52" y="548" font-size="12">⋯</text><text x="66" y="548" font-size="12">+</text>
      <text x="94" y="536">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="94" y="560">∂h<tspan baseline-shift="sub" font-size="8">t</tspan></text>
      <text x="129" y="536">∂h<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="129" y="560">∂h<tspan baseline-shift="sub" font-size="8">t−1</tspan></text>
      <text x="164" y="536">∂h<tspan baseline-shift="sub" font-size="8">t−1</tspan></text><text x="164" y="560">∂h<tspan baseline-shift="sub" font-size="8">t−2</tspan></text>
      <text x="199" y="536">∂h<tspan baseline-shift="sub" font-size="8">t−2</tspan></text><text x="199" y="560">∂a<tspan baseline-shift="sub" font-size="8">t−2</tspan></text>
      <text x="234" y="536">∂a<tspan baseline-shift="sub" font-size="8">t−2</tspan></text><text x="234" y="560">∂V</text>
      <text x="260" y="548" font-size="12">+</text>
      <text x="286" y="536">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="286" y="560">∂h<tspan baseline-shift="sub" font-size="8">t</tspan></text>
      <text x="321" y="536">∂h<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="321" y="560">∂h<tspan baseline-shift="sub" font-size="8">t−1</tspan></text>
      <text x="356" y="536">∂h<tspan baseline-shift="sub" font-size="8">t−1</tspan></text><text x="356" y="560">∂a<tspan baseline-shift="sub" font-size="8">t−1</tspan></text>
      <text x="391" y="536">∂a<tspan baseline-shift="sub" font-size="8">t−1</tspan></text><text x="391" y="560">∂V</text>
      <text x="417" y="548" font-size="12">+</text>
      <text x="443" y="536">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="443" y="560">∂h<tspan baseline-shift="sub" font-size="8">t</tspan></text>
      <text x="478" y="536">∂h<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="478" y="560">∂a<tspan baseline-shift="sub" font-size="8">t</tspan></text>
      <text x="513" y="536">∂a<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="513" y="560">∂V</text>
      <text x="539" y="548" font-size="12">=</text>
      <text x="565" y="536">∂L<tspan baseline-shift="sub" font-size="8">t</tspan></text><text x="565" y="560">∂V</text>
    </g>
    <g stroke="#0f172a" stroke-width="0.7">
      <line x1="78" y1="544" x2="110" y2="544"/><line x1="113" y1="544" x2="145" y2="544"/><line x1="148" y1="544" x2="180" y2="544"/><line x1="183" y1="544" x2="215" y2="544"/><line x1="218" y1="544" x2="250" y2="544"/>
      <line x1="270" y1="544" x2="302" y2="544"/><line x1="305" y1="544" x2="337" y2="544"/><line x1="340" y1="544" x2="372" y2="544"/><line x1="375" y1="544" x2="407" y2="544"/>
      <line x1="427" y1="544" x2="459" y2="544"/><line x1="462" y1="544" x2="494" y2="544"/><line x1="497" y1="544" x2="529" y2="544"/>
      <line x1="549" y1="544" x2="581" y2="544"/>
    </g>
  </g>
</svg>

세 항을 나란히 놓고 보면 왼쪽 항일수록 곱해지는 분수의 수가 하나씩 늘어남. 각 항의 길이 차이가 곧 그 항의 크기가 얼마나 줄어들거나 커지는지를 결정함.

---

### 2.7 두 종류의 합

여기까지 합이 두 번 등장했으므로 구분해 둘 필요가 있음.

첫 번째는 **usage에 대한 합** 임. 하나의 loss $L_t$ 안에서 $U$와 $V$가 여러 time step에 반복 사용되므로 usage마다 항이 하나씩 생기고, 그 항들을 더한 것이 2.5와 2.6의 결과였음.

$$
\frac{\partial L_t}{\partial U}
= \sum_{i} \frac{\partial L_t}{\partial h_i} \frac{\partial h_i}{\partial a_i} \frac{\partial a_i}{\partial U}
$$

$$
\frac{\partial L_t}{\partial V}
= \sum_{i} \frac{\partial L_t}{\partial h_i} \frac{\partial h_i}{\partial a_i} \frac{\partial a_i}{\partial V}
$$

$W$는 usage가 하나뿐이므로 이 합이 나타나지 않고 항 하나로 끝남.

$$
\frac{\partial L_t}{\partial W}
= \frac{\partial L_t}{\partial o_t} \frac{\partial o_t}{\partial W}
$$

두 번째는 **loss에 대한 합** 임. 전체 loss는 각 time step loss의 합이므로, shared parameter의 최종 gradient는 각 $L_t$에 대한 gradient를 다시 합산하여 얻음.

$$
\frac{\partial L}{\partial U} = \sum_{t=1}^{T} \frac{\partial L_t}{\partial U}
$$

$$
\frac{\partial L}{\partial V} = \sum_{t=1}^{T} \frac{\partial L_t}{\partial V}
$$

$$
\frac{\partial L}{\partial W} = \sum_{t=1}^{T} \frac{\partial L_t}{\partial W}
$$

<!-- 각 time step loss의 gradient가 하나의 shared parameter gradient로 합산되는 과정 | source: ./figures/07_accumulation.svg -->
<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 680 552" role="img" aria-labelledby="f7t f7d">
  <title id="f7t">두 종류의 합</title>
  <desc id="f7d">하나의 loss 안에서 usage에 대한 합과, 모든 time step의 loss에 대한 합을 구분해 나타낸 그림</desc>
  <defs><marker id="ar7" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#64748b"/></marker></defs>
  <rect width="680" height="552" rx="20" fill="#f8fafc"/>
  <g font-family="Arial, 'Noto Sans KR', sans-serif">
    <text x="32" y="36" font-size="17" font-weight="700" fill="#0f172a">두 종류의 합</text>
    <rect x="28" y="58" width="624" height="250" rx="14" fill="#ffffff" stroke="#ddd6fe" stroke-width="1.5"/>
    <rect x="44" y="72" width="278" height="26" rx="13" fill="#ede9fe"/>
    <text x="183" y="90" text-anchor="middle" font-size="12" font-weight="700" fill="#6d28d9">A. usage에 대한 합 · 하나의 L<tspan baseline-shift="sub" font-size="9">t</tspan> 안에서</text>
    <g fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5"><rect x="40" y="110" width="170" height="44" rx="8"/><rect x="40" y="162" width="170" height="44" rx="8"/><rect x="40" y="214" width="170" height="44" rx="8"/></g>
    <text x="228" y="136" font-size="9" fill="#6d28d9">i = t</text>
    <text x="228" y="188" font-size="9" fill="#6d28d9">i = t−1</text>
    <text x="228" y="240" font-size="9" fill="#6d28d9">i = t−2</text>
    <text x="89" y="126" text-anchor="middle" font-size="9" fill="#4c1d95">∂L<tspan baseline-shift="sub" font-size="7">t</tspan></text><line x1="73" y1="132" x2="105" y2="132" stroke="#4c1d95" stroke-width="0.6"/><text x="89" y="146" text-anchor="middle" font-size="9" fill="#4c1d95">∂h<tspan baseline-shift="sub" font-size="7">t</tspan></text><text x="125" y="126" text-anchor="middle" font-size="9" fill="#4c1d95">∂h<tspan baseline-shift="sub" font-size="7">t</tspan></text><line x1="109" y1="132" x2="141" y2="132" stroke="#4c1d95" stroke-width="0.6"/><text x="125" y="146" text-anchor="middle" font-size="9" fill="#4c1d95">∂a<tspan baseline-shift="sub" font-size="7">t</tspan></text><text x="161" y="126" text-anchor="middle" font-size="9" fill="#4c1d95">∂a<tspan baseline-shift="sub" font-size="7">t</tspan></text><line x1="145" y1="132" x2="177" y2="132" stroke="#4c1d95" stroke-width="0.6"/><text x="161" y="146" text-anchor="middle" font-size="9" fill="#4c1d95">∂V</text><text x="89" y="178" text-anchor="middle" font-size="9" fill="#4c1d95">∂L<tspan baseline-shift="sub" font-size="7">t</tspan></text><line x1="73" y1="184" x2="105" y2="184" stroke="#4c1d95" stroke-width="0.6"/><text x="89" y="198" text-anchor="middle" font-size="9" fill="#4c1d95">∂h<tspan baseline-shift="sub" font-size="7">t−1</tspan></text><text x="125" y="178" text-anchor="middle" font-size="9" fill="#4c1d95">∂h<tspan baseline-shift="sub" font-size="7">t−1</tspan></text><line x1="109" y1="184" x2="141" y2="184" stroke="#4c1d95" stroke-width="0.6"/><text x="125" y="198" text-anchor="middle" font-size="9" fill="#4c1d95">∂a<tspan baseline-shift="sub" font-size="7">t−1</tspan></text><text x="161" y="178" text-anchor="middle" font-size="9" fill="#4c1d95">∂a<tspan baseline-shift="sub" font-size="7">t−1</tspan></text><line x1="145" y1="184" x2="177" y2="184" stroke="#4c1d95" stroke-width="0.6"/><text x="161" y="198" text-anchor="middle" font-size="9" fill="#4c1d95">∂V</text><text x="89" y="230" text-anchor="middle" font-size="9" fill="#4c1d95">∂L<tspan baseline-shift="sub" font-size="7">t</tspan></text><line x1="73" y1="236" x2="105" y2="236" stroke="#4c1d95" stroke-width="0.6"/><text x="89" y="250" text-anchor="middle" font-size="9" fill="#4c1d95">∂h<tspan baseline-shift="sub" font-size="7">t−2</tspan></text><text x="125" y="230" text-anchor="middle" font-size="9" fill="#4c1d95">∂h<tspan baseline-shift="sub" font-size="7">t−2</tspan></text><line x1="109" y1="236" x2="141" y2="236" stroke="#4c1d95" stroke-width="0.6"/><text x="125" y="250" text-anchor="middle" font-size="9" fill="#4c1d95">∂a<tspan baseline-shift="sub" font-size="7">t−2</tspan></text><text x="161" y="230" text-anchor="middle" font-size="9" fill="#4c1d95">∂a<tspan baseline-shift="sub" font-size="7">t−2</tspan></text><line x1="145" y1="236" x2="177" y2="236" stroke="#4c1d95" stroke-width="0.6"/><text x="161" y="250" text-anchor="middle" font-size="9" fill="#4c1d95">∂V</text>
    <text x="125" y="284" text-anchor="middle" font-size="13" font-weight="700" fill="#7c3aed">⋮</text>
    <g stroke="#64748b" stroke-width="1.6" fill="none" marker-end="url(#ar7)"><path d="M266 132C286 132 286 172 278 180"/><path d="M266 184H278"/><path d="M266 236C286 236 286 196 278 188"/></g>
    <circle cx="300" cy="184" r="20" fill="#fff7ed" stroke="#ea580c" stroke-width="2"/>
    <text x="300" y="191" text-anchor="middle" font-size="18" font-weight="700" fill="#ea580c">Σ</text>
    <path d="M322 184H368" stroke="#64748b" stroke-width="1.6" fill="none" marker-end="url(#ar7)"/>
    <rect x="372" y="160" width="180" height="48" rx="10" fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5"/>
    <text x="462" y="191" text-anchor="middle" font-size="15" font-weight="700" fill="#4c1d95">∂L<tspan baseline-shift="sub" font-size="10">t</tspan> / ∂V</text>
    <text x="462" y="240" text-anchor="middle" font-size="10" fill="#6d28d9">W 는 usage가 하나뿐이라 이 합이 나타나지 않음</text>
    <rect x="28" y="328" width="624" height="180" rx="14" fill="#ffffff" stroke="#bbf7d0" stroke-width="1.5"/>
    <rect x="44" y="342" width="278" height="26" rx="13" fill="#dcfce7"/>
    <text x="183" y="360" text-anchor="middle" font-size="12" font-weight="700" fill="#166534">B. loss에 대한 합 · 모든 time step</text>
    <g fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"><rect x="48" y="372" width="152" height="30" rx="8"/><rect x="48" y="408" width="152" height="30" rx="8"/><rect x="48" y="444" width="152" height="30" rx="8"/></g>
    <g text-anchor="middle" fill="#14532d" font-size="13" font-weight="700"><text x="124" y="392">∂L<tspan baseline-shift="sub" font-size="9">t−1</tspan> / ∂V</text><text x="124" y="428">∂L<tspan baseline-shift="sub" font-size="9">t</tspan> / ∂V</text><text x="124" y="464">∂L<tspan baseline-shift="sub" font-size="9">t+1</tspan> / ∂V</text></g>
    <text x="124" y="490" text-anchor="middle" font-size="13" font-weight="700" fill="#16a34a">⋮</text>
    <g stroke="#64748b" stroke-width="1.6" fill="none" marker-end="url(#ar7)"><path d="M202 387C248 387 248 415 276 420"/><path d="M202 423H276"/><path d="M202 459C248 459 248 432 276 426"/></g>
    <circle cx="298" cy="423" r="20" fill="#fff7ed" stroke="#ea580c" stroke-width="2"/>
    <text x="298" y="430" text-anchor="middle" font-size="18" font-weight="700" fill="#ea580c">Σ</text>
    <path d="M320 423H368" stroke="#64748b" stroke-width="1.6" fill="none" marker-end="url(#ar7)"/>
    <rect x="372" y="399" width="220" height="48" rx="10" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
    <text x="482" y="420" text-anchor="middle" font-size="15" font-weight="700" fill="#14532d">∂L / ∂V</text>
    <text x="482" y="438" text-anchor="middle" font-size="10" fill="#166534">optimizer가 V 를 한 번 update</text>
    <text x="340" y="532" text-anchor="middle" font-size="11" fill="#475569">U 와 W 에도 같은 원리가 적용되며, W 는 A 단계가 없음</text>
  </g>
</svg>

Loss를 time step에 대해 mean으로 정의했다면 gradient의 전체 scale은 달라질 수 있지만, 각 usage에서 발생한 contribution이 하나의 parameter gradient로 accumulation된다는 원리는 동일함.

---

## 3. Gradient Problems

2.6에서 본 것처럼 $V$에 대한 gradient의 각 항에는 $D_i V$ 가 반복해서 곱해짐. 이 반복 곱이 gradient problem의 직접적인 원인임.

### 3.1 Vanishing Gradient

$\tanh$의 derivative가 가지는 범위는 다음과 같음:

$$
0 < \tanh'(a_t) \le 1
$$

$\tanh$가 saturation 영역에 들어가면 derivative가 0에 가까워짐. 따라서 $D_t$는 많은 경우 local gradient의 magnitude를 감소시키는 방향으로 작용함.

Recurrent weight $V$도 해당 direction에서 gradient를 충분히 증폭시키지 못하면 recurrent local Jacobian이 gradient를 줄이는 방향으로 작용함.

이러한 local gradient가 chain rule에 의해 많은 recurrent step에 걸쳐 계속 곱해지면 distant earlier time step에 대한 gradient가 매우 작아질 수 있음. 이를 **vanishing gradient** 라고 함.

<!-- Recurrent step이 누적될수록 gradient magnitude가 0에 가까워지는 vanishing gradient | source: ./figures/08_vanishing_gradient.svg -->
<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 680 330" role="img" aria-labelledby="f8t f8d">
  <title id="f8t">Vanishing gradient</title>
  <desc id="f8d">1보다 작은 local factor가 반복해서 곱해질 때 gradient magnitude가 0에 가까워지는 현상</desc>
  <rect width="680" height="330" rx="20" fill="#f8fafc"/>
  <g font-family="Arial, 'Noto Sans KR', sans-serif">
    <text x="32" y="36" font-size="17" font-weight="700" fill="#0f172a">Vanishing gradient</text>
    <g stroke="#cbd5e1" stroke-width="1.5"><path d="M70 262H636"/><path d="M70 80V262"/></g>
    <g fill="#64748b" font-size="11"><text x="52" y="266">0</text><text x="42" y="86">1.0</text><text x="70" y="290">항에 포함된 반복 곱의 길이 →</text><text x="24" y="180" transform="rotate(-90 24 180)">gradient magnitude</text></g>
    <path d="M76 92C150 116 190 168 240 200S370 244 460 254S590 260 632 261" fill="none" stroke="#2563eb" stroke-width="4"/>
    <g fill="#2563eb"><circle cx="76" cy="92" r="5"/><circle cx="240" cy="200" r="5"/><circle cx="460" cy="254" r="5"/><circle cx="632" cy="261" r="5"/></g>
    <rect x="380" y="86" width="250" height="66" rx="12" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
    <text x="505" y="112" text-anchor="middle" font-size="14" font-weight="700" fill="#1e3a8a">0.7 × 0.7 × 0.7 × ··· → 0</text>
    <text x="505" y="136" text-anchor="middle" font-size="11" fill="#1e40af">긴 항일수록 earlier step의 기여가 작아짐</text>
  </g>
</svg>

그 결과는 다음과 같음.

- Distant earlier time step의 input이나 hidden state가 current output에 중요하더라도 해당 time step에 대한 gradient가 거의 0이 될 수 있음.
- 2.5와 2.6에서 본 합에서 왼쪽의 긴 항들이 사실상 0이 되어, gradient가 최근 몇 step의 기여만으로 결정됨.
- Simple RNN이 distant time steps 사이의 dependency를 학습하기 어려워짐.

즉 **vanishing gradient는 distant earlier time step의 gradient contribution이 parameter update에 충분히 반영되지 못하게 하므로 long-term dependency 학습과 직접적으로 연결됨.**

---

### 3.2 Exploding Gradient

Recurrent weight $V$가 특정 direction에서 gradient를 크게 증폭시키고 그 효과가 activation derivative에 의한 감소보다 크면, recurrent local Jacobian이 gradient를 증폭시키는 방향으로 작용할 수 있음.

이러한 local gradient가 여러 recurrent step에 걸쳐 계속 곱해지면 전체 gradient magnitude가 매우 커질 수 있음. 이를 **exploding gradient** 라고 함.

<!-- Recurrent step이 누적될수록 gradient magnitude가 급격히 증가하는 exploding gradient | source: ./figures/09_exploding_gradient.svg -->
<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 680 330" role="img" aria-labelledby="f9t f9d">
  <title id="f9t">Exploding gradient</title>
  <desc id="f9d">1보다 큰 local factor가 반복해서 곱해질 때 gradient magnitude가 급격히 증가하는 현상</desc>
  <rect width="680" height="330" rx="20" fill="#f8fafc"/>
  <g font-family="Arial, 'Noto Sans KR', sans-serif">
    <text x="32" y="36" font-size="17" font-weight="700" fill="#0f172a">Exploding gradient</text>
    <g stroke="#cbd5e1" stroke-width="1.5"><path d="M70 262H636"/><path d="M70 80V262"/></g>
    <g fill="#64748b" font-size="11"><text x="52" y="266">0</text><text x="30" y="86">large</text><text x="70" y="290">항에 포함된 반복 곱의 길이 →</text><text x="24" y="180" transform="rotate(-90 24 180)">gradient magnitude</text></g>
    <path d="M76 256C200 255 290 248 360 226S470 160 530 116S610 84 632 76" fill="none" stroke="#dc2626" stroke-width="4"/>
    <g fill="#dc2626"><circle cx="76" cy="256" r="5"/><circle cx="360" cy="226" r="5"/><circle cx="530" cy="116" r="5"/><circle cx="632" cy="76" r="5"/></g>
    <rect x="96" y="86" width="250" height="66" rx="12" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
    <text x="221" y="112" text-anchor="middle" font-size="14" font-weight="700" fill="#7f1d1d">1.4 × 1.4 × 1.4 × ··· → ∞</text>
    <text x="221" y="136" text-anchor="middle" font-size="11" fill="#991b1b">large update · oscillation · Inf / NaN</text>
  </g>
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

2.5와 2.6에서 유도한 것처럼 $U$와 $V$의 gradient는 길이가 서로 다른 항들의 합이며, distant earlier time step에 대응하는 항일수록 $D_i V$ 가 더 많이 곱해짐. Vanishing gradient가 발생하면 이 긴 항들이 거의 0이 되어 해당 dependency의 gradient contribution이 parameter update에 반영되지 못함.

<!-- Forward pass에서 earlier information을 유지하는 문제와 backward vanishing gradient의 구분 | source: ./figures/10_long_term_dependency.svg -->
<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 680 520" role="img" aria-labelledby="f10t f10d">
  <title id="f10t">Long-term dependency의 forward와 backward 문제</title>
  <desc id="f10d">Forward pass의 information 유지 문제와 backward pass의 vanishing gradient를 분리해 나타낸 그림</desc>
  <defs><marker id="ar10" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#334155"/></marker><marker id="ap10" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#ea580c"/></marker></defs>
  <rect width="680" height="520" rx="20" fill="#f8fafc"/>
  <g font-family="Arial, 'Noto Sans KR', sans-serif">
    <text x="32" y="36" font-size="17" font-weight="700" fill="#0f172a">Long-term dependency problem</text>
    <rect x="28" y="58" width="624" height="186" rx="14" fill="#ffffff" stroke="#bfdbfe" stroke-width="1.5"/>
    <rect x="44" y="72" width="290" height="26" rx="13" fill="#dbeafe"/>
    <text x="189" y="90" text-anchor="middle" font-size="12" font-weight="700" fill="#1e40af">A. Forward pass · earlier information 유지</text>
    <rect x="48" y="120" width="86" height="44" rx="10" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
    <text x="91" y="148" text-anchor="middle" font-size="14" font-weight="700" fill="#1e3a8a">x<tspan baseline-shift="sub" font-size="9">k</tspan></text>
    <g fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5"><rect x="176" y="120" width="86" height="44" rx="10"/><rect x="304" y="120" width="86" height="44" rx="10"/><rect x="432" y="120" width="86" height="44" rx="10"/></g>
    <g text-anchor="middle" fill="#4c1d95" font-size="14" font-weight="700"><text x="219" y="148">h<tspan baseline-shift="sub" font-size="9">k</tspan></text><text x="347" y="148">h<tspan baseline-shift="sub" font-size="9">k+1</tspan></text><text x="475" y="148">h<tspan baseline-shift="sub" font-size="9">t</tspan></text></g>
    <rect x="560" y="120" width="72" height="44" rx="10" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
    <text x="596" y="148" text-anchor="middle" font-size="14" font-weight="700" fill="#14532d">o<tspan baseline-shift="sub" font-size="9">t</tspan></text>
    <g stroke="#334155" stroke-width="1.5" fill="none" marker-end="url(#ar10)"><path d="M136 142H174"/><path d="M264 142H302"/><path d="M392 142H430"/><path d="M520 142H558"/></g>
    <text x="411" y="116" text-anchor="middle" font-size="13" font-weight="700" fill="#64748b">···</text>
    <text x="340" y="212" text-anchor="middle" font-size="11" fill="#475569">서로 다른 earlier input을 담은 state representation이 later step에서 구분되기 어려워질 수 있음</text>
    <rect x="28" y="264" width="624" height="180" rx="14" fill="#ffffff" stroke="#fed7aa" stroke-width="1.5"/>
    <rect x="44" y="278" width="280" height="26" rx="13" fill="#ffedd5"/>
    <text x="184" y="296" text-anchor="middle" font-size="12" font-weight="700" fill="#9a3412">B. Backward pass · vanishing gradient</text>
    <rect x="536" y="326" width="96" height="40" rx="10" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
    <text x="584" y="351" text-anchor="middle" font-size="14" font-weight="700" fill="#7f1d1d">L<tspan baseline-shift="sub" font-size="9">t</tspan></text>
    <path d="M534 346H366" stroke="#fdba74" stroke-width="1.6" fill="none" marker-end="url(#ap10)"/>
    <g fill="#ea580c" stroke="#ffffff" stroke-width="1"><circle cx="512" cy="346" r="10"/><circle cx="472" cy="346" r="7.5"/><circle cx="432" cy="346" r="5"/><circle cx="396" cy="346" r="3"/></g>
    <text x="452" y="318" text-anchor="middle" font-size="10" fill="#9a3412">반복 곱이 길수록 작아짐</text>
    <rect x="212" y="326" width="148" height="40" rx="10" fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5"/>
    <text x="286" y="351" text-anchor="middle" font-size="12" font-weight="700" fill="#4c1d95">usage at i = k</text>
    <g stroke="#64748b" stroke-width="1.5" fill="none" marker-end="url(#ar10)"><path d="M210 340C192 340 180 324 152 320"/><path d="M210 352C192 352 180 368 152 372"/></g>
    <g fill="#ffffff" stroke="#7c3aed" stroke-width="1.5"><rect x="46" y="304" width="104" height="30" rx="8"/><rect x="46" y="356" width="104" height="30" rx="8"/></g>
    <g text-anchor="middle" fill="#4c1d95" font-size="12" font-weight="700"><text x="98" y="324">∂L<tspan baseline-shift="sub" font-size="9">t</tspan> / ∂U</text><text x="98" y="376">∂L<tspan baseline-shift="sub" font-size="9">t</tspan> / ∂V</text></g>
    <text x="340" y="416" text-anchor="middle" font-size="11" fill="#9a3412">distant usage의 항이 0에 가까워지면 그 dependency가 U 와 V 의 update에 반영되지 않음</text>
    <rect x="120" y="464" width="440" height="30" rx="15" fill="#fff7ed" stroke="#fdba74" stroke-width="1.5"/>
    <text x="340" y="484" text-anchor="middle" font-size="12" font-weight="700" fill="#9a3412">Forward의 information 유지와 backward의 vanishing gradient는 구분해야 함</text>
  </g>
</svg>

두 문제의 관계는 다음과 같음.

- Forward pass에서는 earlier information을 later hidden state의 representation에 유지하고 사용하는 것이 어려울 수 있음.
- Backward pass에서는 vanishing gradient 때문에 distant earlier time step의 gradient contribution이 parameter update에 충분히 반영되지 못할 수 있음.
- Exploding gradient는 같은 recurrent local-gradient multiplication에서 발생할 수 있지만, 주로 optimization stability를 해치는 별도의 문제임.

즉 Simple RNN의 long-term dependency problem을 설명할 때는 **forward pass에서 earlier information을 hidden state에 유지하는 문제** 와 **backward pass의 vanishing gradient problem** 을 구분해야 함.

### 4.4 LSTM과 GRU

LSTM과 GRU는 information을 선택적으로 preserve하고 update하는 **gating mechanism** 을 도입하여 Simple RNN의 long-term dependency problem을 완화하는 RNN architecture임.
