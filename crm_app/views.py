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
    
    # የሂሳብ ስሌቶች
    subtotal = proforma.total_amount or 0
    vat_amount = float(subtotal) * 0.15
    grand_total = float(subtotal) + vat_amount

    context = {
        'proforma': proforma,
        'items': items,
        'vat_amount': round(vat_amount, 2),
        'grand_total': round(grand_total, 2),
        'website': 'mgkmakonnen.com',
        'email': 'mgkethiopia@gmail.com',
    }
    return render(request, 'crm_app/proforma_pdf.html', context)
