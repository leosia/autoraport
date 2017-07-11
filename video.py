# -*- coding: UTF-8 -*-

import cv2
import os
import numpy as np

class Video():

    def file_list(self, directory, file_ext):
        """
        Funkcja przygotowuje listę plików w konkretnym katalogu, mających rozszerzenie pasujące do
        podanej listy rozszerzeń.
        :param directory: Folder docelowy
        :param file_ext: lista rozszerzeń plików
        :return: lista plików (lowercase na wszystkie nazwy)
        """
        fileList = [os.path.normcase(f) for f in os.listdir(directory)]
        fileList = [os.path.join(directory, f) for f in fileList
                    if os.path.splitext(f)[1] in file_ext]
        return fileList


    def video_cutter(self, filename, path):
        """
        Funkcja rozbija plik avi na klatki i zapisuje każdą pod nazwą imgXXX.jpg (gdzie XXX to kolejna liczba)
        :param filename: nazwa pliku wraz z roszerzeniem
        :return:
        """

        file = path + "\\" + filename
        video = cv2.VideoCapture(file)
        counter = 0
        #TODO; sprawdzić dlaczego tworzy tylko jedną klatke
        while(video.isOpened()):
            ret, frame = video.read()
            img_name = 'img' + str(counter) + '.jpg'
            img_path = path + "\\" + filename[:-4] + "\\" + img_name
            if ret == True:
                # cv2.imshow('frame', frame)
                cv2.imwrite(img_path, frame)
                if cv2.waitKey(1):
                    break
            else:
                break
            counter += 1

        video.release()
        # cv2.destroyAllWindows()

    def filesystem_prepare(self):
        """
        Funkcja przygotowuje system plików w podanej ścieżce. Obsługiwane są tylko pliki z rozszerzeniem 'avi',
        Po utworzeniu folderu uruchamiana jest funckja 'video_cutter'.
        :return: None
        """
        main_path = r'\\APL-FS06\Laboratory\03_Temp\fiat'
        ext_list = ['avi']
        #TODO: Wprowadzić nowy system tworzenia listy plików do funkcji (lowercase na nazwach)
        #TODO: tworzenie raportu, pdf?, excel?, moze cos innego?
        for file in self.file_list(main_path, ext_list):
            print("Start", file)
            (short, ext) = os.path.splitext(file)
            if ext.lower() == '.avi':
                video_path = main_path + "\\" + short
                if not os.path.exists(video_path):
                    os.mkdir(video_path)
                self.video_cutter(file, main_path)
            print("End")


v = Video()
v.filesystem_prepare()
