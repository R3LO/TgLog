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
from fluentogram import TranslatorRunner
from textwrap import wrap
from reportlab.lib import colors
import os
import time



def create_w100c_pdf(user, name, number, states, i18n):
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
    pdf_file.setFont("LorenzoSans", 50)
    pdf_file.drawCentredString(width - 160, height - 560, user)  # Заголовок

    # номер диплома
    pdfmetrics.registerFont(TTFont('LorenzoSans', file_path))
    pdf_file.setFillColorRGB(0, 0, 0.5)  # Синий цвет
    # pdf_file.setFillColorRGB(0, 0, 1)  # Синий цвет
    pdf_file.setFont("LorenzoSans", 10)
    pdf_file.drawCentredString(width - 160, 50, f'#{str(number)} - {time.strftime("%d-%m-%Y")}')  # Заголовок


    # текст награды
    # text = f'''Награждается {name} за проведение радиосвязей с любительскими радиостанциями {states} различных стран мира по списку DXCC'''
    text = i18n.w100c.text(name=name, states=states)
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

# -----------------------------------------------------------------------------------------------------------------------------------------

def create_w100l_pdf(user, name, number, locators, i18n):
    file = 'fonts/LorenzoSans.ttf'
    img = "fonts/w500lt.png"
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), img)

    # Создаем новый PDF-файл
    pdf = user + '_w500l.pdf'
    pdf_file = canvas.Canvas(pdf, pagesize=landscape(A4))
    width, height = A4

    # Добавляем иоюражение
    pdf_file.drawImage(img_path, 0, 0, width=height, height=width)

    # Добавляем позывной
    pdfmetrics.registerFont(TTFont('LorenzoSans', file_path))
    pdf_file.setFillColorRGB(1, 1, 1)  # цвет
    # pdf_file.setFillColorRGB(0, 0, 1)  # Синий цвет
    pdf_file.setFont("LorenzoSans", 54)
    pdf_file.drawCentredString(width - 240, height - 555, user.upper())  # Заголовок

    # номер диплома
    pdfmetrics.registerFont(TTFont('LorenzoSans', file_path))
    pdf_file.setFillColorRGB(0, 0, 0.5)  # Синий цвет
    # pdf_file.setFillColorRGB(0, 0, 1)  # Синий цвет
    pdf_file.setFont("LorenzoSans", 10)
    pdf_file.drawCentredString(width - 100, 62, f'#{str(number[0])} - {time.strftime("%d-%m-%Y")}')  # Заголовок


    # текст награды

    # text = f'''Награждается {name} за проведение радиосвязей с любительскими радиостанциями из {locators} различных QTH локаторов через спутник QO-100'''
    text = i18n.w100l.text(name=name, locators=locators)
    pdfmetrics.registerFont(TTFont('LorenzoSans', file_path))
    pdf_file.setFillColorRGB(0, 0, 0.5)  # Синий цвет
    # pdf_file.setFillColorRGB(0, 0, 1)  # Синий цвет
    pdf_file.setFont("LorenzoSans", 18)
    for i, s in enumerate(wrap(text, 40)):
        # y_step  = 25 * i межстрочный интервал
        y_step  = 19 * i
        # y_start = 200 - y_step по высоте
        y_start = 200 - y_step
        # pdf_file.drawCentredString(440, y_start, s) по горизонтали
        pdf_file.drawCentredString(490, y_start, s)


    pdf_file.save()

# -----------------------------------------------------------------------------------------------------------------------------------------

def create_w1000b_pdf(user, name, number, qsos, i18n):
    file = 'fonts/LorenzoSans.ttf'
    img = "fonts/w1000bt.png"
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), img)

    # Создаем новый PDF-файл
    pdf = user + '_w1000b.pdf'
    pdf_file = canvas.Canvas(pdf, pagesize=landscape(A4))
    width, height = A4

    # Добавляем иоюражение
    pdf_file.drawImage(img_path, 0, 0, width=height, height=width)

    # Добавляем позывной
    pdfmetrics.registerFont(TTFont('LorenzoSans', file_path))
    pdf_file.setFillColorRGB(0, 0, 0.5)  # цвет
    # pdf_file.setFillColorRGB(0, 0, 1)  # Синий цвет
    pdf_file.setFont("LorenzoSans", 54)
    # pdf_file.drawCentredString(width - 240, height - 555, user.upper())  # Заголовок
    pdf_file.drawCentredString(440, 240, user.upper())  # Заголовок

    # номер диплома
    pdfmetrics.registerFont(TTFont('LorenzoSans', file_path))
    pdf_file.setFillColorRGB(0, 0, 0.5)  # Синий цвет
    # pdf_file.setFillColorRGB(0, 0, 1)  # Синий цвет
    pdf_file.setFont("LorenzoSans", 10)
    pdf_file.drawCentredString(450, 75, f'#{str(number)} - {time.strftime("%d-%m-%Y")}')  # Заголовок


    # текст награды
    from textwrap import wrap
    # text = f'''Награждается {name} за проведение {qsos} QSO с любительскими радиостанциями через спутник QO-100'''
    text = i18n.w100b.text(name=name, qsos=qsos)
    pdfmetrics.registerFont(TTFont('LorenzoSans', file_path))
    pdf_file.setFillColorRGB(0, 0, 0.5)  # Синий цвет
    # pdf_file.setFillColorRGB(0, 0, 1)  # Синий цвет
    pdf_file.setFont("LorenzoSans", 18)
    for i, s in enumerate(wrap(text, 48)):
        # y_step  = 25 * i межстрочный интервал
        y_step  = 19 * i
        # y_start = 200 - y_step по высоте
        y_start = 200 - y_step
        # pdf_file.drawCentredString(440, y_start, s) по горизонтали
        pdf_file.drawCentredString(430, y_start, s)


    pdf_file.save()

# -----------------------------------------------------------------------------------------------------------------------------------------

def create_w1000u_pdf(user, name, number, unique, i18n):
    file = 'fonts/LorenzoSans.ttf'
    img = "fonts/w1000ut.png"
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), img)

    # Создаем новый PDF-файл
    pdf = user + '_w1000u.pdf'
    pdf_file = canvas.Canvas(pdf, pagesize=landscape(A4))
    width, height = A4

    # Добавляем иоюражение
    pdf_file.drawImage(img_path, 0, 0, width=height, height=width)

    # Добавляем позывной
    pdfmetrics.registerFont(TTFont('LorenzoSans', file_path))
    pdf_file.setFillColorRGB(0, 0, 0.5)  # цвет
    # pdf_file.setFillColorRGB(0, 0, 1)  # Синий цвет
    pdf_file.setFont("LorenzoSans", 54)
    # pdf_file.drawCentredString(width - 240, height - 555, user.upper())  # Заголовок
    pdf_file.drawCentredString(555, 255, user.upper())  # Заголовок

    # номер диплома
    pdfmetrics.registerFont(TTFont('LorenzoSans', file_path))
    pdf_file.setFillColorRGB(0, 0, 0.5)  # Синий цвет
    # pdf_file.setFillColorRGB(0, 0, 1)  # Синий цвет
    pdf_file.setFont("LorenzoSans", 10)
    pdf_file.drawCentredString(520, 55, f'#{str(number)} - {time.strftime("%d-%m-%Y")}')  # Заголовок


    # текст награды
    # text = f'''Награждается {name} за проведение {unique} уникальных QSO с любительскими радиостанциями через спутник QO-100'''
    text = i18n.w100u.text(name=name, unique=unique)
    pdfmetrics.registerFont(TTFont('LorenzoSans', file_path))
    pdf_file.setFillColorRGB(0, 0, 0.5)  # Синий цвет
    # pdf_file.setFillColorRGB(0, 0, 1)  # Синий цвет
    pdf_file.setFont("LorenzoSans", 18)
    for i, s in enumerate(wrap(text, 48)):
        # y_step  = 25 * i межстрочный интервал
        y_step  = 19 * i
        # y_start = 200 - y_step по высоте
        y_start = 160 - y_step
        # pdf_file.drawCentredString(440, y_start, s) по горизонтали
        pdf_file.drawCentredString(540, y_start, s)


    pdf_file.save()

# -----------------------------------------------------------------------------------------------------------------------------------------

def create_w25r_pdf(user, name, number, rus, i18n):
    file = 'fonts/LorenzoSans.ttf'
    img = "fonts/w25rt.png"
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), img)

    # Создаем новый PDF-файл
    pdf = user + '_w25r.pdf'
    pdf_file = canvas.Canvas(pdf, pagesize=landscape(A4))
    width, height = A4

    # Добавляем иоюражение
    pdf_file.drawImage(img_path, 0, 0, width=height, height=width)

    # Добавляем позывной
    pdfmetrics.registerFont(TTFont('LorenzoSans', file_path))
    pdf_file.setFillColorRGB(0, 0, 0.5)  # цвет
    # pdf_file.setFillColorRGB(0, 0, 1)  # Синий цвет
    pdf_file.setFont("LorenzoSans", 54)
    # pdf_file.drawCentredString(width - 240, height - 555, user.upper())  # Заголовок
    pdf_file.drawCentredString(320, 220, user.upper())  # Заголовок

    # номер диплома
    pdfmetrics.registerFont(TTFont('LorenzoSans', file_path))
    pdf_file.setFillColorRGB(0, 0, 0.5)  # Синий цвет
    # pdf_file.setFillColorRGB(0, 0, 1)  # Синий цвет
    pdf_file.setFont("LorenzoSans", 10)
    pdf_file.drawCentredString(270, 63, f'#{str(number)} - {time.strftime("%d-%m-%Y")}')  # Заголовок


    # текст награды
    from textwrap import wrap
    # text = f'''Награждается {name} за проведение любительских радиосвязей с {rus} регионами России через спутник QO-100'''
    text = i18n.w25r.text(name=name, rus=rus)
    pdfmetrics.registerFont(TTFont('LorenzoSans', file_path))
    pdf_file.setFillColorRGB(0, 0, 0.5)  # Синий цвет
    # pdf_file.setFillColorRGB(0, 0, 1)  # Синий цвет
    pdf_file.setFont("LorenzoSans", 18)
    for i, s in enumerate(wrap(text, 45)):
        # y_step  = 25 * i межстрочный интервал
        y_step  = 19 * i
        # y_start = 200 - y_step по высоте
        y_start = 180 - y_step
        # pdf_file.drawCentredString(440, y_start, s) по горизонтали
        pdf_file.drawCentredString(320, y_start, s)


    pdf_file.save()
