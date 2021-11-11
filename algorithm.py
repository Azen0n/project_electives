import numpy as np


def student_allocation(electives, students, min_capacity):
    # У каждого электива список студентов, которые его выбрали: (студент, приоритет электива)
    for elective in electives:
        for student in students:
            if elective.id in student.priorities:
                elective.students.append([student, np.where(student.priorities == elective.id)[0][0] + 1])
        # Сортировка по приоритету электива, затем по успеваемости
        elective.students.sort(key=lambda x: (x[1], x[0].performance))

    for elective in electives:
        for student in elective.students:
            if student[-1] == 1:
                elective.reserve += 1

    electives = np.array(sorted(electives, key=lambda x: x.reserve, reverse=False))

    for elective in electives:
        if elective.reserve < min_capacity:
            # student[0] — студент (есть поля id и прочее)
            # student[1] — приоритет электива

            for student in elective.students:
                first_priority_elective = search_elective(electives, student[0].priorities[0])

                for i in range(2, 6):
                    if student[1] == i and student[0].availability and electives[first_priority_elective].reserve > min_capacity and elective.reserve < min_capacity:
                        elective.reserve += 1
                        student[0].availability = False
                        student[0].elective_id = elective.id
                        electives[first_priority_elective].reserve -= 1
                        elective.result_students.append(student[0])

    for elective in electives:
        for i in range(1, 6):
            for student in elective.students:
                if student[1] == i and student[0].availability and len(elective.result_students) < elective.capacity:
                    student[0].availability = False
                    student[0].elective_id = elective.id
                    elective.result_students.append(student[0])

    print(1)


def search_elective(electives, id):
    i = 0
    for elective in electives:
        if elective.id == id:
            return i
        i += 1
