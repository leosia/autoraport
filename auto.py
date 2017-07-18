# -*- coding: UTF-8 -*-

import kivy
import os
import video
import numpy as np
import getpass
from shutil import copyfile

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from kivy.config import Config
kivy.config.Config.set('graphics','resizable', False)

class VideoPopup(Popup):

    filechooser = ObjectProperty

    def __init__(self, *args, **kwargs):
        super(VideoPopup, self).__init__(**kwargs)
        self.filechooser.path = r'C:\Users' + '\\' + getpass.getuser() + '\\' + 'Desktop'


    def copy_files(self, filepath, selection, text):
        print(filepath, selection, text)

        # fileList = [os.path.normcase(f) for f in os.listdir(directory)]
        # fileList = [f for f in fileList if os.path.splitext(f)[1] in ext_list]
        # return fileList

class AutoLayout(BoxLayout):

    fps = ObjectProperty
    start = ObjectProperty
    interval = ObjectProperty
    vid_path = ObjectProperty
    tu_num = ObjectProperty

    def __init__(self, *args, **kwargs):
        super(AutoLayout, self).__init__(**kwargs)
        self.load_popup = VideoPopup()

    def video_processing(self):
        vid = video.Video(self.fps, self.start, self.interval, self.vid_path, self.to_num)
        vid.main()

class AutoApp(App):
    def __init__(self, **kwargs):
        super(AutoApp, self).__init__(**kwargs)

    def build(self):
        self.title = "Auto Raport"
        return AutoLayout()


if __name__ == '__main__':
    AutoApp().run()