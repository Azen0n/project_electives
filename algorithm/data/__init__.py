import numpy as np


class Elective:
    def __init__(self, id, capacity, students, day):
        self.id = id
        self.capacity = capacity  # Максимальная вместимость
        self.students = students  # Список всех студентов, выбравших этот электив
        self.result_students = []  # Финальный список студентов электива
        self.reserve = 0  # Количество первых приоритетов в запасе
        self.day = day  # День недели

    def __repr__(self):
        return f'id: {self.id}, capacity: {self.capacity}, students: {self.students}, day: {self.day}'


class Student:
    def __init__(self, id, performance, priorities):
        self.id = id
        self.performance = performance
        self.priorities = priorities
        self.elective_id = None
        self.is_available = True

    def __repr__(self):
        return f'id: {self.id}, performance: {self.performance}, priorities: {self.priorities}'


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

    students_priorities = random_shit_part_two(number_of_students, number_of_electives, p)
    return students_priorities


def random_shit_part_two(number_of_students, number_of_electives, p):
    np.random.seed(1)
    students_priorities = [[] for _ in range(number_of_students)]
    for i in range(5):
        for student_i in range(number_of_students):
            priority = np.random.choice(np.array(range(1, number_of_electives + 1)), p=p, size=1)[0]
            while priority in students_priorities[student_i]:
                priority = np.random.choice(np.array(range(1, number_of_electives + 1)), p=p, size=1)[0]
            students_priorities[student_i].append(priority)

        for ipi in range(len(p)):
            p[ipi] -= (p[ipi] - 1 / len(p)) * (1 - np.log10(8))
        p /= p.sum()

    students_priorities = np.array(students_priorities)

    return students_priorities


def random_shit(number_of_students, number_of_electives, p):
    students_priorities = []
    for i in range(number_of_students):
        priorities = []
        random_elective = np.random.choice(np.array(range(1, number_of_electives + 1)), p=p, size=1)[0]
        priorities.append(random_elective)
        for _ in range(4):
            random_elective = np.random.choice(np.array(range(1, number_of_electives + 1)), p=p, size=1)[0]
            while random_elective in priorities:
                random_elective = np.random.choice(np.array(range(1, number_of_electives + 1)), p=p, size=1)[0]
            priorities.append(random_elective)
        students_priorities.append(priorities)

        for pipi in p:
            pipi -= (pipi - 1 / len(p)) * np.log10(8)
        p /= p.sum()

    return students_priorities


def generate_electives(number_of_electives, min_capacity, max_capacity):
    """Генерация массива элективов"""
    return np.array([Elective(i + 1, np.random.randint(min_capacity, max_capacity), [], np.random.randint(1, 5))
                     for i in range(number_of_electives)])


def generate_students(number_of_students, number_of_electives, distribution):
    """Генерация массива студентов"""

    students_priorities = generate_students_priorities(number_of_students, number_of_electives, distribution)
    # Изменён рандом на более логичный 2 -> 3
    return np.array([Student(i + 1,
                             np.round(np.random.uniform(3, 5), 2),
                             students_priorities[i])
                     for i in range(number_of_students)])
