import numpy as np
import warnings

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)


def generate_electives(number_of_electives, min_capacity, max_capacity):
    """Генерация массива элективов"""
    return np.array([Elective(i + 1, np.random.randint(min_capacity, max_capacity), [])
                     for i in range(number_of_electives)])


def generate_students(number_of_students, number_of_electives):
    """Генерация массива студентов"""
    return np.array([Student(i + 1,
                             np.round(np.random.uniform(2, 5), 2),
                             np.random.choice(np.array(range(1, number_of_electives + 1)), 5, replace=False))
                     for i in range(number_of_students)])


class Elective:
    def __init__(self, id, capacity, students):
        self.id = id
        self.capacity = capacity  # Максимальная вместимость
        self.students = students  # Список всех студентов, выбравших этот электив
        self.result_students = []  # Финальный список студентов электива
        self.reserve = 0  # Количество первых приоритетов в запасе

    def __repr__(self):
        return f'[id: {self.id},\tcapacity: {self.capacity},\tstudents: {self.students}]'

    def add_student(self, student, priority):
        self.students.append((student, priority))


class Student:
    def __init__(self, id, performance, priorities):
        self.id = id
        self.performance = performance
        self.priorities = priorities
        self.elective_id = None
        self.availability = True

    def __repr__(self):
        return f'[id: {self.id},\tperformance: {self.performance},\tpriorities: {self.priorities}]'


number_of_electives = 10
min_cap = 20
max_cap = 25

# Массив с элективами: id, вместимость, список студентов (список кортежей: id студента, приоритет на этот электив)
electives = generate_electives(number_of_electives, min_cap, max_cap)

number_of_students = np.array([electives[i].capacity for i in range(number_of_electives)]).sum() - 50

# Массив со студентами: id, успеваемость, список id выбранных элективов
students = generate_students(number_of_students, number_of_electives)

print(f'{electives = }\n')
print(f'{students = }\n')
print(f'{number_of_students = }')
print(f'{number_of_electives = }')


# Метрики
# 1. Квадрат отклонения приоритета
def squared_priority_deviation(students):
    deviation = 0
    deviation1 = []
    for student in students:
        if student.elective_id is None:
            index = 5
        else:
            index, = np.where(student.priorities == student.elective_id)
        deviation += index ** 2
        deviation1.append(index)
    return deviation, deviation1


# TODO: 2. Сумма произведения приоритета на рейтинг
# TODO: 3. Среднее приоритета

# У каждого электива список студентов, которые его выбрали: (студент, приоритет электива)
for elective in electives:
    for student in students:
        if elective.id in student.priorities:
            elective.students.append([student, np.where(student.priorities == elective.id)[0][0] + 1])
    # Сортировка по приоритету электива, затем по успеваемости
    elective.students.sort(key=lambda x: (x[1], 5 - x[0].performance))

# TODO: Переписать
for elective in electives:
    for student in elective.students:
        if student[-1] == 1:
            elective.reserve += 1

electives = np.array(sorted(electives, key=lambda x: x.reserve, reverse=True))
print(1)

# TODO: Изменить
min_capacity = 16


def search_elective(electives, id):
    i = 0
    for elective in electives:
        if elective.id == id:
            return i
        i += 1


for elective in electives:
    if elective.reserve < min_capacity:

        # student[0] — студент (есть поля id и прочее)
        # student[1] — приоритет электива
        for student in elective.students:

            first_priority_elective = search_elective(electives, student[0].priorities[0])
            temp1 = student[0].priorities[0]

            for i in range(1, 6):
                pass

            if student[1] > 1 and student[0].availability and electives[first_priority_elective].reserve > min_capacity:
                elective.reserve += 1
                student[0].availability = False
                student[0].elective_id = elective.id
                electives[first_priority_elective].reserve -= 1
                elective.result_students.append(student[0])

for elective in electives:
    for student in elective.students:
        for i in range(1, 6):
            if student[1] == i and student[0].availability and len(elective.result_students) < elective.capacity:
                student[0].availability = False
                student[0].elective_id = elective.id
                elective.result_students.append(student[0])

for student in students:
    if student.availability:
        print(student)

arr = np.array(squared_priority_deviation(students)[1])
print(arr)
