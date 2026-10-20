
from django.shortcuts import render
from django.http import HttpResponse    
from .data.spots import foods, spots
# Create your views here.



context = {
        'foods': foods,
        'spots': spots
    }

def home(request):
    return render(request, 'food/index.html', context)

def home2(request ):
    return render(request, 'food/about.html', {"spot":pk})

def home3(request ,pk):
    item = None
    for i in spots:
        if i['id'] == "pk":
            item = i
            break
    return render(request, 'food/details.html', {"spot":item})
    