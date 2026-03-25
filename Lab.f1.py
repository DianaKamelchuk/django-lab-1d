class Human:
    def init(self, name, age):
        self.name = name          
        self._age = age          
        
    def get_age(self):
        return self._age

    def set_age(self, age):
        if age > 0:
            self._age = age
        else:
            print("Вік має бути додатнім")

    def introduce(self):
        return f"Привіт, мене звати {self.name}, мені {self._age} років."

    def activity(self):
        return "Людина живе і розвивається."


class Student(Human):
    def init(self, name, age, university):
        super().init(name, age)
        self.university = university

    def introduce(self):
        return (f"Привіт, мене звати {self.name}, мені {self._age} років. "
                f"Я навчаюся в {self.university}.")

    def activity(self):
        return "Студент навчається та отримує знання."


human = Human("Олена", 35)
student = Student("Андрій", 18, "КНУ")

print(human.introduce())
print(human.activity())

print(student.introduce())
print(student.activity())