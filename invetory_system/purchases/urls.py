from django.urls import path
from .views import (SupplierListCreateView,SupplierDetailView,PurchaseListCreateView,PurchaseDetailView,PurchaseItemListCreateView,PurchaseItemDetailView,)

urlpatterns = [
    # Supplier
    path("suppliers/", SupplierListCreateView.as_view(), name="supplier-list-create"),
    path("suppliers/<int:pk>/", SupplierDetailView.as_view(), name="supplier-detail"),

    # Purchase
    path("purchases/", PurchaseListCreateView.as_view(), name="purchase-list-create"),
    path("purchases/<int:pk>/", PurchaseDetailView.as_view(), name="purchase-detail"),

    # Purchase Items
    path("purchase-items/", PurchaseItemListCreateView.as_view(), name="purchase-item-list-create"),
    path("purchase-items/<int:pk>/", PurchaseItemDetailView.as_view(), name="purchase-item-detail"),
]