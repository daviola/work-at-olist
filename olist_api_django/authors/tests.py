from django.test import TestCase
from .models import Author
from .views import authors
from django.http import HttpRequest
import json

class AuthorTestCase(TestCase):
    def setUp(self):
        Author.objects.create(name='test_author')
        Author.objects.create(name='test_author2')

    def test_fields(self):
        request = HttpRequest()
        request.method = "GET"
        request.GET["name"] = 'test_author'
        author = authors(request)
        content = json.loads(author.content.decode())
        self.assertIn("Authors", content)
        self.assertIn("page", content)
        self.assertIn("count", content)
        self.assertIn("num_pages", content)
        self.assertIn("id", content["Authors"][0])
        self.assertIn("name", content["Authors"][0])
    
    def test_page(self):
        request = HttpRequest()
        request.method = "GET"
        request.GET["name"] = 'test_author'
        author = authors(request)
        content = json.loads(author.content.decode())
        self.assertEqual(content["page"], 1)
        # page higher than max page
        request = HttpRequest()
        request.method = "GET"
        request.GET["page"] = 5
        author = authors(request)
        content = json.loads(author.content.decode())
        self.assertEqual(content["page"], 1)

    def test_search_author(self):
        request = HttpRequest()
        request.method = "GET"
        request.GET["name"] = 'test_author'
        author = authors(request)
        content = json.loads(author.content.decode())        
        self.assertEqual(content["Authors"][0]["name"], 'test_author')