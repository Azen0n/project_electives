import psycopg2 as pg
from objects import Elective, Student


def get_electives() -> list[Elective]:
    """Функция возвращает массив с объектами класса Elective, используя запрос в бд."""
    electives = []

    connection = pg.connect(host='localhost', user='postgres', password='nGr5DE&VctB2+=N8kBHb#JcY#W9xdBSR', dbname='test')
    cur = connection.cursor()

    sql = 'select distinct electiveid, capacity, dayofweek from Directions order by electiveid;'
    cur.execute(sql)

    row = cur.fetchone()
    while row:
        elective = Elective(row[0], row[1], row[2], [])
        electives.append(elective)
        row = cur.fetchone()

    return electives


def get_students() -> list[Student]:
    """Функция возвращает массив с объектами класса Student, используя запрос в бд."""
    students = []

    connection = pg.connect(host='localhost', user='postgres', password='nGr5DE&VctB2+=N8kBHb#JcY#W9xdBSR', dbname='test')
    cur = connection.cursor()

    sql = f'select studentid, electiveid, priority, performance from Directions order by studentid, priority;'
    cur.execute(sql)

    rows = cur.fetchmany(5)
    while rows:
        priorities = [rows[i][1] for i in range(5)]
        student = Student(rows[0][0], float(rows[0][3]), priorities)
        students.append(student)
        rows = cur.fetchmany(5)

    return students


def confirm_students_allocation(students):
    """Заполнение таблицы Passed распределенными студентами."""
    connection = pg.connect(host='localhost', user='postgres', password='nGr5DE&VctB2+=N8kBHb#JcY#W9xdBSR', dbname='test')
    cur = connection.cursor()

    sql = f'truncate Passed;'
    cur.execute(sql)

    for student in students:
        if student.elective_id is not None:
            sql = f'insert into Passed (studentid, electiveid) values ({student.id}, {student.elective_id});'
            cur.execute(sql)

    connection.commit()
