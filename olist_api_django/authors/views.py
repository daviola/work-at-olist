from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import Author
from django.core.paginator import Paginator

def authors(request):
    if request.method == 'GET':
        try:
            if 'name' in request.GET:
                authors = Author.objects.filter(name__icontains=request.GET['name'])
            else:
                authors = Author.objects.all()
        
            if 'page' in request.GET:
                page = request.GET['page']            
            else:
                page =1
        except:
            response ={"Cause":"Check your parameters", 'parameters':request.GET}
            return HttpResponse(json.dumps(response),status=400)
        authors = authors.order_by('id')
        paginator = Paginator(authors, 40)
        authors = paginator.get_page(page)

        response = {"Authors": list(authors.object_list.values()), 
                    "page":authors.number,
                    "count":paginator.count,
                    "num_pages":paginator.num_pages}
        return HttpResponse(json.dumps(response), status=200)                       
    else:
        return HttpResponse( status=400)
