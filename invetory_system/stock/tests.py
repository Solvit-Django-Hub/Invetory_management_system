from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import User
from products.models import Category, Product


class StockAPITestCase(TestCase):

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

    def test_stock_adjustment_increases_stock(self):
        data = {
            "product": self.product.product_id,
            "quantity": 5,
            "reference_type": "Manual Adjustment",
            "reference_id": None,
            "notes": "Stock correction"
        }

        response = self.client.post(
            "/api/stock/adjustments/",
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

    def test_stock_adjustment_decreases_stock(self):
        data = {
            "product": self.product.product_id,
            "quantity": -3,
            "reference_type": "Manual Adjustment",
            "reference_id": None,
            "notes": "Stock correction"
        }

        response = self.client.post(
            "/api/stock/adjustments/",
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
            7
        )

    def test_stock_movement_is_created(self):
        data = {
            "product": self.product.product_id,
            "quantity": 5,
            "reference_type": "Manual Adjustment",
            "reference_id": None,
            "notes": "Stock correction"
        }

        response = self.client.post(
            "/api/stock/adjustments/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            self.product.stock_movements.count(),
            1
        )

class LowStockTestCase(TestCase):

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
            name="Low Stock Category"
        )

        self.low_stock_product = Product.objects.create(
            category=self.category,
            name="Low Stock Laptop",
            sku="LOW-001",
            cost_price="500.00",
            selling_price="650.00",
            stock_qty=3,
            min_stock=5
        )

        self.normal_product = Product.objects.create(
            category=self.category,
            name="Normal Laptop",
            sku="NOR-001",
            cost_price="500.00",
            selling_price="650.00",
            stock_qty=20,
            min_stock=5
        )

    def test_low_stock_products_are_returned(self):
        response = self.client.get(
            "/api/stock/low-stock/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        product_ids = [
            product["product_id"]
            for product in response.data["results"]
        ]

        self.assertIn(
            self.low_stock_product.product_id,
            product_ids
        )

        self.assertNotIn(
            self.normal_product.product_id,
            product_ids
        )