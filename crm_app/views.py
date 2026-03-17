from django.shortcuts import render, get_object_or_404
from .models import Proforma, ProformaItem, Product, HoseRecord, Category

def dashboard(request):
    proformas = Proforma.objects.all().order_by('-id')[:5]
    products = Product.objects.all().count()
    hoses = HoseRecord.objects.all().count()
    categories = Category.objects.all().count()
    
    context = {
        'proformas': proformas,
        'product_count': products,
        'hose_count': hoses,
        'category_count': categories,
    }
    return render(request, 'crm_app/dashboard.html', context)

def print_proforma(request, pk):
    proforma = get_object_or_404(Proforma, pk=pk)
    items = ProformaItem.objects.filter(proforma=proforma)
    
    context = {
        'proforma': proforma,
        'items': items,
        'website': 'mgkmakonnen.com',
        'email': 'mgkethiopia@gmail.com',
    }
    return render(request, 'crm_app/proforma_pdf.html', context)
