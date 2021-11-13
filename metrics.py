import numpy as np


def squared_priority_deviation(students):
    """Квадрат отклонения приоритета."""
    deviation = 0
    for student in students:
        if student.elective_id is None:
            index = 5
        else:
            index, = np.where(student.priorities == student.elective_id)
        deviation += index ** 2
    return deviation / len(students)


def mean_priority(students):
    """Среднее приоритета."""
    deviation = 0
    for student in students:
        if student.elective_id is None:
            index = 5
        else:
            index, = np.where(student.priorities == student.elective_id)
        deviation += index
    return deviation / len(students)


def sum_of_priority_performance_product(students):
    """Сумма произведения приоритета на рейтинг."""
    deviation = 0
    for student in students:
        if student.elective_id is None:
            index = 5
        else:
            index, = np.where(student.priorities == student.elective_id)
        deviation += index * student.performance
    return deviation


def students_rate(students):
    """Процент студентов, попавших на каждый приоритет (6 — студент не распределен)."""
    rates = {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0}
    for student in students:
        if student.is_available:
            rates[6] += 1
        else:
            rates[np.where(student.priorities == student.elective_id)[0][0] + 1] += 1

    for key in rates:
        rates[key] = rates[key] / len(students) * 100.0

    return rates


def call_all_metrics(students):
    print(f'squared_priority_deviation = {squared_priority_deviation(students)}')
    print(f'mean_priority = {mean_priority(students)}')
    print(f'sum_of_priority_performance_product = {sum_of_priority_performance_product(students)}')
    print(f'students_rate = {students_rate(students)}')
