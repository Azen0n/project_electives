import psycopg2 as pg
from data import generate_students, generate_electives

if __name__ == '__main__':
    with open('connection_string.txt') as f:
        CONNECTION_STRING = f.readlines()[0]

    connection = pg.connect(CONNECTION_STRING)
    cur = connection.cursor()

    sql = 'truncate Directions;'
    cur.execute(sql)

    number_of_students = 800
    number_of_electives = 40

    students = generate_students(number_of_students, number_of_electives, distribution='gamma')
    electives = generate_electives(number_of_electives, 20, 25)

    for student in students:
        for i, priority in enumerate(student.priorities):
            sql = f'insert into Directions (studentid, electiveid, priority, dayofweek, performance, capacity)' \
                  f'values ({student.id}, {priority}, {i + 1}, {electives[priority - 1].day}, {student.performance}, {electives[priority - 1].capacity});'

            cur.execute(sql)

    connection.commit()
