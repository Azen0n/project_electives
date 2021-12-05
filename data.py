import numpy as np


class Elective:
    def __init__(self, id, capacity, students):
        self.id = id
        self.capacity = capacity    # Максимальная вместимость
        self.students = students    # Список всех студентов, выбравших этот электив
        self.result_students = []   # Финальный список студентов электива
        self.reserve = 0            # Количество первых приоритетов в запасе

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
        self.is_available = True

    def __repr__(self):
        return f'[id: {self.id},\tperformance: {self.performance},\tpriorities: {self.priorities}]'


def generate_students_priorities(number_of_students, number_of_electives, distribution):
    """Генерация приоритетов всех студентов, возвращает массив."""
    if distribution == 'chisquare':
        p = np.random.chisquare(1.0, number_of_electives)
    elif distribution == 'beta':
        p = np.random.beta(2, 7, number_of_electives)
    elif distribution == 'gamma':
        p = np.random.gamma(2, 2, number_of_electives)
    else:
        p = np.absolute(np.random.logistic(2, 1, number_of_electives) + 3)
    p /= p.sum()
    students_priorities = []
    for i in range(number_of_students):
        students_priorities.append(np.random.choice(np.array(range(1, number_of_electives + 1)), p=p, size=5, replace=False))
    return students_priorities


def generate_electives(number_of_electives, min_capacity, max_capacity):
    """Генерация массива элективов"""
    return np.array([Elective(i + 1, np.random.randint(min_capacity, max_capacity), [])
                     for i in range(number_of_electives)])


def generate_students(number_of_students, number_of_electives, distribution):
    """Генерация массива студентов"""

    students_priorities = generate_students_priorities(number_of_students, number_of_electives, distribution)
    """Изменён рандом на более логичный 2->3"""
    return np.array([Student(i + 1,
                             np.round(np.random.uniform(3, 5), 2),
                             students_priorities[i])
                     for i in range(number_of_students)])
