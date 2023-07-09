# Declarative Programming Language vs. Imperative Programming Language

## Declarative Programming Language

Declarative Programming Language는 프로그래밍 소스 코드가 결과물로 ***무엇(what)을 만들기를 원하는지를 기술*** 한다.
이 때, 이를 만들기 위해 어떻게(how) 해야하는 지는 소스코드에서 기술하지 않는다. 

대표적인 예가 SQL (Structured Query Language)과 Prolog이다. SQL의 경우, query로 얻어와야 하는 데이터를 기술하며, 해당 SQL을 요청받은 Database가 이를 반환해준다. 또는 데이터 (or table)간의 관계를 기술해주면 해당 내용대로 데이터 및 table을 생성한다.

즉, Declarative Programming Language에서는 개발자가 원하는 결과 또는 원하는 입력과 결과의 관계를 기술하는 형태로 프로그래밍이 이루어진다. ^^소스 코드에서는 해당 결과를 얻기 위해 어떻게 처리가 이루어질 지는 기술하지 않는다.^^

## Imperative Programming Language

Imperative programming language는 명시적으로 instruction들을 기재하여 컴퓨터가 어떻게(how) 동작할지를 기술한다.

즉, 실행(execute)할 instruction들을 순서대로 기술한다. 프로그래머는 각각의 instruction들이 어떤 조건과 순서로 동작할지를 기술하며 다음을 명시적으로 소스코드에 기재한다.

1. variable assignment
2. loops
3. conditions
4. control structures.

`C`, `Python` 등의 언어가 imperative programming language의 예임.

## 요약.

 Declarative programming languages는 "what"에 집중하고 해당 소스 코드가 동작하는 system이나 interpreter, 또는 기계어로 바꾸어주는 compiler들이 이를 실제로 어떻게 수행할지는 알아서(?) 처리하게 한다. 반면에 imperative programming languages는 "how"에 집중하여 필요한 instruction들을 어떤 순서로 수행할지를 명시적으로 기재한다.
 
 Declarative programming languages로는 내가 원하는 것을 알려주는 형태로 지시를 내린다면, Imperative programming language는 task를 수행하기 위해 해야하는 일을 하나하나 순서대로 지시를 내리는 것으로 생각할 수 있다.