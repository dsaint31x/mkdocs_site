# Encodings

## Quoted-Printable Encoding

QT Encoding은 과거 7bit만을 지원하는 통신 경로로 데이터 통신을 하던 시절에 개발된 encoding방식임 (email 첨부파일 전송 등에 아직도 사용됨).

encoding방식은 다음과 같음.

1. 우선 computer의 internal representation (메모리 등에 저장된 값?)을 1bytes씩 나눈다.
2. 각 1byte를 nibble로 쪼개고 각 nible을 16진수로 표현한다. (2개의 symbol이 나옴.)
3. 해당 2개의 symbol앞에 `=`를 붙인다.
4. 이를 모든 byte에 적용한다.

단, 다음의 추가 규칙이 있음.

* `ASCII`에 있는 printable character들은 사실상 7bit이므로 그대로 전송된다.
* 단, ^^공백문자에 해당하는 `TAB`, `SPACE`^^ 와 `QP Encoding`에서 특별히 사용하는 `=`는 예외로 각 ASCII코드값에 `=`를 붙여 전송한다. 
    * `TAB` : `=09`
    * `SPACE` : `=20`
    * `=` : `=3D`
* 1 line이 ^^76 chracter로 구성^^ 된다.
* 각 line은 soft linebreak인 `=`로 끝난다.
    * 1byte가 3개의 글자로 표시되므로 전부 non-ascii인 한글 글자의 UTF-8 encoding된 바이트의 경우, 25문자가 한 line (한 줄)에 표시됨.
    * $3 \times 25 =75$ 이며 여기에 soft line break를 더해서 76글자임.  

### Examples for QP encoding

```python
import quopri
test = "가나다라마바사아테스트가나다라마바사아테스트가나다라마바사아테스트가나다라마바사아테스트가나다라마바사아테스트가나다라마바사아테스트"
qp = quopri.encodestring(test.encode('utf-8'))
print(qp)
# print(quopri.decodestring(qp)))
# print(qp.decode("ascii"))
```

결과는 다음과 같음.

```
=EA=B0=80=EB=82=98=EB=8B=A4=EB=9D=BC=EB=A7=88=EB=B0=94=EC=82=AC=EC=95=84=ED=
=85=8C=EC=8A=A4=ED=8A=B8=EA=B0=80=EB=82=98=EB=8B=A4=EB=9D=BC=EB=A7=88=EB=B0=
=94=EC=82=AC=EC=95=84=ED=85=8C=EC=8A=A4=ED=8A=B8=EA=B0=80=EB=82=98=EB=8B=A4=
=EB=9D=BC=EB=A7=88=EB=B0=94=EC=82=AC=EC=95=84=ED=85=8C=EC=8A=A4=ED=8A=B8=EA=
=B0=80=EB=82=98=EB=8B=A4=EB=9D=BC=EB=A7=88=EB=B0=94=EC=82=AC=EC=95=84=ED=85=
=8C=EC=8A=A4=ED=8A=B8=EA=B0=80=EB=82=98=EB=8B=A4=EB=9D=BC=EB=A7=88=EB=B0=94=
=EC=82=AC=EC=95=84=ED=85=8C=EC=8A=A4=ED=8A=B8=EA=B0=80=EB=82=98=EB=8B=A4=EB=
=9D=BC=EB=A7=88=EB=B0=94=EC=82=AC=EC=95=84=ED=85=8C=EC=8A=A4=ED=8A=B8
```

원래는 다음이나 위의 코드로 해석가능함.

```
b'=EA=B0=80=EB=82=98=EB=8B=A4=EB=9D=BC=EB=A7=88=EB=B0=94=EC=82=AC=EC=95=84=ED=\n=85=8C=EC=8A=A4=ED=8A=B8=EA=B0=80=EB=82=98=EB=8B=A4=EB=9D=BC=EB=A7=88=EB=B0=\n=94=EC=82=AC=EC=95=84=ED=85=8C=EC=8A=A4=ED=8A=B8=EA=B0=80=EB=82=98=EB=8B=A4=\n=EB=9D=BC=EB=A7=88=EB=B0=94=EC=82=AC=EC=95=84=ED=85=8C=EC=8A=A4=ED=8A=B8=EA=\n=B0=80=EB=82=98=EB=8B=A4=EB=9D=BC=EB=A7=88=EB=B0=94=EC=82=AC=EC=95=84=ED=85=\n=8C=EC=8A=A4=ED=8A=B8=EA=B0=80=EB=82=98=EB=8B=A4=EB=9D=BC=EB=A7=88=EB=B0=94=\n=EC=82=AC=EC=95=84=ED=85=8C=EC=8A=A4=ED=8A=B8=EA=B0=80=EB=82=98=EB=8B=A4=EB=\n=9D=BC=EB=A7=88=EB=B0=94=EC=82=AC=EC=95=84=ED=85=8C=EC=8A=A4=ED=8A=B8'
```

* `b`로 시작은 bytes 형이라는 뜻.
* single quatation으로 묶인 부분이 bytes의 값이며 76번재 `=` 문자 뒤에, new line을 의미하는 Escape sequence인 `\n`이 붙어있음.

ASCII 가 혼재된 예는 다음과 같음.

```python
import quopri

test = 'a가b나c다'
print('len of test:',len(test))
utf8_test = test.encode('utf-8')
print('len of utf8_test:',len(utf8_test),"/ type:",type(utf8_test))
print(quopri.encodestring(test.encode('utf-8')))
```

결과는 다음과 같음.

```
len of test: 6
len of utf8_test: 12 / type: <class 'bytes'>
b'a=EA=B0=80b=EB=82=98c=EB=8B=A4'
```

`quopri` module에 대한 자세한 내용은 다음을 참고하라. : [quopri — MIME quoted-printable 데이터 인코딩과 디코딩](https://docs.python.org/ko/3/library/quopri.html)

## Base64 Encoding

> Quoted Praintable Encoding보다 효율이 좋은 encoding방식으로 email의 첨부파일을 encoding하는데 사용된다.

Base64는 3bytes씩 묶어서 4개의 chracter로 encoding하는 방식으로 3bytes, 즉 24bit를 4등분하여 6bit씩 나누고 이들 6bit를 64진수로 표현한다. 6bit는 64진수 한 글자로 표현되기 때문에 3bytes가 4개의 character가 된다.

64진수를 위해 Alphabet에서 26개의 upper-case와 26개의 lower-case, digit 10개, 그리고 `+`와 `-` 문자들을 사용한다.  
(0-63을 위에서 나열한 순으로 할당.)

3byte씩 처리되는데, 만약 raw data가 3byte의 배수가 아니라면, 끝에 `=`문자로 padding을 하여 3의 배수로 맞춘다.

### Examples for base64

```python
import base64

token = "I love 현무"
byte_utf8 = token.encode('utf-8')
byte_base64 = base64.b64encode(byte_utf8)
ck_str = byte_base64.decode('ascii')
print(ck_str)
print("-------------")
d_token = base64.b64decode(byte_base64)
print(d_token)
print(d_token.decode('utf-8'))
```

결과는 다음과 같다.

```
SSBsb3ZlIO2YhOustA==
-------------
b'I love \xed\x98\x84\xeb\xac\xb4'
I love 현무
```

## URL Encoding (= Percent Encoding)

URL 주소에서 `/`나 `=`등의 문자들은 특별한 의미를 가지기 때문에 이들 문자들을 URL 주소에서 문자 자체로 쓰려면 변환이 필요하다.

이 경우, 사용되는 게 `URL Encoding`이다. URL에서 특별한 의미를 가진 문자를 그냥 문자 그대로 사용하기 위해서는 ^^해당 문자의 ASCII 값을 16진수로 표현^^ 하고 `%` 뒤에 붙여서 기재한다.

URL에 한글 등이 있는 경우에도 자주 이용된다. 한글 한글자는 3byte이므로 각 바이트에 해당하는 16진수를 각각 `%`가 붙여져 변환된다.

URL에서는 

1. 한글은 일단 UTF-8로 변환되고 
2. 해당 bytes를 1byte씩 자른 후 
3. 이를 `%`와 16진수 숫자 2개로 바꾸어 처리

하는 것이다.

