from django.db import transaction
from rest_framework import generics
from .models import Supplier, Purchase, PurchaseItem
from .serializers import SupplierSerializer, PurchaseSerializer, PurchaseItemSerializer
from accounts.views import IsAdminOrManager
from stock.models import StockMovement
from stock.services import increase_stock, decrease_stock


class SupplierListCreateView(generics.ListCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAdminOrManager]


class SupplierDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAdminOrManager]


class PurchaseListCreateView(generics.ListCreateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAdminOrManager]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PurchaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAdminOrManager]


class PurchaseItemListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseItem.objects.all()
    serializer_class = PurchaseItemSerializer
    permission_classes = [IsAdminOrManager]

    def perform_create(self, serializer):
        purchase_item = serializer.save()

        increase_stock(
            product_id=purchase_item.product.product_id,
            quantity=purchase_item.quantity
        )

        StockMovement.objects.create(
            product=purchase_item.product,
            user=self.request.user,
            movement_type="purchase",
            quantity=purchase_item.quantity,
            reference_type="PurchaseItem",
            reference_id=purchase_item.purchase_item_id,
            notes="Stock increased from purchase."
        )


class PurchaseItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseItem.objects.all()
    serializer_class = PurchaseItemSerializer
    permission_classes = [IsAdminOrManager]

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

        purchase_item = serializer.save()

        # Same product: adjust stock by the quantity difference
        if old_product.product_id == new_product.product_id:

            quantity_difference = new_quantity - old_quantity

            if quantity_difference > 0:
                increase_stock(
                    product_id=new_product.product_id,
                    quantity=quantity_difference
                )

                StockMovement.objects.create(
                    product=new_product,
                    user=self.request.user,
                    movement_type="purchase",
                    quantity=quantity_difference,
                    reference_type="PurchaseItem",
                    reference_id=purchase_item.purchase_item_id,
                    notes="Stock increased after purchase quantity update."
                )

            elif quantity_difference < 0:
                decrease_stock(
                    product_id=old_product.product_id,
                    quantity=abs(quantity_difference)
                )

                StockMovement.objects.create(
                    product=old_product,
                    user=self.request.user,
                    movement_type="purchase",
                    quantity=quantity_difference,
                    reference_type="PurchaseItem",
                    reference_id=purchase_item.purchase_item_id,
                    notes="Stock decreased after purchase quantity update."
                )

        # Product changed: remove stock from old product
        # and add stock to new product
        else:
            decrease_stock(
                product_id=old_product.product_id,
                quantity=old_quantity
            )

            StockMovement.objects.create(
                product=old_product,
                user=self.request.user,
                movement_type="purchase",
                quantity=-old_quantity,
                reference_type="PurchaseItem",
                reference_id=purchase_item.purchase_item_id,
                notes="Stock decreased because purchase product was changed."
            )

            increase_stock(
                product_id=new_product.product_id,
                quantity=new_quantity
            )

            StockMovement.objects.create(
                product=new_product,
                user=self.request.user,
                movement_type="purchase",
                quantity=new_quantity,
                reference_type="PurchaseItem",
                reference_id=purchase_item.purchase_item_id,
                notes="Stock increased because purchase product was changed."
            )

    @transaction.atomic
    def perform_destroy(self, instance):
        decrease_stock(
            product_id=instance.product.product_id,
            quantity=instance.quantity
        )

        StockMovement.objects.create(
            product=instance.product,
            user=self.request.user,
            movement_type="purchase",
            quantity=-instance.quantity,
            reference_type="PurchaseItem",
            reference_id=instance.purchase_item_id,
            notes="Stock decreased after purchase item deletion."
        )

        instance.delete()
