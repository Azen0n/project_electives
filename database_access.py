import psycopg2
#Свои данные сюда
conn = psycopg2.connect(host='localhost', user='univer', password='univer', dbname='project_bd')
cursor = conn.cursor()



def get_current_electives_info():
    # TODO: Сделать запрос к БД, взять список элективов (их коды, активные часы, вместимость) в текущем семестре
    # done
    cursor.execute("""
    select code, electiveName, hours, capacity from electives
""")
    elective_tuple_list = cursor.fetchall()
    # elective_tuple_list = [(i, i + 1, 60, 20) for i in range(199)]  # Генерация данных

    elective_info_lists = list(zip(*elective_tuple_list))
    return elective_info_lists


def get_info_by_elective_code(code):
    # TODO: Сделать запрос к БД, взять информацию об элективе по его коду
    # done
    # info_tuple = (0, 1, 2, 3, 4, 5, 6, 7)  # Генерация данных
    cursor.execute(f"""
    SELECT code, electivename, capacity, hours, incharge, author, annotation, dateofchange
    FROM Electives WHERE code = '{code}'
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
    # TODO: Сделать запрос к БД, отдать измененые данные
    # done
    cursor.execute(f"""
    UPDATE Electives
	SET electivename='{info['name']}', capacity='{info['capacity']}', hours='{info['hours']}',
        incharge='{info['in_charge']}', author='{info['author']}', annotation='{info['annotation']}',
        dateofchange='{info['footer_data']}'
	WHERE code='{info['code']}';
        """)
    print(info)
    conn.commit()
    code = info['code']
    info_list = [
        info['name'],
        info['capacity'],
        info['hours'],
        info['in_charge'],
        info['author'],
        info['annotation'],
        info['footer_date']
    ]


def get_semesters():
    # TODO: Сделать запрос к БД, взять список семестров
    # done
    cursor.execute(f"""
    SELECT yearofpassage, semester FROM passedElectives
    GROUP BY yearofpassage, semester
            """)
    semester_tuple_list = cursor.fetchall()  # Генерация данных
    # for i in range(2001, 2021):  # Генерация данных
    #     semester_tuple_list.append((str(i), 'осень'))  # Генерация данных
    #     semester_tuple_list.append((str(i + 1), 'весна'))  # Генерация данных
    semester_list = [str(item[0]) + ' год, ' + item[1] for item in semester_tuple_list]
    return semester_list


def get_electives_info_by_semester(semester):
    # TODO: Сделать запрос к БД, взять список элективов (их коды, активные часы, вместимость) в выбранном семестре
    #done
    cursor.execute(f"""
        SELECT  DISTINCT Electives.code, Electives.electiveName FROM passedElectives
        join Electives on passedElectives.electiveID = Electives.eLectiveID
        WHERE yearofpassage = '{semester[:4]}' and semester = '{semester[10:]}'
                """)
    # semester_tuple = (semester[:4], semester[10:])
    # elective_tuple_list = [(i, i + 1) for i in range(199)]  # Генерация данных
    elective_tuple_list = cursor.fetchall()

    elective_info_lists = list(zip(*elective_tuple_list))
    return elective_info_lists


def get_statistics_by_elective_code(code):
    # TODO: Сделать запрос к БД, взять статистику об выбранном элективе по его коду
    #done
    # average_grade = 4.45  # Генерация данных
    # average_priority = 2.2  # Генерация данных
    # prioritization = [2, 6, 7, 7, 3]  # Генерация данных
    #############
    cursor.execute(f"""
    Select Electives.code, Electives.electiveName, cast(avg(Students.perfomance) as numeric(3,2)) as num from selectedElectives
    join Electives on selectedElectives.electiveID = Electives.electiveID join Students on selectedElectives.studentID = Students.studentID
    where Electives.code = '{code}'
    group by Electives.code, Electives.electiveName
                """)
    average_grade = cursor.fetchall()

    #############
    cursor.execute(f"""
Select Electives.code, Electives.electiveName, cast(avg(priority) as numeric(3,2)) as num from selectedElectives
join Electives on selectedElectives.electiveID = Electives.electiveID
where Electives.code = '{code}'
group by Electives.code, Electives.electiveName
                """)
    average_priority = cursor.fetchall()

    #############
    cursor.execute(f"""
    select priority, количество from 
    (Select Electives.code, Electives.electiveName, SelectedElectives.priority, Count(*) as количество from selectedElectives
    join Electives on selectedElectives.electiveID = Electives.eLectiveID
    where Electives.code = '{code}'
    group by Electives.code, Electives.electiveName, SelectedElectives.priority
    ) as tt
                    """)
    prioritization_bd = cursor.fetchall()
    prioritization = [0]*5
    for priority in prioritization_bd:
        prioritization[priority[0]-1] = priority[1]
    #############
    prioritization_by_grades_1d = [0, 0, 2, 2, 0, 1, 0, 2, 1, 1, 1, 5, 3, 0, 1, 0, 1, 0, 4, 1]  # Генерация данных
    prioritization_by_grades_2d = [[prioritization_by_grades_1d[i:i + 5:] for i in range(0, 4 * 5, 5)]]

    statistics = {
        'average_grade': float(average_grade[0][2]),
        'average_priority': float(average_priority[0][2]),
        'prioritization': prioritization,
        'prioritization_by_grades': prioritization_by_grades_2d
    }
    return statistics
