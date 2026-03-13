from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa  # በቀጥታ እንዲህ ይሁን
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
    try:
        proforma = Proforma.objects.get(pk=pk)
        template_path = 'crm_app/proforma_pdf.html'
        context = {'proforma': proforma}
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename="proforma_{proforma.proforma_no}.pdf"'
        
        template = get_template(template_path)
        html = template.render(context)

        pisa_status = pisa.CreatePDF(html, dest=response)
        
        if pisa_status.err:
           return HttpResponse(f'PDF Error: {pisa_status.err}')
        return response
    except Exception as e:
        return HttpResponse(f'Error occurred: {str(e)}')
