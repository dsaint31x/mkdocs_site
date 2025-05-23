---
title: Totem-Pole Output
tags: [Totem-Pole, Active Pull-Up]
---

# Totem-Pole Output

## Totem-Pole Output: Active Pull-Up

다음 그림은 NPN BJT를 2개를 연결한 Totem-Pole Output을 보여줌.

> 위와 아래에 같은 NPN BJT가 연결되어 토템처럼 보인다고 해서 Totem-Pole이라고 불림


![totem-pole-output](imgs/totem_pole_output.png){style="display: block; margin:0 auto; width:700px"}

* 오른쪽 푸른색 박스가 `Totem-Pole` Output의 구성이고, 왼쪽 검은색 박스는 `Totem-Pole` Output의 Transistor에 입력을 가할 때의 출력을 보여준다. 
    * 왼쪽 검은색 박스의 왼쪽은 input이 `0`이 들어가서, 
        * Totem-Pole의 상단에는 `1`이 하단에는 `0`이 들어가며 이로 인해 Output이 `1`이 나옴.
    * 왼쪽 검은색 박스의 오른쪽은 Output이 `1`이 들어간 경우로 Output이 `0`으로 나옴.
* 왼쪽 검은색 박스의 왼쪽과 오른쪽 각각의 그림에서 ^^상하로 연결된 NPN BJT들의 구조가 `Totem-Pole`^^ 임.
    * 상하의 NPN BJT의 Base에서 들어가는 Input은 항상 달라야 함(상보형 동작).

상단의 BJT는 일종의 **`Active Pull-Up`** 으로 출력을 High Voltage와 연결하고 있음.

---

---

## Note

`Open-Collector` (`FET`의 경우 `Open-Drain`)의 경우와 달리,  
`Totem-Pole` Output은 <span color='red'>절대 서로 곧바로 연결해서는 안됨</span>.

![totem-pole-output-connection](imgs/totem_pole_output_connection_short.png){style="display: block; margin:0 auto;width:500px"}

* output을 서로 연결할 경우, 
* 한쪽이 `1`이고 다른 쪽인 `0`인 경우 ***Short가 일어나서*** 출력단에 연결된 BJT가 망가지게 됨.

---

---

## Example

[tinkerad_ex](https://www.tinkercad.com/things/6S3FmdPsoU3)