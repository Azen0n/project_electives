from algorithm_rework.clean_algorithm import StudentAllocator


def test_students(allocator: StudentAllocator):
    for student in allocator.students:
        if student.elective_id not in student.priorities:
            print(f'Student {student.id} misallocated.'
                  f'{student.priorities} -> {student.elective_id}.')


def test_electives(allocator: StudentAllocator):
    for elective in allocator.electives:
        if len(elective.result_students) < elective.min_capacity and len(elective.result_students) != 0:
            print(f'Elective {elective.id} not completed.'
                  f'Got {len(elective.result_students)} students,'
                  f'expected {elective.min_capacity}.')
