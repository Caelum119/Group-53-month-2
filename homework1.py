class Person:
    def __init__(self, full_name, age, is_married):
        self.full_name = full_name
        self.age = age
        self.is_married = is_married

    def introduce_myself(self):
        print(f"Имя: {self.full_name}")
        print(f"Возраст: {self.age}")
        print(f"Женат/Замужем: {'Да' if self.is_married else 'Нет'}")


class Student(Person):
    def __init__(self, full_name, age, is_married, marks):
        super().__init__(full_name, age, is_married)
        self.marks = marks

    def average_mark(self):
        if not self.marks:
            return 0
        return sum(self.marks.values()) / len(self.marks)

    def introduce_myself(self):
        super().introduce_myself()
        print("Оценки:")
        for subject, mark in self.marks.items():
            print(f" - {subject}: {mark}")
        print(f"Средняя оценка: {self.average_mark():.2f}")


class Teacher(Person):
    base_salary = 50000  # базовая зарплата

    def __init__(self, full_name, age, is_married, experience):
        super().__init__(full_name, age, is_married)
        self.experience = experience

    def calculate_salary(self):
        bonus_years = max(0, self.experience - 3)
        bonus = self.base_salary * 0.05 * bonus_years
        return self.base_salary + bonus

    def introduce_myself(self):
        super().introduce_myself()
        print(f"Опыт работы: {self.experience} лет")
        print(f"Зарплата: {self.calculate_salary():.2f} сом")


# 8. Создание объекта учителя
teacher = Teacher("Айбек уулу Нурбек", 35, True, 6)
teacher.introduce_myself()

print("\n" + "="*40 + "\n")

# 9. Функция для создания студентов
def create_students():
    student1 = Student("Алия Мамбетова", 17, False, {"Математика": 5, "Физика": 4, "История": 5})
    student2 = Student("Бакыт Токтогулов", 16, False, {"Математика": 3, "Физика": 4, "Биология": 4})
    student3 = Student("Чынгыз Асанов", 18, False, {"Химия": 5, "История": 4, "Литература": 5})
    return [student1, student2, student3]

# 10. Печать информации о студентах
students = create_students()
for student in students:
    student.introduce_myself()
    print("-" * 30)
