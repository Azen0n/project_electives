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
    bratki_tapki=np.full((len(electives), len(electives)), np.inf)
    for elective in electives:
        for student in elective.result_students:
            for index, priority in enumerate(student.priorities):
                if elective.id != priority:
                    result_elective_index = np.where(student.priorities == student.elective_id)[0][0]
                    if optimal_transfer_graph[elective.id - 1][priority - 1]>(result_elective_index - index) * student.performance:
                        optimal_transfer_graph[elective.id - 1][priority - 1] = (index - result_elective_index) * student.performance
                        bratki_tapki[elective.id - 1][priority - 1] = student.id

                else:
                    optimal_transfer_graph[priority - 1][priority - 1] = 0.0

    for i in range(len(electives)):
        for j in range(i + 1, len(electives)):
            prikol = 0
            if optimal_transfer_graph[i][j] + optimal_transfer_graph[j][i] < 0:
                prikol += 1

    return (optimal_transfer_graph, bratki_tapki)


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

'''for i in range(int(len(temp_graph[temp_priority][min_index]) / 2)):
            min_student = min(electives[temp_graph[temp_priority][min_index][-i * 2 + 1]].result_students)'''

def remnant_students_allocation(optimal_transfer_graph, temp_graph, bratki_tapki, electives, students, min_capacity):
    """Распределение оставшихся (нераспределенных) студентов."""
    remnant_students = get_remnant_students(students).tolist()
    remnant_students.sort(key=lambda x: 5 - x.performance)
    remnant_students = np.array(remnant_students)



    for student in remnant_students:
        min_value = 25.0
        temp5 = False
        uncompleted_electives = get_uncompleted_electives(electives, min_capacity)
        for i, priority in enumerate(student.priorities):
            for elective in uncompleted_electives:
                if optimal_transfer_graph[priority-1][elective.id - 1] - student.performance * (5 - i) < min_value and optimal_transfer_graph[priority-1][elective.id - 1]!= np.inf:
                    min_value = min(optimal_transfer_graph[priority-1]) + student.performance * (5 - i)
                    min_index = elective.id - 1
                    temp_priority = priority-1
                    temp5 = True
        if temp5:
            Hod(electives, temp_graph, bratki_tapki, temp_priority, min_index, optimal_transfer_graph)
            add_student_to_elective(student, electives[temp_priority])
            optimal_transfer_graph, bratki_tapki = transfer_graph(electives)
            optimal_transfer_graph, temp_graph, bratki_tapki = floyd(optimal_transfer_graph, bratki_tapki, electives, students)

def floyd(optimal_transfer_graph, bratki_tapki, electives, students):
    temp_graph = []
    pop=0
    temp9=True
    for i in range(optimal_transfer_graph.shape[0]):
        temp_graph.append([])
        for j in range(optimal_transfer_graph.shape[0]):
            optimal_transfer_graph[i][j] = (optimal_transfer_graph[i][j])
            temp_graph[i].append([(i, j)])
    temp_graph2 = copy.deepcopy(temp_graph)
    while (temp9):
        temp9=False
        for k in range(optimal_transfer_graph.shape[0]):
            pop+=1
            for p in range(optimal_transfer_graph.shape[0]):
                if (len(temp_graph[p][p])!=1 and optimal_transfer_graph[p][p]!=np.inf):
                    k=0
                    Hod(electives, temp_graph, bratki_tapki, p , p ,optimal_transfer_graph)
                    optimal_transfer_graph, bratki_tapki = transfer_graph(electives)
                    temp_graph=copy.deepcopy(temp_graph2)
                    temp_graph
                    temp9=True
            for i in range(optimal_transfer_graph.shape[0]):
                for j in range(optimal_transfer_graph.shape[0]):
                    if optimal_transfer_graph[i][j] > optimal_transfer_graph[i][k] + optimal_transfer_graph[k][j]:
                        optimal_transfer_graph[i][j] = optimal_transfer_graph[i][k] + optimal_transfer_graph[k][j]
                        temp_graph[i][j] = temp_graph[i][k]+temp_graph[k][j]
    return optimal_transfer_graph, temp_graph, bratki_tapki



def find_delete_student(elective, id):
    for stud in elective.result_students:
        if stud.id == id:
            temp3=stud
            elective.result_students.remove(temp3)
            return temp3

def Hod(electives, temp_graph, bratki_tapki, k, p ,optimal_transfer_graph):
    for transposition in temp_graph[k][p]:
        temp = bratki_tapki[transposition[0]][transposition[1]]
        temp2 = find_delete_student(electives[transposition[0]], temp)
        if temp2==None :
            print(1)
        temp2.elective_id = transposition[1]+1
        electives[transposition[1]].result_students.append(temp2)






