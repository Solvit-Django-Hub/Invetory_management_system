from django.db import models
from django.conf import settings
from products.models import Product


class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=150)

    phone = models.CharField(max_length=20)

    email = models.EmailField(
        unique=True
    )

    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Purchase(models.Model):
    purchase_id = models.AutoField(primary_key=True)

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="purchases"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="purchases"
    )

    purchase_date = models.DateTimeField(
        auto_now_add=True
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"Purchase #{self.purchase_id}"


class PurchaseItem(models.Model):
    purchase_item_id = models.AutoField(primary_key=True)

    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="purchase_items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="purchase_items"
    )

    quantity = models.PositiveIntegerField()

    unit_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"