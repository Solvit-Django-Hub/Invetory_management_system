from django.utils import timezone
from rest_framework import serializers
from .models import Customer, Sale, SaleItem, Product


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = [
            "customer_id",
            "name",
            "phone",
            "email",
            "address",
        ]

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Customer name cannot be empty."
            )

        return value

    def validate_phone(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Phone number is required."
            )

        # Allows an optional + followed by 10–15 digits.
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

        queryset = Customer.objects.filter(email__iexact=value)

        if self.instance:
            queryset = queryset.exclude(
                customer_id=self.instance.customer_id
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "A customer with this email already exists."
            )

        return value

    def validate_address(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Address cannot be empty."
            )

        return value

class SaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sale
        fields = [
            "sale_id",
            "customer",
            "user",
            "sale_date",
            "total_amount",
        ]

        read_only_fields = [
            "sale_id",
            "user",
            "sale_date",
        ]

    def validate_total_amount(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Total amount cannot be negative."
            )

        return value

    def validate_customer(self, value):
        if not Customer.objects.filter(
            customer_id=value.customer_id
        ).exists():
            raise serializers.ValidationError(
                "Selected customer does not exist."
            )

        return value

    def validate_sale_date(self, value):
        if value > timezone.now():
            raise serializers.ValidationError(
                "Sale date cannot be in the future."
            )

        return value

class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = [
            "sale_item_id",
            "sale",
            "product",
            "quantity",
            "unit_price",
        ]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than zero."
            )
        return value

    def validate_unit_price(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Unit price cannot be negative."
            )
        return value

    def validate_sale(self, value):
        if not Sale.objects.filter(
            sale_id=value.sale_id
        ).exists():
            raise serializers.ValidationError(
                "Selected sale does not exist."
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

    def validate(self, data):
        product = data.get("product")
        quantity = data.get("quantity")

        if product and quantity:
            if quantity > product.stock_qty:
                raise serializers.ValidationError({
                    "quantity":
                        "Quantity cannot exceed available stock."
                })

        return data