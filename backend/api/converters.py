"""Describe data converters."""
import base64
import io

from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from rest_framework import serializers

from foodgram.settings import PDFFonts


def convert_tuples_list_to_pdf(list_of_tuples_to_convert, title=None):
    """Perform converting from tuple to strings in pdf."""
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4, bottomup=0)
    textob = p.beginText()
    textob.setTextOrigin(cm, cm)
    if title:
        textob.setFont(PDFFonts.UBUNTU_BOLD, 14)
        textob.textLine(title)
    textob.setFont(PDFFonts.UBUNTU, 14)
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


class Base64ImageField(serializers.ImageField):
    """Perform converting images to base64 format."""

    def to_internal_value(self, data):
        """Change behavior of a function.

        When using converter to internal value.
        """
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)
