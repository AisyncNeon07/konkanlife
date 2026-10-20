
from django.shortcuts import render , redirect
from django.http import HttpResponse
from .data.spots import foods, spots

from  . models import Spots, Category, spot_info

from .forms import SpotForm , spot_infoForm
# Create your views here.




def home(request):
    spots = Spots.objects.all()
    spot_info_list = spot_info.objects.all()
    context = { 'spots': spots, 'spot_info': spot_info_list }
    return render(request, 'food/index.html', context)

def home2(request):
    spots1 = Spots.objects.all()
    return render(request, 'food/about.html', {"spots1":spots1})

def home3(request ,pk):
    spots3 = Spots.objects.get(id=pk)
    details = spots3.spot_info
    return render(request, 'food/details.html', {"spot3":spots3, "details": details})


def create_spot(request):
    form = SpotForm()
    info = spot_infoForm()

    if request.method == 'POST':
        form = SpotForm(request.POST, request.FILES)
        info = spot_infoForm(request.POST)

        if form.is_valid() and info.is_valid():

            # 1. Save Spot first
            spot = form.save()

            # 2. Create spot_info but don't save yet
            spot_info_obj = info.save(commit=False)
            spot_info_obj.spot = spot  # LINK HERE!!!
            spot_info_obj.save()

            return redirect('home')

    context = {'form': form, 'info': info}
    return render(request, 'food/spot_form.html', context)
