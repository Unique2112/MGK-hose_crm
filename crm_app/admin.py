from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from .models import HoseRecord, Proforma, ProformaItem, Product, Category

admin.site.site_header = "MGK Hose CRM"

@admin.register(HoseRecord)
class HoseRecordAdmin(ImportExportModelAdmin):
    list_display = ('date', 'company_name', 'status', 'unit_price')
    search_fields = ('company_name', 'part_number')

# 1. መጀመሪያ ኢንላይኑን (Inline) እንገልጻለን
class ProformaItemInline(admin.TabularInline):
    model = ProformaItem
    extra = 1

# 2. ከዚያ ፕሮፎርማውን እንመዘግባለን
@admin.register(Proforma)
class ProformaAdmin(ImportExportModelAdmin):
    list_display = ('proforma_no', 'customer_name', 'date', 'total_amount')
    inlines = [ProformaItemInline]

# 3. በመጨረሻ አዲሶቹን እቃዎች (Products)
@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('part_number', 'name', 'category', 'quantity', 'unit_price')
    search_fields = ('name', 'part_number')

admin.site.register(Category)
