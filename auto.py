# -*- coding: UTF-8 -*-

import kivy
import numpy as np

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout




class AutoLayout(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(AutoLayout, self).__init__(**kwargs)


class AutoApp(App):
    def __init__(self, **kwargs):
        super(AutoApp, self).__init__(**kwargs)

    def build(self):
        self.title = "Auto Raport"
        return AutoLayout()


if __name__ == '__main__':
    AutoApp().run()