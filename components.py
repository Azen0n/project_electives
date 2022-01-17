from kivy.core.window import Window
from kivy.properties import ListProperty, BooleanProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview.views import RecycleKVIDsDataViewBehavior
from kivymd.uix.behaviors import (
    RectangularRippleBehavior,
    RoundedRectangularElevationBehavior)


class ElectiveCardTextInput(TextInput):
    max_length = 50

    def insert_text(self, substring, from_undo=False):
        if len(self.text) < self.max_length:
            return super().insert_text(substring, from_undo=from_undo)


class HoverBehavior(object):
    hovered = BooleanProperty(False)
    border_point = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(HoverBehavior, self).__init__(**kwargs)

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


class HoverButton(
    Button,
    HoverBehavior,
    RectangularRippleBehavior,
    RoundedRectangularElevationBehavior
):
    border_radius = ListProperty([0])

    def on_enter(self):
        if not self.disabled:
            Window.set_system_cursor('hand')
            self.bg_color[3] -= 0.2

    def on_leave(self):
        if not self.disabled:
            Window.set_system_cursor('arrow')
            self.bg_color[3] += 0.2


class IconButton(HoverButton):
    pass


class MenuButton(HoverButton):
    pass


class ListLine(RecycleKVIDsDataViewBehavior, BoxLayout):
    @staticmethod
    def open_button_click(button):
        button.root.line_open_button_callback(button)

    @staticmethod
    def button_click(button):
        button.root.line_button_callback(button)


