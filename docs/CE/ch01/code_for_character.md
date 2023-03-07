# Codes for Characters

> Code란 특정 형태의 inforamtion을 다른 방법으로 표현하는 규칙 또는 해당 규칙으로 표현된 결과물을 가르킴.

문자를 나타내기 위한 code는 인간이 사용하는 문자를 일종의 기호 또는 숫자로 표현하는 것을 의미한다.

* encoding : ^^대상 information을 code로 변환하는 과정 또는 규칙^^ 을 의미.
* decoding : code로부터 원래의 information으로 얻는 과정 또는 규칙을 의미.

문자를 나타내기 위한 code 중 가장 오래되었지만 여전히 사용되고 있는 ^^**ASCII** (Ameraican Standard Code for Information Interchage)^^ 가 가장 유명하다.

하지만, 비영어권에서도 컴퓨터의 사용이 확장되면서 ^^영문자만을 고려한 ASCII^^ 외의 code가 필요하게 되었고, ^^각 나라마다 자국어를 위한 고유의 코드들이 제안되던 시기^^ 를 거치게 된다. 우리나라로 한정하면 그 시기에 가장 많이 사용된 code가 바로 `EUC-KR` 이다 (역시 아직까지도 사용된다). 비록 각 나라에서 제안된 code들은 나름 효과적이었지만 다국어를 한번에 처리할 필요성이 점점 커지기 시작했고(다국어 지원 사이트를 생각해보자), 이같은 요구에 의해 탄생한 것이 바로 Unicode이다. Unicode는 전세계의 문자기호(고대문자나 음악기호, 수학기호등도 포함)를 단일 코드 테이블로 표현한 code이며 이를 기반으로 하는 여러 encoding 방식을 가진다.

> Unicode는 처음에는 ^^16bit를 기반으로 다양한 언어의 글자를 표현^^ 가능하도록 설계되었으나 현재는 ^^21bit로 확장^^ 되었다 (초기에 16bit로 충분하다고 생각했지만, 점점 더 많은 기호로 포함되었고 이는 보다 많은 bit를 요구하기에 이름).  
> 영문자만 사용하는 경우 8bit(사실은 7bit)의 ASCII 만으로도 충분하기 때문에, 서구권에선 Unicode가 처음 제안될 당시만 해도, ASCII 만을 고려 및 지원하는 경우가 일반적이었기 때문에, 기존의 code 들과의 호환성을 유지하면서 Unicode를 사용하는 encoding의 필요성이 요구되어다. 때문에 Unicode는 code로서만 사용하고, 이를 **컴퓨터에서 실제 저장하는 `byte`는 다르게 하는 encoding 방식** 들이 사용된다. 기존의 code값이 곧 컴퓨터에서 사용하는 `byte` 값이었던 것과 차이가 있다. 이같이 Unicode를 encoding하는 방식으로는 `UTF-8`, `UTF-16`, `UTF-32` 등이 있으나, `UTF-8`이 단일 encoding 으로서 적은 bit를 사용하면서 ASCII 등과의 호환성을 확보하는 장점을 가지고 있기 때문에 2023년 현재 ^^사실상 unicode의 표준 encoding 방식^^ 이 되었다 (초기엔 `UTF-16` 이 대세였지만 `UTF-8`의 효율성과 편리성으로 인해 현재는 거의 대부분이 `UTF-8`임). 자세한 건 아래의 Unicode를 참고하라.

다음은 대표적인 code 들을 등장 시대 순으로 소개하고 있다.

## The American Standard Code for Information INterchange (ASCII)

컴퓨터 초창기에 다양한 code들이 제안되었으나, 1963년 개발된 `ASCII`가 사실상 표준으로 살아남았다. ASCII는 영문자를 처리하는데 아직까지도 널리 사용된다.  
  
`ASCII`는 7bit 만으로 다양한 *숫자기호* 와 *영문자들*, 그리고 *특수문자* 및 *Control character(제어문자)* 들을 표현한다.

> ^^7bit 만으로 표현^^ 되었지만, 컴퓨터가 발전하면서 한번에 처리하는 단위가 `byte`가 되면서 ASCII를 사용하는 데이터 type의 크기가 1byte가 되었다. C언어의 `Char` Data type이 가장 대표적인 ASCII 응용사례라고 할 수 있다.

ASCII 의 상세 구성은 다음과 같다.

* 34개의 Control Character (`NUL`포함)
* 94개의 Printable Character
    * 52개의 알파벳 대소문자
    * 10개의 숫자
    * 32개의 특수 문자

![ASCII](img/ASCII.png)

> `ASCII`는 이름에서 알 수 있듯이 ***Infromation INterachange*** 를 위해 만들어진 것이기 때문에, Control character의 상당수는 communication (통신)과 관련되어 있다. 현재는 이들 중 많은 경우가 사용되지 않는다.

## American National Standard Institute (ANSI)

간략히 애기하면 `ASCII`의 7bit를 기반으로 8bit로 확장을 한 code이다.  
후에 개발된 Unicode가 단일 테이블에 모든 문자를 표현하는 것과 달리 ANSI는 ***code page를 이용*** 하여 한번에 해당 code page에 해당하는 나라의 문자를 표현하는 방식을 취한다.  
즉, 128개는 ASCII를 그리고 추가된 128개는 각국의 언어의 기호들이 할당되는 방식이다. 한글과 같은 경우에 128개로 부족하기 때문에, 8bit를 더 할당하여 2byte를 사용한다. `ANSI`를 이용한 대표적 한글 code는 `CP949`로 이름의 `949`는 ***code page를 지칭*** 한다. 이는 Microsoft에서 제안한 방식으로 `MS949`라고도 불린다 (Windows OS에서 주로 사용되는데, 한국의 당시 OS는 거의 Windows였기 때문에 사실상 한글 표준으로 사용되었다. 참고로 ^^완성형^^ 임). `ANSI` 방식은 자국어만을 지원하는데에는 큰 문제가 없지만, 영어 외의 다른나라 글자들을 동시에 표현해야하는 경우엔 사용이 어렵다는 단점을 가진다.

> ANSI는 미국 국가표준 협회 의 약어로 다른 곳에서는 해당 협회를 가르킨다. 많은 경우, 해당 협회가 정한 표준안을 ANSI라고 지칭한다.

## Extended Unix Code-Korea (EUC-KR)

이름에서 알 수 있듯이 ^^Unix 계열에서 한글 지원을 위해 등장^^ 한 encoding 방식이며, 2byte를 이용한 ^^완성형^^ 방식이다.  
`CP949`와 마찬가지로 `ANSI`를 한글 지원을 위해 확장한 형태이며, `CP949`와 마찬가지로 완성형의 한계로 인해 모든 한글을 표현하지 못한다(또한, `ANSI`의 단점도 그대로 가진다). `CP949` 보다 먼저 개발되었고 웹페이지 등에서 `CP949` 못지 않게 널리 사용되었다 (표현 가능한 한글 문자 수는 `CP949`보다 적었으나 인터넷에서 서버로 사용되는 장비의 OS가 주로 Unix 계열이었기 때문에 널리 사용되었다).

## Unicode

전세계 문자와 기호를 하나의 테이블에 정리한 code : 때문에 전세계의 문자를 일관되게 표현하고 다룰 수 있음.

> 지원되는 문자가 계속 추가되면서 필요한 bit 크기가 점점 늘어나고 있다 (사실 16bit면 충분할 것으로 생각했지만 현재는 21bit로 늘어났음.) 

한글 문자들의 code는 다음을 통해 확인 가능함. [Unicode:Hangul Syllables](http://unicode.org/charts/PDF/UAC00.pdf)

Unicode는 기존의 다른 code들과 달리 ***할당된 code와 다른 byte로 컴퓨터에서 저장*** 된다. 때문에, Unicode를 컴퓨터에 저장되는 byte로 바꾸는 여러 encoding방식이 제안되었다.

> byte라고 표현한 것은 컴퓨터에서 기본으로 byte단위로 저장이 이루어지 때문에 컴퓨터에서 실제 저장되는 코드(or 방식)를 지칭하다고 보면 된다.

### Code와 Encoding

앞서 살펴본 code와 encoding의 정의를 다시 표현하면 다음과 같다.

`code`
: 일상 생활에서 사용되는 문자나 숫자, 또는 정보를 컴퓨터 등에서 인식하기 쉬운 특정 기호로 기호화한 것. (보통 숫자, hexadecimal 또는 binary로 표현됨)

`encoding`
: 특정 데이터를 code로 바꾸는 것을 encoding이라고 함. 역의 과정은 decoding이라고 한다.

Unicode는 엄밀히 말해서 code이지 encoding이 아니다. 즉, Unicode의 글자 하나를 나타내는 code를 컴퓨터가 2진수로 바꿔 그대로 저장하지 않는다는 애기이다.  

Unicode 기반의 encoding은 `UTF-8` (가변길이), `UTF-16` (가변길이), `UTF-32` (고정길이) 등이 있기 때문에 사용한 encoding 방식에 따라 저장되는 byte가 달라지게 된다. 
이와 달리, `ANSI` 계열과 `ASCII`는 code에 해당하는 바이트가 그대로 저장되기 때문에 code이자 encoding 이라고 할 수 있다.

> 가변길이방식을 multi-bytes라고 부름.

때문에, Unicode라 해도 실제 저장된 byte의 값을 보면 다를 수 있음을 유의해야 한다.

---

### Encodings for Unicode.

어떤 데이터 (음성, 영상, 문자 등)을 code로 만드는 것을 encoding이라고 할 수 있는데, Unicode의 경우는 좀 독특하다.

글자를 Unicode로 code로 변환하는 것 자체가 encoding이라고 할 수 있는데, Unicode는 요구되는 bit가 크다보니, 이를 그대로 컴퓨터에서 저장하기에 효율이 떨어진다. 때문에 Unicode를 컴퓨터에 저장하기 위한 byte 단위의 code(?)로 변환해주는 encoding들이 제안되었다 (code를 위한 code?).

> code이자 encoding방식인 ASCII만을 배운 입장에서 Unicode를 마주치면 꽤 헷갈린다.

초기 많이 사용된 encoding은 다국적 기업들이 적극적으로 사용한 UTF-16이었다. 하지만 비영어권 개발자들에게 `UTF-16`은 장점보다 단점이 많은 방식이었고 사용하기 불편한 점이 많아서 자국 서비스 이외의 경우를 고려하는 경우 아니면 기존의 `ANSI`계열의 encoding이 사용되었다. 하지만 `UTF-8`이 등장하면서 ^^단일 encoding으로서 다국어가 처리^^ 될 수 있었기 때문에 개발자 영역에서 적극적인 도입되었다. 사실 `UTF-8`은 한글 만으로 한정짓게 되면 효율적이지 않다. 한글 문자 하나가 2byte로 처리가 가능한 `UTF-16`이나 `ANSI` 방식(`EUC-KR`, `CP949`)과 달리 ^^3byte로 처리되는 경우가 대부분^^ 인 `UTF-8`은 효율성이 나쁜 encoding이다. 하지만 storage 용량과 통신속도가 나날이 빨라지는 현실에서 ^^단일 방식으로 쉽게 처리^^가 되는 `UTF-8`은 대부분의 개발자들에게 환영을 받았고, 거의 대부분의 unicode 지원 SW들이 `UTF-8`을 기본으로 사용하면서 ***실제적인 표준*** 이 되었다. 

`UTF-32`는 고정형으로 어찌보면 가장 처리가 쉬운 방식이다. 문자 하나에 4bytes를 쓴다는 단점이 무색해질 만큼 storage가 더욱 가격이 내려가고 통신속도나 압축기술이 발전한다면 UTF-8을 대체할 수도 있겠지만, 아직 시간이 더 필요해 보인다.
  
이 문서에서는 `UTF-8` 만을 다룬다.

#### UTF-8 (Universal Coded Character Set + Transformation Format – 8-bit)

Go언어 개발자로 더 유명한 `롭 파이크`가 `켄 톰슨`과 함께 개발한 Unicode encoding이다.  

한 문자를 표현하는데 1~4bytes를 사용하며 하위 1바이트 영역은 `ASCII`와 호환된다. `ASCII`로 충분한 영어권의 경우, 1 byte 만을 사용하는 효율성을 보이며 동시에 다국어 처리가 단일 방식으로 쉽게 처리되기 때문에 다른 Unicode encoder 들을 제치고 사실상 표준이 되었다. 경쟁방식인 UTF-16 경우, 다국적 기업들의 초기 전폭적인 지원이 있었음에도 `UTF-8`의 사용하기 쉽다는 장점을 넘지 못했다. 한글의 경우, 대부분이 3byte를 사용되어 효율성이 떨어지지만 동일한 방식으로 다국어 문자를 활용할 수 있다는 편의성으로 인해 실제적인 표준 encoding이 되었다.

가변길이(multi-bytes)를 사용하면 각 경우의 규칙은 다음과 같음.

* 1byte만을 사용하는 경우, `MSB`가 `0`으로 시작한다.
* 2bytes를 사용하는 경우, 상위 byte는 `110`으로 시작하고, 하위 byte는 `10`으로 시작한다.
* 3bytes를 사용하는 경우, 상위 bytes는 `1110`으로 시작하고, 2번째, 3번째 bytes는 `10`으로 시작한다.
* 4bytes를 사용하는 경우, 상위 byte는 `11110`으로 시작하고 나머지 byte들은 `10`으로 시작한다.

다음 테이블과 예를 참고하면 위의 규칙을 쉽게 이해할 수 있다.

![https://namu.wiki/w/UTF-8](img/utf-8_table_namu.png)

![ref. https://namu.wiki/w/UTF-8](img/utf-8_example_namu.png)

#### Example

```python
test = 'a가b나c다'
print('len of test:',len(test))
utf8_test = test.encode('utf-8')
print('len of utf8_test:',len(utf8_test),"/ type:",type(utf8_test))
```

* built-in function `len()`은 글자수를 반환한다.
* 특정 encoding으로 처리된 bytes에 대한 길이는 사용되는 byte 수이다.
* 영문자는 1byte를 차지. ASCII!!
* 한글은 3bytes를 차지함.

> Python 3.x는 `UTF-8`을 기본 encoding으로 사용한다.
