from django.shortcuts import render, redirect

from . models import Profile 

from . forms import Profileform
# Create your views here.

def users(request):
    profiles = Profile.objects.all() 
    return render(request, 'users/users.html',{'profiles':profiles})


def create_users(request):
    users_form = Profileform()  
    if request.method == 'POST':
        users_form= Profileform(request.POST , request.FILES)
        if users_form.is_valid():
            users_form.save()
            return redirect('home')
    return render(request, 'users/users_form.html', {"users_form":users_form})

def user_page(request , pk):
    return render(request, 'users/user_profile.html')