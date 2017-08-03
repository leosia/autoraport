# -*- coding: UTF-8 -*-
import kivy
import os
import video
import getpass
import webbrowser

import shutil
from shutil import copyfile

from win32com.shell import shell, shellcon

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.deps import sdl2, glew

kivy.config.Config.set('graphics','resizable', False)

class StartPopup(Popup):

    start = ObjectProperty

    def __init__(self, *args, **kwargs):
        super(StartPopup, self).__init__(**kwargs)

    def complete(self):
        pass

class VersionPopup(Popup):

    version_popup = ObjectProperty

    def __init__(self, *args, **kwargs):
        super(VersionPopup, self).__init__(**kwargs)

    def get_text(self):
        text = ("[b]Autoliv Automatic Report[/b]\n"
                "Version 1.0\n"
                "\n"
                "This application is under the [b]MIT License[/b] (click [b][ref=mit]here[/ref][/b])\n"
                "Libraries OpenCV and ReportLab are under the [b]BSD License[/b] (click [b][ref=opencv]here[/ref][/b])\n"
                "\n"
                "Known bugs:\n"
                " - if you use only one video file and set start time as 0ms, pdf will have blank pages.\n"
                " - with more videos, after pressing the 'Start' button, app will froze for some time,\n"
                " decompressing videos need more time, please be patient :)\n"
                "\n"
                "If you find any more bugs please let me know by email [b]mateusz.sobek@autoliv.com[/b]")
        return text

    def on_ref_press(self, instance, ref):
        ref_dict = {
            "mit": "https://en.wikipedia.org/wiki/MIT_License",
            "opencv": "https://github.com/opencv/opencv/blob/master/LICENSE"
        }

        webbrowser.open(ref_dict[ref])

    def open_popup(self):
        self.open()

    def close_popup(self):
        self.dismiss()

class InfoPopup(Popup):

    info_label = ObjectProperty

    def __init__(self, *args, **kwargs):
        super(InfoPopup, self).__init__(**kwargs)

    def open_popup(self, info):
        self.info_label.text = info
        self.open()


    def close_popup(self):
        self.dismiss()

class VideoPopup(Popup):

    filechooser = ObjectProperty

    def __init__(self, *args, **kwargs):
        super(VideoPopup, self).__init__(**kwargs)
        # self.filechooser.path = r'C:\Users' + '\\' + getpass.getuser() + '\\' + 'Desktop'
        self.filechooser.path = shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, None, 0)

    def copy_files(self, filepath):
        if os.path.exists(r'C:\Temp\afr'):
            shutil.rmtree(r'C:\Temp\afr')
        os.mkdir(r'C:\Temp\afr')
        temp_dir = r'C:\Temp\afr'
        fileList = [os.path.normcase(f) for f in os.listdir(filepath)]
        fileList = [f for f in fileList if os.path.splitext(f)[1] in ['.avi', '.mkv', '.mp4']]
        App.get_running_app().root.files.font_size = '15sp'
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
    pdftitle = ObjectProperty


    def __init__(self, *args, **kwargs):
        super(AutoLayout, self).__init__(**kwargs)
        self.load_popup = VideoPopup()
        self.filenames = ""
        self.start_popup = StartPopup()
        self.infopopup_class = InfoPopup()
        self.version_popup = VersionPopup()
        self.mainpath = shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, None, 0)
        self.run_time = 0

        self.info1 = "Please choose video files first."
        self.info2 = "Time interval must be greater then 0."
        # self.mainpath = r'C:\Users' + '\\' + getpass.getuser() + '\\' + 'Desktop'

    # def start_second_thread(self, l_text):
    #     threading.Thread(target=self.second_thread, args=(l_text,)).start()

    def video_processing(self):
        if not os.path.exists(r'C:\Temp\afr'):
            self.infopopup_class.open_popup(self.info1)
            return None
        if int(self.interval.text) <= 0:
            self.interval.text = ''
            self.infopopup_class.open_popup(self.info2)
            return None
        vid = video.Video(int(self.fps.text), int(self.start.text), int(self.interval.text), self.to_num.text, self.pdftitle.text)
        vid.main(self.mainpath)
        self.files.markup = True
        self.files.text = "[b]Done![/b]"
        self.files.font_size = '50sp'
        self.run_time += 1
        # if vid.main():
        #     self.start_popup.start.text = "<b>Done!</b>"
        #     time.sleep(2)
        #     self.start_popup.dismiss()

    def get_filenames(self, file):
        self.filenames += file + '\n'
        self.files.text = self.filenames

class AutoApp(App):
    def __init__(self, **kwargs):
        super(AutoApp, self).__init__(**kwargs)

    def build(self):
        self.title = "Auto Raport"
        return AutoLayout()

    def on_stop(self):
        if os.path.exists(r'C:\Temp\afr'):
            shutil.rmtree(r'C:\Temp\afr')

if __name__ == '__main__':
    AutoApp().run()
