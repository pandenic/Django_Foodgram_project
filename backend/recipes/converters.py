import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import textobject, canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def convert_tuples_list_to_pdf(list_of_tuples_to_convert, title=None):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4, bottomup=0)
    pdfmetrics.registerFont(TTFont('Ubuntu', 'Ubuntu-R.ttf'))
    pdfmetrics.registerFont(TTFont('Ubuntu_B', 'Ubuntu-B.ttf'))
    textob = p.beginText()

    textob.setTextOrigin(cm, cm)
    if title:
        textob.setFont('Ubuntu_B', 14)
        textob.textLine(title)
    textob.setFont('Ubuntu', 14)
    for one_tuple in list_of_tuples_to_convert:
        pdf_string = ""
        for element in one_tuple:
            pdf_string += f'{element} '
        textob.textLine(pdf_string)

    p.drawText(textob)
    p.showPage()
    p.save()
    buffer.seek(0)

    return buffer
