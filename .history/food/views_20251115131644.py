
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
    food3 = FoodItem.objects.get(id=pk)
    details = food3.foodinfo
    return render(request, 'food/details.html', {"food3":food3, "details": details})