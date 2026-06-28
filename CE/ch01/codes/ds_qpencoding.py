import quopri
test = "가나다라마바사아테스트가나다라마바사아테스트가나다라마바사아테스트가나다라마바사아테스트가나다라마바사아테스트가나다라마바사아테스트"
qp = quopri.encodestring(test.encode('utf-8'))
print(qp)
# print(quopri.decodestring(qp)))
print("==========================")
print(qp.decode("ascii"))