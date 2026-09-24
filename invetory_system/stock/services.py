from django.db import transaction
from rest_framework.exceptions import ValidationError
from products.models import Product


@transaction.atomic
def increase_stock(product_id, quantity):
    product = Product.objects.select_for_update().get(
        product_id=product_id
    )

    product.stock_qty += quantity
    product.save(update_fields=["stock_qty"])

    return product


@transaction.atomic
def decrease_stock(product_id, quantity):
    product = Product.objects.select_for_update().get(
        product_id=product_id
    )

    if quantity > product.stock_qty:
        raise ValidationError(
            "Insufficient stock available."
        )

    product.stock_qty -= quantity
    product.save(update_fields=["stock_qty"])

    return product