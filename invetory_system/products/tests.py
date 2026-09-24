from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User
from products.models import Category, Product


class ProductAPITestCase(TestCase):

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
            name="Electronics",
            description="Electronic products"
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

    def test_get_products(self):
        response = self.client.get(
            "/api/products/products/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_create_product(self):
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

    def test_negative_cost_price_is_rejected(self):
        data = {
            "category": self.category.category_id,
            "name": "Keyboard",
            "sku": "KEY-001",
            "cost_price": "-10.00",
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
            status.HTTP_400_BAD_REQUEST
        )