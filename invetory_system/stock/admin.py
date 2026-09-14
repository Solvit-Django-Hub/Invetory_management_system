from django.contrib import admin
from .models import StockMovement


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = (
        "movement_id",
        "product",
        "user",
        "movement_type",
        "quantity",
        "movement_date",
    )

    list_filter = (
        "movement_type",
        "movement_date",
    )

    search_fields = (
        "product__name",
        "user__email",
    )