from django.db import models
from django.utils import timezone

class Author(models.Model):
    """
    Author model stores the name of a writer.
    One Author can have many Books.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model stores title, year of publication,
    and the associated Author.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
from django.db import models

# Create your models here.
