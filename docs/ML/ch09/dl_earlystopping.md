# Early Stopping

`Early Stopping`은 training을 정해진 epoch 끝까지 무조건 진행하지 않고, validation 성능이 더 이상 좋아지지 않는 시점에서 학습을 멈추는 regularization(정규화) 기법임.

<img width="438" height="239" alt="image" src="https://github.com/user-attachments/assets/2b994da1-8b55-4a1a-aae9-2799f9dd9543" />


## 배경

* Deep Learning model은 학습을 오래 진행할수록 training loss는 계속 감소하는 경향이 있음.
* 하지만 어느 시점 이후에는 training data에 지나치게 맞춰지면서(overfitting) validation loss가 다시 증가할 수 있음.
* 즉, 다음과 같은 상황이 발생함.
    * training loss는 계속 감소함 (training data의 noise까지 학습).
    * validation loss는 어느 시점까지 감소하다가 다시 증가함.
    * 이 시점 이후부터는 generalization performance(일반화 성능)가 나빠질 가능성이 커짐.

수식으로 나타내면 다음과 같음. $t$를 epoch, $L_{val}(t)$를 validation loss라 할 때,

$$
L_{val}(t) \;\begin{cases} \text{decreasing} & t < t^{*} \\ \text{increasing} & t > t^{*} \end{cases}
$$

* 여기서 $t^{*}$는 validation loss가 최소가 되는 epoch이며, 이 지점을 넘기면 overfitting이 본격화되는 구간으로 볼 수 있음.

## 동작 방식

* Early Stopping은 validation metric을 기준으로 model의 성능을 관찰함.
* 일정 epoch(=`patience`) 동안 성능 개선이 없으면 학습을 중단함.
    * 예: `patience=5` → validation loss가 5 epoch 연속 개선되지 않으면 training 중단.
* 학습을 멈춘 마지막 epoch의 model을 그대로 쓰는 것이 아니라, validation 성능이 가장 좋았던 epoch의 model weight를 별도로 저장해두었다가 최종 model로 사용하는 경우가 많음.
    * 즉, "마지막 epoch"과 "best epoch"을 구분해서 다뤄야 함.

## 정리

* Early Stopping은 overfitting이 본격적으로 진행되기 전에 학습을 멈추는 기법임.
* validation 성능이 가장 좋았던 model을 최종적으로 선택함으로써 generalization performance를 높임.
* 별도의 model architecture 변경 없이 적용 가능한 regularization 기법이라는 점에서 dropout, weight decay 등과 함께 자주 병행됨.

## PyTorch 예제

* PyTorch는 Early Stopping을 위한 built-in class를 별도로 제공하지 않음.
* 대신 `torch.save` / `torch.load`로 model checkpoint를 저장하고 복원하는 방식이 가장 널리 쓰이는 표준 패턴임.

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

torch.manual_seed(0)

# 1. 데이터 준비 (synthetic regression data)
N = 2000
X = torch.randn(N, 10)
true_w = torch.randn(10, 1)
y = X @ true_w + 0.5 * torch.randn(N, 1)  # noise 포함

n_train = int(N * 0.8)
X_train, y_train = X[:n_train], y[:n_train]
X_val, y_val = X[n_train:], y[n_train:]

train_loader = DataLoader(TensorDataset(X_train, y_train), batch_size=32, shuffle=True)
val_loader = DataLoader(TensorDataset(X_val, y_val), batch_size=32, shuffle=False)

# 2. model / optimizer / loss 정의
model = nn.Sequential(
    nn.Linear(10, 64),
    nn.ReLU(),
    nn.Linear(64, 64),
    nn.ReLU(),
    nn.Linear(64, 1),
)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.MSELoss()

# 3. Early Stopping 관련 변수
best_val_loss = float("inf")
patience = 5
min_delta = 1e-4
patience_counter = 0
checkpoint_path = "best_model.pt"

# 4. training loop
num_epochs = 200
for epoch in range(num_epochs):
    model.train()
    train_loss_sum = 0.0
    for xb, yb in train_loader:
        optimizer.zero_grad()
        pred = model(xb)
        loss = criterion(pred, yb)
        loss.backward()
        optimizer.step()
        train_loss_sum += loss.item() * xb.size(0)
    train_loss = train_loss_sum / len(train_loader.dataset)

    model.eval()
    val_loss_sum = 0.0
    with torch.no_grad():
        for xb, yb in val_loader:
            pred = model(xb)
            loss = criterion(pred, yb)
            val_loss_sum += loss.item() * xb.size(0)
    val_loss = val_loss_sum / len(val_loader.dataset)

    print(f"Epoch {epoch:3d} | train_loss={train_loss:.4f} | val_loss={val_loss:.4f}")

    if val_loss < best_val_loss - min_delta:
        best_val_loss = val_loss
        patience_counter = 0
        torch.save(
            {
                "epoch": epoch,
                "model_state_dict": model.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
                "val_loss": val_loss,
            },
            checkpoint_path,
        )
    else:
        patience_counter += 1
        if patience_counter >= patience:
            print(f"Early stopping triggered at epoch {epoch}")
            break

# 5. best checkpoint 복원
checkpoint = torch.load(checkpoint_path, weights_only=True)
model.load_state_dict(checkpoint["model_state_dict"])
print(f"Restored model from epoch {checkpoint['epoch']} (val_loss={checkpoint['val_loss']:.4f})")
```

* `best_val_loss` : 지금까지의 가장 작은 validation loss 저장
* `patience` : 성능 개선이 없어도 몇 epoch까지 기다릴지 결정
* `min_delta` : 이 값 이상 loss가 줄어야 “개선”으로 인정
* `patience_counter` :개 선되지 않은 epoch 수를 누적
* `checkpoint_path` : 가장 성능이 좋았던 모델을 저장할 경로

정리하면, `val_loss`가 `best_val_loss - min_delta` 보다 작아지면 개선으로 보고 patience_counter를 0으로 초기화함.  
그렇지 않으면 `patience_counter`를 증가시키고, 이 값이 `patience`에 도달하면 학습을 조기 종료함.

## 참고

* 위 패턴을 좀 더 구조화한 형태로 `pytorch-lightning`의 `EarlyStopping` callback이나 `ignite`의 `EarlyStopping` handler를 사용하는 경우도 많음.
* 다만 순수 PyTorch만 사용하는 환경에서는 위와 같이 `torch.save` 기반 checkpoint 저장 + 수동 patience counter 관리가 가장 표준적인 방식임.
