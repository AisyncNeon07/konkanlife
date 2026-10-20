
from django.shortcuts import render , redirect
from django.http import HttpResponse
from .data.spots import foods, spots

from  . models import FoodItem 

from . forms import FoodItemForm 

# Create your views here.

def home(request):
    food_items = FoodItem.objects.all()
    context = { 'food_items': food_items }
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
    food_items = FoodItemForm(instance=food)
    if request.method == 'POST':
        food_item = FoodItemForm(request.POST, instance=food)
        if food_item.is_valid():
            food_item.save()
            return redirect('home')
    return render(request, 'food/food_form.html', {"food_items":food_items})


def delete_food(request ,pk):
    food_item = FoodItem.objects.get(id=pk)
    if request.method == 'POST':
        food_item.delete()
        return redirect('home')
    return render(request, 'food/delete.html', {"food_item":food_item})        
    
def home3(request , pk):
    food_items = FoodItem.objects.get(id=pk)
    food3 = food_items.foodinfo
    context = { 'spot3': food_items , 'food3': food3 }
    return render(request, 'food/details.html', context)    