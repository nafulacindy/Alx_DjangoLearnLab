from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse
from posts.models import Post

User = get_user_model()

class LikeTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass"
        )
        self.client.force_authenticate(user=self.user)

        # create a post to like
        self.post = Post.objects.create(
            author=self.user,
            content="My first post"
        )

    def test_like_post(self):
        url = reverse("post-like", args=[self.post.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 201)

    def test_unlike_post(self):
        # first like it
        url = reverse("post-like", args=[self.post.id])
        self.client.post(url)

        # then unlike (same endpoint, toggles)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
