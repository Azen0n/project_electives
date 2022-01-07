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

Builder.load_file('authentication_screen.kv')
Builder.load_file('student_menu.kv')

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
        screen_manager.display_screen('semester_list',
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
        # FIXME: Убрать обращение через children
        elective_card_screen.children[0].fill_card_with_info(elective_info)
        elective_card_screen.children[0].change_text_input_to(False)


class ElectiveCard(BoxLayout):
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

    def back_to_list(self):
        back_list = screen_manager.get_screen(self.back_list_name)
        screen_manager.display_screen(back_list,
                                      transition=SlideTransition(),
                                      direction='right')
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
        list_of_selected_semester_screen = screen_manager.get_screen('list_of_selected_semester')
        screen_manager.display_screen(list_of_selected_semester_screen,
                                      transition=SlideTransition(),
                                      direction='left')
        Window.set_system_cursor('arrow')

        semester = button.code
        # FIXME: Убрать обращение через children
        ListOfSelectedSemester.fill_list_of_selected_semester(list_of_selected_semester_screen.children[0], semester)

    @staticmethod
    def back_to_list():
        screen_manager.display_screen('list_of_current_semester',
                                      transition=SlideTransition(),
                                      direction='right')
        Window.set_system_cursor('arrow')


# FIXME: Объединить с SemestersList
class ListOfSelectedSemester(BoxLayout):
    @staticmethod
    def fill_list_of_selected_semester(list_of_electives, semester):
        list_of_electives.ids.title.text = semester
        elective_code_list, elective_name_list = database_access.get_elective_codes_and_names_by_semester(semester)
        list_of_electives.ids.recycleView.data = [
            {'line_button.code': elective_code_list[i],
             'line_label.text': elective_name_list[i],
             'line_button.text': 'Открыть',
             'line_button.root': list_of_electives}
            for i in range(len(elective_code_list))]

    @staticmethod
    # Перемещает фокус на экран статистики и заполняет его
    def line_button_callback(button):
        statistics_screen = screen_manager.get_screen('statistics')
        screen_manager.display_screen(statistics_screen,
                                      transition=SlideTransition(),
                                      direction='left')
        Window.set_system_cursor('arrow')

        elective_code = button.code
        # FIXME: Убрать обращение через children
        elective_ids = statistics_screen.children[0].ids
        elective_statistics = database_access.get_statistics_by_elective_code(elective_code)

    @staticmethod
    def back_to_list():
        screen_manager.display_screen('semester_list',
                                      transition=SlideTransition(),
                                      direction='right')
        Window.set_system_cursor('arrow')


class Statistics(BoxLayout):
    pass


class Menu(BoxLayout):
    @staticmethod
    def admin_menu_button_click():
        screen_manager.display_screen('list_of_current_semester',
                                      transition=RiseInTransition(clearcolor=Window.clearcolor))

    @staticmethod
    def student_menu_button_click():
        screen_manager.display_screen('student_menu',
                                      transition=RiseInTransition(clearcolor=Window.clearcolor))

    @staticmethod
    def list_of_priorities_button_click():
        screen_manager.display_screen('list_of_priorities',
                                      transition=RiseInTransition(clearcolor=Window.clearcolor))


class StudentMenu(BoxLayout):
    def __init__(self, **kwargs):
        super(StudentMenu, self).__init__(**kwargs)
        self.button_afraided_of_being_banned = 'just some text to be var element'

    @staticmethod
    def open_list_screen(button):
        labels_list = screen_manager.get_screen('list_of_priorities').children[0].list_of_labels
        list_of_selected_day_screen = screen_manager.get_screen('list_of_selected_day')
        for i in range(len(labels_list)):
            if labels_list[i].text == "":
                screen_manager.display_screen(list_of_selected_day_screen,
                                              transition=SlideTransition(),
                                              direction='left')
                StudentMenu.button_afraided_of_being_banned = button
                # FIXME: Убрать обращение через children
                ListOfSelectedDay.fill_list_of_selected_day(list_of_selected_day_screen.children[0])
                break


# FIXME: Объединить с SemestersList
class ListOfSelectedDay(BoxLayout):

    @staticmethod
    def fill_list_of_selected_day(list_of_electives):
        # list_of_electives.ids.title.text = day
        elective_code_list, elective_name_list = database_access.get_current_elective_codes_and_names()
        list_of_electives.ids.recycleView.data = [
            {'line_button.code': elective_code_list[i],
             'line_button2.code': elective_code_list[i],
             'line_label.text': elective_name_list[i],
             'line_button.text': 'Описание',
             'line_button2.text': 'Добавить',
             'line_button.root': list_of_electives,
             'line_button2.root': list_of_electives}
            for i in range(len(elective_code_list))]

    @staticmethod
    def block_button():
        StudentMenu.button_afraided_of_being_banned.disabled = True

    @staticmethod
    def line_button_callback(button):
        elective_card_screen = screen_manager.get_screen('elective_card')
        screen_manager.display_screen(elective_card_screen,
                                      transition=SlideTransition(),
                                      direction='left')
        Window.set_system_cursor('arrow')
        elective_code = button.code
        elective_info = database_access.get_info_by_elective_code(elective_code)
        # FIXME: Убрать обращение через children
        elective_card_screen.children[0].fill_card_with_info(elective_info)
        elective_card_screen.children[0].change_text_input_to(True)

    @staticmethod
    def line_button2_callback(button):
        elective_code = button.code
        labels_list = screen_manager.get_screen('list_of_priorities').children[0].list_of_labels

        for i in range(len(labels_list)):
            if labels_list[i].text == '':
                labels_list[i].text = elective_code
                ListOfSelectedDay.block_button()
                break
        ListOfSelectedDay.back_to_list()

    @staticmethod
    def back_to_list():
        screen_manager.display_screen('student_menu',
                                      transition=SlideTransition(),
                                      direction='right')
        Window.set_system_cursor('arrow')


class ListOfPriorities(BoxLayout):
    def __init__(self, **kwargs):
        super(ListOfPriorities, self).__init__(**kwargs)
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
        list_of_priorities_screen = screen_manager.get_screen('list_of_priorities').children[0]
        for i in range(len(list_of_priorities_screen.list_of_boxLayouts)):
            if button.parent == list_of_priorities_screen.list_of_boxLayouts[i]:
                list_of_priorities_screen.list_of_labels[i].text, \
                list_of_priorities_screen.list_of_labels[i + 1].text = \
                    list_of_priorities_screen.list_of_labels[i + 1].text, \
                    list_of_priorities_screen.list_of_labels[i].text

    # TODO:сделать красиво через второй аргумент +-

    @staticmethod
    def button_up(button):
        list_of_priorities_screen = screen_manager.get_screen('list_of_priorities').children[0]
        for i in range(len(list_of_priorities_screen.list_of_boxLayouts)):
            if button.parent == list_of_priorities_screen.list_of_boxLayouts[i]:
                list_of_priorities_screen.list_of_labels[i].text, \
                list_of_priorities_screen.list_of_labels[i - 1].text = \
                    list_of_priorities_screen.list_of_labels[i - 1].text, \
                    list_of_priorities_screen.list_of_labels[i].text

    @staticmethod
    def delete_button(button):
        list_of_priorities_screen = screen_manager.get_screen('list_of_priorities').children[0]
        for i in range(len(list_of_priorities_screen.list_of_boxLayouts)):
            if button.parent == list_of_priorities_screen.list_of_boxLayouts[i]:
                list_of_priorities_screen.list_of_labels[i].text = ''


class BrainDeadApp(App):
    def build(self):
        self.title = '内部で死んでいる'
        self.icon = 'images/braindead_logo.png'
        global screen_manager
        screen_manager = self.root.ids.screen_manager


BrainDeadApp().run()
