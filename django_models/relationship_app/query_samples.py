import os
import sys
import django


sys.path.append("C:/Users/cindy/Desktop/Alx_DjangoLearnLab/django_models")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')

django.setup()
from relationship_app.models import Author, Book, Library, Librarian

author = Author.objects.get(name="Chinua Achebe")
books = Book.objects.filter(author=author)
print(f"Books by {author.name}: {[book.title for book in books]}")

library = Library.objects.get(name="Central Library")
books_in_library = library.books.all()
print(f"Books in {library.name}: {[book.title for book in books_in_library]}")

librarian = Librarian.objects.get(library=library)
print(f"Librarian for {library.name}: {librarian.name}")
