from dataclasses import dataclass, field


@dataclass
class Student:
    id: int
    performance: float
    priorities: list[int]
    elective_id: int = None

    def get_elective_priority(self, elective_id: int) -> int:
        """Возвращает позицию электива в списке приоритетов. Если электив не выбран, возвращает 6."""
        return self.priorities.index(elective_id) + 1 if elective_id in self.priorities else 6

    def is_available(self) -> bool:
        return self.elective_id is None


@dataclass
class Elective:
    id: int
    max_capacity: int
    day: int
    students: list[Student] = field(default_factory=list)
    result_students: list[Student] = field(default_factory=list)
    min_capacity: int = 10
    reserve: int = 0  # Количество первых приоритетов

    def add_student(self, student: Student):
        student.elective_id = self.id
        self.result_students.append(student)

    def delete_student(self, student: Student):
        student.elective_id = None
        self.result_students.remove(student)

    def fill(self, students: list[Student]):
        """Заполняет список студентов, выбравших электив на один из приоритетов и подсчитывает резерв."""
        for student in students:
            if self.id in student.priorities:
                self.students.append(student)
                if student.get_elective_priority(self.id) == 1:
                    self.reserve += 1

    def sort_students_by_priority(self, smart_students_first: bool = True):
        """Сортирует список студентов по приоритету электива и успеваемости."""
        if smart_students_first:
            self.students.sort(key=lambda student: (student.get_elective_priority(self.id), 5 - student.performance))
        else:
            self.students.sort(key=lambda student: (student.get_elective_priority(self.id), student.performance))

    def is_potentially_completable(self) -> bool:
        return self.min_capacity / 2 <= self.reserve < self.min_capacity

    def is_completable(self) -> bool:
        return self.reserve >= self.min_capacity

    def is_popular_enough(self) -> bool:
        return len(self.students) / 2.0 > self.min_capacity

    def is_max_completed(self) -> bool:
        return len(self.result_students) >= self.max_capacity

    def is_min_completed(self) -> bool:
        return len(self.result_students) > self.min_capacity
