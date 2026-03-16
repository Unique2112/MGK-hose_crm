from django.shortcuts import render, get_object_or_404
from .models import Proforma, ProformaItem

def print_proforma(request, pk):
    # ዳታውን ከዳታቤዝ እናመጣለን
    proforma = get_object_or_404(Proforma, pk=pk)
    items = ProformaItem.objects.filter(proforma=proforma)
    
    # የሂሳብ ስሌቶች (ምንም አይነት የፒዲኤፍ ላይብረሪ አያስፈልግም)
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
    
    # ቀጥታ ገጹን ለብሮውዘር ይሰጣል፤ ብሮውዘሩ እንዲያትመው ያደርጋል
    return render(request, 'crm_app/proforma_pdf.html', context)
