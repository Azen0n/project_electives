import psycopg2 as pg
from data_generation import generate_students, generate_electives

if __name__ == '__main__':
    connection = pg.connect(host='localhost', user='postgres', password='nGr5DE&VctB2+=N8kBHb#JcY#W9xdBSR', dbname='test')
    cur = connection.cursor()

    sql = 'truncate Directions;'
    cur.execute(sql)

    number_of_students = 500
    number_of_electives = 60

    students = generate_students(number_of_students, number_of_electives, distribution='gamma')
    electives = generate_electives(number_of_electives, 20, 25)

    for student in students:
        for i, priority in enumerate(student.priorities):
            sql = f'insert into Directions (studentid, electiveid, priority, dayofweek, performance, capacity)' \
                  f'values ({student.id}, {priority}, {i + 1}, {electives[priority - 1].day}, {student.performance}, {electives[priority - 1].capacity});'

            cur.execute(sql)

    connection.commit()
