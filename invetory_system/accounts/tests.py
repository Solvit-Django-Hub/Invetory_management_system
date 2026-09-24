from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import User
from products.models import Category, Product


class PermissionAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_user(
            email="admin@example.com",
            name="Admin",
            password="Password123",
            role="admin"
        )

        self.manager = User.objects.create_user(
            email="manager@example.com",
            name="Manager",
            password="Password123",
            role="manager"
        )

        self.cashier = User.objects.create_user(
            email="cashier@example.com",
            name="Cashier",
            password="Password123",
            role="cashier"
        )

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

    def test_manager_can_create_product(self):
        self.client.force_authenticate(
            user=self.manager
        )

        data = {
            "category": self.category.category_id,
            "name": "Mouse",
            "sku": "MOU-001",
            "cost_price": "10.00",
            "selling_price": "15.00",
            "stock_qty": 20,
            "min_stock": 5
        }

        response = self.client.post(
            "/api/products/products/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_cashier_cannot_create_product(self):
        self.client.force_authenticate(
            user=self.cashier
        )

        data = {
            "category": self.category.category_id,
            "name": "Keyboard",
            "sku": "KEY-001",
            "cost_price": "20.00",
            "selling_price": "30.00",
            "stock_qty": 10,
            "min_stock": 5
        }

        response = self.client.post(
            "/api/products/products/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_cashier_can_view_products(self):
        self.client.force_authenticate(
            user=self.cashier
        )

        response = self.client.get(
            "/api/products/products/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )