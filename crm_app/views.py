from django.shortcuts import render
from .models import Proforma, Product, Category

def dashboard(request):
    proformas = Proforma.objects.all().order_by('-id')[:5]
    products_count = Product.objects.all().count()
    categories_count = Category.objects.all().count()
    
    context = {
        'proformas': proformas,
        'product_count': products_count,
        'category_count': categories_count,
    }
    return render(request, 'crm_app/dashboard.html', context)

def print_proforma(request, pk):
    # ይህ ለጊዜው ባዶ ነው፣ በኋላ እናስተካክለዋለን
    return render(request, 'crm_app/proforma_pdf.html')
