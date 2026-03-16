from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class TestUserProfile(TestCase):

    def setUp(self):
        # 1. Create the user
        self.user = User.objects.create_user(
            username='testuser', 
            password='password123'
        )
        # 2. Log them in IMMEDIATELY for every test
        self.client.login(username='testuser', password='password123')

    def test_profile_page_loads(self):
        # Now you don't need to call login() here!
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_created_on_user_signup(self):
        """Verify that a profile is created via signals when a user is made."""
        # Assuming your profile model is named 'UserProfile'
        from .models import UserProfile
        profile = UserProfile.objects.get(user=self.user)
        self.assertIsInstance(profile, UserProfile)
        self.assertEqual(profile.user.username, 'testuser')

    def test_profile_page_loads_for_logged_in_user(self):
        """Verify user can access their profile page."""
        # 1. Log the user in first!
        self.client.login(username='testuser', password='password123')
        
        # 2. Now the request has a 'User' object instead of 'AnonymousUser'
        response = self.client.get(reverse('profile')) 
        
        self.assertEqual(response.status_code, 200)

    def test_profile_page_redirects_anonymous_user(self):
        """Verify anonymous users are redirected to login."""
        self.client.logout()
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_update_profile_info(self):
        """Test that the profile form updates data correctly."""
        self.client.login(username='testuser', password='password123')
        
        # Adjust these fields to match your UserProfile model
        updated_data = {
            'default_phone_number': '123456789',
            'default_postcode': 'SW1A 1AA',
            'default_town_or_city': 'London',
        }
        
        # Assuming the POST request to 'profile' handles the update
        response = self.client.post(reverse('profile'), updated_data)
        
        from .models import UserProfile
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.default_town_or_city, 'London')