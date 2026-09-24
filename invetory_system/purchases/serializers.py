from django.utils import timezone
from rest_framework import serializers
from .models import Supplier, Purchase, PurchaseItem
from .models import Product

class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = [
            "supplier_id",
            "name",
            "phone",
            "email",
            "address",
        ]

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Supplier name cannot be empty."
            )

        return value

    def validate_phone(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Phone number is required."
            )

        if not value.startswith("+") or not value[1:].isdigit():
            raise serializers.ValidationError(
                "Enter a valid phone number, e.g. +250788123456."
            )

        if not 10 <= len(value[1:]) <= 15:
            raise serializers.ValidationError(
                "Phone number must contain 10 to 15 digits."
            )

        return value

    def validate_email(self, value):
        value = value.strip().lower()

        queryset = Supplier.objects.filter(email__iexact=value)

        if self.instance:
            queryset = queryset.exclude(
                supplier_id=self.instance.supplier_id
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "A supplier with this email already exists."
            )

        return value

    def validate_address(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Address cannot be empty."
            )

        return value

class PurchaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchase
        fields = [
            "purchase_id",
            "supplier",
            "user",
            "purchase_date",
            "total_amount",
        ]

        read_only_fields = [
            "purchase_id",
            "user",
            "purchase_date",
        ]

    def validate_total_amount(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Total amount cannot be negative."
            )

        return value

    def validate_supplier(self, value):
        if not Supplier.objects.filter(
            supplier_id=value.supplier_id
        ).exists():
            raise serializers.ValidationError(
                "Selected supplier does not exist."
            )

        return value

    def validate_purchase_date(self, value):
        if value > timezone.now():
            raise serializers.ValidationError(
                "Purchase date cannot be in the future."
            )

        return value

class PurchaseItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseItem
        fields = [
            "purchase_item_id",
            "purchase",
            "product",
            "quantity",
            "unit_cost",
        ]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than zero."
            )

        return value

    def validate_unit_cost(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Unit cost cannot be negative."
            )

        return value

    def validate_purchase(self, value):
        if not Purchase.objects.filter(
            purchase_id=value.purchase_id
        ).exists():
            raise serializers.ValidationError(
                "Selected purchase does not exist."
            )

        return value

    def validate_product(self, value):
        if not Product.objects.filter(
            product_id=value.product_id
        ).exists():
            raise serializers.ValidationError(
                "Selected product does not exist."
            )

        return value