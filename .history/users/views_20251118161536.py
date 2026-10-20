from django.shortcuts import render

from . models import Profile
# Create your views here.

def users(request):
    return render(request, 'users/users.html')

