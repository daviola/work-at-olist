from django.test import TestCase
from .models import Book
from authors.models import Author
from .views import books, book, book_id
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
    
     # /book POST
    def test_post_book(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST["name"] = 'book_test_2'
        request.POST["publication_year"] = 1998
        request.POST["edition"] = 3        
        request.POST["authors"] = json.dumps([self.author1.id])
        book_posted = book(request)
        content = json.loads(book_posted.content.decode())
        self.assertIn("id", content)
        self.assertIn("name", content)
        self.assertIn("publication_year", content)
        self.assertIn("authors", content)
        self.assertIn("edition", content)
        self.assertEqual(request.POST["name"], content["name"])
        self.assertEqual(request.POST["publication_year"], content["publication_year"])
        self.assertEqual(request.POST["edition"], content["edition"])
        self.assertEqual(book_posted.status_code, 201)
        # verify is posted        
        book_got = Book.objects.get(pk=3)
        self.assertEqual(book_got.name, request.POST["name"])

    # /book POST
    def test_post_book_wrong_values(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST["name"] = ''
        request.POST["publication_year"] = 1998
        request.POST["edition"] = 3        
        request.POST["authors"] = json.dumps([self.author1.id])
        book_posted = book(request)
        content = json.loads(book_posted.content.decode())
        self.assertEqual(content,{"cause":"Missing parameters"})
        self.assertEqual(book_posted.status_code, 400)
    
    # /book/<id> GET
    def test_get_book_fields(self):
        request = HttpRequest()
        request.method = "GET"                
        book_got = book_id(request, self.book.id)
        content = json.loads(book_got.content.decode())        
        self.assertIn("id", content)
        self.assertIn("name", content)
        self.assertIn("publication_year", content)
        self.assertIn("edition", content)
        self.assertIn("authors", content)
        self.assertEqual(list, type(content["authors"]))
        self.assertEqual(book_got.status_code, 200)

    # /book/<id> GET
    def test_get_book_values(self):
        request = HttpRequest()
        request.method = "GET"                
        book_got = book_id(request, self.book.id)
        content = json.loads(book_got.content.decode())
        self.assertEqual(content['id'], self.book.id)
        self.assertEqual(content['name'], "book_test1")
        self.assertEqual(content['publication_year'], 2020)
        self.assertEqual(content['edition'], 20)
        self.assertIn({'id': self.author1.id, "name": self.author1.name}, content['authors'])
        self.assertEqual(book_got.status_code, 200)

    # /book/<id> GET
    def test_get_wrong_id(self):
        request = HttpRequest()
        request.method = "GET"                
        book_got = book_id(request,3)
        content = json.loads(book_got.content.decode())
        self.assertEqual(content, {'cause': 'invalid id'})
        self.assertEqual(book_got.status_code, 400)
    
    # /book/<id> forbidden method
    def test_forbidden_method(self):
        request = HttpRequest()
        request.method = "COPY"                
        book_got = book_id(request,3)
        content = json.loads(book_got.content.decode())
        self.assertEqual(content, {'cause': 'forbidden method: COPY'})
        self.assertEqual(book_got.status_code, 403)
