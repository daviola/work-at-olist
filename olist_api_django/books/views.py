from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import Book
from authors.models import Author
from django.core.paginator import Paginator

def books(request):
    # return a list of books based on some paremeters
    # GET
    if request.method == 'GET':
        name = None
        edition = None
        publication_year = None
        authors = None
        page = 1
        try:
            if 'name' in request.GET:
                name = request.GET['name']
            if 'publication_year' in request.GET:
                publication_year = request.GET['publication_year']
            if 'edition' in request.GET:
                edition = int(request.GET['edition'])
            if 'authors' in request.GET:
                authors = list(json.loads(request.GET['authors']))
                print(authors)
            if 'page' in request.GET:
                page = request.GET['page']
        except:
            response ={"Cause":"Check your parameters", 'parameters':request.GET}
            return HttpResponse(json.dumps(response),status=400)            
        queryset_list = Book.objects.all()
        if name:            
            queryset_list = queryset_list.filter(name__iexact=name)
        if edition:
            queryset_list = queryset_list.filter(edition__iexact=edition)
        if publication_year:
            queryset_list = queryset_list.filter(publication_year__iexact=publication_year)        
        if authors:
            cont = 0            
            for author in authors:
                if cont > MAX_AUTHORS:
                    break
                author_got= Author.objects.get(pk=int(author))
                queryset_list = queryset_list.filter(authors=author_got)

        queryset_list = queryset_list.order_by('id')
        paginator = Paginator(queryset_list, 40)
        books_got = paginator.get_page(page)
        response_books = []
        for book_got in books_got:
            j= {"id": book_got.id,
                            "name": book_got.name,
                            "publication_year": book_got.publication_year,
                            "edition": book_got.edition,
                            "authors": list(book_got.authors.values())}
            response_books.append(j)        
        response = {"books": response_books, 
                    "page":page,
                    "count":paginator.count,
                    "num_pages":paginator.num_pages}
        return HttpResponse(json.dumps(response), status=200)          
    else:
        return HttpResponse(status=400)
    response = json.dumps({})
    return HttpResponse(response, content_type="text/json", status=200)

