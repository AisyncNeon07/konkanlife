
from django.shortcuts import render , redirect
from django.http import HttpResponse
from .data.spots import foods, spots

from  . models import FoodItem , FoodInfo

from . forms import FoodItemForm , FoodInfoForm

# Create your views here.

def home(request):
    food_items = FoodItem.objects.all()
    food_info_list = FoodInfo.objects.all()
    context = { 'food_items': food_items, 'food_info': food_info_list }
    return render(request, 'food/index.html', context)

def create_food(request):
    food_items = FoodItemForm()
    if request.method == 'POST':
        food_item = FoodItemForm(request.POST)
        if food_item.is_valid():
            food_item.save()
            return redirect('home')
    return render(request, 'food/food_form.html', {"food_items":food_items})


def update_food(request , pk):
    food = FoodItem.objects.get(id=pk)
    food_item = FoodItemForm(instance=food)
    if request.method == 'POST':
        food_item = FoodItemForm(request.POST, instance=food)
        if food_item.is_valid():
            food_item.save()
            return redirect('home')
    return render(request, 'food/food_form.html', {"food":food})


def delete_food(request ,pk):
    food_item = FoodItem.objects.get(id=pk)
    food_item.delete()

def home3(request ,pk):
    food3 = FoodItem.objects.get(id=pk)
    details = food3.foodinfo
    return render(request, 'food/details.html', {"food3":food3, "details": details})