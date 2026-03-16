from django.shortcuts import render, get_object_or_404
from .models import Proforma, ProformaItem

def print_proforma(request, pk):
    # ዳታውን ከዳታቤዝ እናመጣለን
    proforma = get_object_or_404(Proforma, pk=pk)
    items = ProformaItem.objects.filter(proforma=proforma)
    
    # የሂሳብ ስሌቶች (ምንም አይነት የፒዲኤፍ ላይብረሪ አያስፈልግም)
    subtotal = proforma.sub_total or 0
    vat_amount = proforma.vat_amount or 0
    grand_total = proforma.total_amount or 0

    context = {
        'proforma': proforma,
        'items': items,
        'vat_amount': vat_amount,
        'grand_total': grand_total,
        'website': 'mgkmakonnen.com', #
        'email': 'mgkethiopia@gmail.com', #
    }
    
    # ይህ ቀጥታ የኤችቲኤምኤል ገጹን ለብሮውዘር ይሰጣል
    return render(request, 'crm_app/proforma_pdf.html', context)
