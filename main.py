from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_file('elective_card.kv')
Builder.load_file('administrator_menu.kv')

Window.size = 1280, 720
Window.clearcolor = 1, 1, 1, 1

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


# TODO: Сделать запрос к БД, взять список элективов


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
            return  # do proceed if I'm not displayed <=> If have no parent
        pos = args[1]
        # Next line to_widget allow to compensate for relative layout
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

    def back_to_list(self):
        screen_manager.current = 'menu'
        screen_manager.transition.direction = 'right'


class ElectiveCard(Widget):
    pass


class AdministrativeMenu(Widget):
    def __init__(self):
        super(AdministrativeMenu, self).__init__()

        # for i in range(len(list_of_elective_names)):
        #     elective_line = ElectiveLine()
        #     elective_line.children[0].children[1].text = list_of_elective_names[i]
        #     self.ids.box_layout.add_widget(elective_line)

        for i in range(len(list_of_elective_names)):
            elective_label = Label(text=list_of_elective_names[i],
                                   color=(0, 0, 0, 1),
                                   halign='left',
                                   valign='center',
                                   padding_x=50,
                                   size_hint_y=None,
                                   height=50)
            elective_label.bind(size=elective_label.setter('text_size'))
            elective_line = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
            elective_line.add_widget(elective_label)
            edit_button = HoverButton(text='Редактировать',
                                      size_hint=(None, None),
                                      size=(150, 50),
                                      background_normal='',
                                      background_color=(40 / 255, 167 / 255, 69 / 255, 255 / 255))
            edit_button.bind(on_press=self.edit_button_click)
            elective_line.add_widget(edit_button)
            self.ids.box_layout.add_widget(elective_line)

    @staticmethod
    def edit_button_click(instance):
        screen_manager.current = 'elective'
        screen_manager.transition.direction = 'left'
        Window.set_system_cursor('arrow')
        fill_elective_fields(instance)


def fill_elective_fields(instance):
    elective_name = instance.parent.children[1].text
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


screen_manager = ScreenManager()
menu_screen = Screen(name='menu')
elective_screen = Screen(name='elective')
screen_manager.add_widget(menu_screen)
screen_manager.add_widget(elective_screen)


class KivyApp(App):
    def build(self):
        menu_screen.add_widget(AdministrativeMenu())
        elective_screen.add_widget(ElectiveCard())
        return screen_manager


KivyApp().run()
