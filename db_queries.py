import numpy as np
import psycopg2 as pg
from data import Elective, Student


with open('connection_string.txt') as f:
    CONNECTION_STRING = f.readlines()[0]


def get_electives() -> np.ndarray:
    """Функция возвращает массив с объектами класса Elective, используя запрос в бд."""
    electives = []

    connection = pg.connect(CONNECTION_STRING)
    cur = connection.cursor()

    sql = 'select distinct electiveid, capacity, dayofweek from Directions order by electiveid;'
    cur.execute(sql)

    row = cur.fetchone()
    while row:
        elective = Elective(row[0], row[1], [], row[2])
        electives.append(elective)
        row = cur.fetchone()

    return np.array(electives)


def get_students() -> np.ndarray:
    """Функция возвращает массив с объектами класса Student, используя запрос в бд."""
    students = []

    connection = pg.connect(CONNECTION_STRING)
    cur = connection.cursor()

    sql = f'select studentid, electiveid, priority, performance from Directions order by studentid, priority;'
    cur.execute(sql)

    rows = cur.fetchmany(5)
    while rows:
        priorities = np.array([rows[i][1] for i in range(5)])
        student = Student(rows[0][0], float(rows[0][3]), priorities)
        students.append(student)
        rows = cur.fetchmany(5)

    return np.array(students)


def confirm_students_allocation(students):
    """Заполнение таблицы Passed распределенными студентами."""

    connection = pg.connect(CONNECTION_STRING)
    cur = connection.cursor()

    sql = f'truncate Passed;'
    cur.execute(sql)

    for student in students:
        if student.elective_id is not None:
            sql = f'insert into Passed (studentid, electiveid) values ({student.id}, {student.elective_id});'
            cur.execute(sql)

    connection.commit()


def main():
    get_students()
    get_electives()


if __name__ == '__main__':
    main()
