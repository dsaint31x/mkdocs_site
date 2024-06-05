# Assembly Language (어셈블리어)

1세대 programming language인 machine code의 뒤를 이어 등장한 2세대 programming language임.

## 특징

Machine code와 1:1로 대응하는 Mnemonic언어임.

* Machine Language의 binary code에서의 bit pattern 들의 조합 대신 간단한 영어단어에 해당하는 mnemonics를 사용.
* address에 label을 붙여서 보다 기억하기 쉽고 효율적인 프로그래밍이 가능해짐.
* comment가 가능해짐 (가독성 대폭 향상됨)

> 기억하기 쉽도록 machine language 의 instructor에 상징적인 기호 (영어단어로 생각하면 쉬움)를 할당한 것임.  
>  

다음과 같은 대응이 이루어짐.

***기계어***

```
00000000 00000000 10110000 01110001
```

***Assembly language***

```
mov al, 061h
```


매우 실행 속도가 빠르며, 약간의 호환성(메인 프레임과 유닉스 간)을 가짐.

---

## Assembler 란?

Assembly language 로 작성된 source code를 읽어들여서 해당하는 machine language code (binary code)를 생성해주는 프로그램.

* Assembly language에서 사용된 symbol과 label을 실제 binary pattern으로 바꾸어줌.

> 최초의 assembler는 machine language로 작성되었음. 해당 assembler를 이용하여 assembly language로 좀 더 나은 assembler를 만들고, 이 assembler를 이용하여 assembly language로 좀 더 나은 assembler를 만드는 식으로 개선이 이루어짐.  
> 이같은 개선을 bootstrap (or boot)이라고도 한다. 좀더 자세한 건 다음 URL 참고 : [Bootstrap](https://ds31x.blogspot.com/2023/07/term-bootstrap.html)  

---

---

## 사용분야

80196과 같은 마이크로프로세서 혹은 firmware 프로그래밍에서 꽤 자주 사용됨. 

* [Micro-Controller, Micro Controller Unit, Micro Control Unit](https://dsaint31.me/mkdocs_site/CE/ch04/ce04_04_cpu/#micro-controller-unit-mcu)

---


## Examples

Hello World를 출력하는 C 소스코드 에 대응하는 Assemly language program.

```Asm
_main:

push ebp

mov ebp, esp

push sHelloWorld ; 명령어와 주석을 조합할 수 있습니다.

call print_string ; print_string 프로시저를 호출합니다.

mov eax, 0 
; 빈 줄에도 주석을 달 수 있습니다.
; 프로세스가 0 이외의 값을 반환하면
; 정상적으로 종료되지 않은 것으로
; 간주하기 때문에, 반환 값을 언제나
; 0으로 맞춰주어야 합니다.

end1: mov esp, ebp ; 구문의 모든 요소를 적용한 명령입니다.
end2: pop ebp
end3: ret ; 프로시저를 반환합니다.
end4: ; _main의 경우 프로그램이 종료됩니다.
```

Fibonacci sequence에 해당하는 Assembly language program.

```Asm
        load    #0
        store   first
        load    #1
        store   second
again:
        load    first
        add     second
        store   next

        load    second
        store   first
        load    next
        store   second
        cmp     #200    ;200까지만 계산.
        ble     again   ; 작거나 같은 경우 agina label로 jump 
first:  bss     1 ; memory 할당.
second: bss     1 
next:   bss     1       
```

---

## 더 읽어보면 좋은 자료들

* [Mnemonic 이란?](https://medium.com/hexlant/mnemonic-%EC%9D%B4%EB%9E%80-7fb48106bd77)
* [어셈블리 튜토리얼(Assembly Tutorial): C를 이용한 Assembly 코드 분석(Assembly Code Analysis Using C)](https://blog.naver.com/rbfwmqwntm/30165613835)
