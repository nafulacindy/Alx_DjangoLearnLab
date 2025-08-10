from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Book

class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create a user for authenticated tests
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.book1 = Book.objects.create(title="The Hobbit", author="Tolkien", publication_year=1937)
        self.book2 = Book.objects.create(title="1984", author="Orwell", publication_year=1949)

        self.list_url = reverse('book-list')
        self.detail_url = lambda pk: reverse('book-detail', kwargs={'pk': pk})
        self.create_url = reverse('book-create')
        self.update_url = lambda pk: reverse('book-update', kwargs={'pk': pk})
        self.delete_url = lambda pk: reverse('book-delete', kwargs={'pk': pk})

    # --- CRUD Tests ---

    def test_list_books(self):
      response = self.client.get(self.list_url)
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      self.assertEqual(len(response.data), 2)
      self.assertEqual(response.data[0]['title'], self.book1.title)  # <-- explicit data check
 
        

    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='password123')
        data = {"title": "Django for APIs", "author": "William", "publication_year": 2021}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(response.data['title'], "Django for APIs") 

    def test_create_book_unauthenticated(self):
        data = {"title": "Unauthorized", "author": "None", "publication_year": 2020}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_authenticated(self):
        self.client.login(username='testuser', password='password123')
        data = {"title": "The Hobbit Updated", "author": "Tolkien", "publication_year": 1937}
        response = self.client.put(self.update_url(self.book1.id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "The Hobbit Updated")

    def test_delete_book_authenticated(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.delete(self.delete_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    # --- Filtering, Searching, Ordering Tests ---

    def test_filter_books_by_author(self):
        response = self.client.get(f"{self.list_url}?author=Tolkien")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books(self):
        response = self.client.get(f"{self.list_url}?search=1984")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], "1984")

    def test_order_books_by_year_desc(self):
        response = self.client.get(f"{self.list_url}?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], "1984")  # Latest year first
