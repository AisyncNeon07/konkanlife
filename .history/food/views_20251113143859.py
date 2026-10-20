
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

def home2(request ,pk=None):
    item= None
    for i in item:
        if i['id']==int(pk):
            item = i
            break
    return render(request, 'food/about.html', {"spot":item})
