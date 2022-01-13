from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import RiseInTransition, SlideTransition, NoTransition

import database_access
from components import IconButton, MenuButton
from extended_screen_manager import ExtendedScreenManager

Builder.load_file('screens/start_menu.kv')
Builder.load_file('screens/main_app.kv')
Builder.load_file('components.kv')

Builder.load_file('screens/list_of_current_semester.kv')
Builder.load_file('screens/elective_card.kv')
Builder.load_file('screens/list_of_semesters.kv')
Builder.load_file('screens/list_of_selected_semester.kv')
Builder.load_file('screens/statistics.kv')
Builder.load_file('screens/algorithm.kv')

Builder.load_file('screens/authentication.kv')
Builder.load_file('screens/student_menu.kv')
Builder.load_file('screens/list_of_selected_day.kv')
Builder.load_file('screens/priorities.kv')

Window.size = 1280, 720
Window.minimum_width = 800
Window.minimum_height = 600
Window.clearcolor = 242 / 255, 242 / 255, 242 / 255, 255 / 255


class ListOfCurrentSemester(BoxLayout):
    def __init__(self, **kwargs):
        super(ListOfCurrentSemester, self).__init__(**kwargs)
        Clock.schedule_once(self._init_recycle_view)

    def _init_recycle_view(self, dt):
        elective_info_list = database_access.get_current_electives_info()
        self.recycleView.data = [
            {'line_button.code': str(elective_info_list[0][i]),
             'name.text': str(elective_info_list[1][i]),
             'hours.text': str(elective_info_list[2][i]),
             'capacity.text': str(elective_info_list[3][i]),
             'line_open_button.size': (0, 0),
             'line_button.text': 'Редактировать',
             'line_button.root': self}
            for i in range(len(elective_info_list[0]))]

    @staticmethod
    def statistics_button_click():
        screen_manager.display_screen('list_of_semesters',
                                      transition=SlideTransition(),
                                      direction='left')
        Window.set_system_cursor('arrow')

    @staticmethod
    def line_button_callback(button):
        elective_card_screen = screen_manager.get_screen('elective_card')
        screen_manager.display_screen(elective_card_screen,
                                      transition=SlideTransition(),
                                      direction='left')
        Window.set_system_cursor('arrow')

        elective_code = button.code
        elective_info = database_access.get_info_by_elective_code(elective_code)
        elective_card_screen.children[0].fill_card_with_info(elective_info)
        elective_card_screen.children[0].change_text_input_to(False)


class ElectiveCard(BoxLayout):
    def __init__(self, **kwargs):
        super(ElectiveCard, self).__init__(**kwargs)
        self.back_list_name = 'list_of_current_semester'

    def fill_card_with_info(self, info):
        self.ids.name.text = info['name']
        self.ids.code.text = info['code']
        self.ids.hours.text = info['hours']
        self.ids.max_students.text = info['capacity']
        self.ids.in_charge.text = info['in_charge']
        self.ids.author.text = info['author']
        self.ids.annotation.text = info['annotation']
        self.ids.footer.text = 'Создан черновик: {0} | Отправлено на согласование: {0} | Опубликован: {0} ({1})' \
            .format(info['footer_date'], info['author'])

    def change_text_input_to(self, readonly: bool):
        if readonly:
            self.back_list_name = 'list_of_selected_day'
        else:
            self.back_list_name = 'list_of_current_semester'

        self.ids.name.readonly = readonly
        self.ids.code.readonly = readonly
        self.ids.hours.readonly = readonly
        self.ids.max_students.readonly = readonly
        self.ids.in_charge.readonly = readonly
        self.ids.author.readonly = readonly
        self.ids.annotation.readonly = readonly
        self.ids.footer.readonly = readonly

    @staticmethod
    def save_elective_info():
        elective_card = screen_manager.get_screen('elective_card').children[0]
        elective_info = {
            'code': elective_card.ids.code,
            'name': elective_card.ids.name,
            'hours': elective_card.ids.hours,
            'capacity': elective_card.ids.max_students,
            'in_charge': elective_card.ids.in_charge,
            'author': elective_card.ids.author,
            'annotation': elective_card.ids.annotation,
            'footer_date': elective_card.ids.footer
        }

        database_access.set_info_by_elective_code(elective_info)

    def back_to_list(self):
        back_list = screen_manager.get_screen(self.back_list_name)
        screen_manager.display_screen(back_list,
                                      transition=SlideTransition(),
                                      direction='right')
        Window.set_system_cursor('arrow')


class ListOfSemesters(BoxLayout):
    def __init__(self, **kwargs):
        super(ListOfSemesters, self).__init__(**kwargs)
        Clock.schedule_once(self._init_recycle_view)

    def _init_recycle_view(self, dt):
        semester_name_list = database_access.get_semesters()
        self.recycleView.data = [{
            'line_button.code': semester_name_list[i],
            'name.text': semester_name_list[i],
            'line_open_button.size': (0, 0),
            'line_button.text': 'Открыть',
            'line_button.root': self
        } for i in range(len(semester_name_list))]

    @staticmethod
    def line_button_callback(button):
        list_of_selected_semester_screen = screen_manager.get_screen('list_of_selected_semester')
        screen_manager.display_screen(list_of_selected_semester_screen,
                                      transition=SlideTransition(),
                                      direction='left')
        Window.set_system_cursor('arrow')

        semester = button.code
        list_of_selected_semester_screen.children[0].fill_list_of_selected_semester(semester)


class ListOfSelectedSemester(BoxLayout):
    def fill_list_of_selected_semester(self, semester):
        self.ids.title.text = semester
        elective_info_list = database_access.get_electives_info_by_semester(semester)
        self.ids.recycleView.data = [
            {'line_button.code': str(elective_info_list[0][i]),
             'name.text': str(elective_info_list[1][i]),
             'hours.text': str(elective_info_list[2][i]),
             'capacity.text': str(elective_info_list[3][i]),
             'line_open_button.size': (0, 0),
             'line_button.text': 'Открыть',
             'line_button.root': self}
            for i in range(len(elective_info_list[0]))]

    @staticmethod
    # Перемещает фокус на экран статистики и заполняет его
    def line_button_callback(button):
        statistics_screen = screen_manager.get_screen('statistics')
        screen_manager.display_screen(statistics_screen,
                                      transition=SlideTransition(),
                                      direction='left')
        Window.set_system_cursor('arrow')

        elective_code = button.code
        elective_statistics = database_access.get_statistics_by_elective_code(elective_code)
        statistics_screen.children[0].fill_statistics(elective_statistics)

    @staticmethod
    def back_to_list():
        screen_manager.display_screen('list_of_semesters',
                                      transition=SlideTransition(),
                                      direction='right')
        Window.set_system_cursor('arrow')


class Statistics(BoxLayout):
    def fill_statistics(self, statistics):
        # self.ids.title.text = str(statistics['name'])

        self.ids.average_score.text = str(statistics['average_grade'])
        self.ids.average_priority.text = str(statistics['average_priority'])

        self.ids.first.text = str(statistics['prioritization'][0])
        self.ids.second.text = str(statistics['prioritization'][1])
        self.ids.third.text = str(statistics['prioritization'][2])
        self.ids.fourth.text = str(statistics['prioritization'][3])
        self.ids.fifth.text = str(statistics['prioritization'][4])

    @staticmethod
    def back_to_list():
        screen_manager.display_screen('list_of_selected_semester',
                                      transition=SlideTransition(),
                                      direction='right')
        Window.set_system_cursor('arrow')


class Algorithm(RelativeLayout):
    @staticmethod
    def start_distribution():
        # TODO: Добавить запуск алгортима распределения
        pass


class StudentMenu(BoxLayout):
    def __init__(self, **kwargs):
        super(StudentMenu, self).__init__(**kwargs)

    @staticmethod
    def open_list_screen(button):
        labels_list = screen_manager.get_screen('priorities').children[0].list_of_labels
        list_of_selected_day_screen = screen_manager.get_screen('list_of_selected_day')
        for i in range(len(labels_list)):
            if labels_list[i].text == "":
                screen_manager.display_screen(list_of_selected_day_screen,
                                              transition=SlideTransition(),
                                              direction='left')
                button.disabled = True

                ListOfSelectedDay.fill_list_of_selected_day(list_of_selected_day_screen.children[0])
                break


class ListOfSelectedDay(BoxLayout):
    @staticmethod
    def fill_list_of_selected_day(list_of_electives):
        elective_info_list = database_access.get_current_electives_info()
        list_of_electives.ids.recycleView.data = [
            {'line_open_button.code': str(elective_info_list[0][i]),
             'line_button.code': str(elective_info_list[0][i]),
             'name.text': str(elective_info_list[1][i]),
             'hours.text': str(elective_info_list[2][i]),
             'capacity.text': str(elective_info_list[3][i]),
             'line_button.text': 'Описание',
             'line_button.root': list_of_electives,
             'line_open_button.root': list_of_electives}
            for i in range(len(elective_info_list[0]))]

    @staticmethod
    def line_button_callback(button):
        elective_card_screen = screen_manager.get_screen('elective_card')
        screen_manager.display_screen(elective_card_screen,
                                      transition=SlideTransition(),
                                      direction='left')
        Window.set_system_cursor('arrow')

        elective_code = button.code
        elective_info = database_access.get_info_by_elective_code(elective_code)
        elective_card_screen.children[0].fill_card_with_info(elective_info)
        elective_card_screen.children[0].change_text_input_to(True)

    @staticmethod
    def line_button2_callback(button):
        elective_code = button.code
        labels_list = screen_manager.get_screen('priorities').children[0].list_of_labels
        for i in range(len(labels_list)):
            if labels_list[i].text == '':
                labels_list[i].text = elective_code
                break
        ListOfSelectedDay.back_to_list()

    @staticmethod
    def back_to_list():
        screen_manager.display_screen('student_menu',
                                      transition=SlideTransition(),
                                      direction='right')
        Window.set_system_cursor('arrow')


class Priorities(BoxLayout):
    def __init__(self, **kwargs):
        super(Priorities, self).__init__(**kwargs)
        Clock.schedule_once(self._init_recycle_view)

    def _init_recycle_view(self, dt):
        self.list_of_labels = [
            self.ids.first_priority,
            self.ids.second_priority,
            self.ids.third_priority,
            self.ids.fourth_priority,
            self.ids.fifth_priority
        ]
        self.list_of_boxLayouts = [
            self.ids.firstLine,
            self.ids.secondLine,
            self.ids.thirdLine,
            self.ids.fourthLine,
            self.ids.fifthLine
        ]
        pass

    @staticmethod
    def button_down(button):
        list_of_priorities_screen = screen_manager.get_screen('priorities').children[0]
        for i in range(len(list_of_priorities_screen.list_of_boxLayouts)):
            if button.parent == list_of_priorities_screen.list_of_boxLayouts[i]:
                list_of_priorities_screen.list_of_labels[i].text, \
                list_of_priorities_screen.list_of_labels[i + 1].text = \
                    list_of_priorities_screen.list_of_labels[i + 1].text, \
                    list_of_priorities_screen.list_of_labels[i].text

    # TODO:сделать красиво через второй аргумент +-

    @staticmethod
    def button_up(button):
        list_of_priorities_screen = screen_manager.get_screen('priorities').children[0]
        for i in range(len(list_of_priorities_screen.list_of_boxLayouts)):
            if button.parent == list_of_priorities_screen.list_of_boxLayouts[i]:
                list_of_priorities_screen.list_of_labels[i].text, \
                list_of_priorities_screen.list_of_labels[i - 1].text = \
                    list_of_priorities_screen.list_of_labels[i - 1].text, \
                    list_of_priorities_screen.list_of_labels[i].text

    @staticmethod
    def delete_button(button):
        list_of_priorities_screen = screen_manager.get_screen('priorities').children[0]
        for i in range(len(list_of_priorities_screen.list_of_boxLayouts)):
            if button.parent == list_of_priorities_screen.list_of_boxLayouts[i]:
                list_of_priorities_screen.list_of_labels[i].text = ''


class StartMenuScreenManager(ExtendedScreenManager):
    pass


class StartMenu(RelativeLayout):
    @staticmethod
    def start_student(start_screen_manager):
        main_app = start_screen_manager.get_screen('main_app').children[0]
        StartMenu.add_menu_line(main_app,
                                'images/braindead_logo.png',
                                'Выбор элективов',
                                MainApp.student_menu_button_click)
        StartMenu.add_menu_line(main_app,
                                'images/braindead_logo.png',
                                'Приоритеты',
                                MainApp.priorities_button_click)
        main_app.ids.icon_box.add_widget(BoxLayout())
        main_app.ids.text_box.add_widget(BoxLayout())
        main_app.ids.screen_manager.display_screen('student_menu',
                                                   transition=NoTransition())
        StartMenu.change_to_main_app(start_screen_manager)

    @staticmethod
    def start_administrator(start_screen_manager):
        main_app = start_screen_manager.get_screen('main_app').children[0]
        StartMenu.add_menu_line(main_app,
                                'images/braindead_logo.png',
                                'Текущий семестр',
                                MainApp.list_of_current_semester_button_click)
        StartMenu.add_menu_line(main_app,
                                'images/braindead_logo.png',
                                'Статистика',
                                MainApp.statistics_button_click)
        StartMenu.add_menu_line(main_app,
                                'images/braindead_logo.png',
                                'Алгоритм',
                                MainApp.algorithm_button_click)
        main_app.ids.icon_box.add_widget(BoxLayout())
        main_app.ids.text_box.add_widget(BoxLayout())
        StartMenu.change_to_main_app(start_screen_manager)

    @staticmethod
    def add_menu_line(menu, icon_path, name, button_click):
        menu.ids.icon_box.add_widget(IconButton(icon=icon_path,
                                                size=(50, 50),
                                                on_release=button_click))
        menu.ids.text_box.add_widget(MenuButton(text=name,
                                                size_hint=(1, None),
                                                on_release=button_click))

    @staticmethod
    def change_to_main_app(start_screen_manager: ExtendedScreenManager):
        global screen_manager
        screen_manager = start_screen_manager.get_screen('main_app').children[0].ids.screen_manager
        start_screen_manager.display_screen('main_app',
                                            transition=RiseInTransition(clearcolor=Window.clearcolor))


class MainApp(BoxLayout):
    def list_of_current_semester_button_click(self):
        screen_manager.display_screen('list_of_current_semester',
                                      transition=RiseInTransition(clearcolor=Window.clearcolor))

    def statistics_button_click(self):
        screen_manager.display_screen('list_of_semesters',
                                      transition=RiseInTransition(clearcolor=Window.clearcolor))

    def algorithm_button_click(self):
        screen_manager.display_screen('algorithm',
                                      transition=RiseInTransition(clearcolor=Window.clearcolor))

    def student_menu_button_click(self):
        screen_manager.display_screen('student_menu',
                                      transition=RiseInTransition(clearcolor=Window.clearcolor))

    def priorities_button_click(self):
        screen_manager.display_screen('priorities',
                                      transition=RiseInTransition(clearcolor=Window.clearcolor))


screen_manager: ExtendedScreenManager


class BrainDeadApp(App):
    def build(self):
        self.title = '内部で死んでいる'
        return StartMenuScreenManager()


BrainDeadApp().run()
