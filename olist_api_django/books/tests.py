from django.test import TestCase
from .models import Book
from authors.models import Author
from .views import books
from django.http import HttpRequest
import json

class BooksTestCase(TestCase):
    def setUp(self):
        self.author1 = Author.objects.create(name='test_author')
        self.author2 = Author.objects.create(name='test_author2')
        self.book = Book.objects.create(name="book_test1", publication_year=2020, edition=20)
        self.book.authors.add(self.author1, self.author2)
        self.book2 = Book.objects.create(name="book_test2", publication_year=2010, edition=10)
        self.book2.authors.add(self.author1)

# /books GET
    def test_search_books_empty(self):
        self.book.delete()
        self.book2.delete()
        request = HttpRequest()
        request.method = "GET"                
        book_got = books(request)
        content = json.loads(book_got.content.decode())
        self.assertEqual(content['books'], [])
        self.assertEqual(content['count'], 0)
        self.assertEqual(content['num_pages'], 1)
        self.assertEqual(content['page'], 1)
        self.assertEqual(book_got.status_code, 200)

    # /books GET        
    def test_get_books(self):
        request = HttpRequest()
        request.method = "GET"                
        book_got = books(request)
        content = json.loads(book_got.content.decode())
        self.assertIn("books", content)
        self.assertIn("page", content)
        self.assertIn("count", content)
        self.assertIn("num_pages", content)
        self.assertEqual(type(content["books"]), list)
        self.assertEqual(book_got.status_code, 200)
        self.assertEqual(content['count'], 2)
    
    # /books GET
    def test_get_specific(self):
        request = HttpRequest()
        request.method = "GET"
        request.GET["name"]='book_test2' 
        book_got = books(request)
        content = json.loads(book_got.content.decode())
        self.assertEqual(content['count'],1)
        self.assertEqual(content['books'][0]['name'],'book_test2')
        self.assertEqual(content['books'][0]['publication_year'],2010)
        self.assertEqual(content['books'][0]['edition'],10)
        self.assertEqual(content['books'][0]['authors'][0],{'name':self.author1.name, "id":self.author1.id})