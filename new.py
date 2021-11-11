from data import Elective, Student, generate_electives, generate_students
from metrics import squared_priority_deviation, mean_priority, sum_of_priority_performance_product
from algorithm import student_allocation
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)


def print_students(students):
    for student in students:
        if student.availability:
            print(student)


if __name__ == '__main__':
    number_of_electives = 10
    min_cap = 20        # Границы рандома
    max_cap = 25

    min_capacity = 16   # Минимальная вместимость электива

    # Массив с элективами: id, вместимость, список студентов (список кортежей: id студента, приоритет на этот электив)
    electives = generate_electives(number_of_electives, min_cap, max_cap)

    number_of_students = np.array([electives[i].capacity for i in range(number_of_electives)]).sum() - 50

    # Массив со студентами: id, успеваемость, список id выбранных элективов
    students = generate_students(number_of_students, number_of_electives)

    # print(f'{electives = }\n')
    # print(f'{students = }\n')
    # print(f'{number_of_students = }')
    # print(f'{number_of_electives = }')

    student_allocation(electives, students, min_capacity)
    print_students(students)

    print(np.array(squared_priority_deviation(students)))
    print(np.array(mean_priority(students)))
    print(np.array(sum_of_priority_performance_product(students)))