from django.shortcuts import render, get_object_or_404
from .models import Proforma, ProformaItem, HoseRecord

def dashboard(request):
    proformas = Proforma.objects.all().order_by('-id')[:5]
    hoses = HoseRecord.objects.all().count()
    return render(request, 'crm_app/dashboard.html', {'proformas': proformas, 'hose_count': hoses})

def print_proforma(request, pk):
    proforma = get_object_or_404(Proforma, pk=pk)
    items = proforma.items.all()
    return render(request, 'crm_app/proforma_pdf.html', {'proforma': proforma, 'items': items})
