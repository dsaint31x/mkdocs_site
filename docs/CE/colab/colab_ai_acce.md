# AI 가속기 for Colab 및 아키텍처 종합 정리

## 1. AI Accelerators Combined (NVIDIA GPU + Google TPU, Sorted by Performance)

NVIDIA 아키텍처는 Turing → Ampere → Hopper → Ada Lovelace → Blackwell → Rubin 순으로 발전함.  
Google TPU는 v5e → v6e(Trillium) → v7(Ironwood) 순으로 세대가 진행됨.

이 절에서는 다음 기준으로 정렬함.

* 가능한 경우 BF16/FP16 Tensor 연산 기준 dense peak 성능
* 제조사 표기가 sparsity 포함값인 경우 dense 값과 구분함
* 높은 순서대로 나열함

참고: [FLOPS](../ch00/history_of_computers.md#flops)

<img width="408" height="385" alt="image" src="https://github.com/user-attachments/assets/824a06b7-2941-4be0-aa59-74695b5626e7" />


사용 가능한 가속기들은 다음과 같음:

1. H100
    * 2022년, NVIDIA Hopper architecture
    * 메모리: 80GB HBM3
    * Performance: 약 989 TFLOPS BF16 Tensor dense, sparsity 사용 시 약 1,979 TFLOPS, FP8 지원
    * 무료 계정 사용 가능 여부: 불가능 - Colab Pro+ 또는 Pay As You Go 등 유료 계정에서 선택 가능하나 가용성은 수시로 변동됨

2. G4 (NVIDIA RTX PRO 6000 Blackwell Server Edition)
    * 2025년 공개, Colab 적용은 2026년
    * 메모리: 96GB GDDR7
    * Performance: FP16/BF16 Tensor Core 약 1 PFLOP급 peak, FP4 Tensor Core 약 4 PFLOPS급 peak
    * 무료 계정 사용 가능 여부: 불가능 - 최신 고성능 GPU로 유료 계정의 compute unit이 필요하며 가용성은 수시로 변동됨

3. TPU v6e (Trillium)
    * 2024년 발표 및 출시
    * 메모리: 칩당 32GB HBM
    * 성능: 칩당 약 918 TFLOPS BF16
    * 무료 계정 사용 가능 여부: 보장되지 않음 - Colab의 TPU 제공 여부는 시점과 계정 상태에 따라 달라짐

4. A100 80GB
    * 출시: 2020년, NVIDIA Ampere architecture
    * 메모리: 80GB HBM2e
    * 성능: BF16 약 312 TFLOPS dense, sparsity 사용 시 약 624 TFLOPS
    * 무료 계정 사용 가능 여부: 불가능 - 유료 계정에서 선택 가능하나 가용성은 수시로 변동됨

5. A100
    * 출시: 2020년, NVIDIA Ampere architecture
    * 메모리: 40GB HBM2
    * 성능: BF16 약 312 TFLOPS dense, sparsity 사용 시 약 624 TFLOPS
    * 무료 계정 사용 가능 여부: 불가능 - 유료 계정에서 선택 가능하나 가용성은 수시로 변동됨

6. TPU v5e
    * 출시: 2023년
    * 메모리: 칩당 약 16GB HBM
    * 성능: 칩당 약 197 TFLOPS BF16
    * 무료 계정 사용 가능 여부: 제한적 - 무료 등급에서도 TPU 런타임이 노출될 수 있으나 할당량과 가용성은 보장되지 않음

7. L4
    * 출시: 2023년, NVIDIA Ada Lovelace architecture
    * 메모리: 24GB GDDR6
    * 성능: FP32 약 30.3 TFLOPS, BF16 약 121 TFLOPS dense, sparsity 사용 시 약 242 TFLOPS
    * 무료 계정 사용 가능 여부: 불가능 - 주로 유료 계정에서 제공되며 가용성은 수시로 변동됨

8. T4
    * 출시: 2018년, NVIDIA Turing architecture
    * 메모리: 16GB GDDR6(ECC 적용 시 약 15GB 가용)
    * 성능: FP32 약 8.1 TFLOPS, FP16 Tensor 약 65 TFLOPS
    * 무료 계정 사용 가능 여부: 가능 - 무료 등급에서 자주 배정되는 GPU이나 세션 시간과 가용성에는 제한이 있음

---

## 2. Colab 할당 가능성 순 정렬

아래 순서는 공식 등급(무료/Pro/Pro+) 에서 사용가능한 가속기들의 종류를 배정 빈도 순으로 정렬(쉽게 배정가능한 순)함.

* T4
    - 무료 등급의 기본 GPU로,
    - 신용카드나 구독 없이 거의 항상 즉시 배정되어 할당 가능성이 가장 높음.
* L4
    * Colab Pro 등급에서 비교적 자주 배정되는 중급 GPU
    * A100보다 수요가 적어 확보 가능성이 높음.
* A100
    * Pro/Pro+에서 선택 가능하지만 인기가 높아 경쟁이 있는 편
    * 컴퓨팅 단위가 있으면 비교적 잘 배정됨.
* TPU v5e
    * 무료 등급에서도 런타임 옵션으로 노출
    * 할당량이 매우 제한적이어서, GPU보다는 배정 가능성이 다소 낮음.
* A100 80GB
    * "High-RAM" 옵션을 함께 켜야 선택됨
    * 기본 A100보다 확보가 더 어려움.
* TPU v6e (Trillium)
    * 신형 TPU
    * v5e보다 공급이 적어 배정 가능성이 더 낮음.
* H100
    * Pro+에서도 수요가 매우 높으나 배정 가능성이 매우 낮음.
* G4 (RTX PRO 6000 Blackwell)
    * Colab에 가장 최근 추가된 최상위 GPU
    * 재고가 가장 한정적이어서, 배정 가능성이 가장 낮음.

---

## 3. NVIDIA 아키텍처 연표 (개발년도순)

* Rubin (2026년 하반기 출시 예정)
    * Blackwell의 후속 아키텍처
    * 2024년 6월 Computex에서 코드명이 처음 공개
    * HBM4 메모리와 NVFP4 기반 3세대 Transformer Engine을 통해
    * 추론 토큰 비용을 Blackwell 대비 최대 10배 절감하고
    * MoE 학습에 필요한 GPU 수를 최대 4배 줄이는 것을 목표로 함.
* Blackwell (2024~2025)
    * G4(RTX PRO 6000 Blackwell)에 적용된 아키텍처
    * FP4 네이티브 지원과 대용량 GDDR7 메모리를 통해 추론·미세조정 효율을 극대화함. 
* Ada Lovelace (2023)
    * L4에 적용된 아키텍처
    * 추론 효율과 전력 대비 성능에 초점을 맞춘 중급 라인업. 
* Hopper (2022)
    * H100에 적용된 아키텍처
    * FP8 연산과 Transformer Engine을 도입해 LLM 학습·추론 성능을 크게 끌어올림.
* Ampere (2020)
    * A100/A100 80GB에 적용된 아키텍처
    *  TF32와 구조적 sparsity를 지원해 대규모 학습 효율을 크게 높임. 
* Turing (2018)
    * T4에 적용된 보급형 아키텍처
    * Tensor Core를 처음 도입한 세대는 Volta이고, Turing은 2세대 Tensor Core와 INT8/INT4 추론 지원을 강화한 세대임.
    * 추론과 경량 학습에 적합함.

---

## 4. Google TPU 세대 연표 (개발년도순)

* Turing (2018)
    * T4에 적용된 보급형 아키텍처
    * Tensor Core를 처음 도입한 세대는 Volta이고, Turing은 2세대 Tensor Core와 INT8/INT4 추론 지원을 강화한 세대임.
    * 추론과 경량 학습에 적합함.
- TPU v6e, Trillium (2024)
    * v5e 대비 약 4.7배 연산 성능과 2배의 HBM 용량·대역폭(칩당 32GB)을 제공하는 6세대 TPU.
* TPU v5e (2023)
    * 비용 효율에 초점을 맞춤
    * 칩당 약 16GB HBM을 탑재해 JAX/TensorFlow/PyTorch-XLA 학습·추론을 저비용으로 처리함.

