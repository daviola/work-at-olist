from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import Book
from authors.models import Author
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
MAX_AUTHORS = 10

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
            book_to_insert= {"id": book_got.id,
                            "name": book_got.name,
                            "publication_year": book_got.publication_year,
                            "edition": book_got.edition,
                            "authors": list(book_got.authors.values())}
            response_books.append(book_to_insert)        
        response = {"books": response_books, 
                    "page":page,
                    "count":paginator.count,
                    "num_pages":paginator.num_pages}
        return HttpResponse(json.dumps(response), status=200)          
    else:
        return HttpResponse(status=400)
    response = json.dumps({})
    return HttpResponse(response, content_type="text/json", status=200)

@csrf_exempt
def book(request):    
    # POST 
    # create a book
    if request.method == 'POST':
        name = None
        edition = None
        publication_year = None
        authors = None
        try:    
            name = request.POST.get('name', "")            
            publication_year = int(request.POST.get('publication_year', ""))
            edition = int(request.POST.get('edition', ""))
            authors = list(json.loads(request.POST.get('authors', "")))
        except:            
            response ={"Cause":"Check your parameters"}
            return HttpResponse(json.dumps(response),status=400)        
        # We must receive all parameters
        if not(name and edition and publication_year and authors):
            response ={"cause":"Missing parameters"}
            return HttpResponse(json.dumps(response), content_type="text/json", status=400)      

        new_book = Book(
            name=name,
            edition=edition,
            publication_year=publication_year,            
        )
        new_book.save()
        cont = 0
        for author in authors:
            if cont> MAX_AUTHORS:
                break
            author_to_add = Author.objects.get(pk=int(author))

            new_book.authors.add(author_to_add)
            cont +=1
        new_book.save()
        response = json.dumps({"id": new_book.id,
                            "name": new_book.name,
                            "publication_year": new_book.publication_year,
                            "edition": new_book.edition,
                            "authors": list(new_book.authors.values())})
        return HttpResponse(response, content_type="text/json", status=201)
    else:
        return HttpResponse(status=400)

@csrf_exempt
def book_id(request, id):
    # PUT GET DELETE
    # Get book by id
    if request.method == "GET":
        try:
            book_got = Book.objects.get(pk=int(id))
        except:
            return HttpResponse(json.dumps({"cause":"invalid id"}),status=400)
        response = {"id": book_got.id,
                            "name": book_got.name,
                            "publication_year": book_got.publication_year,
                            "edition": book_got.edition,
                            "authors": list(book_got.authors.values())}
        return HttpResponse(json.dumps(response), content_type="text/json")
    
    # update book by id
    if request.method == "PUT":
        name = None
        edition = None
        publication_year = None
        authors = None
        try:
            if 'name' in request.GET:
                name = request.GET['name']
            if 'publication_year' in request.GET:
                publication_year = int(request.GET['publication_year'])
            if 'edition' in request.GET:
                edition = int(request.GET['edition'])
            if 'authors' in request.GET:
                authors = list(json.loads(request.GET['authors']))
        except:
            response ={"Cause":"Check your parameters", 'parameters':request.GET}
            return HttpResponse(json.dumps(response),status=400)
        try:
            book_got = Book.objects.get(pk=int(id))
        except:
            return HttpResponse(json.dumps({'cause': 'not found'}), content_type="text/json", status=204)
        if name:
            book_got.name = name
        if publication_year:
            book_got.publication_year = publication_year
        if edition:
            book_got.edition = edition
        if authors:
            cont = 0
            # clear authors            
            book_got.authors.clear()
            for author in authors:
                if cont> MAX_AUTHORS:
                    break                
                author_to_add = Author.objects.get(pk=int(author))                

                book_got.authors.add(author_to_add)
                cont +=1
        book_got.save()            

        response = {"id": book_got.id,
                            "name": book_got.name,
                            "publication_year": book_got.publication_year,
                            "edition": book_got.edition,
                            "authors": list(book_got.authors.values())}
        return HttpResponse(json.dumps(response), content_type="text/json")

    return HttpResponse(json.dumps({'cause':'forbidden method: '+str(request.method)}), content_type="text/json", status=403)