from django.contrib import admin
from .models import Category, Product, HoseRecord, Proforma, ProformaItem

# የ CRM ስም እና ሎጎ
admin.site.site_header = "MGK Hose CRM"
admin.site.site_title = "MGK Admin"
admin.site.index_title = "Welcome to MGK Makonnen Ethiopia"

class ProformaItemInline(admin.TabularInline):
    model = ProformaItem
    extra = 1

@admin.register(Proforma)
class ProformaAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'date', 'total_amount')
    inlines = [ProformaItemInline]

@admin.register(HoseRecord)
class HoseRecordAdmin(admin.ModelAdmin):
    list_display = ('hose_type', 'size', 'quantity', 'category')
    list_filter = ('category',)

admin.site.register(Category)
admin.site.register(Product)
