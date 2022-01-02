import components
import database_access
from extended_screen_manager import ExtendedScreenManager
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import RiseInTransition, SlideTransition

Builder.load_file('administrator_menu.kv')
Builder.load_file('elective_card.kv')
Builder.load_file('statistics.kv')
Builder.load_file('list_line.kv')

Window.size = 1280, 720
Window.minimum_width = 800
Window.minimum_height = 600
Window.clearcolor = 0.98, 0.98, 0.98, 1

screen_manager: ExtendedScreenManager


class AdminMenu(BoxLayout):
    def __init__(self, **kwargs):
        super(AdminMenu, self).__init__(**kwargs)
        Clock.schedule_once(self._init_recycle_view)

    def _init_recycle_view(self, dt):
        elective_code_list, elective_name_list = database_access.get_current_elective_codes_and_names()
        self.recycleView.data = [
            {'line_button.code': elective_code_list[i],
             'line_label.text': elective_name_list[i],
             'line_button.text': 'Редактировать',
             'line_button.root': self}
            for i in range(len(elective_code_list))]

    @staticmethod
    def statistics_button_click():
        screen_manager.display_screen('semester_list', transition=SlideTransition(), direction='left')
        Window.set_system_cursor('arrow')

    @staticmethod
    def line_button_callback(button):
        elective_card_screen = screen_manager.get_screen('elective_card')
        screen_manager.display_screen(elective_card_screen, transition=SlideTransition(), direction='left')
        Window.set_system_cursor('arrow')

        elective_code = button.code
        elective_info = database_access.get_info_by_elective_code(elective_code)
        # FIXME: Убрать обращение через children
        ElectiveCard.fill_card_with_info(elective_card_screen.children[0], elective_info)


class ElectiveCard(BoxLayout):
    @staticmethod
    def fill_card_with_info(card, info):
        card.ids.name.text = info['name']
        card.ids.code.text = info['code']
        card.ids.hours.text = info['hours']
        card.ids.max_students.text = info['capacity']
        card.ids.in_charge.text = info['in_charge']
        card.ids.author.text = info['author']
        card.ids.annotation.text = info['annotation']
        card.ids.footer.text = 'Создан черновик: {0} | Отправлено на согласование: {0} | Опубликован: {0} ({1})' \
            .format(info['footer_date'], info['author'])

    @staticmethod
    def save_elective_info():
        kek = screen_manager.get_screen('elective_card')
        elective_card = kek.ids.elective_card
        elective_info = {
            'code': elective_card.ids.code,
            'name': elective_card.ids.name,
            'hours': elective_card.ids.hours,
            'capacity': elective_card.ids.max_students,
            'in_charge': elective_card.ids.in_charge,
            'author': elective_card.ids.author,
            'annotation': elective_card.ids.annotation,
            'footer_data': elective_card.ids.footer
        }

        database_access.set_info_by_elective_code(elective_info)

    @staticmethod
    def back_to_list():
        screen_manager.display_screen('admin_menu', transition=SlideTransition(), direction='right')
        Window.set_system_cursor('arrow')


class SemesterList(BoxLayout):
    def __init__(self, **kwargs):
        super(SemesterList, self).__init__(**kwargs)
        Clock.schedule_once(self._init_recycle_view)

    def _init_recycle_view(self, dt):
        semester_name_list = database_access.get_semesters()
        self.recycleView.data = [{
            'line_button.code': semester_name_list[i],
            'line_label.text': semester_name_list[i],
            'line_button.text': 'Открыть',
            'line_button.root': self
        } for i in range(len(semester_name_list))]

    @staticmethod
    def line_button_callback(button):
        elective_list_screen = screen_manager.get_screen('elective_list')
        screen_manager.display_screen(elective_list_screen, transition=SlideTransition(), direction='left')
        Window.set_system_cursor('arrow')

        semester = button.code
        # FIXME: Убрать обращение через children
        ElectiveList.fill_elective_list_by_semester(elective_list_screen.children[0], semester)

    @staticmethod
    def back_to_list():
        screen_manager.display_screen('admin_menu', transition=SlideTransition(), direction='right')
        Window.set_system_cursor('arrow')


# FIXME: Объединить с SemestersList
class ElectiveList(BoxLayout):
    @staticmethod
    def fill_elective_list_by_semester(elective_list, semester):
        elective_list.ids.title.text = semester
        elective_code_list, elective_name_list = database_access.get_elective_codes_and_names_by_semester(semester)
        elective_list.ids.recycleView.data = [
            {'line_button.code': elective_code_list[i],
             'line_label.text': elective_name_list[i],
             'line_button.text': 'Открыть',
             'line_button.root': elective_list}
            for i in range(len(elective_code_list))]

    @staticmethod
    # Перемещает фокус на экран статистики и заполняет его
    def line_button_callback(button):
        statistics_screen = screen_manager.get_screen('statistics')
        screen_manager.display_screen(statistics_screen, transition=SlideTransition(), direction='left')
        Window.set_system_cursor('arrow')

        elective_code = button.code
        # FIXME: Убрать обращение через children
        elective_ids = statistics_screen.children[0].ids
        elective_statistics = database_access.get_statistics_by_elective_code(elective_code)

    @staticmethod
    def back_to_list():
        screen_manager.display_screen('semester_list', transition=SlideTransition(), direction='right')
        Window.set_system_cursor('arrow')


class Statistics(BoxLayout):
    pass


class Menu(BoxLayout):
    @staticmethod
    def admin_menu_button_click():
        screen_manager.display_screen('admin_menu', transition=RiseInTransition(clearcolor=Window.clearcolor))


class BrainDeadApp(App):
    def build(self):
        self.title = '内部で死んでいる'
        self.icon = 'images/braindead_logo.png'
        global screen_manager
        screen_manager = self.root.ids.screen_manager


BrainDeadApp().run()
