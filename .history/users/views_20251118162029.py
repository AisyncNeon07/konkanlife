from django.shortcuts import render

from . models import Profile
# Create your views here.

def users(request):
    profile = Profile.objects.all() 
    return render(request, 'users/users.html',{'profile':profile})