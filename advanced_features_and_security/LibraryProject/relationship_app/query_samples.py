import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


def books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    return Book.objects.filter(author=author)


def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()


def librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    return Librarian.objects.get(library=library)


if __name__ == "__main__":
    print("Books by Chinua Achebe:")
    for book in books_by_author("Chinua Achebe"):
        print(book)

    print("\nBooks in National Library:")
    for book in books_in_library("National Library"):
        print(book)

    print("\nLibrarian at National Library:")
    print(librarian_for_library("National Library"))
