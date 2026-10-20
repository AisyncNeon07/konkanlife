
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Spots
from .forms import SpotsForm

# Create your views here.

def spots_home(request):
    spots = list(Spots.objects.select_related('category', 'uploaded_by').prefetch_related('tags').all())
    context = {'spots': spots}
    return render(request, 'spots/index.html', context)

@login_required
def create_spot(request):
    spots_form = SpotsForm()
    if request.method == 'POST':
        spots_form = SpotsForm(request.POST, request.FILES)
        if spots_form.is_valid():
            try:
                spot = spots_form.save(commit=False)
                if hasattr(request.user, 'profile'):
                    spot.uploaded_by = request.user.profile
                spot.save()
                return redirect('home_spots')
            except Exception as e:
                messages.error(request, f"Error creating spot: {str(e)}")
    return render(request, 'spots/spot_form.html', {'spots_form': spots_form})


@login_required
def update_spot(request, pk):
    spot = get_object_or_404(Spots, id=pk)
    user_profile = getattr(request.user, 'profile', None)
    if spot.uploaded_by != user_profile and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to edit this spot.")

    spots_form = SpotsForm(instance=spot)
    if request.method == 'POST':
        spots_form = SpotsForm(request.POST, request.FILES, instance=spot)
        if spots_form.is_valid():
            try:
                spots_form.save()
                return redirect('home_spots')
            except Exception as e:
                messages.error(request, f"Error updating spot: {str(e)}")
    return render(request, 'spots/spot_form.html', {'spots_form': spots_form})


@login_required
def delete_spot(request, pk):
    spot = get_object_or_404(Spots, id=pk)
    user_profile = getattr(request.user, 'profile', None)
    if spot.uploaded_by != user_profile and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to delete this spot.")

    if request.method == 'POST':
        spot.delete()
        return redirect('home_spots')
    return render(request, 'spots/delete.html', {'spots': spot})


def home3(request, pk):
    spot = get_object_or_404(Spots.objects.select_related('category', 'uploaded_by').prefetch_related('tags'), id=pk)
    context = {'spots': spot}
    return render(request, 'spots/details.html', context)