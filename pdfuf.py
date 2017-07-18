import os
import re
import numpy as np
import getpass
import datetime as dt
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.pagesizes import A4

date = dt.datetime.now()

def sorted_nicely(l):
    """
    # http://stackoverflow.com/questions/2669059/how-to-sort-alpha-numeric-set-in-python

    Sort the given iterable in the way that humans expect.
    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

path = r'C:\Temp'
path_content = os.listdir(path)
fileList = [f for f in os.listdir(path) if os.path.isfile(path + "\\" + f)]
dirList = [f for f in os.listdir(path) if not os.path.isfile(path + "\\" + f)]

file_list_sorted = []
for file_no in range(0, len(fileList)):
    file_list_sorted.append(sorted_nicely(os.listdir(path + "\\" + dirList[file_no])))

files_qty = len(sorted_nicely(os.listdir(path + "\\" + dirList[0])))

doc = canvas.Canvas('report.pdf', pagesize=A4)

doc.setFont('Helvetica-Bold', 65)
doc.drawCentredString((A4[0] / 2), ((A4[1] / 2) + 5 *cm), "Fiat Report")
doc.setFontSize(24)
doc.drawString(((A4[0] / 2) / 2), ((A4[1] / 2) - 5*cm), 'Created: ' + date.strftime('%d %B %Y'))
doc.drawString(((A4[0] / 2) / 2), ((A4[1] / 2) - 6*cm), 'By: ' + getpass.getuser())
doc.showPage()

columns = len(dirList)
margins = 0.5*cm
spacing = 0.5*cm

box_width = (A4[0]  - 2*margins -(spacing*(columns-1))) / columns
box_height = box_width / 0.8

pos_y = box_height*(files_qty - 1) - margins

doc.setPageSize((A4[0], files_qty*box_height+(2*cm)))

for y in range(0, files_qty):
    for x in range(0, columns):
        pos_x = margins + x * (box_width + margins)
        src = path + '\\' + file_list_sorted[x][y]
        doc.drawImage(src, pos_x, pos_y, box_width, box_height, preserveAspectRatio=True, anchor='n')
        if y == files_qty and x == columns:
            break
    if y == files_qty:
        break
    pos_y -= box_height

doc.showPage()
doc.save()

# for y in range(1, 9):
#     for x in range(1, 7):
#             print(i)
#             src = path + "\\" + file_list_sorted[i]
#             print(file_list_sorted[i])
#             doc.drawImage(src, pos_x*cm, pos_y*cm, box_width*cm, box_height*cm, preserveAspectRatio=True, anchor='n')
#             # doc.drawString(, pos_x*cm, pos_y*cm
#             if i < len(file_list_sorted) - 1:
#                 i += 1
#             else:
#                 break
#             pos_x += box_width + 0.4
#     pos_x = 0.5
#     pos_y -= box_height + 0.1



# doc.setFillColorRGB(155, 155, 155)
# doc.rect(0, 0, A4[0], A4[1], fill=1)
# doc.setFillColorRGB(104, 104, 104)
# doc.rect(0, 28*cm, A4[0], 3*cm, fill=1)

# text_width = stringWidth('Fiat Report', 'Helvetica-Bold', 16)
# doc.setFont('Helvetica-Bold', 16)
# doc.drawCentredString((A4[0]/2)*cm, 3*cm, 'Fiat Report')
# doc.setFont('Helvetica', 8)

# def description(i, file_qty, fps):
#     start = -2
#     if i > 6:
#         video_len = (len(file_qty) - 1) / (fps / 1000)
#         time = i * (len(file_qty) - 1) / video_len
#         return time
#     elif i == 6:
#         return 0
#     else:



# src = path + "\\" + file_list_sorted[0]
# doc.drawImage(src, 0, 0, box_width*cm, box_height*cm, preserveAspectRatio=True, anchor='n')




#
# i = 0
# for y in range(1, 9):
#     for x in range(1, 7):
#             print(i)
#             src = path + "\\" + file_list_sorted[i]
#             print(file_list_sorted[i])
#             doc.drawImage(src, pos_x*cm, pos_y*cm, box_width*cm, box_height*cm, preserveAspectRatio=True, anchor='n')
#             # doc.drawString(, pos_x*cm, pos_y*cm
#             if i < len(file_list_sorted) - 1:
#                 i += 1
#             else:
#                 break
#             pos_x += box_width + 0.4
#     pos_x = 0.5
#     pos_y -= box_height + 0.1
#
# doc.save()