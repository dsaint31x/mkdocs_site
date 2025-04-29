# Warrior

class Human:
    def __init__(self, name):
        Human.ds_type = "Human"
        self.job = None
        self.name = name

    def introduce(self):
        print("------------------------")
        print(f"제 이름은 {self.name}입니다.")
        print(f"제 직업은 {self.job}입니다.")
        print(f"저의 종족은 {Human.ds_type}입니다.")
        
class Warrior (Human):

    def __init__(self, name):
        super().__init__(name)
        self.job = "Warrior"

    def bash (self):
        print("강타 능력")

class Knight(Warrior):
    def __init__(self, name):
        super().__init__(name)
        self.job = "knight"
    def riding (self):
        print("말타기 능력")

class Healer (Human):
    def __init__(self, name):
        super().__init__(name)
        self.job = "Healer"

    def healing (self):
        print("치료하기 능력")

class Paladin (Knight, Healer):
    def __init__(self, name):
        super().__init__(name)
        self.job = "Paladin"

if __name__ == "__main__":
    ins0 = Human("김 아무개")
    ins1 = Warrior("이 아무개")
    ins2 = Healer("박 아무개")
    ins3 = Knight("박 기사")

    humans = [ins0, ins1, ins2, ins3]
    for h in humans:
        h.introduce()

    ins4 = Paladin("정 아무개")
    ins4.introduce()
    ins4.healing()
    ins4.riding()
    print(Paladin.mro())

    for h in humans:
        if isinstance(h, Human):
            print(f"[{h}] is a Human")



    

