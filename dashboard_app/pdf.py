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

import uuid
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse



def html2pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        customer_name = context_dict.get('invoice').customer_name
        response['Content-Disposition'] = f'attachment; filename="{customer_name}.pdf"'
        return response
    return None






