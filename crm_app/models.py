from django.db import models
from decimal import Decimal # ይህች የግድ ከላይ መኖር አለባት
class HoseRecord(models.Model):
    date = models.DateField(auto_now_add=True, verbose_name="Date", blank=True, null=True)
    company_name = models.CharField(max_length=200, verbose_name="Company Name")
    tin_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="TIN Number")
    contact_phone = models.CharField(max_length=20, verbose_name="Contact Phone No.", blank=True, null=True)
    machine_make = models.CharField(max_length=100, verbose_name="Machine Make", blank=True, null=True)
    machine_model = models.CharField(max_length=100, verbose_name="Machine Model", blank=True, null=True)

    # ይሄው psi እዚህ ተጨምሯል
    psi = models.IntegerField(verbose_name="PSI", default=0, help_text="Working Pressure in PSI")

    product_description = models.TextField(verbose_name="Product Description", blank=True, null=True)
    part_number = models.CharField(max_length=100, verbose_name="Part Number", blank=True, null=True)
    hose_designation = models.CharField(max_length=100, verbose_name="Gates Hose Designation", blank=True, null=True)
    cut_length = models.FloatField(verbose_name="Hose cut length (meters)", default=0.0)

    HOSE_SIZES = [('1/4', '1/4'), ('3/8', '3/8'), ('1/2', '1/2'), ('3/4', '3/4'), ('1', '1'), ('1.1/4', '1.1/4')]
    hose_size = models.CharField(max_length=20, choices=HOSE_SIZES, verbose_name="Hose Size", blank=True, null=True)

    coupling_a = models.CharField(max_length=100, verbose_name="A - Coupling", blank=True, null=True)
    coupling_b = models.CharField(max_length=100, verbose_name="B - Coupling", blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name="Total Price (ETB)")
    demand_cycle = models.IntegerField(default=30, verbose_name="Demand cycle (days)")

    STATUS_CHOICES = [('Sold', 'Sold'), ('Lost Sale', 'Lost Sale')]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Sold')

    LOST_REASONS = [('Price', 'High Price'), ('Stock', 'Out of Stock'), ('Fitting', 'Fitting Mismatch'), ('Time', 'Long Waiting Time')]
    lost_reason = models.CharField(max_length=50, choices=LOST_REASONS, blank=True, null=True)
    remark = models.TextField(blank=True, null=True, verbose_name="Remark")

    def __str__(self):
        return f"{self.company_name} - {self.date}"
class Category(models.Model):
    name = models.CharField(max_length=100) # SDMO, Gates, TEU...
    def __str__(self): return self.name

class Product(models.Model):
    part_number = models.CharField(max_length=100, unique=True) # PartNo
    name = models.CharField(max_length=255) # Description
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, blank=True, null=True) # Location
    quantity = models.IntegerField(default=0) # Balance
    unit_price = models.DecimalField(max_digits=12, decimal_places=2) # Unit Price
    
    def __str__(self): return f"{self.part_number} - {self.name}"
class ProformaItem(models.Model):
    proforma = models.ForeignKey(Proforma, related_name='items', on_delete=models.CASCADE)
    # HoseRecord ሳይሆን Product እንዲሆን ተቀይሯል
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True) 
    description = models.CharField("Item Description", max_length=255)
    quantity = models.PositiveIntegerField("Quantity", default=1)
    unit_price = models.DecimalField("Unit Price", max_digits=12, decimal_places=2)
    total_price = models.DecimalField("Total Price", max_digits=12, decimal_places=2, editable=False)
    
    # ለናሙናው የተጨመሩ
    validity = models.IntegerField(default=5)
    delivery = models.CharField("Delivery", max_length=100, default="Stock") # ከናሙናው
    payment_terms = models.TextField("Payment Terms", blank=True, null=True) # ከናሙናው
    
    sub_total = models.DecimalField("Sub Total (ETB)", max_digits=12, decimal_places=2, default=0, editable=False)
    vat_amount = models.DecimalField("VAT (15%)", max_digits=12, decimal_places=2, default=0, editable=False)
    total_amount = models.DecimalField("Grand Total (ETB)", max_digits=12, decimal_places=2, default=0, editable=False)
    
    # ገንዘቡን በቃላት ለመጻፍ (Amount in Words)
    amount_in_words = models.TextField("Amount In Word", blank=True, null=True) # ከናሙናው

    def update_totals(self):
        items_total = sum(item.total_price for item in self.items.all())
        self.sub_total = items_total
        self.vat_amount = (self.sub_total * Decimal('0.15')).quantize(Decimal('0.01'))
        self.total_amount = self.sub_total + self.vat_amount
        # እዚህ ጋር update_totals ሲጠራ ሰላም እንዲያደርግ .save() እንጠቀማለን
        Proforma.objects.filter(pk=self.pk).update(
            sub_total=self.sub_total, 
            vat_amount=self.vat_amount, 
            total_amount=self.total_amount
        )

    def __str__(self):
        return f"{self.proforma_no} - {self.customer_name}"
# 2. ልጁ (ProformaItem)
class ProformaItem(models.Model):
    proforma = models.ForeignKey(Proforma, related_name='items', on_delete=models.CASCADE)
    # ዕቃውን ከዳታቤዝህ እንዲመርጥ Foreign Key ብታደርገው ዋጋውን ራሱ ያመጣልዋል
    product = models.ForeignKey(HoseRecord, on_delete=models.SET_NULL, null=True, blank=True) 
    description = models.CharField("Item Description", max_length=255) # ካስፈለገ እጅህንም መጻፍ ትችላለህ
    quantity = models.PositiveIntegerField("Quantity", default=1)
    unit_price = models.DecimalField("Unit Price", max_digits=12, decimal_places=2)
    total_price = models.DecimalField("Total Price", max_digits=12, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total_price = Decimal(str(self.quantity)) * Decimal(str(self.unit_price))
        super().save(*args, **kwargs)
        self.proforma.update_totals()
