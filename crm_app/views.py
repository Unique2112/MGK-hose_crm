from django.shortcuts import render, get_object_or_404
from .models import Proforma, ProformaItem, Product, HoseRecord

# 1. የዳሽቦርድ ኮድ (ይህ ስለጠፋ ነው አፑ ክራሽ ያደረገው)
def dashboard(request):
    proformas = Proforma.objects.all().order_by('-date')[:5]
    products = Product.objects.all().count()
    hoses = HoseRecord.objects.all().count()
    
    context = {
        'proformas': proformas,
        'product_count': products,
        'hose_count': hoses,
    }
    return render(request, 'crm_app/dashboard.html', context)

# 2. የፕሮፎርማ ህትመት ኮድ
def print_proforma(request, pk):
    proforma = get_object_or_404(Proforma, pk=pk)
    items = ProformaItem.objects.filter(proforma=proforma)
    
    subtotal = proforma.sub_total or 0
    vat_amount = proforma.vat_amount or 0
    grand_total = proforma.total_amount or 0

    context = {
        'proforma': proforma,
        'items': items,
        'vat_amount': vat_amount,
        'grand_total': grand_total,
        'website': 'mgkmakonnen.com',
        'email': 'mgkethiopia@gmail.com',
    }
    return render(request, 'crm_app/proforma_pdf.html', context)
