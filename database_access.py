def get_current_elective_codes_and_names():
    # TODO: Сделать запрос к БД, взять список элективов (и их коды) в текущем семестре
    elective_tuple_list = [(i, i + 1) for i in range(199)]  # Генерация данных

    elective_code_and_name_lists = list(zip(*elective_tuple_list))
    elective_code_list = list(map(str, elective_code_and_name_lists[0]))
    elective_name_list = list(map(str, elective_code_and_name_lists[1]))
    return elective_code_list, elective_name_list


def get_info_by_elective_code(code):
    # TODO: Сделать запрос к БД, взять информацию об элективе по его коду
    info_tuple = (0, 1, 2, 3, 4, 5, 6, 7)  # Генерация данных

    info = {
        'code': info_tuple[0],
        'name': info_tuple[1],
        'capacity': info_tuple[2],
        'hours': info_tuple[3],
        'in_charge': info_tuple[4],
        'author': info_tuple[5],
        'annotation': info_tuple[6],
        'footer_date': info_tuple[7]
    }
    return info


def set_info_by_elective_code(info):
    # TODO: Сделать запрос к БД, отдать измененые данные
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
    semester_tuple_list = []  # Генерация данных
    for i in range(2001, 2021):  # Генерация данных
        semester_tuple_list.append((str(i), 'осень'))  # Генерация данных
        semester_tuple_list.append((str(i + 1), 'весна'))  # Генерация данных

    semester_list = [item[0] + ' год, ' + item[1] for item in semester_tuple_list]
    return semester_list


def get_elective_codes_and_names_by_semester(semester):
    # TODO: Сделать запрос к БД, взять список элективов (и их коды) в выбранном семестре
    semester_tuple = (semester[:4], semester[-1:-6])

    elective_tuple_list = [(i, i + 1) for i in range(199)]  # Генерация данных

    elective_code_and_name_lists = list(zip(*elective_tuple_list))
    elective_code_list = list(map(str, elective_code_and_name_lists[0]))
    elective_name_list = list(map(str, elective_code_and_name_lists[1]))
    return elective_code_list, elective_name_list


def get_statistics_by_elective_code(code):
    # TODO: Сделать запрос к БД, взять статистику об выбранном элективе по его коду
    average_grade = 4.45  # Генерация данных
    average_priority = 2.2  # Генерация данных
    prioritization = [2, 6, 7, 7, 3]  # Генерация данных
    prioritization_by_grades_1d = [0, 0, 2, 2, 0, 1, 0, 2, 1, 1, 1, 5, 3, 0, 1, 0, 1, 0, 4, 1]  # Генерация данных

    prioritization_by_grades_2d = [[prioritization_by_grades_1d[i:i + 5:] for i in range(0, 4 * 5, 5)]]

    statistics = {
        'average_grade': average_grade,
        'average_priority': average_priority,
        'prioritization': prioritization,
        'prioritization_by_grades': prioritization_by_grades_2d
    }
    return statistics
