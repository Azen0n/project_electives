import numpy as np


def student_allocation(electives, students, min_capacity):
    for elective in electives:
        fill_elective_with_students(students, elective)
        sort_students_in_elective(elective, reverse=False)
        calculate_reserve(elective)

    electives = np.array(sorted(electives, key=lambda x: x.reserve, reverse=True))

    for elective in electives:
        if min_capacity / 2.0 <= elective.reserve < min_capacity:
            # student[0] — студент (есть поля id и прочее)
            # student[1] — приоритет электива

            for student in elective.students:
                if elective.reserve >= min_capacity:
                    break

                first_priority_elective = search_elective(electives, student[0].priorities[0])

                for i in range(2, 6):
                    if student[1] == i and student[0].availability and electives[first_priority_elective].reserve > min_capacity and elective.reserve < min_capacity:
                        elective.reserve += 1
                        electives[first_priority_elective].reserve -= 1
                        add_student_to_elective(student[0], elective)

    for elective in electives:
        sort_students_in_elective(elective, reverse=True)

    for i in range(1, 6):
        for elective in electives:
            for student in elective.students:
                if student[1] == i and student[0].availability and len(elective.result_students) < elective.capacity:
                    add_student_to_elective(student[0], elective)


def search_elective(electives, id):
    i = 0
    for elective in electives:
        if elective.id == id:
            return i
        i += 1


def fill_elective_with_students(students, elective):
    """Заполнение списка студентов, выбравших электив и позиция выбора."""
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
    """Добавление стдуента в финальный список электива."""
    student[0].availability = False
    student[0].elective_id = elective.id
    elective.result_students.append(student)
