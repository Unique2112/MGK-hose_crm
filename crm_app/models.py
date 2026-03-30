from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Categories"

class HoseRecord(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    hose_type = models.CharField(max_length=100)
    size = models.CharField(max_length=50)
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=20, default="Meter")

    def __str__(self):
        return f"{self.hose_type} - {self.size}"
