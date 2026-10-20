
from django.shortcuts import render
from django.http import HttpResponse    
from .data.spots import foods, spots

from  . models import Spots, Category, spot_info
# Create your views here.





def home(request):
    spots = Spots.objects.all()
    return render(request, 'food/index.html', {"spots": spots})

def home2(request):
    spots = Spots.objects.all()
    return render(request, 'food/about.html', {"spots":spots})

def home3(request ,pk):
    spot_info = None
    spot_infos = spot_info.objects.all().values()
    for info in spot_infos:
        if str(info['spot_id']) == pk:
            spot_info = info
            break
    return render(request, 'food/info.html', {"spot_info":spot_info})
