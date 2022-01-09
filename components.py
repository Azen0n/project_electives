from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview.views import RecycleKVIDsDataViewBehavior
from kivymd.uix.behaviors import (HoverBehavior,
                                  RectangularRippleBehavior,
                                  RoundedRectangularElevationBehavior)


class ElectiveCardTextInput(TextInput):
    max_length = 50

    def insert_text(self, substring, from_undo=False):
        if len(self.text) < self.max_length:
            return super().insert_text(substring, from_undo=from_undo)


class HoverButton(
    Button,
    HoverBehavior,
    RectangularRippleBehavior,
    RoundedRectangularElevationBehavior
):
    def on_enter(self):
        Window.set_system_cursor('hand')
        self.bg_color[3] -= 0.2

    def on_leave(self):
        Window.set_system_cursor('arrow')
        self.bg_color[3] += 0.2


class ListLine(RecycleKVIDsDataViewBehavior, BoxLayout):
    @staticmethod
    def button_click(button):
        button.root.line_button_callback(button)
