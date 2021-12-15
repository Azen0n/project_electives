import copy

import numpy as np


def student_allocation(electives, students, min_capacity):
    for elective in electives:
        fill_elective_with_students(students, elective)
        sort_students_in_elective(elective, reverse=False)
        calculate_reserve(elective)

    electives = np.array(sorted(electives, key=lambda x: x.reserve, reverse=True))

    for elective in electives:
        if min_capacity / 2.0 <= elective.reserve < min_capacity:
            for student in elective.students:
                # student[0] — студент (есть поля id и прочее)
                # student[1] — приоритет электива
                if elective.reserve >= min_capacity:
                    break
                first_priority_elective = search_elective(electives, student[0].priorities[0])

                for i in range(2, 6):
                    if student[1] == i and student[0].is_available and electives[
                        first_priority_elective].reserve > min_capacity and elective.reserve < min_capacity:
                        elective.reserve += 1
                        electives[first_priority_elective].reserve -= 1
                        add_student_to_elective(student[0], elective)

    for elective in electives:
        sort_students_in_elective(elective, reverse=True)

    for i in range(1, 6):
        for elective in electives:
            for student in elective.students:
                if student[1] == i and student[0].is_available and len(
                        elective.result_students) < elective.capacity and (
                        min_capacity < len(elective.students) / 2.0 or elective.reserve >= min_capacity) and len(
                    elective.result_students) < min_capacity:
                    add_student_to_elective(student[0], elective)

    for i in range(1, 6):
        for elective in electives:
            for student in elective.students:
                if student[1] == i and student[0].is_available and len(
                        elective.result_students) < elective.capacity and min_capacity < len(elective.students) / 2.0:
                    add_student_to_elective(student[0], elective)

    electives = np.array(sorted(electives, key=lambda x: x.id))


def search_elective(electives, id):
    """Поиск индекса электива в списке элективов."""
    i = 0
    for elective in electives:
        if elective.id == id:
            return i
        i += 1


def fill_elective_with_students(students, elective):
    """Заполнение списка студентов, выбравших электив, с позицией выбора."""
    for student in students:
        if elective.id in student.priorities:
            elective.students.append([student, np.where(student.priorities == elective.id)[0][0] + 1])


def sort_students_in_elective(elective, reverse):
    """Сортировка списка студентов по позиции выбора и успеваемости."""
    if reverse:
        elective.students.sort(key=lambda x: (x[1], 5 - x[0].performance))
    else:
        elective.students.sort(key=lambda x: (x[1], x[0].performance))


def calculate_reserve(elective):
    """Вычисление количества студентов, выбравших этот электив первым."""
    for student in elective.students:
        if student[1] == 1:
            elective.reserve += 1


def add_student_to_elective(student, elective):
    """Добавление студента в финальный список студентов электива."""
    student.is_available = False
    student.elective_id = elective.id
    elective.result_students.append(student)


def transfer_graph(electives):
    """Составление графа стоимости трансфера студентов."""
    optimal_transfer_graph = np.full((len(electives), len(electives)), np.inf)
    id_graph = np.full((len(electives), len(electives)), np.inf)
    for elective in electives:
        for student in elective.result_students:
            for index, priority in enumerate(student.priorities):
                if elective.id != priority:
                    if elective.id in student.priorities:
                        result_elective_index = np.where(student.priorities == student.elective_id)[0][0]
                    else:
                        result_elective_index = 5
                    if optimal_transfer_graph[elective.id - 1][priority - 1] > (
                            result_elective_index - index) * student.performance:
                        optimal_transfer_graph[elective.id - 1][priority - 1] = np.round((
                                                                                                 index - result_elective_index) * student.performance,
                                                                                         10)
                        id_graph[elective.id - 1][priority - 1] = student.id

                else:
                    optimal_transfer_graph[priority - 1][priority - 1] = 0.0

    for i in range(len(electives)):
        for j in range(i + 1, len(electives)):
            prikol = 0
            if optimal_transfer_graph[i][j] + optimal_transfer_graph[j][i] < 0:
                prikol += 1

    return (optimal_transfer_graph, id_graph)


def get_remnant_students(students):
    """Поиск нераспределенных студентов."""
    remnant_students = []
    for student in students:
        if student.is_available:
            remnant_students.append(student)
    return np.array(remnant_students)


def get_uncompleted_electives(electives, min_capacity):
    """Поиск незаполненных элективов."""
    uncompleted_electives = []
    for elective in electives:
        if min_capacity <= len(elective.result_students) < elective.capacity:
            uncompleted_electives.append(elective)
    return np.array(uncompleted_electives)


def remnant_students_allocation(optimal_transfer_graph, trans_graph, id_graph, electives, students, min_capacity):
    """Распределение оставшихся (нераспределенных) студентов."""
    remnant_students = get_remnant_students(students).tolist()
    remnant_students.sort(key=lambda x: 5 - x.performance)
    new_remnant_students = list()
    for i, remnant in enumerate(remnant_students):
        availability = False
        for i1, priorities in enumerate(remnant.priorities):
            tempp=min(optimal_transfer_graph[priorities - 1])
            availability = min(optimal_transfer_graph[priorities - 1]) >= remnant.performance * (5 - i1)
        if availability:
            new_remnant_students.append(remnant)
    while (len(remnant_students) != 0):
        for elective in electives:
            for i in range(elective.capacity - len(elective.result_students)):
                elective.result_students.append(remnant_students[0])
                remnant_students[0].elective_id = elective.id
                remnant_students[0].is_available = False
                remnant_students.pop(0)
                if len(remnant_students) == 0:
                    break
            if len(remnant_students) == 0:
                break
    optimal_transfer_graph, id_graph = transfer_graph(electives)
    floyd(optimal_transfer_graph, id_graph, electives, students)
    for elective in electives:
        templist = []
        for student in elective.result_students:
            if elective.id not in student.priorities:
                student.elective_id = None
                student.is_available = True
            else:
                templist.append(student)
        elective.result_students = templist
    print(1)


# for student in remnant_students:
#     min_value = 25.0
#     temp5 = False
#     uncompleted_electives = get_uncompleted_electives(electives, min_capacity)
#     for i, priority in enumerate(student.priorities):
#         for elective in uncompleted_electives:
#             if optimal_transfer_graph[priority - 1][elective.id - 1] - student.performance * (5 - i) < min_value and \
#                     optimal_transfer_graph[priority - 1][elective.id - 1] != np.inf:
#                 min_value = min(optimal_transfer_graph[priority - 1]) + student.performance * (5 - i)
#                 min_index = elective.id - 1
#                 temp_priority = priority - 1
#                 temp5 = True
#     if temp5:
#         Hod(electives, trans_graph, id_graph, temp_priority, min_index, optimal_transfer_graph)
#         add_student_to_elective(student, electives[temp_priority])
#         optimal_transfer_graph, id_graph = transfer_graph(electives)
#         optimal_transfer_graph, trans_graph, id_graph = floyd(optimal_transfer_graph, id_graph, electives, students)
#

def floyd(optimal_transfer_graph, id_graph, electives, students):
    trans_graph = []
    pop = 0
    temp9 = True
    for i in range(optimal_transfer_graph.shape[0]):
        trans_graph.append([])
        for j in range(optimal_transfer_graph.shape[0]):
            optimal_transfer_graph[i][j] = (optimal_transfer_graph[i][j])
            trans_graph[i].append([(i, j)])
    trans_graph2 = copy.deepcopy(trans_graph)
    while (temp9):
        temp9 = False
        for k in range(optimal_transfer_graph.shape[0]):
            pop += 1
            for p in range(optimal_transfer_graph.shape[0]):
                if (len(trans_graph[p][p]) != 1 and optimal_transfer_graph[p][p] != np.inf):
                    k = 0
                    Hod(electives, trans_graph, id_graph, p, p, optimal_transfer_graph)
                    optimal_transfer_graph, id_graph = transfer_graph(electives)
                    trans_graph = copy.deepcopy(trans_graph2)
                    trans_graph
                    temp9 = True
            for i in range(optimal_transfer_graph.shape[0]):
                for j in range(optimal_transfer_graph.shape[0]):
                    if optimal_transfer_graph[i][j] > optimal_transfer_graph[i][k] + optimal_transfer_graph[k][j]:
                        optimal_transfer_graph[i][j] = np.round(
                            optimal_transfer_graph[i][k] + optimal_transfer_graph[k][j], 10)
                        trans_graph[i][j] = trans_graph[i][k] + trans_graph[k][j]
    return optimal_transfer_graph, trans_graph, id_graph


def find_delete_student(elective, id):
    for stud in elective.result_students:
        if stud.id == id:
            temp3 = stud
            elective.result_students.remove(temp3)
            return temp3


def Hod(electives, trans_graph, id_graph, k, p, optimal_transfer_graph):
    for transposition in reversed(trans_graph[k][p]):
        temp = int(id_graph[transposition[0]][transposition[1]])
        temp2 = find_delete_student(electives[transposition[0]], temp)
        if temp2 is None:
            print(1)
        else:
            temp2.elective_id = transposition[1] + 1
            electives[transposition[1]].result_students.append(temp2)
