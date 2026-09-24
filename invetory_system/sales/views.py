from django.db import transaction
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Customer, Sale, SaleItem
from .serializers import CustomerSerializer, SaleSerializer, SaleItemSerializer
from accounts.views import IsAdminOrManager
from stock.models import StockMovement
from stock.services import increase_stock, decrease_stock


class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_permissions(self):
        return [IsAuthenticated()]


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_permissions(self):
        if self.request.method in ["GET", "PUT", "PATCH"]:
            return [IsAuthenticated()]

        return [IsAdminOrManager()]


class SaleListCreateView(generics.ListCreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    def get_permissions(self):
        if self.request.method in ["GET", "POST"]:
            return [IsAuthenticated()]

        return [IsAdminOrManager()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SaleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]

        return [IsAdminOrManager()]


class SaleItemListCreateView(generics.ListCreateAPIView):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer

    def get_permissions(self):
        if self.request.method in ["GET", "POST"]:
            return [IsAuthenticated()]

        return [IsAdminOrManager()]

    @transaction.atomic
    def perform_create(self, serializer):
        sale_item = serializer.save()

        decrease_stock(
            product_id=sale_item.product.product_id,
            quantity=sale_item.quantity
        )

        StockMovement.objects.create(
            product=sale_item.product,
            user=self.request.user,
            movement_type="sale",
            quantity=-sale_item.quantity,
            reference_type="SaleItem",
            reference_id=sale_item.sale_item_id,
            notes="Stock decreased from sale."
        )


class SaleItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]

        return [IsAdminOrManager()]

    @transaction.atomic
    def perform_update(self, serializer):
        old_item = self.get_object()

        old_product = old_item.product
        old_quantity = old_item.quantity

        new_product = serializer.validated_data.get(
            "product",
            old_product
        )
        new_quantity = serializer.validated_data.get(
            "quantity",
            old_quantity
        )

        sale_item = serializer.save()

        # Same product: adjust stock by the quantity difference
        if old_product.product_id == new_product.product_id:

            quantity_difference = new_quantity - old_quantity

            if quantity_difference > 0:
                decrease_stock(
                    product_id=new_product.product_id,
                    quantity=quantity_difference
                )

                StockMovement.objects.create(
                    product=new_product,
                    user=self.request.user,
                    movement_type="sale",
                    quantity=-quantity_difference,
                    reference_type="SaleItem",
                    reference_id=sale_item.sale_item_id,
                    notes="Stock decreased after sale quantity update."
                )

            elif quantity_difference < 0:
                increase_stock(
                    product_id=old_product.product_id,
                    quantity=abs(quantity_difference)
                )

                StockMovement.objects.create(
                    product=old_product,
                    user=self.request.user,
                    movement_type="sale",
                    quantity=abs(quantity_difference),
                    reference_type="SaleItem",
                    reference_id=sale_item.sale_item_id,
                    notes="Stock increased after sale quantity reduction."
                )

        # Product changed
        else:
            # Return old quantity to old product
            increase_stock(
                product_id=old_product.product_id,
                quantity=old_quantity
            )

            StockMovement.objects.create(
                product=old_product,
                user=self.request.user,
                movement_type="sale",
                quantity=old_quantity,
                reference_type="SaleItem",
                reference_id=sale_item.sale_item_id,
                notes="Stock restored because sale product was changed."
            )

            # Remove new quantity from new product
            decrease_stock(
                product_id=new_product.product_id,
                quantity=new_quantity
            )

            StockMovement.objects.create(
                product=new_product,
                user=self.request.user,
                movement_type="sale",
                quantity=-new_quantity,
                reference_type="SaleItem",
                reference_id=sale_item.sale_item_id,
                notes="Stock decreased because sale product was changed."
            )

    @transaction.atomic
    def perform_destroy(self, instance):
        # Return the sold quantity to stock
        increase_stock(
            product_id=instance.product.product_id,
            quantity=instance.quantity
        )

        StockMovement.objects.create(
            product=instance.product,
            user=self.request.user,
            movement_type="sale",
            quantity=instance.quantity,
            reference_type="SaleItem",
            reference_id=instance.sale_item_id,
            notes="Stock restored after sale item deletion."
        )

        instance.delete()