from xhtml2pdf import pisa
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from .models import HoseRecord, Proforma

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
# ... ሌሎች ፈንክሽኖች እዚህ ይኖራሉ ...

def print_proforma(request, pk):
    proforma = get_object_or_404(Proforma, pk=pk)

    # 1. እቃዎቹን (items) ከዳታቤዝ መሳብ (በጣም ወሳኝ)
    items = proforma.items.all()

    # 2. ለ HTML ፋይሉ ዳታውን መላክ
    context = {
        'proforma': proforma,
        'items': items,
    }

    response = HttpResponse(content_type='application/pdf')

    # 3. የፋይል ስም ስህተቱን ለማስተካከል (proforma_no ወደ id ተቀይሯል)
    response['Content-Disposition'] = f'attachment; filename="proforma_{proforma.id}.pdf"'

    template_path = 'crm_app/proforma_pdf.html'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=400)
    return response