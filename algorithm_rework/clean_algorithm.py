from dataclasses import dataclass
from math import inf
from time import time

from algorithm.db_queries.clean_test import get_electives, get_students
from algorithm_rework.metrics import get_allocation_quality
from algorithm_rework.tests import test_students, test_electives
from objects import Elective, Student


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
        print(f'Greedy Allocation quality: {get_allocation_quality(self.students)}')

        self.floyd_allocation()
        print(f'Floyd Allocation quality: {get_allocation_quality(self.students)}')

        self.remnant_allocation()
        print(f'Remnant Allocation quality: {get_allocation_quality(self.students)}')

    def sort_electives_by_reserve(self):
        """Сортирует список элективов в порядке убывания резерва."""
        self.electives.sort(key=lambda elective: elective.reserve, reverse=True)

    def greedy_allocation(self):
        """Запуск жадного алгоритма."""
        self.__equate_reserve_with_min_capacity()
        self.__min_capacity_allocation()
        self.__max_capacity_allocation()

    def __equate_reserve_with_min_capacity(self):
        """Заполняет элективы, которым не хватает несколько студентов до минимальной заполненности, студентами,
        выбравшими его на второй и далее приоритеты, пока резерв не сравняется с минимальной вместимостью."""
        for elective in self.electives:
            if elective.is_potentially_completable():
                elective.sort_students_by_priority(smart_students_first=False)
                students = get_students_with_secondary_priorities(elective)
                for student in students:
                    if elective.is_completable():
                        break
                    first_priority_elective = self.__find_elective(student.priorities[0])
                    if student.is_available() and is_first_priority_elective_available(first_priority_elective, elective):
                        elective.reserve += 1
                        first_priority_elective.reserve -= 1
                        elective.add_student(student)
                elective.sort_students_by_priority()

    def __find_elective(self, elective_id: int) -> Elective:
        """Возвращает электив из списка по id."""
        for elective in self.electives:
            if elective.id == elective_id:
                return elective

    def __min_capacity_allocation(self):
        """Заполняет элективы, пока не будет достигнуто минимальное количество студентов в элективах."""
        for elective in self.electives:
            for student in elective.students:
                if student.is_available() and not elective.is_min_completed() and elective.is_completable():
                    elective.add_student(student)

    def __max_capacity_allocation(self):
        """Полностью заполняет элективы студентами."""
        for elective in self.electives:
            for student in elective.students:
                if student.is_available() and not elective.is_max_completed() and elective.is_completable():
                    elective.add_student(student)

    def floyd_allocation(self):
        """Запуск алгоритма Флойда."""
        number_of_electives = len(self.electives)
        transfer_cost_graph, transfer_id_graph = self.__get_student_transfer_graph()
        transfer_path_graph = self.__get_transfer_path_graph()
        is_in_negative_cycle = True

        while is_in_negative_cycle:
            is_in_negative_cycle = False
            for k in range(number_of_electives):
                for p in range(number_of_electives):
                    if is_possible_to_transfer_student(transfer_path_graph[p][p], transfer_cost_graph[p][p]):
                        self.__transfer_student(transfer_path_graph[p][p], transfer_id_graph)
                        transfer_cost_graph, transfer_id_graph = self.__get_student_transfer_graph()
                        transfer_path_graph = self.__get_transfer_path_graph()
                        k = 0
                        is_in_negative_cycle = True
                adjust_transfer_graph(transfer_cost_graph, transfer_path_graph, k)

    def __get_student_transfer_graph(self) -> (list[list[float]], list[list[int]]):
        """Возвращает граф стоимости трансфера студентов с одного электива на другой и граф id этих студентов."""
        number_of_electives = len(self.electives)
        transfer_cost_graph = [[inf for _ in range(number_of_electives)] for _ in range(number_of_electives)]
        transfer_id_graph = [[0 for _ in range(number_of_electives)] for _ in range(number_of_electives)]

        for elective in self.electives:
            for student in elective.result_students:
                for priority in student.priorities:
                    if elective.id != priority:
                        transfer_cost = count_transfer_cost(student, elective.id, priority)
                        if transfer_cost < transfer_cost_graph[elective.id - 1][priority - 1]:
                            transfer_cost_graph[elective.id - 1][priority - 1] = round(-transfer_cost, 2)
                            transfer_id_graph[elective.id - 1][priority - 1] = student.id
                    else:
                        transfer_cost_graph[priority - 1][priority - 1] = 0.
        return transfer_cost_graph, transfer_id_graph

    def __get_transfer_path_graph(self) -> list[list[list[tuple[int]]]]:
        """Возвращает начальный граф путей трансфера студентов."""
        number_of_electives = len(self.electives)
        transfer_path_graph = []
        for i in range(number_of_electives):
            transfer_path_graph.append([])
            for j in range(number_of_electives):
                transfer_path_graph[i].append([(i + 1, j + 1)])
        return transfer_path_graph

    def __transfer_student(self, path: list[tuple[int]], transfer_id_graph: list[list[int]]):
        """Трансфер студента из одного электива в другой по пути трансферов."""
        for transfer in path:
            student = self.__find_student(transfer_id_graph[transfer[0] - 1][transfer[1] - 1])
            first_elective = self.__find_elective(transfer[0])
            second_elective = self.__find_elective(transfer[1])
            first_elective.delete_student(student)
            second_elective.add_student(student)

    def __find_student(self, student_id: int) -> Student:
        """Возвращает студента из списка по id."""
        for student in self.students:
            if student.id == student_id:
                return student

    def remnant_allocation(self):
        """Запуск алгоритма распределения нераспределенных студентов."""
        self.__greedy_remnant_allocation()
        self.floyd_allocation()
        self.__delete_misallocated_students()

    def __greedy_remnant_allocation(self):
        """Распределение нераспределенных студентов на любые незаполненные элективы без учета приоритетов."""
        remnant_students = self.__get_remnant_students()
        for elective in self.electives:
            for i in range(elective.max_capacity - len(elective.result_students)):
                if remnant_students:
                    elective.add_student(remnant_students.pop(0))
                else:
                    break

    def __delete_misallocated_students(self):
        """Удаляет всех студентов, записанных на чужой или незаполнившийся электив."""
        for student in self.students:
            if student.elective_id not in student.priorities:
                elective = self.__find_elective(student.elective_id)
                elective.delete_student(student)
        for elective in self.electives:
            if len(elective.result_students) < elective.min_capacity:
                for student in elective.result_students:
                    elective.delete_student(student)

    def __get_remnant_students(self) -> list[Student]:
        """Возвращает нераспределенных студентов, отсортированных по успеваемости."""
        remnant_students = []
        for student in self.students:
            if student.is_available():
                remnant_students.append(student)
        remnant_students.sort(key=lambda student: 5 - student.performance)
        return remnant_students


def is_possible_to_transfer_student(path: list[tuple[int]], cost: float) -> bool:
    return len(path) != 1 and cost != inf


def adjust_transfer_graph(transfer_cost_graph: list[list[float]], transfer_path_graph: list[list[list[tuple]]], k: int):
    """Корректирует граф трансфера, добавляя оптимальные трансферы студентов из i электива в j через k."""
    number_of_electives = len(transfer_cost_graph)
    for i in range(number_of_electives):
        for j in range(number_of_electives):
            new_transfer_cost = transfer_cost_graph[i][k] + transfer_cost_graph[k][j]
            if transfer_cost_graph[i][j] > new_transfer_cost:
                transfer_cost_graph[i][j] = new_transfer_cost
                transfer_path_graph[i][j] = transfer_path_graph[i][k] + transfer_path_graph[k][j]


def count_transfer_cost(student: Student, first_elective_id: int, second_elective_id: int) -> float:
    """Возвращает стоимость трансфера студента с одного электива на другой."""
    first_elective_position = student.get_elective_position(first_elective_id)
    second_elective_position = student.get_elective_position(second_elective_id)
    return student.performance * (first_elective_position - second_elective_position)


def get_students_with_secondary_priorities(elective: Elective) -> list[Student]:
    """Возвращает список студентов, выбравших электив на второй и далее приоритеты."""
    secondary_students = []
    for student in elective.students:
        if student.priorities[0] != elective.id:
            secondary_students.append(student)
    return secondary_students


def is_first_priority_elective_available(first_priority_elective: Elective, current_elective: Elective) -> bool:
    """Первый выбранный студентом электив сможет заполниться, если записать студента на другой электив."""
    return first_priority_elective.reserve > current_elective.min_capacity > current_elective.reserve


def main():
    electives = get_electives().tolist()
    students = get_students().tolist()

    allocator = StudentAllocator(electives, students)
    allocator.run()

    test_students(allocator)
    test_electives(allocator)


if __name__ == '__main__':
    main()
