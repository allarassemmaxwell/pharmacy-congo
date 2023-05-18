from io import BytesIO
from unittest import result
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from xhtml2pdf import pisa


def html2pdf(template_source, context_dict={}):
    template = get_template(template_source)
    html = template.render(context_dict)
    result = BytesIO()

    pdf = pisa.pisaDocument(
        BytesIO(html.encode("UTF-8")), 
        result, 
        encoding='UTF-8', 
        show_error_as_pdf=True
    )

    if not pdf.err:
        return result.getvalue()

    return None