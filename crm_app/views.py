import xhtml2pdf.pisa as pisa
from io import BytesIO
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Proforma, ProformaItem
from xhtml2pdf import pisa
from django.template.loader import get_template
from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Proforma, ProformaItem
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO

def print_proforma(request, pk):
    proforma = get_object_or_404(Proforma, pk=pk)
    items = ProformaItem.objects.filter(proforma=proforma)
    
    context = {
        'proforma': proforma,
        'items': items,
        'grand_total': proforma.total_amount, # ለጊዜው ቀለል ባለ ስሌት
    }

    template = get_template('crm_app/proforma_pdf.html')
    html = template.render(context)
    result = BytesIO()
    
    # PDF የመፍጠር ሂደት
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse("Error generating PDF", status=500)
