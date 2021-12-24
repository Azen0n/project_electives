from data import Elective, Student, generate_electives, generate_students
from db_queries import get_electives, get_students, confirm_students_allocation
from metrics import squared_priority_deviation, mean_priority, sum_of_priority_performance_product, call_all_metrics, \
    students_rate, get_number_of_priorities_remaining
from algorithm import student_allocation, floyd, transfer_graph, remnant_students_allocation, reset_variables
import numpy as np
import warnings
import time
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)


if __name__ == '__main__':
    np.random.seed(5)
    min_capacity = 10       # Минимальная вместимость электива

    electives = get_electives()
    students = get_students()

    number_of_students = students.shape[0]
    number_of_electives = electives.shape[0]

    print(f'{number_of_students = }')
    print(f'{number_of_electives = }')

    start = time.time()
    student_allocation(electives, students, min_capacity, quota=0)

    print('\nmetrics (initial allocation):')
    call_all_metrics(students)

    bratki_tapki, optimal_transfer_graph = transfer_graph(electives)
    optimal_transfer_graph, temp_graph, bratki_tapki = floyd(bratki_tapki, optimal_transfer_graph, electives, students)
    end2 = time.time()

    print('\nmetrics (after optimal transfer graph):')
    call_all_metrics(students)
    print(f'Time: {np.round((end2 - start) / 60, 2)} min')

    remnant_students_allocation(optimal_transfer_graph, temp_graph, bratki_tapki, electives, students, min_capacity)

    print('\nmetrics (after allocation of remnant students):')
    call_all_metrics(students)
    end = time.time()
    print(f'Time: {np.round((end - start) / 60, 2)} min')

    confirm_students_allocation(students)

    reset_variables(students, electives, bratki_tapki, temp_graph, optimal_transfer_graph)
    print(get_number_of_priorities_remaining(students))

    start = time.time()
    student_allocation(electives, students, min_capacity, quota=0)

    print('\nmetrics (initial allocation):')
    call_all_metrics(students)

    bratki_tapki, optimal_transfer_graph = transfer_graph(electives)
    optimal_transfer_graph, temp_graph, bratki_tapki = floyd(bratki_tapki, optimal_transfer_graph, electives, students)
    end2 = time.time()

    print('\nmetrics (after optimal transfer graph):')
    call_all_metrics(students)
    print(f'Time: {np.round((end2 - start) / 60, 2)} min')

    remnant_students_allocation(optimal_transfer_graph, temp_graph, bratki_tapki, electives, students, min_capacity)

    print('\nmetrics (after allocation of remnant students):')
    call_all_metrics(students)
    end = time.time()
    print(f'Time: {np.round((end - start) / 60, 2)} min')

    confirm_students_allocation(students)
