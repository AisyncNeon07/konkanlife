
from django.shortcuts import render
from django.http import HttpResponse
from .data.spots import foods, spots

from  . models import Spots, Category, spot_info
# Create your views here.




class home_view:
    def home(request):
        context = {
            'spots': spots
        }
        return render(request, 'food/index.html', context)

    def home2(request):
        context = {
            'spots1': spots 
        }
        return render(request, 'food/about.html', context)

    def home3(request, pk):
        spot3 = None
        for spot in spots:
            if str(spot.id) == str(pk):
                spot3 = spot
                break
        context = {
            'spot3': spot3
        }
        return render(request, 'food/details.html', context)