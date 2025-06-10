from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import landscape
from reportlab.lib.pagesizes import portrait
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch

from reportlab.lib import colors
import os
import time



def create_w100c_pdf(user, name, number, states):
    file = 'fonts/LorenzoSans.ttf'
    img = "fonts/w100ct.png"
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), img)

    # Создаем новый PDF-файл
    pdf = user + '_w100c.pdf'
    pdf_file = canvas.Canvas(pdf, pagesize=landscape(A4))
    width, height = A4

    # Добавляем иоюражение
    pdf_file.drawImage(img_path, 0, 0, width=height, height=width)

    # Добавляем позывной
    pdfmetrics.registerFont(TTFont('LorenzoSans', file_path))
    pdf_file.setFillColorRGB(0, 0, 0.5)  # Синий цвет
    # pdf_file.setFillColorRGB(0, 0, 1)  # Синий цвет
    pdf_file.setFont("LorenzoSans", 34)
    pdf_file.drawCentredString(width - 160, height - 560, user)  # Заголовок

    # номер диплома
    pdfmetrics.registerFont(TTFont('LorenzoSans', file_path))
    pdf_file.setFillColorRGB(0, 0, 0.5)  # Синий цвет
    # pdf_file.setFillColorRGB(0, 0, 1)  # Синий цвет
    pdf_file.setFont("LorenzoSans", 10)
    pdf_file.drawCentredString(width - 160, 50, f'#{str(number)} от {time.strftime("%d-%m-%Y")}')  # Заголовок


    # текст награды
    from textwrap import wrap
    text = f'''Награждается {name} за проведение радиосвязей с любительскими радиостанциями {states} различных стран мира по списку DXCC'''
    pdfmetrics.registerFont(TTFont('LorenzoSans', file_path))
    pdf_file.setFillColorRGB(0, 0, 0.5)  # Синий цвет
    # pdf_file.setFillColorRGB(0, 0, 1)  # Синий цвет
    pdf_file.setFont("LorenzoSans", 18)
    for i, s in enumerate(wrap(text, 40)):
        # y_step  = 25 * i межстрочный интервал
        y_step  = 19 * i
        # y_start = 220 - y_step по высоте
        y_start = 200 - y_step
        # pdf_file.drawCentredString(380, y_start, s) по горизонтали
        pdf_file.drawCentredString(440, y_start, s)


    pdf_file.save()
