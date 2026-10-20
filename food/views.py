
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import FoodItem 
from .forms import FoodItemForm 

# Create your views here.

def main(request):
    return render(request, 'food/index.html')


def home(request):
    food_items = list(FoodItem.objects.select_related('uploaded_by').all())
    context = {'food_items': food_items}
    return render(request, 'food/index.html', context)

@login_required
def create_food(request):
    food_items = FoodItemForm()
    if request.method == 'POST':
        food_item_form = FoodItemForm(request.POST, request.FILES)
        if food_item_form.is_valid():
            try:
                food_item = food_item_form.save(commit=False)
                if hasattr(request.user, 'profile'):
                    food_item.uploaded_by = request.user.profile
                food_item.save()
                return redirect('food_home')
            except Exception as e:
                messages.error(request, f"Error adding food item: {str(e)}")
    return render(request, 'food/food_form.html', {"food_items": food_items})


@login_required
def update_food(request, pk):
    food = get_object_or_404(FoodItem, id=pk)
    user_profile = getattr(request.user, 'profile', None)
    if food.uploaded_by != user_profile and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to edit this food item.")

    food_items = FoodItemForm(instance=food)
    if request.method == 'POST':
        food_item = FoodItemForm(request.POST, request.FILES, instance=food)
        if food_item.is_valid():
            try:
                food_item.save()
                return redirect('food_home')
            except Exception as e:
                messages.error(request, f"Error updating food item: {str(e)}")
    return render(request, 'food/food_form.html', {'food_items': food_items})


@login_required
def delete_food(request, pk):
    food_item = get_object_or_404(FoodItem, id=pk)
    user_profile = getattr(request.user, 'profile', None)
    if food_item.uploaded_by != user_profile and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to delete this food item.")

    if request.method == 'POST':
        food_item.delete()
        return redirect('food_home')
    return render(request, 'food/delete.html', {'food_item': food_item})


def home3(request, pk):
    food_items = get_object_or_404(FoodItem.objects.select_related('uploaded_by'), id=pk)
    context = {'food_items': food_items}
    return render(request, 'food/details.html', context)