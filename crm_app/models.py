from django.db import models

# 1. የዕቃዎችን ዓይነት ለመለየት (ለምሳሌ፡ Hose, Fitting)
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

# 2. የዕቃዎችን ዝርዝር ለመመዝገብ
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# 3. የደንበኞችን መረጃ ለመያዝ
class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# 4. የፕሮፎርማ (Proforma Invoice) መረጃ
class Proforma(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Proforma #{self.id} - {self.customer.name}"
