from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.recycleview.views import RecycleKVIDsDataViewBehavior
from kivymd.uix.behaviors import (HoverBehavior,
                                  RectangularRippleBehavior,
                                  RoundedRectangularElevationBehavior,
                                  CircularRippleBehavior)


class HoverButton(Button, HoverBehavior):
    def on_enter(self):
        Window.set_system_cursor('hand')
        self.background_color[3] -= 0.2

    def on_leave(self):
        Window.set_system_cursor('arrow')
        self.background_color[3] += 0.2


class ElectiveCardTextInput(TextInput):
    max_length = 50

    def insert_text(self, substring, from_undo=False):
        if len(self.text) < self.max_length:
            return super().insert_text(substring, from_undo=from_undo)


class ClipboardButton(
    HoverButton,
    RectangularRippleBehavior,
    RoundedRectangularElevationBehavior
):
    @staticmethod
    def on_enter(**kwargs):
        Window.set_system_cursor('hand')

    @staticmethod
    def on_leave(**kwargs):
        Window.set_system_cursor('arrow')


class RippleElevationHoverButton(
    HoverButton,
    RectangularRippleBehavior,
    RoundedRectangularElevationBehavior
):
    @staticmethod
    def on_enter(**kwargs):
        Window.set_system_cursor('hand')

    @staticmethod
    def on_leave(**kwargs):
        Window.set_system_cursor('arrow')


class ImageButton(ButtonBehavior,
                  Image,
                  HoverBehavior,
                  CircularRippleBehavior):
    @staticmethod
    def on_enter(**kwargs):
        Window.set_system_cursor('hand')

    @staticmethod
    def on_leave(**kwargs):
        Window.set_system_cursor('arrow')


class ListLine(RecycleKVIDsDataViewBehavior, BoxLayout):
    @staticmethod
    def button_click(button):
        button.root.line_button_callback(button)


# FIXME: Объединить с ListLine
class ListLine2(RecycleKVIDsDataViewBehavior, BoxLayout):
    @staticmethod
    def button_click(button):
        button.root.line_button_callback(button)

    @staticmethod
    def button2_click(button):
        button.root.line_button2_callback(button)
