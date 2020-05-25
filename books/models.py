from django.db import models

from authors.models import Author

class Book(models.Model):
    name = models.CharField(max_length=100)
    edition = models.IntegerField()
    publication_year = models.IntegerField()
    authors = models.ManyToManyField(Author)