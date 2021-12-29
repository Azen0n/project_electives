def get_current_elective_codes_and_names():
    # TODO: Сделать запрос к БД, взять список элективов (и их коды) в текущем семестре
    elective_code_list = [str(i) for i in range(199)]
    elective_name_list = [str(i) for i in range(1, 200)]
    return elective_code_list, elective_name_list


def get_info_by_elective_code(code):
    # TODO: Сделать запрос к БД, взять информацию об элективе по его коду
    info = dict()
    return info


def set_info_by_elective_code(info):
    # TODO: Сделать запрос к БД, отдать измененые данные
    pass


def get_semesters():
    # TODO: Сделать запрос к БД, взять список семестров
    semester_list = [str(i) for i in range(1, 20)]
    return semester_list


def get_elective_codes_and_names_by_semester(semester):
    # TODO: Сделать запрос к БД, взять список элективов (и их коды) в выбранном семестре
    elective_code_list = [str(i) for i in range(199)]
    elective_name_list = [str(i) for i in range(1, 200)]
    return elective_code_list, elective_name_list


def get_statistics_by_elective_code(code):
    # TODO: Сделать запрос к БД, взять статистику об выбранном элективе по его коду
    statistics = dict()
    return statistics
