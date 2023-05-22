from io import BytesIO
from unittest import result
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from reportlab.pdfgen import canvas
from django.template.loader import get_template
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from .models import Invoice
import xhtml2pdf.pisa as pisa
import uuid
from django.conf import settings


def html2pdf(template_source, context_dict={}):
    template = get_template(template_source)
    html = template.render(context_dict)
    result = BytesIO()

    pdf = pisa.pisaDocument(html, result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="output.pdf"'
        return response

    return HttpResponse("Error generating PDF", status=500)







