from objects import Student, Elective


def test_students(students: list[Student]):
    """Выводит студентов, распределенных на электив не из списка приоритетов."""
    for student in students:
        if student.elective_id not in student.priorities and student.elective_id is not None:
            print(f'Student {student.id} misallocated. '
                  f'{student.priorities} -> {student.elective_id}.')


def test_electives(electives: list[Elective]):
    """Выводит незаполнившиеся элективы, на которые распределены студенты."""
    for elective in electives:
        if len(elective.result_students) < elective.min_capacity and len(elective.result_students) != 0:
            print(f'Elective {elective.id} not completed. '
                  f'Got {len(elective.result_students)} students, '
                  f'expected {elective.min_capacity}.')
