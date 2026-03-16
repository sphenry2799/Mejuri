from django.test import TestCase
from django.urls import reverse
from .models import Product

from decimal import Decimal

class ProductTests(TestCase):

    def setUp(self):
        """
        Optional: This runs before every single test method.
        Use it to create objects you'll need for multiple tests.
        """
        self.product = Product.objects.create(
            name="Test Widget", 
            price=19.99,
            description="A great product"
        )

    def test_product_content(self):
        """Check if the product data is saved correctly."""
        product = Product.objects.get(id=1)
        expected_name = f'{product.name}'
        self.assertEqual(expected_name, 'Test Widget')
        self.assertEqual(product.price, Decimal('19.99'))

    def test_product_list_view(self):
        """Check if the products page loads correctly (Status 200)."""
        # Change 'product_list' to whatever your URL name is in urls.py
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Widget")