class Student:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age #Naming mangling
    
    def get_name(self):
        return self.__name
    def set_name(self,name):
        self.__name = name    
    name = property(get_name, set_name)# property 이용
    # name = property() # 위의 라인과 동일한 효과의 3개 라인임.
    # name.getter(get_name)
    # name.setter(set_name)
    
    @property
    def age(self):
        return f"[{self.__age}]"

    @age.setter
    def age(self,age):
        if age < 0:
            self.age = 0
        else:
            self.__age = age
    

    def display(self):
        print(f"{self.__name}'s age is {self.__age}")

if __name__ == "__main__":
    s = Student("김 아무개", 21)
    s.name = "박 아무개" 
    s.age = -10
    print(s.age)
    print("------------")
    print(s.display())
    print("------------")
    print(s.__dict__) # property들은 보이지 않음.
    print("------------")
    print(dir(s)) # property확인 가능.