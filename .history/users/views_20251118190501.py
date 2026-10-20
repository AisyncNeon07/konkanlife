from django.shortcuts import render

from . models import Profile
# Create your views here.

def users(request):
    profiles = Profile.objects.all() 
    return render(request, 'users/users.html',{'profiles':profiles})


def create_user(request , pk):
    pro = Profile.object.get(id=pk)