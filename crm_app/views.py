from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.db.models import Count
from xhtml2pdf import pisa
from .models import Proforma, HoseRecord
from django.shortcuts import render, get_object_or_404
from .models import Proforma

def dashboard(request):
    stats = HoseRecord.objects.values('status').annotate(total=Count('id'))
    lost_reasons = HoseRecord.objects.filter(status='Lost Sale').values('lost_reason').annotate(total=Count('id'))
    size_stats = HoseRecord.objects.filter(status='Sold').values('hose_size').annotate(total=Count('id'))

    context = {
        'stats': stats,
        'lost_reasons': lost_reasons,
        'size_stats': size_stats,
    }
    return render(request, 'crm_app/dashboard.html', context)

def get_customer_by_tin(request):
    tin = request.GET.get('tin', None)
    data = {'exists': False, 'company_name': ''}
    if tin:
        customer = HoseRecord.objects.filter(tin_number=tin).last()
        if customer:
            data = {'exists': True, 'company_name': customer.company_name}
    return JsonResponse(data)

def print_proforma(request, pk):
    proforma = get_object_or_404(Proforma, pk=pk)
    context = {'proforma': proforma}
    # ይህ በቀጥታ የ HTML ገጽ ይከፍታል፣ ከዚያ በብራውዘርህ Print ትለዋለህ
    return render(request, 'crm_app/proforma_pdf.html', context)
