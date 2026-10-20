from django.shortcuts import render
from django.http import HttpResponse    
# Create your views here.


def home(request):
    return render(request, 'food/index.html')

def home2(request, pk):
    return render(request, 'food/about.html',)