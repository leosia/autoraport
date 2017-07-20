# -*- coding: UTF-8 -*-

import cv2
import os
import re
import getpass
import datetime as dt

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4


class Video:
    def __init__(self, fps, start, interval, to_num):
        self.fps = fps
        self.start = start
        self.to_num = to_num
        self.interval = interval
        self.temp_dict = r'C:\Temp\afr'
        self.ext_list = ['.avi', '.mp4', '.mkv']
        self.res_list = []


    def main(self, mainpath):
        self.temp_dirs(self.temp_dict, self.ext_list)
        file_list = self.file_list(self.temp_dict, self.ext_list)
        for file in file_list:
            self.video_cutter(file, self.temp_dict)
        self.pdf_creator(min(self.res_list), mainpath)
        return True


    def file_list(self, directory, ext_list):
        """
        Funkcja przygotowuje listę plików konkretnego katalogu, mających rozszerzenie pasujące do
        podanej listy rozszerzeń.
        :param directory: Folder docelowy
        :param file_ext: lista rozszerzeń plików
        :return: lista plików (lowercase na wszystkie nazwy)
        """
        fileList = [os.path.normcase(f) for f in os.listdir(directory)]
        fileList = [f for f in fileList if os.path.splitext(f)[1] in ext_list]
        return fileList


    def temp_dirs(self, main_path, ext_list):
        """
        Funkcja tworząca foldery o nazwach plków w folderze C:\Temp, ale tylko dla plików o porządanym rozszerzeniu
        :param main_path: ścieżka do plików
        :param ext_list: lista rozserzeń
        :return: None
        """
        for file in self.file_list(main_path, ext_list):
            temp_dict = r'C:\Temp\afr' + '\\' + file[:-4]
            if not os.path.exists(temp_dict):
                os.mkdir(temp_dict)


    def time_converter(self, frame):
        time = (1000/3000)*(frame - 6)
        return time


    def video_cutter(self, filename, path):
        """
        Funkcja rozbija plik avi na klatki i zapisuje każdą pod nazwą imgXXX.jpg (gdzie XXX to kolejna liczba)
        :param filename: nazwa pliku wraz z roszerzeniem
        :param path: ścieżka do pliku
        :return:
        """
        file = path + "\\" + filename
        video = cv2.VideoCapture(file)
        c = 0
        width = video.get(3)
        height = video.get(4)
        ratio = width/height
        self.res_list.append(ratio) if ratio not in self.res_list else None
        while(video.isOpened()):
            ret, frame = video.read()
            if self.time_converter(c) % self.interval == 0:
                img_name = filename[:11] + str(c) + "_" + format(self.time_converter(c), '.1f') + '.jpg'
                img_path = r'C:\Temp\afr' + "\\" + filename[:-4] + "\\" + img_name
                if ret == True:
                    cv2.imwrite(img_path, frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    break
            c += 1
        video.release()


    def pdf_creator(self, ratio, mainpath):

        def sorted_nicely(l):
            """
            # http://stackoverflow.com/questions/2669059/how-to-sort-alpha-numeric-set-in-python
            Sort the given iterable in the way that humans expect.
            """
            convert = lambda text: int(text) if text.isdigit() else text
            alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
            return sorted(l, key=alphanum_key)

        def prepare_description(filename):
            name = os.path.splitext(filename)
            time = name[0][-4:]
            if time[:1] == '_':
                time = time[1:]
            text = name[0][:10].upper() + '   Time: ' + time + ' ms'
            return text

        date = dt.datetime.now()
        fileList = [f for f in os.listdir(self.temp_dict) if os.path.isfile(self.temp_dict + "\\" + f)]
        dirList = [f for f in os.listdir(self.temp_dict) if not os.path.isfile(self.temp_dict + "\\" + f)]

        file_list_sorted = []
        for file_no in range(0, len(fileList)):
            file_list_sorted.append(sorted_nicely(os.listdir(self.temp_dict + "\\" + dirList[file_no])))

        files_qty = len(sorted_nicely(os.listdir(self.temp_dict + "\\" + dirList[0])))

        username = getpass.getuser().split('.')
        username = username[0].capitalize() + ' ' + username[1].capitalize()

        pdf_path = mainpath + '\\' + 'report.pdf'
        doc = canvas.Canvas(pdf_path, pagesize=A4)

        doc.setFont('Helvetica-Bold', 65)
        doc.setFillColorRGB(0, (40/255), (81/255))
        doc.drawCentredString((A4[0] / 2), ((A4[1] / 2) + 5 * cm), "Fiat Report")
        doc.setFontSize(24)
        doc.drawImage('logo2.png', ((A4[0] / 2)-((A4[0]/3)/2.125)), ((A4[1] / 2)), A4[0]/3, (A4[0]/3)/2.125, preserveAspectRatio=True, anchor='c')
        doc.drawCentredString((A4[0] / 2) + 3, ((A4[1] / 2) - 1 * cm), 'TO-' + self.to_num)
        doc.drawCentredString((A4[0] / 2), ((A4[1] / 2) - 5 * cm), 'Created:')
        doc.drawCentredString((A4[0] / 2), ((A4[1] / 2) - 6 * cm), date.strftime('%d %B %Y'))
        doc.drawCentredString((A4[0] / 2), ((A4[1] / 2) - 7 * cm), username)
        doc.showPage()

        columns = len(dirList)
        margins = 0.5 * cm
        spacing = 0.5 * cm



        box_width = (A4[0] - 2 * margins - (spacing * (columns - 1))) / columns
        box_height = box_width / ratio
        box_height += box_height*0.2

        pos_y = box_height * (files_qty - 1) + margins

        doc.setPageSize((A4[0], files_qty * box_height + (2 * cm)))
        doc.setFont('Helvetica-Bold', 38 / (columns if columns < 12 else columns * 2))

        for y in range(0, files_qty):
            for x in range(0, columns):
                pos_x = margins + x * (box_width + margins)
                src = self.temp_dict + '\\' + dirList[x] + '\\' + file_list_sorted[x][y]
                doc.drawImage(src, pos_x, pos_y, box_width, box_height, preserveAspectRatio=True, anchor='n')
                doc.drawCentredString(pos_x + (box_width / 2), pos_y + ((box_height - box_width) / 2.5), prepare_description(file_list_sorted[x][y]))
                if y == files_qty and x == columns:
                    break
            if y == files_qty:
                break
            pos_y -= box_height

        doc.showPage()
        doc.save()
