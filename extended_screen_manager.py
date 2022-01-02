from kivy import Logger
from kivy.compat import iteritems, string_types
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import ScreenManagerException


class ExtendedScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        Logger.debug('ExtScreenManager.__init__')
        self.register_event_type('on_finish_screen_switch')
        super(ExtendedScreenManager, self).__init__(**kwargs)

    def on_finish_screen_switch(self):
        Logger.debug('ExtScreenManager.on_finish_screen_switch')

    def display_screen(self, screen, **options):
        """Display screen.
        Given ``screen`` can be either a screen instance or a screen name as
        string.
        If screen instance is given and not child of manager yet, it gets added
        as long as no screen with same name already exists.
        If screen name is given, corresponding screen must already be contained
        in manager.
        ``options`` might contain a :attr:`remove` flag, which causes the
        already displayed screen to be removed after switching to given screen.
        :attr:`transition` instance can be given in ``options`` to use a
        custom transition for this screen switch.
        """
        Logger.debug('ExtScreenManager.display_screen')
        assert (screen is not None)
        add_screen = False
        current_screen = self.current_screen
        if isinstance(screen, Screen):
            if current_screen is screen:
                return
            screen_name = screen.name
            if screen not in self.screens:
                if self.has_screen(screen_name):
                    raise ScreenManagerException('Screen with name {0} already exists'.format(screen_name))
                add_screen = True
        else:
            if not isinstance(screen, string_types):
                raise ScreenManagerException('Given screen must be either Screen instance or screen name as string')
            screen_name = screen
            if not self.has_screen(screen_name):
                raise ScreenManagerException('No screen found for given screen name')
            if current_screen and current_screen.name == screen_name:
                return
        is_remove = options.pop("remove", False)
        custom_transition = options.pop("transition", None)
        origin_transition = self.transition
        if custom_transition:
            for key, value in iteritems(options):
                setattr(custom_transition, key, value)
            self.transition = custom_transition

        def finish_screen_switch(transition):
            if is_remove and current_screen in self.children:
                self.remove_widget(current_screen)
            if custom_transition:
                self.transition = origin_transition
            transition.unbind(on_complete=finish_screen_switch)
            self.dispatch('on_finish_screen_switch')

        self.transition.bind(on_complete=finish_screen_switch)
        if add_screen:
            initial = self.current is None
            self.add_widget(screen)
            if not initial:
                self.current = screen_name
        else:
            self.current = screen_name
