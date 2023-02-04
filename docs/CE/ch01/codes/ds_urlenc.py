from urllib import parse


str = "가abc"

url_enc = parse.quote(str)
print(url_enc)
print(parse.unquote(url_enc))
