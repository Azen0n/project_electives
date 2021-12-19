import numpy as np
from data import Elective, Student, generate_electives, generate_students


def get_electives() -> np.ndarray:
    """Функция возвращает массив с объектами класса Elective, используя запрос в бд."""
    return generate_electives(40, 20, 25)


def get_students() -> np.ndarray:
    """Функция возвращает массив с объектами класса Student, используя запрос в бд."""
    return generate_students(800, 40, 'gamma')


def main():
    pass


if __name__ == '__main__':
    main()
