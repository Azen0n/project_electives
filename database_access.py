from random import randint

import psycopg2

connection = psycopg2.connect(host='localhost', user='postgres', password='89058539346Dds', dbname='electives')
cursor = connection.cursor()


def get_current_electives_info():
    cursor.execute("""
        SELECT code, electiveName, hours, capacity
        FROM electives
        """)
    elective_tuple_list = cursor.fetchall()

    elective_info_lists = list(zip(*elective_tuple_list))
    return elective_info_lists


def not_distribution():
    cursor.execute("""
        SELECT COUNT(*)
        FROM electives
        """)
    number_of_electives = cursor.fetchall()[0][0]

    weekdays = ['Вторник', 'Среда', 'Четверг', 'Пятница']
    for i in range(number_of_electives):
        day_number = randint(2, 5)
        cursor.execute(f"""
            INSERT INTO elective_groups_datatable(electiveid, groupid, day)
            VALUES ({i + 1}, {day_number - 2}, '{weekdays[day_number - 2]}')
            """)
    connection.commit()


def get_info_by_elective_code(code):
    cursor.execute(f"""
        SELECT code, electivename, capacity, hours, incharge, author, annotation, dateofchange
        FROM electives
        WHERE code = '{code}'
        """)
    info_tuple = cursor.fetchall()

    string_info_tuple = list(map(str, info_tuple[0]))
    info = {
        'code': string_info_tuple[0],
        'name': string_info_tuple[1],
        'capacity': string_info_tuple[2],
        'hours': string_info_tuple[3],
        'in_charge': string_info_tuple[4],
        'author': string_info_tuple[5],
        'annotation': string_info_tuple[6],
        'footer_date': string_info_tuple[7]
    }
    return info


def set_info_by_elective_code(info):
    cursor.execute(f"""
        UPDATE electives
        SET electivename='{info['name']}',
            capacity='{info['capacity']}',
            hours='{info['hours']}',
            incharge='{info['in_charge']}',
            author='{info['author']}',
            annotation='{info['annotation']}',
            dateofchange='{info['footer_data']}'
        WHERE code='{info['code']}';
        """)
    connection.commit()


def get_semesters():
    cursor.execute(f"""
        SELECT yearofpassage, semester
        FROM selected_electives
        GROUP BY yearofpassage, semester
        """)
    semester_tuple_list = cursor.fetchall()

    list_of_semesters = [str(item[0]) + ' год, ' + item[1] for item in semester_tuple_list]
    return list_of_semesters


def get_electives_info_by_semester(semester):
    year, season = semester[:4], semester[-1:-6]

    cursor.execute(f"""
        SELECT DISTINCT electives.code, electives.electiveName
        FROM selected_electives
            JOIN electives ON selected_electives.electiveID = electives.eLectiveID
        WHERE yearofpassage = '{year}' AND semester = '{season}'
        """)
    elective_tuple_list = cursor.fetchall()

    elective_info_lists = list(zip(*elective_tuple_list))
    return elective_info_lists


def get_statistics_by_elective_code(semester, code):
    year, season = semester[:4], semester[-1:-6]

    # Возвращает имя электива по его коду
    cursor.execute(f"""
        SELECT electiveName
        FROM electives
        WHERE code = {code}
        """)
    elective_name = cursor.fetchall()

    # Возвращает среднюю оценку для электива в определенном семестре
    cursor.execute(f"""
        SELECT CAST(AVG(Students.perfomance) AS NUMERIC(3, 2))
        FROM selected_electives 
            JOIN Electives ON selected_electives.electiveID = Electives.eLectiveID
            JOIN Students ON selected_electives.studentID = Students.studentID
        WHERE yearofpassage = {year} AND semester = {season} AND code = {code}
        """)
    average_grade = cursor.fetchall()

    # Возвращает средний приоритет для электива в определенном семестре
    cursor.execute(f"""
        SELECT CAST(AVG(priority) AS NUMERIC(3, 2))
        FROM selected_electives
            JOIN Electives ON selected_electives.electiveID = Electives.eLectiveID
        WHERE yearofpassage = {year} AND semester = {season} AND code = {code}
        """)
    average_priority = cursor.fetchall()

    # Возвращает список с количеством людей для каждого приоритета для электива в определенном семестре
    cursor.execute(f"""
        SELECT selected_electives.priority, COUNT(*) AS number_of_elections 
        FROM selected_electives
            JOIN Electives ON selected_electives.electiveID = Electives.eLectiveID
        WHERE yearofpassage = {year} AND semester = {season} AND Electives.code = {code}
        GROUP BY selected_electives.priority
        """)
    prioritization_bd = cursor.fetchall()

    prioritization = [0] * 5
    for priority in prioritization_bd:
        prioritization[priority[0] - 1] = priority[1]

    #############
    prioritization_by_grades_1d = [0, 0, 2, 2, 0, 1, 0, 2, 1, 1, 1, 5, 3, 0, 1, 0, 1, 0, 4, 1]  # Генерация данных
    prioritization_by_grades_2d = [[prioritization_by_grades_1d[i:i + 5:] for i in range(0, 4 * 5, 5)]]

    statistics = {
        'name': str(elective_name),
        'average_grade': float(average_grade),
        'average_priority': float(average_priority),
        'prioritization': prioritization,
        'prioritization_by_grades': prioritization_by_grades_2d
    }
    return statistics


def get_current_elective_codes_and_names(day):
    cursor.execute(f"""
        SELECT electives.code, electives.electiveName, electives.hours, electives.capacity
        FROM electives
            JOIN elective_groups_datatable ON electives.electiveID = elective_groups_datatable.electiveID
        WHERE elective_groups_datatable.day = '{day}'
        """)
    elective_tuple_list = cursor.fetchall()

    elective_info_lists = list(zip(*elective_tuple_list))
    return elective_info_lists


def authentication_by_id(auth_id):
    cursor.execute(f"""
        SELECT 1
        FROM students
        WHERE studentID = '{auth_id}'
        """)
    user = cursor.fetchall()
    return user


def student_priorities(student_id, elective_code_list):
    # TODO: Послать в БД данные: id студента и упорядоченный массив кодов его выбранных элективов
    pass
