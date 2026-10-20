
from django.shortcuts import render
from django.http import HttpResponse    
from .data.spots import foods, spots
# Create your views here.


def home(request):

    return render(request, 'food/index.html', context)

def home2(request, pk):
    return render(request, 'food/about.html', context)