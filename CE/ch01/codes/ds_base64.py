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