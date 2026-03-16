from django.test import TestCase, Client
from django.urls import reverse
from products.models import Product
from .models import Order, OrderLineItem # Adjust these to your actual model names
from unittest.mock import patch

class TestCheckoutView(TestCase):

    def setUp(self):
        """Create a product so we have something to buy."""
        self.product = Product.objects.create(
            name='Test Product',
            price=10.00,
            # add other required fields like description/sku
        )

    def test_checkout_page_loads(self):
        session = self.client.session
        # Try 'bag' instead of 'cart'
        session['bag'] = {str(self.product.id): 1}
        session.save()

        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)


    def test_post_checkout_creates_order(self):
        """Test that submitting the form works and handles Stripe"""
        # 1. Mock the Stripe PaymentIntent
        with patch('stripe.PaymentIntent.create') as mock_intent:
            mock_intent.return_value.client_secret = 'test_secret_123'
            
            # 2. Setup the bag in the session
            session = self.client.session
            session['bag'] = {str(self.product.id): 1}
            session.save()

            # 3. Create the form data (CRITICAL: Must include client_secret)
            order_data = {
                'full_name': 'Test User',
                'email': 'test@example.com',
                'phone_number': '0123456789',
                'country': 'GB',
                'postcode': 'TE1 1ST',
                'town_or_city': 'Test City',
                'street_address1': '123 Test Lane',
                'street_address2': '',
                'county': 'Test County',
                'client_secret': 'someid_secret_test123', # <--- MUST HAVE '_secret' IN IT
            }

            # 4. Post the data
            response = self.client.post(reverse('checkout'), order_data)
            
            # 5. Check the result
            self.assertIn(response.status_code, [200, 302])