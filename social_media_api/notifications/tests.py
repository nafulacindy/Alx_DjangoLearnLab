from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse

User = get_user_model()

class NotificationTests(APITestCase):
    def setUp(self):
        # create a user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass"
        )
        # authenticate
        self.client.force_authenticate(user=self.user)

    def test_list_notifications(self):
        url = reverse("notification-list")  # router auto-generates this
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
