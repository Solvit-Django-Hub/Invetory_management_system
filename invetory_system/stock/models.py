from django.db import models
from django.conf import settings
from products.models import Product


class StockMovement(models.Model):

    MOVEMENT_TYPES = [
        ("purchase", "Purchase"),
        ("sale", "Sale"),
        ("adjustment", "Adjustment"),
    ]

    movement_id = models.AutoField(primary_key=True)

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="stock_movements"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="stock_movements"
    )

    movement_type = models.CharField(
        max_length=20,
        choices=MOVEMENT_TYPES
    )

    quantity = models.IntegerField()

    reference_type = models.CharField(
        max_length=50,
        blank=True
    )

    reference_id = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    movement_date = models.DateTimeField(
        auto_now_add=True
    )

    notes = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.product.name} - {self.movement_type}"