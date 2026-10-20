from django.shortcuts import render

from . models import Profile
# Create your views here.

def users(request):
    profiles = Profile.objects.all() 
    return render(request, 'users/users.html',{'profiles':profiles})


def create_users(request):
    spots_form = SpotsForm()
    if request.method == 'POST':
        spots_form = SpotsForm(request.POST , request.FILES)
        if spots_form.is_valid():
            spots_form.save()
            return redirect('home_spots')
    return render(request, 'spots/spot_form.html', {"spots_form":spots_form})
