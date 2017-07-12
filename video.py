# -*- coding: UTF-8 -*-

import cv2
import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from shutil import copyfile
import numpy as np

class Video:

    def file_list(self, directory, file_ext):
        """
        Funkcja przygotowuje listę plików w konkretnym katalogu, mających rozszerzenie pasujące do
        podanej listy rozszerzeń.
        :param directory: Folder docelowy
        :param file_ext: lista rozszerzeń plików
        :return: lista plików (lowercase na wszystkie nazwy)
        """
        fileList = [os.path.normcase(f) for f in os.listdir(directory)]
        fileList = [f for f in fileList if os.path.splitext(f)[1] in file_ext]
        return fileList


    def temp_dirs(self, main_path, ext_list):
        """
        Funkcja tworząca foldery o nazwach plków w folderze C:\Temp, ale tylko dla plików o porządanym rozszerzeniu
        :param main_path: ścieżka do plików
        :param ext_list: lista rozserzeń
        :return: None
        """
        for file in self.file_list(main_path, ext_list):
            temp_dict = r'C:\Temp' + '\\' + file[:-4]
            if not os.path.exists(temp_dict):
                os.mkdir(temp_dict)


    def video_cutter(self, filename, path):
        """
        Funkcja rozbija plik avi na klatki i zapisuje każdą pod nazwą imgXXX.jpg (gdzie XXX to kolejna liczba)
        :param filename: nazwa pliku wraz z roszerzeniem
        :param path: ścieżka do pliku
        :return:
        """
        file = path + "\\" + filename
        video = cv2.VideoCapture(file)
        counter = 0
        #TODO; sprawdzić dlaczego tworzy tylko jedną klatke
        while(video.isOpened()):
            ret, frame = video.read()
            print(ret)
            img_name = filename[:11] + str(counter) + '.jpg'
            img_path = r'C:\Temp' + "\\" + filename[:-4] + "\\" + img_name
            if ret == True:
                cv2.imwrite(img_path, frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
            counter += 1
        video.release()
        # cv2.destroyAllWindows()

    def pdf_creator(self):
        pass

    def main(self):
        """

        :return: None
        """
        main_path = r'\\APL-FS06\Laboratory\02_Operations\00_COP\03_Auto_Reports_Fiat'
        temp_dict = r'C:\Temp'
        ext_list = ['.avi']
        # self.temp_dirs(main_path, ext_list)
        # file_list = self.file_list(main_path, ext_list)
        # for file in file_list:
        #     src = main_path + "\\" + file
        #     dst = r'C:\Temp' + "\\" + file
        #     copyfile(src, dst)
        #     self.video_cutter(file, temp_dict)
        self.temp_dirs(temp_dict, ext_list)
        file_list = self.file_list(temp_dict, ext_list)
        for file in file_list:
            src = main_path + "\\" + file
            dst = r'C:\Temp' + "\\" + file
            # copyfile(src, dst)
            self.video_cutter(file, temp_dict)

v = Video()
v.main()