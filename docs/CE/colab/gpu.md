# Colab: GPU 사용하기

Colab에서는 주로 CUDA 기반의 [GPU](../ch04/ce04_51_gpu_tpu.md#graphics-processing-units) 가속을 지원

- 런타임 → 런타임 유형 변경 → 하드웨어 가속기를 GPU로 변경
- 유의사항 – GPU는 최대 12시간 실행을 지원
- 12시간 실행 이후에는 런타임 재시작으로 VM을 교체해야 함

![](./img/colab_GPU.png)

> [TPU (Tensor Processing Unit)](../ch04/ce04_51_gpu_tpu.md#tensor-processing-unit-tpu)은 GPU가 아닌 AI Accelerator로  
> 애당초 Tensor Processing을 위해 설계 구현된 ASIC (Application Specific Integrated Circuit).

GPU 가속을 사용하면 다음을 통해, GPU 사양과 상태도 확인 가능함.

```
!nvidia-smi
```

* 참고: [GPU Acceleration 기술 소개](https://ds31x.tistory.com/375)

---

## NVIDIA 의 CUDA (Compute Unified Device Architecture)를 이용한 GPU가속

PyTorch 에서 확인은 다음 코드를 사용.

```Python

import torch

print(torch.cuda.is_available()) 
print(torch.cuda.device_count()) # returns number of available GPU. 1 in my case
print(torch.cuda.current_device()) # returns index. 0 in my case
print(torch.cuda.get_device_name(0)) # Tesla T4
```

다음은 PyTorch에서 GPU를 확인하고, 특정 tensor를 CUDA GPU에 지정하는 예제코드임.

[PyTorch Example](https://gist.github.com/dsaint31x/ad7181dbb1b8c12c2db8b9454cfa0ddb)

---

## Apple 의 MPS (Metal Performance Shaders)를 이용한 GPU가속.

PyTorch 에서의 확인은 다음과 같음.

```Python
print(f"Metal Performance Shaders (MPS)를 지원하도록 build 되었음: {torch.backends.mps.is_built()}")
print(f"현재 mps 가속을 사용할 수 있음: {torch.backends.mps.is_available()}")

devices = []

if torch.cuda.is_available():
    for i in range(torch.cuda.device_count()):
        devices.append(f"cuda:{i}")
if torch.backends.mps.is_available():
    devices.append("mps")
devices.append("cpu")

print(f"Available devices: {devices}")

device = torch.device(devices[0])
```

다음은 PyTorch에서 MPS 가속을 사용하는 예제 코드임.

[DL_MPS_Test](https://gist.github.com/dsaint31x/bdd3b9461d5cdc1779b86665f774c821)