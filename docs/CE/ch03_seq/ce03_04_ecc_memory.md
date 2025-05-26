# Error Checking and Correction Memory (ECC Memory)

> RAM 중에서 ***data의 무결성이 중요*** 한 경우(서버용)를 위한 것으로
>   
> * 저장된 데이터의 오류를 
> * 체크하고 수정하는 기능이 있는 것.
>
> 매우 고가이며, PC 등에서는 보통 사용하지 않음.

`Parity check` 와 같이 parity bit를 통해 오류 발생여부를 확인만 가능한 기법부터, `Hamming code` 등과 같이 오류의 수정까지 가능한 좀 더 복잡한 방법 등이 사용됨.

> 단순히 오류를 검출하는 기능만을 가지는 경우보다 **오류 수정을 하는 기능** 까지 가지려면 ***보다 많은 bit를 사용해야 함.***

* 참고: [Hamming Code](https://ds31x.tistory.com/438)

---

# Checksum and CRC

**1) 특정 파일이 변조되지 않았는지** 라던지 **2) 제대로 다운로드되었는지** 등을 **검증하는 방법들**.

* `parity bit`를 이용한 기술들이 동적인 데이터(계속해서 값이 변화하는 RAM에 저장된 데이터)에 적합한 기술이라면, 
* `Checksum`과 `CRC`는 ***정적인 데이터 (설치 파일 등)에 적합*** 한 기술임.

특정 데이터가 생성되었을 때, Checksum(데이터들을 단위별로 더하고 넘어가는 값은 무시)이나 Cyclic Redundancy Check(CRC), Hash code 등을 계산해 저장해두면, 이후 예기치 않게 해당 데이터가 바뀐 경우 이를 확인할 수 있음.
