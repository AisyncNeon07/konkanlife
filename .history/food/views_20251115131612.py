
from django.shortcuts import render , redirect
from django.http import HttpResponse
from .data.spots import foods, spots

from  . models import FoodItem , FoodInfo

# Create your views here.




def home(request):
    food_items = FoodItem.objects.all()
    food_info_list = FoodInfo.objects.all()
    context = { 'food_items': food_items, 'food_info': food_info_list }
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
    if request.method == 'POST':
        form = SpotForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form, }
    return render(request, 'food/spot_form.html', context)

def update_spot(request, pk):
    spot = Spots.objects.get(id=pk)
    form = SpotForm(instance=spot)\
        
    if request.method == 'POST':
        form = SpotForm(request.POST, instance=spot)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form, }
    return render(request, 'food/spot_form.html', context)
 
 
def delete_spot(request, pk):
    spot = Spots.objects.get(id=pk)
    if request.method == 'POST':
        spot.delete()
        return redirect('home')
    context = {'item': spot}
    return render(request, 'food/delete.html', context)