from objects import Student


def get_mean_priority(students: list[Student]) -> float:
    """Возвращает среднюю позицию электива в списке приоритетов, на который распределены студенты."""
    total_priority = 0.0
    for student in students:
        total_priority += student.get_elective_position(student.elective_id)
    return total_priority / len(students)


def get_priority_distribution(students: list[Student]) -> dict[int, float]:
    """Возвращает процентное распределение приоритетов элективов, на которые распределены студенты."""
    priority_rates = {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0}
    for student in students:
        priority_rates[student.get_elective_position(student.elective_id)] += 1.0
    for key in priority_rates:
        priority_rates[key] = priority_rates[key] / len(students) * 100.0
    return priority_rates


def get_allocation_quality(students: list[Student]) -> float:
    """Возвращает качество распределения по формуле (приоритет - 1) ^ 2 * успеваемость * (5 - успеваемость)."""
    product = 0.0
    for student in students:
        elective_position = student.get_elective_position(student.elective_id)
        product += (elective_position - 1) * (elective_position - 1) * student.performance * (5 - student.performance)
    return product
