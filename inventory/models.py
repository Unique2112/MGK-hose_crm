from django.db import models

class Product(models.Model):
    part_number = models.CharField(max_length=100, unique=True) # PartNo
    name = models.CharField(max_length=255) # Description
    category = models.CharField(max_length=100) # Category
    quantity = models.IntegerField(default=0) # Balance
    unit_price = models.DecimalField(max_digits=12, decimal_places=2) # Unit Price

    def __str__(self):
        return f"{self.part_number} - {self.name}"
