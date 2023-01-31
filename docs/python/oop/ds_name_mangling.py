class Student:
    def __init__(self, name, age):
        self.name = name
        self.__age = age #Naming mangling
        self._job = "test" # 관례적으로 접근하지 말것을 _로 표시.

    def set_name(self,age):
        self.name = name

    def set_age(self,age):
        if age < 0:
            self.age = 0
        else:
            self.__age = age
    def get_age(self):
        return f"[{self.__age}]"

    age = property(get_age, set_age) # property 이용
    # age = property() # 위의 라인과 동일한 효과의 3개 라인임.
    # age.getter(get_age)
    # age.setter(set_age)

    def set_job(self,job):
        self._job = job # 관례상 _가 앞에 있으면 접근하지 말라는 애기임.

    def display(self):
        print(f"{self.name}'s age is {self.__age}")
        print(f"{self.name}'s job is {self._job}")

if __name__ == "__main__":
    s = Student("김 아무개", 21)
    s.name = "박 아무개"
    s._job = "학생" # 관례이므로 강제력이 Name mangling보다 약하다. (그냥 됨)
    s.display()
    print("================")
    # print(dir(s))
    print(s.__dict__) #attribute들을 출력해줌.
    print("================")
    s.age = -10
    print(s.age)