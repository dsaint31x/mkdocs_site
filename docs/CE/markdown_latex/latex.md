# LaTeX

`LaTeX`` (발음은 '라텍' 또는 '레이텍', 라텍스라고 하면... ㅠㅠ)은  
고품질의 문서를 생성하기 위한 open-source 문서 조판 시스템 (Typesetting System)임. 

* 특히 수학적 및 과학적 문서 작성에 매우 적합. 
* 학술 출판 및 기술적인 문서 작성에 널리 사용됨. 

## 수식 입력을 위한 LaTeX

기존의 LaTeX는 문서를 일종의 이미지 형식으로 주로 변환하는 방식을 취했는데, 이는 인터넷 시대에 적합하지 않은 단점을 가지고 있었고, 명령어 방식이라 일반 사용자들이 쓰기는 까다롭다는 단점이 있음.

하지만 수식을 워낙 잘 표기할 수 있다는 장점이 있었기 때문에 칸 아카데미에서 만든 open-source 수식입력기의 라이브러인 KaTex의 개발(SVG로 결과물을 내놓기 때문에 웹브라우저에서 랜더링이 쉬움)로 이어졌고, 웹에서의 LaTex 또는 MathML 로 작성된 수식을 표현해주는 JavaScript 라이브러리 MathJax 의 대중화와 함께 인터넷에서 수식을 표현하는 기본 문법으로 자리잡음.

## 사용예

```
$$F(\Omega) = \int^\infty_{t=-\infty}f(x)e^{-j\Omega t}dt$$
```

$$F(\Omega) = \int^\infty_{t=-\infty}f(x)e^{-j\Omega t}dt$$

$t$ 와 $\Omega$ 간의 Fourier Transform에 대한 수식을 LaTex 으로 표현한 것임 (MathJax를 이용.)

`$` 를 사용하면 inline 으로 수식을 추가할 수 있고, `$$`를 사용하면 중앙에 정렬된 수식을 기재할 수 있음.

## 관련 Site

* [KaTex 문법](https://katex.org/docs/supported.html)
* [Blogger에서 LaTeX 이용하여 수식 표현하기](https://ds31x.blogspot.com/2022/10/latex-blogger-dynamic-theme.html)
* [Tistory에 수식 넣기](https://dsaint31.tistory.com/206?category=1006251)