from django.contrib import admin
from .models import Category, HoseRecord, Product, Proforma

@admin.register(HoseRecord)
class HoseRecordAdmin(admin.ModelAdmin):
    list_display = ('hose_type', 'size', 'quantity', 'category')
    list_filter = ('category', 'hose_type')

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Proforma)
