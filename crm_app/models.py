from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class HoseRecord(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    hose_type = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=20, default="Meter")
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.hose_type} - {self.size}"

class Proforma(models.Model):
    customer_name = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vat_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    def __str__(self):
        return f"Proforma - {self.customer_name}"

class ProformaItem(models.Model):
    proforma = models.ForeignKey(Proforma, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=255)
    quantity = models.FloatField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
