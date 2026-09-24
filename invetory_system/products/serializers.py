from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            "category_id",
            "name",
            "description",
        ]
    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Category name cannot be empty."
            )

        queryset = Category.objects.filter(name__iexact=value)

        if self.instance:
            queryset = queryset.exclude(
                category_id=self.instance.category_id
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "A category with this name already exists."
            )

        return value

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "product_id",
            "category",
            "name",
            "sku",
            "cost_price",
            "selling_price",
            "stock_qty",
            "min_stock",
        ]

    def validate_cost_price(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Cost price cannot be negative."
            )

        return value

    def validate_selling_price(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Selling price cannot be negative."
            )

        return value

    def validate(self, data):
        cost_price = data.get(
            "cost_price",
            getattr(self.instance, "cost_price", None)
        )

        selling_price = data.get(
            "selling_price",
            getattr(self.instance, "selling_price", None)
        )

        if (
            cost_price is not None
            and selling_price is not None
            and selling_price < cost_price
        ):
            raise serializers.ValidationError({
                "selling_price":
                    "Selling price cannot be lower than cost price."
            })

        return data