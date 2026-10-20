
from django.shortcuts import render
from django.http import HttpResponse
from .data.spots import foods, spots

from  . models import Spots, Category, spot_info
# Create your views here.





def home(request):
    spots = Spots.objects.all()
    return render(request, 'food/index.html', {"spots": spots})

def home2(request):
    spots1 = Spots.objects.all()
    return render(request, 'food/about.html', {"spots1":spots1})

def home3(request ,pk):
    spots3 = Spots.objects.get(id=pk)
    return render(request, 'food/info.html', {"spot3":spots3})
