from django.contrib import admin
from .models import Category, HoseRecord, Proforma, ProformaItem

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
