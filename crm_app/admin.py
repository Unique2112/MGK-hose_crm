from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from .models import HoseRecord, Proforma, ProformaItem, Product, Category
from django.utils.safestring import mark_safe

# ==========================================
# 1. የዳሽቦርዱ ገጽታ እና የዲዛይን ስራ (Header, CSS, JS)
# ==========================================
admin.site.site_header = mark_safe(
    '<div style="display: flex; align-items: center; background: rgba(255, 255, 255, 0.95); padding: 5px 15px; border-radius: 8px; border-left: 5px solid #D60420; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">'
    '  <img src="/static/images/logo.png" alt="MGK" style="height: 45px; width: auto; margin-right: 15px; display: block;">'
    '  <span style="font-size: 24px; color: #D60420; font-weight: bold;">MGK Hose CRM</span>'
    '</div>'
    '<style>'
    '  /* ጀርባ ምስል - በ Figma መሰረት 25% Opacity እንዲሆን (0.75 ነጭ ሽፋን) */'
    '  html, body { '
    '    background-image: linear-gradient(rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0.75)), '
    '    url("/static/images/hose_bg.jpg") !important; '
    '    background-attachment: fixed !important; '
    '    background-size: cover !important; '
    '  }'
    '  '
    '  /* የርዕስ ቦታዎች - MGK Red */'
    '  #header, .module h2, .caption, div.breadcrumbs, .module caption { '
    '    background: #D60420 !important; '
    '    color: white !important; '
    '    border-radius: 8px 8px 0 0 !important;'
    '  }'
    '  '
    '  /* የሳጥኖቹ ዲዛይን - በ Figma መሰረት (Shadow & Radius) */'
    '  fieldset.module, .module, #changelist, #content-main { '
    '    background: white !important; '
    '    border: none !important; '
    '    border-radius: 12px !important;'
    '    box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;'
    '    padding: 15px !important;'
    '    margin-bottom: 20px !important;'
    '  }'
    '  '
    '  /* Sidebar ማሻሻያ - Dashboard ቀይ እንዲሆን */'
    '  .nav-sidebar .nav-link.active { background: #D60420 !important; }'
    '  '
    '  /* የቀኝ ጽሁፎች (Logout/Password) */'
    '  #user-tools, #user-tools a, #user-tools strong { '
    '    color: #D60420 !important; '
    '    font-weight: bold !important; '
    '    background: rgba(255, 255, 255, 0.9) !important; '
    '    padding: 4px 10px !important; '
    '    border-radius: 20px !important;'
    '    text-decoration: none !important;'
    '  }'
    '  '
    '  /* በፎርም ውስጥ ያሉ ጽሁፎች */'
    '  .aligned label { '
    '    color: #333 !important; '
    '    font-weight: 700 !important; '
    '  }'
    '  '
    '  /* ዋናው ሄደር */'
    '  #header { background: #ffffff !important; border-bottom: 3px solid #D60420 !important; height: 60px !important; }'
    '</style>'
    '<script>'
    '  document.addEventListener("DOMContentLoaded", function() {'
    '    var ut = document.getElementById("user-tools");'
    '    if (ut) {'
    '      var lnks = ut.getElementsByTagName("a");'
    '      for (var i = 0; i < lnks.length; i++) {'
    '        if (lnks[i].href.includes("password_change")) lnks[i].innerHTML = " 🔑 Password";'
    '      }'
    '    }'
    '  });'
    '</script>'
)

admin.site.site_title = "MGK CRM"
admin.site.index_title = "Welcome to MGK Sales Portal"

# ==========================================
# 2. የዳታ አስተዳደር (HoseRecord Admin)
# ==========================================
@admin.register(HoseRecord)
class HoseRecordAdmin(ImportExportModelAdmin):
    list_display = ('date', 'company_name', 'psi', 'colored_status', 'unit_price')
    search_fields = ('company_name', 'part_number')
    
    def colored_status(self, obj):
        color = '#ffffff'
        background = '#28a745' if obj.status == 'Sold' else '#dc3545'
        return format_html('<span style="background: {}; color: {}; padding: 5px; border-radius: 5px;">{}</span>', background, color, obj.status)

class ProformaItemInline(admin.TabularInline):
    model = ProformaItem
    extra = 1

@admin.register(Proforma)
class ProformaAdmin(ImportExportModelAdmin):
    list_display = ('proforma_no', 'customer_name', 'date', 'total_amount', 'print_button')
    inlines = [ProformaItemInline]
    readonly_fields = ('sub_total', 'vat_amount', 'total_amount')

    def print_button(self, obj):
        return format_html('<a class="button" href="/print-proforma/{}/" target="_blank">Print PDF</a>', obj.pk)

# --- ይሄው Inventory እዚህ ጋር ተስተካክሏል ---
@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('part_number', 'name', 'category', 'quantity', 'unit_price')
    search_fields = ('name', 'part_number')

admin.site.register(Category)
