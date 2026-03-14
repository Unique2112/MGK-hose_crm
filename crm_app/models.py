from django.db import models
from decimal import Decimal

class HoseRecord(models.Model):
    date = models.DateField(auto_now_add=True, verbose_name="Date", blank=True, null=True)
    company_name = models.CharField(max_length=200, verbose_name="Company Name")
    tin_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="TIN Number")
    contact_phone = models.CharField(max_length=20, verbose_name="Contact Phone No.", blank=True, null=True)
    machine_make = models.CharField(max_length=100, verbose_name="Machine Make", blank=True, null=True)
    machine_model = models.CharField(max_length=100, verbose_name="Machine Model", blank=True, null=True)
    psi = models.IntegerField(verbose_name="PSI", default=0)
    product_description = models.TextField(verbose_name="Product Description", blank=True, null=True)
    part_number = models.CharField(max_length=100, verbose_name="Part Number", blank=True, null=True)
    hose_designation = models.CharField(max_length=100, verbose_name="Gates Hose Designation", blank=True, null=True)
    cut_length = models.FloatField(verbose_name="Hose cut length (meters)", default=0.0)
    HOSE_SIZES = [('1/4', '1/4'), ('3/8', '3/8'), ('1/2', '1/2'), ('3/4', '3/4'), ('1', '1'), ('1.1/4', '1.1/4')]
    hose_size = models.CharField(max_length=20, choices=HOSE_SIZES, blank=True, null=True)
    coupling_a = models.CharField(max_length=100, blank=True, null=True)
    coupling_b = models.CharField(max_length=100, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField(max_length=20, choices=[('Sold', 'Sold'), ('Lost Sale', 'Lost Sale')], default='Sold')
    remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.company_name} - {self.date}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self): return self.name
        
class Product(models.Model):
    part_number = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    def __str__(self): return f"{self.part_number} - {self.name}"

class Proforma(models.Model):
    proforma_no = models.CharField("Reference No", max_length=50, unique=True)
    customer_name = models.CharField("Customer Name", max_length=200)
    date = models.DateField("Date", auto_now_add=True)
    validity = models.IntegerField(default=5)
    delivery = models.CharField("Delivery", max_length=100, default="Stock")
    payment_terms = models.TextField("Payment Terms", blank=True, null=True)
    sub_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vat_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount_in_words = models.TextField("Amount In Word", blank=True, null=True)

    def __str__(self):
        return f"{self.proforma_no} - {self.customer_name}"

class ProformaItem(models.Model):
    proforma = models.ForeignKey(Proforma, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField("Item Description", max_length=255)
    quantity = models.PositiveIntegerField("Quantity", default=1)
    unit_price = models.DecimalField("Unit Price", max_digits=12, decimal_places=2)
    total_price = models.DecimalField("Total Price", max_digits=12, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total_price = Decimal(str(self.quantity)) * Decimal(str(self.unit_price))
        super().save(*args, **kwargs)
