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
                    if student[1] == i and student[0].is_available and electives[first_priority_elective].reserve > min_capacity and elective.reserve < min_capacity:
                        elective.reserve += 1
                        electives[first_priority_elective].reserve -= 1
                        add_student_to_elective(student[0], elective)

    for elective in electives:
        sort_students_in_elective(elective, reverse=True)

    for i in range(1, 6):
        for elective in electives:
            for student in elective.students:
                if student[1] == i and student[0].is_available and len(elective.result_students) < elective.capacity:
                    add_student_to_elective(student[0], elective)


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
    electives_graph = np.full((len(electives), len(electives)), 25.0)   # 25 — максимум
    for elective in electives:
        for student in elective.result_students:
            for index, priority in enumerate(student.priorities):
                if elective.id != priority:
                    sink = np.where(student.priorities == student.elective_id)[0][0]
                    electives_graph[elective.id - 1][priority - 1] = min((index - sink) * student.performance, electives_graph[elective.id - 1][priority - 1])
                else:
                    electives_graph[priority - 1][priority - 1] = 0.0

    return electives_graph


def get_remnant_students(students):
    """Поиск нераспределенных студентов."""
    remnant_students = []
    for student in students:
        if student.is_available:
            remnant_students.append(student)
    return np.array(remnant_students)


def remnant_students_allocation():
    """Распределение оставшихся (нераспределенных) студентов."""
    pass


def sosat():
    pass
