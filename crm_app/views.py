from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Proforma, ProformaItem
from xhtml2pdf import pisa
from django.template.loader import get_template
from decimal import Decimal

def print_proforma(request, pk):
    proforma = get_object_or_404(Proforma, pk=pk)
    items = ProformaItem.objects.filter(proforma=proforma)
    
    # የሂሳብ ስሌቶች
    subtotal = proforma.total_amount or Decimal('0.00')
    vat_amount = subtotal * Decimal('0.15')
    grand_total = subtotal + vat_amount

    context = {
        'proforma': proforma,
        'items': items,
        'vat_amount': round(vat_amount, 2),
        'grand_total': round(grand_total, 2),
        'website': 'mgkmakonnen.com',
        'email': 'mgkethiopia@gmail.com',
    }

    # PDF የመፍጠር ሂደት
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="proforma_{proforma.proforma_no}.pdf"'
    
    template = get_template('crm_app/proforma_pdf.html')
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('PDF Error', status=500)
    return response
