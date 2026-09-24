from django.urls import path
from .views import StockMovementListView, StockMovementDetailView, StockAdjustmentView, LowStockProductListView

urlpatterns = [
    path("movements/", StockMovementListView.as_view(), name="stock-movement-list"),
    path("movements/<int:pk>/", StockMovementDetailView.as_view(), name="stock-movement-detail"),
    path("adjustments/", StockAdjustmentView.as_view(), name="stock-adjustment"),
    path("low-stock/",LowStockProductListView.as_view(),name="low-stock-products"),
]