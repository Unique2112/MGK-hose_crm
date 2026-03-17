from django.contrib import admin
from .models import Category, Product, Customer, Proforma

# እነዚህን ሞዴሎች በ Admin Panel ላይ እንዲታዩ መመዝገብ
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Proforma)
