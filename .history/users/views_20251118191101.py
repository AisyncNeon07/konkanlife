from django.shortcuts import render, redirect

from . models import Profile 

from . forms import Profileform
# Create your views here.

def users(request):
    profiles = Profile.objects.all() 
    return render(request, 'users/users.html',{'profiles':profiles})


def create_users(request):
    spots_form = Profileform()
    if request.method == 'POST':
        spots_form = Profileform(request.POST , request.FILES)
        if spots_form.is_valid():
            spots_form.save()
            return redirect('home/')
    return render(request, 'users/users.html', {"spots_form":spots_form})
