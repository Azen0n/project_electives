import components
import database_access
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

# region Builder Loading Files
from kivy.lang import Builder

Builder.load_file('administrator_menu.kv')
Builder.load_file('elective_card.kv')
Builder.load_file('statistics.kv')
Builder.load_file('list_line.kv')
# endregion

# region Window Settings
from kivy.core.window import Window

Window.size = 1280, 720
Window.minimum_width, Window.minimum_height = 800, 600
Window.clearcolor = 0.98, 0.98, 0.98, 1
# endregion

# region ScreenManager Initialize
from kivy.uix.screenmanager import ScreenManager, Screen

screen_manager = ScreenManager()
menu_screen = Screen(name='menu')
elective_screen = Screen(name='elective')
semesters_list_screen = Screen(name='semesters_list')
electives_list_screen = Screen(name='electives_list')
statistics_screen = Screen(name='statistics')
screen_manager.add_widget(menu_screen)
screen_manager.add_widget(elective_screen)
screen_manager.add_widget(semesters_list_screen)
screen_manager.add_widget(electives_list_screen)
screen_manager.add_widget(statistics_screen)


# endregion


class AdministrativeMenu(BoxLayout):
    def __init__(self):
        super(AdministrativeMenu, self).__init__()

        elective_code_list, elective_name_list = database_access.get_current_elective_codes_and_names()
        self.recycleView.data = [
            {'code': elective_code_list[i],
             'line_label.text': elective_name_list[i],
             'line_button.text': 'Редактировать',
             'line_button.on_press': AdministrativeMenu.edit_button_click}
            for i in range(len(elective_code_list))]

    @staticmethod
    def statistics_button_click():
        screen_manager.current = 'semesters_list'
        screen_manager.transition.direction = 'left'
        Window.set_system_cursor('arrow')

    # FIXME: Добавить аргумент button
    @staticmethod
    def edit_button_click():
        screen_manager.current = 'elective'
        screen_manager.transition.direction = 'left'
        Window.set_system_cursor('arrow')
        # AdministrativeMenu.fill_elective_fields(button)

    @staticmethod
    def fill_elective_fields(button):
        elective_code = button.parent.elective_code
        # FIXME: Убрать обращение через children
        elective_ids = elective_screen.children[0].ids

        elective_info = database_access.get_info_by_elective_code(elective_code)


class ElectiveCard(BoxLayout):
    @staticmethod
    def save_elective(button):
        # FIXME: Убрать обращение через parent
        elective_ids = button.parent.parent.ids
        elective_info = dict()
        elective_info['code'] = elective_ids.code
        elective_info['name'] = elective_ids.name
        elective_info['hours'] = elective_ids.hours
        elective_info['max_students'] = elective_ids.max_students
        elective_info['in_charge'] = elective_ids.in_charge
        elective_info['author'] = elective_ids.author
        elective_info['footer'] = elective_ids.footer

        database_access.set_info_by_elective_code(elective_info)

    @staticmethod
    def back_to_list():
        screen_manager.current = 'menu'
        screen_manager.transition.direction = 'right'


class SemestersList(BoxLayout):
    def __init__(self):
        super(SemestersList, self).__init__()

        semester_name_list = database_access.get_semesters()
        self.recycleView.data = [
            {'code': semester_name_list[i],
             'line_label.text': semester_name_list[i],
             'line_button.text': 'Открыть',
             'line_button.on_press': SemestersList.open_button_click}
            for i in range(len(semester_name_list))]

    # FIXME: Добавить аргумент button
    @staticmethod
    def open_button_click():
        screen_manager.current = 'electives_list'
        screen_manager.transition.direction = 'left'
        Window.set_system_cursor('arrow')
        # SemestersList.fill_electives_list(button)

    @staticmethod
    def fill_electives_list(button):
        # FIXME: Убрать обращение через parent
        semester_name = button.parent.children[1].text
        # FIXME: Убрать обращение через screens
        electives_list_ids = screen_manager.screens[3].children[0].ids
        electives_list_ids.title.text = semester_name

        elective_code_list, elective_name_list = database_access.get_elective_codes_and_names_by_semester(semester_name)
        electives_list_ids.recycleView.data = [
            {'code': elective_code_list[i],
             'line_label.text': elective_name_list[i],
             'line_button.text': 'Открыть',
             'line_button.on_press': SemestersList.open_button_click}
            for i in range(len(elective_code_list))]

    @staticmethod
    def back_to_list():
        screen_manager.current = 'menu'
        screen_manager.transition.direction = 'right'


# FIXME: Объединить с SemestersList
class ElectivesList(BoxLayout):
    # FIXME: Добавить аргумент button
    @staticmethod
    def open_button_click():
        screen_manager.current = 'statistics'
        screen_manager.transition.direction = 'left'
        Window.set_system_cursor('arrow')
        # ElectivesList.fill_statistics(button)

    @staticmethod
    def fill_statistics(button):
        elective_code = button.parent.elective_code
        # FIXME: Убрать обращение через screens
        elective_ids = screen_manager.screens[4].children[0].ids

        elective_statistics = database_access.get_statistics_by_elective_code(elective_code)

    @staticmethod
    def back_to_list():
        screen_manager.current = 'semesters_list'
        screen_manager.transition.direction = 'right'


class Statistics(BoxLayout):
    pass


class KivyApp(App):
    def build(self):
        self.title = '内部で死んでいる'
        self.icon = 'images/braindead_logo.png'

        menu_screen.add_widget(AdministrativeMenu())
        elective_screen.add_widget(ElectiveCard())
        semesters_list_screen.add_widget(SemestersList())
        electives_list_screen.add_widget(ElectivesList())
        statistics_screen.add_widget(Statistics())
        return screen_manager


KivyApp().run()
