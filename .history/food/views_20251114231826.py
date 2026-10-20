
from django.shortcuts import render
from django.http import HttpResponse
from .data.spots import foods, spots

from  . models import Spots, Category, spot_info

from .forms import SpotForm
# Create your views here.




def home(request):
    spots = Spots.objects.all()
    spot_info_list = spot_info.objects.all()
    context = { 'spots': spots, 'spot_info': spot_info_list }
    return render(request, 'food/index.html', context)

def home2(request):
    spots1 = Spots.objects.all()
    return render(request, 'food/about.html', {"spots1":spots1})

def home3(request ,pk):
    spots3 = Spots.objects.get(id=pk)
    details = spots3.spot_info
    return render(request, 'food/details.html', {"spot3":spots3, "details": details})


def create_spot(request):
    form = SpotForm()
    if:
        
    context = {'form': form}
    return render(request, 'food/spot_form.html', context)