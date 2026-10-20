
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

def home2(request ,pk):
    spotobj = None
    for items in spots.items():
        for item in items:
            if item['name'] == pk:
                spotobj = item
                break
        if spotobj:
            break   
    return render(request, 'food/about.html', {'spot': spotobj})