from django.shortcuts import render
from django.http import HttpResponse    
# Create your views here.


def home(request):
    return HttpResponse("initail project page")

def home2(request):
    return HttpResponse("second page of the project")