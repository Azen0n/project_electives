from dataclasses import dataclass

from algorithm.db_queries.clean_test import get_electives, get_students
from objects import Elective, Student
from algorithm.metrics import call_all_metrics_clean


@dataclass
class StudentAllocator:
    electives: list[Elective]
    students: list[Student]

    def __post_init__(self):
        for elective in self.electives:
            elective.fill(self.students)
            elective.sort_students_by_priority(smart_students_first=True)
        self.sort_electives_by_reserve()

    def run(self):
        """Запуск алгоритма распределения студентов по элективам."""
        raise NotImplementedError

    def sort_electives_by_reserve(self):
        """Сортирует список элективов в порядке убывания резерва."""
        self.electives.sort(key=lambda elective: elective.reserve, reverse=True)

    def greedy_allocation(self):
        """Запуск жадного алгоритма."""
        equate_reserve_with_min_capacity(self.electives)
        min_capacity_allocation(self.electives)
        max_capacity_allocation(self.electives)


def equate_reserve_with_min_capacity(electives: list[Elective]):
    """Заполняет элективы, которым не хватает несколько студентов до минимальной заполненности, студентами,
    выбравшими его на второй и далее приоритеты, пока резерв не сравняется с минимальной вместимостью."""
    for elective in electives:
        if elective.is_potentially_completable():
            elective.sort_students_by_priority(smart_students_first=False)
            students = get_students_with_secondary_priorities(elective)
            for student in students:
                if elective.is_completable():
                    break
                first_priority_elective = find_elective(electives, student.priorities[0])
                if student.is_available() and is_first_priority_elective_available(first_priority_elective, elective):
                    elective.reserve += 1
                    first_priority_elective.reserve -= 1
                    elective.add_student(student)
            elective.sort_students_by_priority()


def get_students_with_secondary_priorities(elective: Elective) -> list[Student]:
    """Возвращает список студентов, выбравших электив на второй и далее приоритеты."""
    secondary_students = []
    for student in elective.students:
        if student.priorities[0] != elective.id:
            secondary_students.append(student)
    return secondary_students


def find_elective(electives: list[Elective], elective_id: int) -> Elective:
    """Возвращает электив из списка по id."""
    for elective in electives:
        if elective.id == elective_id:
            return elective


def is_first_priority_elective_available(first_priority_elective: Elective, current_elective: Elective) -> bool:
    """Первый выбранный студентом электив сможет заполниться, если записать студента на другой электив."""
    return first_priority_elective.reserve > current_elective.min_capacity > current_elective.reserve


def min_capacity_allocation(electives: list[Elective]):
    """Заполняет элективы, пока не будет достигнуто минимальное количество студентов в элективах."""
    for elective in electives:
        for student in elective.students:
            if student.is_available() and not elective.is_min_completed() and elective.is_popular_enough():
                elective.add_student(student)


def max_capacity_allocation(electives: list[Elective]):
    """Полностью заполняет элективы студентами."""
    for elective in electives:
        for student in elective.students:
            if student.is_available() and not elective.is_max_completed() and elective.is_popular_enough():
                elective.add_student(student)


def main():
    electives = get_electives().tolist()
    students = get_students().tolist()

    allocator = StudentAllocator(electives, students)
    allocator.greedy_allocation()
    call_all_metrics_clean(allocator.students)


if __name__ == '__main__':
    main()
