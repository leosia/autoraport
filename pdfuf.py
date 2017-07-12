import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate

path = r'C:\Temp\t-17246511_kab-drv_nd_front_ht'
fileList = [f for f in os.listdir(path)]
doc = canvas.Canvas('report.pdf')

qty = os.listdir(path)

# pos_y1 =

for i in range(1, qty + 1):
    for y in range(1, 5):
        if y % 2 != 0:
            src = path + "\\" + fileList[i]
            doc.drawImage(src, 1*cm, *cm, 9*cm, 12*cm, preserveAspectRatio=True, anchor='n')
        else:
            src = path + "\\" + fileList[i]
            doc.drawImage(src, 11*cm, 10*cm, 9*cm, 12*cm, preserveAspectRatio=True, anchor='n')
    if i % 6 == 0:
        doc.showPage()
doc.save()

# if i % 2 == 0:
#     src = path + "\\" + fileList[i + 1]
#     doc.drawImage(src, 10 * cm, 10 * cm, 6 * cm, 8 * cm, preserveAspectRatio=True, anchor='n')
# elif i % 2 != 0:
#     src = path + "\\" + fileList[i + 1]
#     doc.drawImage(src, 10 * cm, 10 * cm, 6 * cm, 8 * cm, preserveAspectRatio=True, anchor='n')