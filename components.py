from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import HoverBehavior, RectangularRippleBehavior, RoundedRectangularElevationBehavior


class HoverButton(Button, HoverBehavior):
    def on_enter(self):
        Window.set_system_cursor('hand')
        self.background_color[3] -= 0.2

    def on_leave(self):
        Window.set_system_cursor('arrow')
        self.background_color[3] += 0.2


class ElectiveTextInput(TextInput):
    max_length = 50

    def insert_text(self, substring, from_undo=False):
        if len(self.text) < self.max_length:
            return super().insert_text(substring, from_undo=from_undo)


class ImageButton(ButtonBehavior, Image):
    pass


class RippleElevationHoverButton(
    HoverButton,
    RectangularRippleBehavior,
    RoundedRectangularElevationBehavior
):
    @staticmethod
    def on_enter():
        Window.set_system_cursor('hand')

    @staticmethod
    def on_leave():
        Window.set_system_cursor('arrow')
