# -*- coding: UTF-8 -*-

import kivy
import os
import video
import time
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

class StartPopup(Popup):

    start = ObjectProperty

    def __init__(self, *args, **kwargs):
        super(StartPopup, self).__init__(**kwargs)

    def complete(self):
        pass


class VideoPopup(Popup):

    filechooser = ObjectProperty

    def __init__(self, *args, **kwargs):
        super(VideoPopup, self).__init__(**kwargs)
        self.filechooser.path = r'C:\Users' + '\\' + getpass.getuser() + '\\' + 'Desktop'


    def copy_files(self, filepath):
        print(filepath)
        temp_dir = r'C:\Temp'
        fileList = [os.path.normcase(f) for f in os.listdir(filepath)]
        fileList = [f for f in fileList if os.path.splitext(f)[1] in ['.avi', '.mkv', '.mp4']]
        App.get_running_app().root.filenames = ""
        for file in fileList:
            App.get_running_app().root.get_filenames(file[:-4].upper())
            copyfile(filepath + '\\' + file, temp_dir + '\\' + file)
        self.dismiss()

class AutoLayout(BoxLayout):

    fps = ObjectProperty
    start = ObjectProperty
    interval = ObjectProperty
    vid_path = ObjectProperty
    tu_num = ObjectProperty
    files = ObjectProperty

    def __init__(self, *args, **kwargs):
        super(AutoLayout, self).__init__(**kwargs)
        self.load_popup = VideoPopup()
        self.filenames = ""
        self.start_popup = StartPopup()

    def video_processing(self):
        self.start_popup.open()
        time.sleep(1)
        vid = video.Video(int(self.fps.text), int(self.start.text), int(self.interval.text), self.to_num.text)
        if vid.main():
            self.start_popup.start.text = "<b>Done!</b>"
            time.sleep(2)
            self.start_popup.dismiss()

    def get_filenames(self, file):
        self.filenames += file + '\n'
        self.files.text = self.filenames

class AutoApp(App):
    def __init__(self, **kwargs):
        super(AutoApp, self).__init__(**kwargs)

    def build(self):
        self.title = "Auto Raport"
        return AutoLayout()


if __name__ == '__main__':
    AutoApp().run()