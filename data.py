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
        self.availability = True

    def __repr__(self):
        return f'[id: {self.id},\tperformance: {self.performance},\tpriorities: {self.priorities}]'


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
