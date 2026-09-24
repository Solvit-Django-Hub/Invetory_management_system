from django.urls import path
from .views import CustomerListCreateView, CustomerDetailView, SaleListCreateView, SaleDetailView, SaleItemListCreateView, SaleItemDetailView


urlpatterns = [
    # Customer
    path("customers/", CustomerListCreateView.as_view(), name="customer-list-create"),
    path("customers/<int:pk>/", CustomerDetailView.as_view(), name="customer-detail"),

    # Sale
    path("sales/", SaleListCreateView.as_view(), name="sale-list-create"),
    path("sales/<int:pk>/", SaleDetailView.as_view(), name="sale-detail"),

    # Sale Items
    path("sale-items/", SaleItemListCreateView.as_view(), name="sale-item-list-create"),
    path("sale-items/<int:pk>/", SaleItemDetailView.as_view(), name="sale-item-detail"),
]