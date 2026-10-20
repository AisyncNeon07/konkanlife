
from django.shortcuts import render , redirect
from django.http import HttpResponse
from  . models import Spots 

from . forms import SpotsForm 

# Create your views here.

def spots_home(request):
    spots = Spots.objects.all()
    context = { 'spots': spots }
    return render(request, 'spots/index.html', context)

def create_spot(request):
    spots_form = SpotsForm()
    if request.method == 'POST':
        spots_form = SpotsForm(request.POST , request.FILES)
        if spots_form.is_valid():
            spots_form.save()
            return redirect('home')
    return render(request, 'spots/spot_form.html', {"spots_form":spots_form})


def update_spot(request , pk):
    spots = Spots.objects.get(id=pk)
    spots_form = SpotsForm(instance=spots)
    if request.method == 'POST':
        spots_form = SpotsForm(request.POST, request.FILES, instance=spots)
        if spots_form.is_valid():
            spots_form.save()
            return redirect('home')
    return render(request, 'spots/spots_form.html', {"spots_form":spots_form})


def delete_spot(request ,pk):
    spots = Spots.objects.get(id=pk)
    if request.method == 'POST':
        spots.delete()
        return redirect('home')
    return render(request, 'spots/delete.html', {"spots":spots})        
    
def home3(request , pk):
    spots = Spots.objects.get(id=pk)
    context = { 'spots': spots }
    return render(request, 'spots/details.html', context)    