import components
import database_access
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

# region Builder Loading Files
Builder.load_file('administrator_menu.kv')
Builder.load_file('elective_card.kv')
Builder.load_file('statistics.kv')
Builder.load_file('list_line.kv')
# endregion

# region Window Settings
Window.size = 1280, 720
Window.minimum_width, Window.minimum_height = 800, 600
Window.clearcolor = 0.98, 0.98, 0.98, 1


# endregion


class AdminMenu(BoxLayout):
    def __init__(self):
        super(AdminMenu, self).__init__()

        elective_code_list, elective_name_list = database_access.get_current_elective_codes_and_names()
        self.recycleView.data = [
            {'code': elective_code_list[i],
             'line_label.text': elective_name_list[i],
             'line_button.text': 'Редактировать',
             'line_button.root': self}
            for i in range(len(elective_code_list))]

    @staticmethod
    def statistics_button_click():
        screen_manager.switch_to(semester_list_screen, direction='left')
        Window.set_system_cursor('arrow')

    @staticmethod
    def line_button_callback(button):
        screen_manager.switch_to(elective_screen, direction='left')
        Window.set_system_cursor('arrow')
        AdminMenu.fill_elective_fields(button)

    @staticmethod
    def fill_elective_fields(button):
        elective_code = button.parent.code
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
        screen_manager.switch_to(admin_menu_srceen, direction='right')


class SemestersList(BoxLayout):
    def __init__(self):
        super(SemestersList, self).__init__()

        semester_name_list = database_access.get_semesters()
        self.recycleView.data = [
            {'code': semester_name_list[i],
             'line_label.text': semester_name_list[i],
             'line_button.text': 'Открыть',
             'line_button.root': self}
            for i in range(len(semester_name_list))]

    @staticmethod
    def line_button_callback(button):
        screen_manager.switch_to(elective_list_screen, direction='left')
        Window.set_system_cursor('arrow')
        SemestersList.fill_elective_list(button)

    @staticmethod
    def fill_elective_list(button):
        # FIXME: Убрать обращение через parent
        semester_name = button.parent.children[1].text
        # FIXME: Убрать обращение через children
        elective_list = elective_list_screen.children[0]
        elective_list.ids.title.text = semester_name

        ElectivesList.fill_elective_list_by_semester(elective_list, semester_name)

    @staticmethod
    def back_to_list():
        screen_manager.switch_to(admin_menu_srceen, direction='right')


# FIXME: Объединить с SemestersList
class ElectivesList(BoxLayout):
    @staticmethod
    def fill_elective_list_by_semester(elective_list, semester_name):
        elective_code_list, elective_name_list = database_access.get_elective_codes_and_names_by_semester(semester_name)
        elective_list.ids.recycleView.data = [
            {'code': elective_code_list[i],
             'line_label.text': elective_name_list[i],
             'line_button.text': 'Открыть',
             'line_button.root': elective_list}
            for i in range(len(elective_code_list))]

    @staticmethod
    def line_button_callback(button):
        screen_manager.switch_to(statistics_screen, direction='left')
        Window.set_system_cursor('arrow')
        ElectivesList.fill_statistics(button)

    @staticmethod
    def fill_statistics(button):
        elective_code = button.parent.code
        # FIXME: Убрать обращение через children
        elective_ids = statistics_screen.children[0].ids

        elective_statistics = database_access.get_statistics_by_elective_code(elective_code)

    @staticmethod
    def back_to_list():
        screen_manager.switch_to(semester_list_screen, direction='right')


class Statistics(BoxLayout):
    pass


# region ScreenManager Initialize

screen_manager = ScreenManager()
admin_menu_srceen = Screen(name='admin_menu')
elective_screen = Screen(name='elective')
semester_list_screen = Screen(name='semesters_list')
elective_list_screen = Screen(name='electives_list')
statistics_screen = Screen(name='statistics')
admin_menu_srceen.add_widget(AdminMenu())
elective_screen.add_widget(ElectiveCard())
semester_list_screen.add_widget(SemestersList())
elective_list_screen.add_widget(ElectivesList())
statistics_screen.add_widget(Statistics())
screen_manager.add_widget(admin_menu_srceen)
screen_manager.add_widget(elective_screen)
screen_manager.add_widget(semester_list_screen)
screen_manager.add_widget(elective_list_screen)
screen_manager.add_widget(statistics_screen)


# endregion

class KivyApp(App):
    def build(self):
        self.title = '内部で死んでいる'
        self.icon = 'images/braindead_logo.png'

        return screen_manager


KivyApp().run()
