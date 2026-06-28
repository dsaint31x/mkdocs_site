class Samp:
    def get_x(self):
        return self.x

def some_method(self): # closuer기법으로 self를 기억.

    def func():
        print(f"hi! : {self.x}")
    return func

class SampTwo:
    def get_x(self):
        return self.x

if __name__ == "__main__":
    s = Samp()
    s.x = 23 #주석처리시 에러.
    s.dynamic_get = some_method(s)
    s.dynamic_get()

    print("------------")
    s2 =SampTwo()
    s2.x = 77
    s2.dynamic_get = some_method(s2)
    s2.dynamic_get()
    s2.x = 33
    s2.dynamic_get()
    print("------------")
    s2.dynamic_get_one = some_method(s)
    s2.dynamic_get_one()
    s.x = 2323
    s2.dynamic_get_one() # 이런 유연성은 안쓰는게 낫지 않을까?
    print("------------")
    print(s.get_x())
    del s.x
    print(s.get_x()) # attribute가 제거되어 AttributeError가 발생함.