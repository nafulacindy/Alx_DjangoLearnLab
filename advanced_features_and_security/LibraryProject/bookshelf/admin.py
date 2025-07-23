from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # shows these columns in list view
    list_filter = ('author', 'publication_year')            # adds filter sidebar
    search_fields = ('title', 'author')                     # adds search box
