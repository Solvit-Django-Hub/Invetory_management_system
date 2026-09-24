from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import User
from products.models import Category, Product
from purchases.models import Supplier, Purchase


class PurchaseStockTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email="manager@example.com",
            name="Manager",
            password="Password123",
            role="manager"
        )

        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(
            name="Electronics"
        )

        self.product = Product.objects.create(
            category=self.category,
            name="Laptop",
            sku="LAP-001",
            cost_price="500.00",
            selling_price="650.00",
            stock_qty=10,
            min_stock=5
        )

        self.supplier = Supplier.objects.create(
            name="Tech Supplier",
            phone="+250788123456",
            email="supplier@example.com",
            address="Kigali"
        )

        self.purchase = Purchase.objects.create(
            supplier=self.supplier,
            user=self.user,
            total_amount="1000.00"
        )

    def test_purchase_item_increases_stock(self):
        data = {
            "purchase": self.purchase.purchase_id,
            "product": self.product.product_id,
            "quantity": 5,
            "unit_cost": "500.00"
        }

        response = self.client.post(
            "/api/purchases/purchase-items/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.stock_qty,
            15
        )