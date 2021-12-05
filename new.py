from data import Elective, Student, generate_electives, generate_students
from metrics import squared_priority_deviation, mean_priority, sum_of_priority_performance_product, call_all_metrics, \
    students_rate
from algorithm import student_allocation, floyd, transfer_graph,remnant_students_allocation
import numpy as np
import warnings
import time
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)


if __name__ == '__main__':
    number_of_electives = 200
    low_capacity = 20       # Границы рандома
    high_capacity = 25

    min_capacity = 10       # Минимальная вместимость электива

    electives = generate_electives(number_of_electives, low_capacity, high_capacity)
    number_of_students = np.array([electives[i].capacity for i in range(number_of_electives)]).sum() - 50
    students = generate_students(number_of_students, number_of_electives, 'gamma')
    start=time.time()
    student_allocation(electives, students, min_capacity)

    print(f'{number_of_students = }')
    print(f'{number_of_electives = }')
    print('metrics:')
    call_all_metrics(students)
    bratki_tapki , optimal_transfer_graph=transfer_graph(electives)
    optimal_transfer_graph, temp_graph, bratki_tapki = floyd(bratki_tapki, optimal_transfer_graph, electives, students)
    end2 = time.time()
    call_all_metrics(students)
    print((end2 - start)/60)

    remnant_students_allocation(optimal_transfer_graph, temp_graph, bratki_tapki, electives, students, min_capacity)
    call_all_metrics(students)
    end = time.time()
    print((end - start)/60)
    for el in electives:
        if el.capacity < len(el.result_students):
            print('a')