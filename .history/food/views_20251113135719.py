from django.shortcuts import render
from django.http import HttpResponse    
# Create your views here.


def home(request):
    foods = {
        "Seafood": [
            "Bangda Fry",
            "Pomfret Fry",
            "Prawns Sukka",
            "Bombil Fry",
        ],
        "Veg Dishes": [
            "Solkadhi",
            "Alu Vadi",
            "Konkani Dal",   
        ],
        "Rice & Bread": [
            "Ghavan",
            "Amboli",
            "Varan Bhaat",
        ],
    }
    
    spots = 
    return render(request, 'food/index.html', {'foods':foods})

def home2(request, pk):
    return render(request, 'food/about.html',)