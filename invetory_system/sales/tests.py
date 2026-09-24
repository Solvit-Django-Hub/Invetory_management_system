from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import User
from products.models import Category, Product
from sales.models import Customer, Sale


class SaleStockTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email="cashier@example.com",
            name="Cashier",
            password="Password123",
            role="cashier"
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

        self.customer = Customer.objects.create(
            name="John Doe",
            phone="+250788123456",
            email="customer@example.com",
            address="Kigali"
        )

        self.sale = Sale.objects.create(
            customer=self.customer,
            user=self.user,
            total_amount="650.00"
        )

    def test_sale_item_decreases_stock(self):
        data = {
            "sale": self.sale.sale_id,
            "product": self.product.product_id,
            "quantity": 3,
            "unit_price": "650.00"
        }

        response = self.client.post(
            "/api/sales/sale-items/",
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

    def test_sale_cannot_exceed_stock(self):
        data = {
            "sale": self.sale.sale_id,
            "product": self.product.product_id,
            "quantity": 20,
            "unit_price": "650.00"
        }

        response = self.client.post(
            "/api/sales/sale-items/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )