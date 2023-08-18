a = 10

def test_fn ():
    b = 10
    print(a)
    # a = 100
    
test_fn()


from dis import dis

print(dis(test_fn))
