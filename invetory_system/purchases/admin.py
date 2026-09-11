from django.contrib import admin
from .models import Supplier, Purchase, PurchaseItem


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        "supplier_id",
        "name",
        "phone",
        "email",
    )

    search_fields = (
        "name",
        "phone",
        "email",
    )


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "purchase_id",
        "supplier",
        "user",
        "purchase_date",
        "total_amount",
    )

    list_filter = ("purchase_date",)


@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = (
        "purchase_item_id",
        "purchase",
        "product",
        "quantity",
        "unit_cost",
    )