
from django.shortcuts import render
from django.http import HttpResponse    
from .data.spots import foods, spots

from models import Spots, Category, spot_info
# Create your views here.





def home(request):
    spots = Spots.objects.all()
    return render(request, 'food/index.html', {"spots": spots})

def home2(request):
    return render(request, 'food/about.html', {"spots":spots})

def home3(request ,pk):
    item = None
    for i in spots:
        if str(i['id']) == pk:
            item = i
            break
    return render(request, 'food/details.html', {"spot":item})

