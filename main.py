from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

from kivy.lang import Builder

Builder.load_file('elective_card.kv')
Builder.load_file('administrator_menu.kv')

from kivy.core.window import Window

Window.size = 1280, 720
Window.minimum_width, Window.minimum_height = 800, 600
Window.clearcolor = 0.98, 0.98, 0.98, 1

from kivy.uix.screenmanager import ScreenManager, Screen

screen_manager = ScreenManager()
menu_screen = Screen(name='menu')
elective_screen = Screen(name='elective')
screen_manager.add_widget(menu_screen)
screen_manager.add_widget(elective_screen)


class AdministrativeMenu(ScrollView):
    def __init__(self):
        super(AdministrativeMenu, self).__init__()

        # TODO: Сделать запрос к БД, взять список элективов
        list_of_elective_names = ['Программирование для начинающих',
                                  'Теория чисел',
                                  'Логика',
                                  'Начала физики',
                                  'Английский язык',
                                  'История культуры',
                                  'Искусство и человек',
                                  'Русский язык и культура речи',
                                  'Психология общения',
                                  'Литература',
                                  'Системная биология']
        for i in range(len(list_of_elective_names)):
            self.ids.box_layout.add_widget(ElectiveLine(list_of_elective_names[i]))


class ElectiveLine(BoxLayout):
    def __init__(self, name):
        super(ElectiveLine, self).__init__()
        self.ids.elective_name_label.text = name

    @staticmethod
    def edit_button_click(button):
        screen_manager.current = 'elective'
        screen_manager.transition.direction = 'left'
        Window.set_system_cursor('arrow')
        ElectiveLine.fill_elective_fields(button)

    def fill_elective_fields(button):
        elective_name = button.parent.children[1].text
        # TODO: Сделать запрос к БД, взять информацию об элективе

        elective_ids = elective_screen.children[0].ids
        elective_ids.title.text = elective_name
        elective_ids.code.text += ''
        elective_ids.hours.text += ''
        elective_ids.max_students.text += ''
        elective_ids.in_charge.text += ''
        elective_ids.author.text += ''
        elective_ids.annotation.text += ''
        elective_ids.footer.text += ''


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
    def save_elective(self):
        # TODO: Сделать запрос к БД, отдать измененые данные
        pass

    @staticmethod
    def back_to_list():
        screen_manager.current = 'menu'
        screen_manager.transition.direction = 'right'


class ElectiveCard(BoxLayout):
    pass


class KivyApp(App):
    def build(self):
        self.title = '内部で死んでいる'
        self.icon = 'images/braindead_logo.png'

        menu_screen.add_widget(AdministrativeMenu())
        elective_screen.add_widget(ElectiveCard())
        return screen_manager


KivyApp().run()
