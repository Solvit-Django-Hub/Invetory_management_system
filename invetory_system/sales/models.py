from django.db import models
from django.conf import settings
from products.models import Product


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=150)

    phone = models.CharField(max_length=20)

    email = models.EmailField(
        unique=True
    )

    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Sale(models.Model):
    sale_id = models.AutoField(primary_key=True)

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="sales"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="sales"
    )

    sale_date = models.DateTimeField(
        auto_now_add=True
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"Sale #{self.sale_id}"


class SaleItem(models.Model):
    sale_item_id = models.AutoField(primary_key=True)

    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name="sale_items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="sale_items"
    )

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"