from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import StockMovement
from .serializers import StockMovementSerializer
from accounts.views import IsAdminOrManager
from django.db.models import F
from products.models import Product
from products.serializers import ProductSerializer

class StockMovementListView(generics.ListAPIView):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated]


class StockMovementDetailView(generics.RetrieveAPIView):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated]


class StockAdjustmentView(generics.CreateAPIView):
    serializer_class = StockMovementSerializer
    permission_classes = [IsAdminOrManager]

    def perform_create(self, serializer):
        movement = serializer.save(
            user=self.request.user,
            movement_type="adjustment"
        )

        product = movement.product
        product.stock_qty += movement.quantity
        product.save(update_fields=["stock_qty"])

class LowStockProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(
            stock_qty__lte=F("min_stock")
        )