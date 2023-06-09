# Compiler Language and Interpreter Language

## Compiler Language

![](./img/compiler_language.png){width="500"}

* `Compiler`(High-level language를 machine language로 번역)를 사용하는 고급 언어.
* 프로그램 전체를 읽어들여 이를 object code(목적코드)로 바꿈.
* `Compiler` 능력에 따른 최적화 등이 가능(source code전체를 읽어들이기에 가능함.).
* 한번 번역한 경우 빠르게 프로그램 전체 실행이 가능하나, source code 변경시 전체를 다시 compile을 해야하는 단점이 있음.

대표적인 예로 `Fortran`, `Pascal`, `Cobol`, `Ada`, `C`, `C++` 등을 들 수 있음.

`Java`도 compiler language라고 볼 수 있음 (단 `compile` 과정의 결과물인 `byte code`가 `Java VM`에서 동작한다).

## Interpreter Language

* `Interpreter(행, line 단위로 기계어로 번역)`에 의해, line 단위로 컴파일 없이 실행되는 언어.
* High-level language의 한 종류.
* `Script Language`로도 불림.
    * compile 과정 없이 라인 (정확히는 `statement`) 단위의 execution(실행)이 가능하므로 개발 단계에서 적은 양의 수정에 대한 결과를 쉽게 확인 가능 (이는 source code전체를 가지고 출발하는 compiler와 차이점).
    * 대화식 프로그래밍이 가능하여 교육용으로 적합.

대표적인 예로 `Python`, PHP, ASP, Java Script, Perl 등을 들 수 있다.

## 비교

| Compiler Language | Interpreter Lanugae |
| :---: | :---: |
|object code생성 | 일반적으로 object code만들지 않음 |
| program단위로 translation이 이루어짐 | statement단위로 translation이 이루어짐 |
| translation에 많은 시간이 필요. | translation 속도가 빠름 |
| execution 속도가 빠름 | execution 속도가 느린 편 |
| executable code로 변환된 이후에는 compiler 필요없음 | 원칙대로는 interpreter가 수행을 위해 필요함|
| 결과물이 OS(or 플랫폼) 종속적인 경우 많음(VM에서 동작하는 Java는 예외)| 결과물(?)이 OS 독립적인 경우가 많음(interpreter만 제공된다면)|

## 관련 용어 정리.

compiler의 결과물인 `object code`나 입력이 되는 `source code` 등의 용어를 간략히 정리한다.

#### `Object code (목적코드)`
: object module(목적파일)이라고도 불리며, `compiler`가 ^^source code로부터 compile을 수행하여 생성한 code^^ 혹은 파일을 의미함. `machine language`나 intermediate language (register transfer language,RTL)와 같은 ^^binary code^^ 이며, **`linker`등을 통해 여러 다른 object code와 연결되어 executable code가 된다 (linking)**. 일반적으로 executable인 binary code를 machine language라고 보기 때문에 완벽한 기계어는 아니라고 보는 경우가 많다 (내부에서 cpu가 읽어들이는 logical address를 사용하고 있으며, loader에 의해 loading이 된 이후 실제 physical address로 변경됨).

#### `Source code (원시코드)`
: programming language로 작성된 텍스트로서 인간이 사용하는 문자로 이루어진 code임. 일반적으로 compiler나 interpreter의 도움 없이는 컴퓨터가 직접 읽고 수행하지 못한다.

#### `Byte code (바이트코드)`
: Virtual Machine이 인식하여 수행가능한 code로 byte단위로 처리되는 것(Java에서)에 이름이 붙여짐. VM에 의해 실제 host system이 인식할 수 있는 binary code로 변경됨.

#### `Binary code (바이너리코드, 이진코드)`
: 실제 컴퓨터(정확히는 cpu)가 인식 및 수행할 수 있는 bit pattern. cpu의 instruction set에 기반. `Object code`는 binary code임 (logical address를 사용). 인식만 할 수 있는 경우를 binary code라고 부르는 경우가 많고, 실행까지 가능할 때 machine language라고 하는 사람들도 있음 (대략적으로 cpu가 인식할 수 있는 binary pattern이라고 생각해도 된다.)

#### `Machine language (기계어)`
: Programming language라기보다는 cpu가 이해하고 실행할 수 있는 operation code들, 즉 instruction set을 의미함. 이들은 binary code들이며 cpu가 읽고 수행이 가능하다.

