from django.shortcuts import render
from django.http import HttpResponse    
from . data import foods, spots
# Create your views here.


def home(request):
    context = {
        'foods': foods,
        'spots': spots
    }
    return render(request, 'food/index.html', context)

def home2(request, pk):
    return render(request, 'food/about.html',)