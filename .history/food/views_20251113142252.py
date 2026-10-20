
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

def home2(request):
    return render(request, 'food/about.html', context)

def single_post(request, pk):
    