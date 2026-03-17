from django.shortcuts import render
from .models import Proforma, Product, Category

def dashboard(request):
    proformas = Proforma.objects.all().order_by('-id')[:5]
    products = Product.objects.all().count()
    hoses = HoseRecord.objects.all().count() # አሁን ይሰራል!
    
    context = {
        'proformas': proformas,
        'product_count': products,
        'hose_count': hoses,
    }
    return render(request, 'crm_app/dashboard.html', context)

def print_proforma(request, pk):
    # ይህ ለጊዜው ባዶ ነው፣ በኋላ እናስተካክለዋለን
    return render(request, 'crm_app/proforma_pdf.html')
