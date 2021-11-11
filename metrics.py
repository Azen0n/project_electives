import numpy as np


# Метрики
# 1. Квадрат отклонения приоритета
def squared_priority_deviation(students):
    deviation = 0
    for student in students:
        if student.elective_id is None:
            index = 5
        else:
            index, = np.where(student.priorities == student.elective_id)
        deviation += index ** 2
    return deviation / len(students)


# 2. Среднее приоритета
def mean_priority(students):
    deviation = 0
    for student in students:
        if student.elective_id is None:
            index = 5
        else:
            index, = np.where(student.priorities == student.elective_id)
        deviation += index
    return deviation / len(students)


# 3. Сумма произведения приоритета на рейтинг
def sum_of_priority_performance_product(students):
    deviation = 0
    for student in students:
        if student.elective_id is None:
            index = 5
        else:
            index, = np.where(student.priorities == student.elective_id)
        deviation += index * student.performance
    return deviation