from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ButtonBehavior

from kivy.lang import Builder

Builder.load_file('administrator_menu.kv')
Builder.load_file('elective_card.kv')
Builder.load_file('statistics.kv')
Builder.load_file('lines_list.kv')

from kivy.core.window import Window

Window.size = 1280, 720
Window.minimum_width, Window.minimum_height = 800, 600
Window.clearcolor = 0.98, 0.98, 0.98, 1

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


class AdministrativeMenu(ScrollView):
    def __init__(self):
        super(AdministrativeMenu, self).__init__()

        # TODO: Сделать запрос к БД, взять список элективов (и их коды) в текущем семестре
        list_of_elective_names = [str(i) for i in range(1, 20)]
        list_of_elective_codes = [str(i) for i in range(19)]
        elective_dictionary = dict(zip(list_of_elective_codes, list_of_elective_names))
        self.ids.box_layout.add_widget(LinesList(elective_dictionary,
                                                 'Редактировать',
                                                 AdministrativeMenu.edit_button_click))

    @staticmethod
    def statistics_button_click():
        screen_manager.current = 'semesters_list'
        screen_manager.transition.direction = 'left'
        Window.set_system_cursor('arrow')

    @staticmethod
    def edit_button_click(button):
        screen_manager.current = 'elective'
        screen_manager.transition.direction = 'left'
        Window.set_system_cursor('arrow')
        AdministrativeMenu.fill_elective_fields(button)

    @staticmethod
    def fill_elective_fields(button):
        elective_code = button.parent.elective_code

        # TODO: Сделать запрос к БД, взять информацию об элективе по его коду
        elective_ids = elective_screen.children[0].ids
        elective_ids.title.text = ''
        elective_ids.code.text += ''
        elective_ids.hours.text += ''
        elective_ids.max_students.text += ''
        elective_ids.in_charge.text += ''
        elective_ids.author.text += ''
        elective_ids.annotation.text += ''
        elective_ids.footer.text += ''


class LinesList(BoxLayout):
    def __init__(self, objects, button_text, button_click):
        super(LinesList, self).__init__()

        if type(objects) == dict:
            for item in objects.items():
                self.add_widget(ListLine(item, button_text, button_click))
        else:
            for i in objects:
                self.add_widget(ListLine(i, button_text, button_click))


class ListLine(BoxLayout):
    def __init__(self, item, button_text, button_click):
        super(ListLine, self).__init__()
        if type(item) == tuple:
            self.elective_code = item[0]
            self.ids.line_label.text = item[1]
        else:
            self.ids.line_label.text = item
        self.ids.line_button.text = button_text
        self.ids.line_button.bind(on_press=button_click)


class HoverBehavior(object):
    hovered = False
    border_point = None

    def __init__(self):
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(HoverBehavior, self).__init__()

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return
        pos = args[1]
        inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            return
        self.border_point = pos
        self.hovered = inside
        if inside:
            self.dispatch('on_enter')
        else:
            self.dispatch('on_leave')


class HoverButton(Button, HoverBehavior):
    @staticmethod
    def on_enter():
        Window.set_system_cursor('hand')

    @staticmethod
    def on_leave():
        Window.set_system_cursor('arrow')


class ElectiveTextInput(TextInput):
    max_length = 50

    def insert_text(self, substring, from_undo=False):
        if len(self.text) < self.max_length:
            return super().insert_text(substring, from_undo=from_undo)


class ImageButton(ButtonBehavior, Image):
    pass


class ElectiveCard(BoxLayout):
    @staticmethod
    def save_elective(button):
        elective_ids = button.parent.parent.ids
        # TODO: Сделать запрос к БД, отдать измененые данные

    @staticmethod
    def back_to_list():
        screen_manager.current = 'menu'
        screen_manager.transition.direction = 'right'


class SemestersList(ScrollView):
    def __init__(self):
        super(SemestersList, self).__init__()

        # TODO: Сделать запрос к БД, взять список семестров
        list_of_semesters = [str(i) for i in range(1, 20)]
        self.ids.box_layout.add_widget(LinesList(list_of_semesters,
                                                 'Открыть',
                                                 SemestersList.open_button_click))

    @staticmethod
    def open_button_click(button):
        screen_manager.current = 'electives_list'
        screen_manager.transition.direction = 'left'
        Window.set_system_cursor('arrow')
        SemestersList.fill_electives_list(button)

    @staticmethod
    def fill_electives_list(button):
        semester_name = button.parent.children[1].text
        electives_list_ids = screen_manager.screens[3].children[0].ids
        electives_list_ids.title.text = semester_name

        # TODO: Сделать запрос к БД, взять список элективов (и их коды) в выбранном семестре
        list_of_elective_names = [str(i) for i in range(1, 20)]
        list_of_elective_codes = [str(i) for i in range(19)]
        elective_dictionary = dict(zip(list_of_elective_codes, list_of_elective_names))
        if len(electives_list_ids.box_layout.children) > 1:
            electives_list_ids.box_layout.remove_widget(electives_list_ids.box_layout.children[0])
        electives_list_ids.box_layout.add_widget(LinesList(elective_dictionary,
                                                           'Открыть',
                                                           ElectivesList.open_button_click))

    @staticmethod
    def back_to_list():
        screen_manager.current = 'menu'
        screen_manager.transition.direction = 'right'


class ElectivesList(ScrollView):
    @staticmethod
    def open_button_click(button):
        screen_manager.current = 'statistics'
        screen_manager.transition.direction = 'left'
        Window.set_system_cursor('arrow')
        ElectivesList.fill_statistics(button)

    @staticmethod
    def fill_statistics(button):
        elective_code = button.parent.elective_code

        # TODO: Сделать запрос к БД, взять статистику об выбранном элективе по его коду
        elective_ids = screen_manager.screens[4].children[0].ids
        elective_ids.title.text = ''
        elective_ids.first.text = ''
        elective_ids.second.text = ''
        elective_ids.third.text = ''
        elective_ids.fourth.text = ''
        elective_ids.fifth.text = ''

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
