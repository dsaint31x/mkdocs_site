---
title: Register
tags: [Register, Flip-Flop, SRAM]
---

# Registers 

## `Flip-Flop` 들을 묶어서 Register로.

**1 Bit를 기억할 수 있는 `Filp-flop`** 들을 여러 개를 묶어서,  
***여러 Bits를 기억*** 하도록 만들어진 Device.
  
> ^^CPU 내부에 위치하며, ALU 등이 직접 접근하여 사용되는 Memory가 바로 Register임.^^    
> 
> * 가장 빠르고, 
> * 가장 비싼 memory 라고 할 수 있음 (여러 bits를 저장하는).

---

---

## Register 들을 묶어서 Memory로.

* Register를 ***여러 개 사용하면 보다 많은 Bit를 저장*** 할 수 있음. 
* 이는 여러 Flip-Flop을 사용하여 여러 Bits 를 기억하는 Register로 확장한 것과 같음.
    * 8개의 `D flip-flop`들을 묶어서 사용하면 8bit Register가 가능함.
* 하지만 보다 많은 여러 Bits 를 기억하기 위해서는 
    * ^^각각의 값들이 어느 Register에 저장되는지를 나타내는 ***Address가 필요***^^ 하며, 
    * 이를 위해 `Decoder`와 `Selector (Mux)`가 연결된 
    * `memory` device (`Static RAM`)가 등장하게 됨.

> 여기서 애기하는 Memory와 Register는 `Static RAM` 기반임. 

---

---

## Schematic Representation

![8bit Register](img/register_8bit.png){style="display:block; margin:0 auto;width:300px"}

- `clock` : rising edge에 입력 `D`의 값이 `Q`에서 출력.
- `enable` : 해당 입력이 `Active` 여야 Register가 동작함(여기선 `1`이어야함.)
