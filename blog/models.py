from django.contrib.auth.models import AbstractUser
from django.db import models
class Role(models.TextChoices):
    ADMIN = 'admin', 'admin'
    CASHIER = 'cashier', 'cashier'

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=33, choices=Role.choices, default=Role.CASHIER)

    def __str__(self):
        return self.username


# 2 Category
class Category (models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=66,null=False,blank=False)

    def __str__(self):
        return self.name

# 3 Product /////
class Product(models.Model):
    product_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=66, null=False, blank=False)
    barcode = models.CharField(max_length=99, unique=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    purchase_price=models.DecimalField(max_digits=10, decimal_places=2)
    selling_price=models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity=models.IntegerField()


    def __str__(self):
        return self.name


# 4 Sale/////
class PaymentType(models.TextChoices):
    CASH='cash','cash'
    CARD='card', 'card'
class Sale(models.Model):
    id=models.AutoField(primary_key=True)
    cashier=models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount=models.DecimalField(max_digits=51, decimal_places=3)
    payment_type=models.CharField(max_length=10,choices=PaymentType.choices,default=PaymentType.CASH)
    created_at=models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.cashier


# 5 SaleItem
class SaleItem(models.Model):
    id=models.AutoField(primary_key=True)
    sale=models.ForeignKey(Sale, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    price_at_sale=models.DecimalField(max_digits=10, decimal_places=3)
