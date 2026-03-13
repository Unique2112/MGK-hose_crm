from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Product

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('part_number', 'name', 'category', 'quantity', 'unit_price')
    search_fields = ('part_number', 'name')
