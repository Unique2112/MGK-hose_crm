from django.contrib import admin
from .models import Category, Product, Customer, Proforma

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity') # እነዚህን ሰንጠረዡ ላይ ያሳያል
    list_filter = ('category',) # በካታጎሪ እንድትለይ ይረዳሃል

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Proforma)
