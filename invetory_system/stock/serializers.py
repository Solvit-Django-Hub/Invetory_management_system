
from rest_framework import serializers
from .models import StockMovement


class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = [
            "movement_id",
            "product",
            "user",
            "movement_type",
            "quantity",
            "reference_type",
            "reference_id",
            "movement_date",
            "notes",
        ]
        read_only_fields = [
            "movement_id",
            "user",
            "movement_type",
            "movement_date",
        ]

    def validate_quantity(self, value):
        if value == 0:
            raise serializers.ValidationError(
                "Movement quantity cannot be zero."
            )

        return value

    def validate_movement_type(self, value):
        if value not in ["purchase", "sale", "adjustment"]:
            raise serializers.ValidationError(
                "Invalid movement type."
            )

        return value

