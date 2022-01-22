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
        self.greedy_allocation()
        self.floyd_allocation()

    def sort_electives_by_reserve(self):
        """Сортирует список элективов в порядке убывания резерва."""
        self.electives.sort(key=lambda elective: elective.reserve, reverse=True)

    def greedy_allocation(self):
        """Запуск жадного алгоритма."""
        equate_reserve_with_min_capacity(self.electives)
        min_capacity_allocation(self.electives)
        max_capacity_allocation(self.electives)

    def floyd_allocation(self):
        """Запуск алгоритма Флойда."""
        student_transfer_cost_graph, student_transfer_id_graph = get_student_transfer_graph(self.electives)
        transfer_path_graph = get_transfer_path_graph(student_transfer_cost_graph)
        is_in_negative_cycle = True
        while is_in_negative_cycle:
            break


def get_student_transfer_graph(electives) -> (list[list[float]], list[list[int]]):
    """Возвращает граф стоимости трансфера студентов с одного электива на другой и граф id этих студентов."""
    number_of_electives = len(electives)
    student_transfer_cost_graph = [[50. for _ in range(number_of_electives)] for _ in range(number_of_electives)]
    student_transfer_id_graph = [[0 for _ in range(number_of_electives)] for _ in range(number_of_electives)]

    for elective in electives:
        for student in elective.result_students:
            for priority in student.priorities:
                if elective.id != priority:
                    transfer_cost = count_transfer_cost(student, elective.id, priority)
                    if transfer_cost < student_transfer_cost_graph[elective.id - 1][priority - 1]:
                        student_transfer_cost_graph[elective.id - 1][priority - 1] = round(-transfer_cost, 2)
                        student_transfer_id_graph[elective.id - 1][priority - 1] = student.id
                else:
                    student_transfer_cost_graph[priority - 1][priority - 1] = 0.
    return student_transfer_cost_graph, student_transfer_id_graph


def count_transfer_cost(student: Student, first_elective_id: int, second_elective_id: int) -> float:
    """Возвращает стоимость трансфера студента с одного электива на другой."""
    first_elective_position = student.get_elective_priority(first_elective_id)
    second_elective_position = student.get_elective_priority(second_elective_id)
    return student.performance * (first_elective_position - second_elective_position)


def get_transfer_path_graph(student_transfer_cost_graph: list[list[float]]):
    """??????????"""
    number_of_electives = len(student_transfer_cost_graph)
    transfer_path_graph = []
    for i in range(number_of_electives):
        transfer_path_graph.append([])
        for j in range(number_of_electives):
            transfer_path_graph[i].append([(i, j)])
    return transfer_path_graph


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
    allocator.run()
    call_all_metrics_clean(allocator.students)


if __name__ == '__main__':
    main()
